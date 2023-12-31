from collections import Counter
import os
import re
from colorama import init, Fore


os.system('cls' if os.name == 'nt' else 'clear')

mace = Fore.LIGHTRED_EX + "mace"


ascii_art = rf"""
 $$$$$$$$\ $$\                 $$\                     
 $$  _____|\__|                $$ |                    
 $$ |      $$\ $$$$$$$\   $$$$$$$ | $$$$$$\   $$$$$$\  
 $$$$$\    $$ |$$  __$$\ $$  __$$ |$$  __$$\ $$  __$$\ 
 $$  __|   $$ |$$ |  $$ |$$ /  $$ |$$ |  \__|$$ |  \__|
 $$ |      $$ |$$ |  $$ |$$ |  $$ |$$ |      $$ |      
 $$ |      $$ |$$ |  $$ |\$$$$$$$ |$$ |      $$ |      
 \__|      \__|\__|  \__| \_______|\__|      \__|  by {mace}    


"""

init(autoreset=True)


def create_results_folder():
    if not os.path.exists("results"):
        os.makedirs("results")


def create_combo_file():
    if not os.path.exists("combo.txt"):
        with open("combo.txt", "w") as combo_file:
            print(Fore.GREEN + "The 'combo.txt' file has been created.")


def rexmail(cfile, xfile):
    rexmail = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+:[a-zA-Z0-9._-]+')
    cfile = rexmail.findall(cfile.read())

    lenofclist = len(cfile)
    for i in range(lenofclist):
        xfile.write("\n")
        xfile.write(str(cfile[i]))


def combo_extractor():
    input_file = "combo.txt"
    output_file_name = input("Enter the name for the output file (without extension): ") + ".txt"
    output_file = os.path.join("results", output_file_name)

    with open(input_file, 'r') as cfile, open(output_file, 'w') as xfile:
        rexmail(cfile, xfile)

    print(Fore.LIGHTGREEN_EX + f"Results saved to {output_file}")


def search_in_files(folder_path, search_text):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line_number, line in enumerate(lines, start=1):
                    if re.search(r'\b{}\b'.format(re.escape(search_text)), line):
                        results.append((filename, line_number, line))
    return results


def perform_searches(search_file, folder_path, output_file):
    with open(search_file, 'r') as search_input:
        search_queries = search_input.read().splitlines()

    with open(output_file, 'w') as results_output:
        for search_text in search_queries:
            results = search_in_files(folder_path, search_text)
            if results:
                results_output.write(f"'{search_text}' found in the following files:\n")
                for filename, line_number, line in results:
                    formatted_line = line.replace(search_text, f"{search_text}")
                    results_output.write(f"In file: {filename}, line {line_number}: {formatted_line.strip()}\n")
                results_output.write("\n")


def manual_search(folder_path):
    print("")
    print(' Type "exit" to go back.')
    while True:
        print("")
        search_text = input(" User: ")

        if search_text.lower() == "exit":
            print("Exiting the search.")
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break

        results = search_in_files(folder_path, search_text)

        if results:
            print(Fore.LIGHTGREEN_EX +f" '{search_text}'", "found in:")
            for filename, line_number, line in results:
                formatted_line = line.replace(search_text, f"'{search_text}'")
                print(" > " + Fore.LIGHTBLUE_EX + "In file" + Fore.WHITE + f": {filename}", Fore.LIGHTBLUE_EX + f"line {line_number}" + Fore.WHITE + f": {formatted_line.strip()}")
        else:
            print(Fore.LIGHTRED_EX +f" '{search_text}'", "Not found.")

def extract_domains(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    domains = []
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) == 2 and '@' in parts[0]:
            email = parts[0]
            domain = email.split('@')[1]
            domains.append(domain.lower())

    return domains


def main():
    print(Fore.RED + ascii_art)
    print(Fore.WHITE + " 1. " + Fore.LIGHTRED_EX + "Automatic: " + Fore.WHITE + "Bulk search")
    print(" 2. " + Fore.LIGHTRED_EX + "Manual: " + Fore.WHITE + "Specific search")
    print(" 3. " + Fore.LIGHTRED_EX + "Combo Extractor: " + Fore.WHITE + "Email:Pass Extractor")
    print(" 4. " + Fore.LIGHTRED_EX + "Domain Extractor: " + Fore.WHITE + "Extract domains from combo list")

    create_results_folder()
    create_combo_file()

    option = input(" > ")

    if option == "1":
        search_file = "combo.txt"
        folder_path = "list"
        output_file = os.path.join("results", input(
            Fore.WHITE + "Enter the name for the output file (without extension): ") + ".txt")

        perform_searches(search_file, folder_path, output_file)

        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(Fore.LIGHTGREEN_EX + f"Search results saved to '{output_file}'")
        else:
            print(Fore.RED + "No results found in the automatic search.")

        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    elif option == "2":
        folder_path = "list"
        manual_search(folder_path)
    elif option == "3":
        combo_extractor()
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    elif option == "4":
        filename = "combo.txt"
        domains = extract_domains(filename)
        domain_count = Counter(domains)

        sorted_domains = sorted(domain_count.items(), key=lambda x: x[1],
                                reverse=True)

        output_text = ""
        for domain, count in sorted_domains:
            output_text += f"{domain} ( {count} )\n"

        file_name = input("Enter the name for the output file (without extension): ")
        file_name_with_extension = file_name + "_DOMAINs.txt"
        output_path = os.path.join("results", file_name_with_extension)

        if not os.path.exists("results"):
            os.makedirs("results")

        with open(output_path, 'w') as file:
            file.write(output_text)

        print(Fore.LIGHTGREEN_EX + f"Results saved to {output_path}")

        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    else:
        print(Fore.RED + "Invalid option.")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()


if __name__ == "__main__":
    main()

    # what u looking at
