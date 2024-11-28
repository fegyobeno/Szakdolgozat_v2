import subprocess
from termcolor import colored

def get_multipass_list():
    try:
        result = subprocess.run(['multipass', 'list'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return None

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

if __name__ == "__main__":
    multipass_list_output = get_multipass_list()
    multipass_list_output = multipass_list_output.strip().split('\n')[1:]
    multipass_list_output = [x.split() for x in multipass_list_output]

    update_nodelist_file()