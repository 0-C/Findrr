import os
import re
from colorama import init, Fore

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

mace = Fore.LIGHTRED_EX + "mace"

# ASCII art
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

    print(Fore.LIGHTGREEN_EX + f"Combo extraction results saved to '{output_file}'")


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
                    formatted_line = line.replace(search_text, f"'{search_text}'")
                    results_output.write(f"In file: {filename}, line {line_number}: {formatted_line.strip()}\n")
                results_output.write("\n")  # Write a newline after each search query


def manual_search(folder_path):
    while True:
        search_text = input("Enter the exact text to search (or type 'exit' to quit): ")

        if search_text.lower() == "exit":
            print("Exiting the search.")
            break

        results = search_in_files(folder_path, search_text)

        if results:
            print(f"'{search_text}' found in the following files:")
            for filename, line_number, line in results:
                formatted_line = line.replace(search_text, f"'{search_text}'")
                print(f"In file: {filename}, line {line_number}: {formatted_line.strip()}")
        else:
            print(f"'{search_text}' not found in any files.")


def main():
    print(Fore.RED + ascii_art)
    print(Fore.WHITE + " 1. " + Fore.LIGHTRED_EX + "Automatic: " + Fore.WHITE + "Bulk search")
    print(" 2. " + Fore.LIGHTRED_EX + "Manual: " + Fore.WHITE + "Specific search")
    print(" 3. " + Fore.LIGHTRED_EX + "Combo Extractor: " + Fore.WHITE + "Email:Pass Extractor")

    create_results_folder()
    create_combo_file()

    option = input()

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
    else:
        print(Fore.RED + "Invalid option.")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()


if __name__ == "__main__":
    main()
