import subprocess
from termcolor import colored
import time

ALL_TESTS = 6
TESTS_PASSED = 0

def get_multipass_list():
    try:
        result = subprocess.run(['multipass', 'list'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return None
    
def check_node_statuses() -> bool:
    try:
        assert True == all([True if "Running" in x else False for x in multipass_list_output])
        print(colored('All instances are running', 'green'))
        return True
    except AssertionError:
        print(colored("Not all instances are running", 'red'))
        return False
    
def check_ubuntu_versions_of_nodes() -> bool:
    try:
        assert True == all([True if "22.04" in x else False for x in multipass_list_output if "Mosquitto" not in x])
        print(colored('All nodes are running Ubuntu 22.04 LTS', 'green'))
        return True
    except AssertionError:
        print(colored("Not all nodes are running Ubuntu 22.04 LTS", 'red'))
        return False
    
def check_mosquitt_broker_version() -> bool:
    try:
        assert True == all([True if all([True if y in x else False for y in "Ubuntu Mosquitto Appliance".split()] ) else False for x in multipass_list_output if x[0] == "MosquittoBroker"])
        print(colored('Mosquitto Broker is running the correct multipass appliance', 'green'))
        return True
    except AssertionError:
        print(colored("Mosquitto Broker is not running the correct multipass appliance", 'red'))
        return False
    
def update_nodelist_file() -> bool:
    try:
        with open('../Blueprint/nodelist.txt', 'r') as file:
            lines = file.readlines()

        ip_addresses = {x[0]: x[2] for x in multipass_list_output}
        ip_addresses = dict(list(ip_addresses.items())[1::-1] + list(ip_addresses.items())[2:])
        #print(ip_addresses)
        #print(ip_addresses.items())

        with open('../Blueprint/nodelist.txt', 'w') as file:
            for i, line in enumerate(list(ip_addresses.items())):
                #print(f"i: {i}, line: {line}")
                if i == 0:
                    file.write(f"ubuntu|{list(ip_addresses.items())[i][1]}|pwd\n")
                elif i == len(lines) - 1:
                    file.write(f"vmuser|{list(ip_addresses.items())[i][1]}|")
                else:
                    file.write(f"vmuser|{list(ip_addresses.items())[i][1]}|\n")

        print(colored("nodelist.txt file updated", 'green'))
        return True
    except Exception as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def check_ssh_connection_to_nodes() -> bool:
    with open('../Blueprint/nodelist.txt', 'r') as _file:
        lines = _file.readlines()

    for line in lines[1:]:
        # print(line.strip().split('|'))
        try:
            username, ip, _ = line.strip().split('|')
            #subprocess.run([f'ssh {username}@{ip} -i ../Virtual_ENV/multipass-ssh-key'], check=True)
            subprocess.run(
                ['ssh', '-v', f'{username}@{ip}', '-i', '../Virtual_ENV/multipass-ssh-key', '-o', 'BatchMode=yes', '-o', 'ConnectionAttempts=1', 'true'],
                check=True,
                timeout=10,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(colored(f"SSH connection to {username}@{ip} successful", 'green'))
        except subprocess.CalledProcessError:
            print(colored(f"SSH connection to {username}@{ip} failed", 'red'))
            return False
        except subprocess.TimeoutExpired:
            print(colored(f"SSH connection to {username}@{ip} timed out", 'red'))
            return False
    return True
            
def check_mosquitto_service() -> bool:
        try:
            result = subprocess.run(['multipass', 'exec', 'MosquittoBroker', '--', 'sudo', 'systemctl', 'is-active', '--quiet', 'snap.mosquitto.mosquitto.service'], check=True, timeout=10)
            #print(result)
            print(colored("Mosquitto service is running on MosquittoBroker", 'green'))
            return True
        except subprocess.CalledProcessError:
            print(colored("Mosquitto service is not running on MosquittoBroker", 'red'))
            return False
        except subprocess.TimeoutExpired:
            print(colored("Connection to MosquittoBroker timed out", 'red'))
            return False

if __name__ == "__main__":
    multipass_list_output = get_multipass_list()
    multipass_list_output = multipass_list_output.strip().split('\n')[1:]
    multipass_list_output = [x.split() for x in multipass_list_output]
    

    # Check if all instances are running
    if check_node_statuses():
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))
    
    # Check if all instances are running Ubuntu 22.04 LTS and the Broker is an Ubuntu Mosquitto Broker appliance
    if check_ubuntu_versions_of_nodes():
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    # Check if the Mosquitto Broker is running the correct multipass appliance
    if check_mosquitt_broker_version():
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    # Update the IP addresses in the nodelist.txt file
    if update_nodelist_file():
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))
    
    # Check if SSH connection to all nodes is successful
    if check_ssh_connection_to_nodes():
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    # Check if the Mosquitto service is running on MosquittoBroker
    if check_mosquitto_service():
        TESTS_PASSED += 1
        print(colored(f"Test {TESTS_PASSED}/{ALL_TESTS} passed", 'yellow'))

    print(colored("----------------------Testing The Virtual Environment : completed----------------------", 'blue'))

    if TESTS_PASSED == ALL_TESTS:
        print(colored("All tests passed", 'green'))
    elif TESTS_PASSED == 0:
        print(colored("All tests failed", 'red'))
    else:
        print(colored(f"{TESTS_PASSED}/{ALL_TESTS} tests passed", 'yellow'))
        print(colored(f"{ALL_TESTS - TESTS_PASSED}/{ALL_TESTS} tests failed", 'red'))
