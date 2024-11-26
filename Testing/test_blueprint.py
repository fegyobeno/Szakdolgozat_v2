import subprocess
from termcolor import colored

ALL_TESTS = 9
TESTS_PASSED = 0

def get_multipass_list():
    try:
        result = subprocess.run(['multipass', 'list'], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return None

def check_git_repo(host, user, repo_path, expected_url) -> bool:
    try:
        print(colored(f"Checking git repo on {host}", 'blue'))
        result = subprocess.run([".\ensure_git.bat", user, host, "../Virtual_ENV/multipass-ssh-key"], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        result = result.stdout.split('\n')
        if result[0] and result[1] == expected_url:
            print(colored(f"Git repo is correct on {host}", 'green'))
            return True
        else:
            print(colored(f"Git repo is not correct on {host}", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def ensure_libraries_CN(host, user, ssh_key_path) -> bool:
    try:
        result = subprocess.run([".\ensure_python_CN.bat", user, host, ssh_key_path], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        result = result.stdout.strip().split('\n')
        if result[-1] == "True":
            print(colored(f"Python libraries are installed correctly on {host}", 'green'))
            return True
        else:
            print(colored(f"Python libraries are not installed on {host}", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def ensure_libraries_WN(host, user, ssh_key_path) -> bool:
    try:
        result = subprocess.run([".\ensure_python_WN.bat", user, host, ssh_key_path], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        result = result.stdout.strip().split('\n')
        if result[-1] == "True":
            print(colored(f"Python libraries are installed correctly on {host}", 'green'))
            return True
        else:
            print(colored(f"Python libraries are not installed on {host}", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def check_mqtt_connection(host, user, ssh_key_path) -> bool:
    try:
        result = subprocess.run([".\check_mqtt.bat", user, host, ssh_key_path], capture_output=True, text=True, check=True)
        result.check_returncode()  # Ensure the subprocess completed successfully
        result = result.stdout.strip().split('\n')
        if result[-1] == "True":
            print(colored(f"MQTT is working correctly on {host}", 'green'))
            return True
        else:
            print(colored(f"MQTT is not working on {host}", 'red'))
            return False
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False
        

if __name__ == "__main__":
    multipass_list_output = get_multipass_list()

    with open('../Blueprint/nodelist.txt', 'r') as _file:
        lines = _file.readlines()
        lines = [x.split('|') for x in lines]

    # Check if the git repo is correct on each node
    for i, line in enumerate(lines):
        if i == 0:
            continue
        if check_git_repo(lines[i][1], lines[i][0], "/Szakdolgozat_v2", "https://github.com/fegyobeno/Szakdolgozat_v2.git"):
            TESTS_PASSED += 1
            print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))
        
    # Check if the control node has the necessary python modules installed
    if ensure_libraries_CN(lines[1][1], lines[1][0], "../Virtual_ENV/multipass-ssh-key"):
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    # Check if the worker nodes have the necessary python modules installed
    for line in lines[2:]:
        if ensure_libraries_WN(line[1], line[0], "../Virtual_ENV/multipass-ssh-key"):
            TESTS_PASSED += 1
            print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    # Check if the MQTT works between the nodes
    for line in lines[1:]:
        if check_mqtt_connection(line[1], line[0], "../Virtual_ENV/multipass-ssh-key"):
            TESTS_PASSED += 1
            print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    print(colored("----------------------Testing The Blueprint Setup : completed----------------------", 'blue'))
    if TESTS_PASSED == ALL_TESTS:
        print(colored("All tests passed", 'green'))
    elif TESTS_PASSED == 0:
        print(colored("All tests failed", 'red'))
    else:
        print(colored(f"{TESTS_PASSED}/{ALL_TESTS} tests passed", 'yellow'))
        print(colored(f"{ALL_TESTS - TESTS_PASSED}/{ALL_TESTS} tests failed", 'red'))
