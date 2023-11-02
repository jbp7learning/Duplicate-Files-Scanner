# project.py

import os
import math
import csv
import datetime
import sys
import copy
from tabulate import tabulate


program_name = "Duplicate Files Scanner"
version = "2023.0.5"
backup_csv = "backup.csv"


def main():
    try:
        # START
        start_py()

        # INITIALIZE VARIABLES
        just_started = True
        added_dirs = []
        all_files = []
        duplicate_files = []
        options_ls = [
            "Scan more directory for duplicates.",
            "Scan a different directory.",
            "Print list of duplicates.",
            "Delete the identified duplicate files.",
            "Exit",
        ]
        selected_optn = 0
        with open(backup_csv, "w", newline=""): pass  # Clearing backup_csv

        # LOOP THRU FILES
        while True:
            if just_started == True:
                directory = get_dir()
                if directory != "cancel":
                    scan_dir(directory, all_files, duplicate_files)
                    if duplicate_files:
                        sort_by_date_created(duplicate_files)
                        id_this(duplicate_files)
                        save_to_csv(duplicate_files, "w")
                    print_summary(all_files, duplicate_files)
                just_started = False

            selected_optn = menu(options_ls)

            match options_ls[selected_optn]:
                case "Scan more directory for duplicates.":
                    print("=" * 75)
                    print(f"({selected_optn+1}) {options_ls[selected_optn]}")
                    print("=" * 75)
                    if directory != "cancel":
                        added_dirs.append(directory)
                    while True:
                        directory = get_dir()
                        if directory in added_dirs:
                            print(
                                "Directory entered has already been scanned!\nPlease try again."
                            )
                        else:
                            break
                    if directory != "cancel":
                        scan_dir(directory, all_files, duplicate_files)
                        if duplicate_files:
                            sort_by_date_created(duplicate_files)
                            id_this(duplicate_files)
                            save_to_csv(duplicate_files, "a")
                        print_summary(all_files, duplicate_files)

                case "Scan a different directory.":
                    print("=" * 75)
                    print(f"({selected_optn+1}) {options_ls[selected_optn]}")
                    print("=" * 75)
                    directory = get_dir()
                    if directory != "cancel":
                        # Clear previous data
                        with open(backup_csv, "w", newline=""):
                            pass
                        all_files.clear()
                        duplicate_files.clear()

                        scan_dir(directory, all_files, duplicate_files)
                        if duplicate_files:
                            sort_by_date_created(duplicate_files)
                            id_this(duplicate_files)
                            save_to_csv(duplicate_files, "w")
                        print_summary(all_files, duplicate_files)

                case "Print list of duplicates.":
                    print("=" * 75)
                    print(f"({selected_optn+1}) {options_ls[selected_optn]}")
                    print("=" * 75)
                    print_duplicate_files(duplicate_files)

                case "Delete the identified duplicate files.":
                    print("=" * 75)
                    print(f"({selected_optn+1}) {options_ls[selected_optn]}")
                    print("=" * 75)
                    del_files = input("Would you like to delete the duplicates (y/n)? ")
                    print("")
                    if del_files.strip().lower() in ["y", "yes"]:
                        result, cancel = del_duplicates(duplicate_files)
                        if not cancel:
                            with open(backup_csv, "w", newline=""):
                                pass
                            all_files.clear()
                            duplicate_files.clear()
                            added_dirs.clear()
                            directory = ""
                        print(result)
                    else:
                        print(f"\nDeleted: 0 files.\n")

                case "Exit":
                    print("=" * 75)
                    print(f"({selected_optn+1}) {options_ls[selected_optn]}")
                    print("=" * 75)
                    with open(backup_csv, "w", newline=""):
                        pass
                    sys.exit("Thank you for using 'Duplicate Files Scanner'!!!\n")

    except KeyboardInterrupt:
        with open(backup_csv, "w", newline=""):
            pass
        print("")
        print("=" * 75)
        sys.exit(
            "Thank you for using 'Duplicate Files Scanner'!!!\n"
        )
    except PermissionError:
        print("Please close any open files before running this program.")
        print("=" * 75)
        sys.exit("Thank you for using 'Duplicate Files Scanner'!!!\n")


# Prints the program name and version.
def start_py():
    print("")
    print("=" * 75)
    print(f"Program: {program_name}", f"Version: {version}", sep="\n")
    print("=" * 75)


# Prompts the user for the directory to scan or to cancel request.
def get_dir():
    user_input = input(
        "Enter a directory to scan:\n"
        + "*Type 'cancel' if you want to go back to the options.\n\n>> "
    )
    while True:
        user_input = str(user_input).strip().lower()
        if user_input == "cancel":
            print("")
            return user_input
        elif os.path.isdir(user_input):
            print("")
            return user_input
        else:
            user_input = input("\nInvalid directory! Please try again:\n>> ")
            user_input = str(user_input)


# Loop through the given directory.
# Adds each file's info to the all_files_ls
# Adds duplicate files to duplicate_files_ls
def scan_dir(dir_to_scan, all_files_ls, duplicate_files_ls):
    for root, _, files in os.walk(dir_to_scan):
        for file in files:

            # Getting the current file's information:
            f_name = file.split(".")
            f_extn = f_name[-1]
            del f_name[-1]
            f_name = ".".join(f_name)
            f_size = os.path.getsize(os.path.join(root, file))  # in bytes
            creation_timestamp = os.path.getctime(os.path.join(root, file))
            creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
            with open(os.path.join(root, file), "r", encoding="latin1") as f:
                f_content = f.read()
            current_file = {
                "entry no.": "",
                "name": f_name,
                "type": f_extn,
                "size": f_size,
                "creation_datetime": creation_datetime,
                "path": os.path.join(root, file),
                "content": f_content,
            }

            # Checking if the currently being processed file's filetype and content
            # is the same with an already been processed file.
            keys_to_check = ["type", "content"]
            if all_files_ls != []:
                for listed in all_files_ls:
                    if (
                        all(
                            current_file[key] == listed[key]
                            for key in keys_to_check
                        )
                    ):
                        # A listed file and current file is confirmed to be duplicate.
                        # Adding files to duplicate list.
                        add_to_duplicate_list(
                            current_file, listed, duplicate_files_ls
                        )
            # Making sure that no the same file is being added to the list of all files.
            if all(d["path"] != current_file["path"] for d in all_files_ls):
                all_files_ls.append(current_file)


# Prints the summary of the successful scan in a table.
def print_summary(all_ls, duplicate_ls):
    summary = [
        ["            SCAN RESULT          ", ""],
        ["No. of files in the given DIR:", len(all_ls)],
        ["No. of files duplicated:", len(duplicate_ls)],
        ["Total no. of duplicate files:", sum(len(ls) for ls in duplicate_ls)],
        ["Space that can be saved:", convert_size(space_to_free(duplicate_ls))],
    ]
    print(
        tabulate(
            summary, headers="firstrow", colalign=("left", "center"), tablefmt="grid"
        )
    )
    print("")


# The new_file and old_file are confirmed the same files.
# Adding them to the duplicate list.
def add_to_duplicate_list(new_file, old_file, ls_of_ls_of_d):
    kys = ["type", "content"]
    for inner_list in ls_of_ls_of_d:
        # Checks if a file that has the same filetype and content is already listed as duplicate.
        if (
            all(inner_list[0][key] == new_file[key] for key in kys)
        ):
            # Making sure that no the same file is added.
            if all(d["path"] != new_file["path"] for d in inner_list):
                # Since the is already some file with the same filetype and content,
                # Only adding the new_file to the list of the same files.
                inner_list.append(new_file)
            return
    # Adding both old file and new file to the duplicate list as a new group of duplicate files.
    ls_of_ls_of_d.append([old_file, new_file])


# Prompting user for the options one can make.
# Add more to options_ls if necessary.
def menu(options):
    print("=" * 75)
    print("What would you like to do next?")
    i = 0
    for op in options:
        i += 1
        print(f"    ({i}) {op}")
    print("")
    while True:
        try:
            opt = int(input("Enter the corresponding opt-number above: "))
            if opt in range(1, 1 + len(options)):
                print("")
                return opt - 1
            else:
                print("Invalid opt-number! Please try again.")
        except ValueError:
            print("Invalid opt-number! Please try again.")


# Prints the list of duplicate files.
def print_duplicate_files(duplicate_ls):
    selected_data = []
    for inner_ls in duplicate_ls:
        for file in inner_ls:
            selected_data.append(
                {
                    "Entry No.": file["entry no."],
                    "Filename": file["name"] + "." + file["type"],
                }
            )
    if selected_data:
        print(
            tabulate(
                selected_data,
                headers="keys",
                colalign=("center", "left"),
                tablefmt="grid",
            )
        )
    else:
        print(
            tabulate(selected_data, headers=("Entry No.", "Filename"), tablefmt="grid")
        )
    print("")


# Sorting files by their date created.
# Oldest file could be the original file.
def sort_by_date_created(duplicates):
    for inner_list in duplicates:
        sorted_inner_ls = sorted(inner_list, key=lambda x: x["creation_datetime"])
        inner_list.clear()
        inner_list.extend(sorted_inner_ls)


# Calling this function will generate an ID for the file that is a duplicate
def id_this(duplicates):
    # Duplicate file ID format: <file number>C<duplicate number>
    file_no = 0
    duplicate_no = 0
    for inner_list in duplicates:
        for entry in inner_list:
            file_no = duplicates.index(inner_list)
            duplicate_no = inner_list.index(entry)
            entry["entry no."] = f"{file_no+1}C{duplicate_no+1}"


# Computing the space that can be freed from deleting the duplicate files.
# Sum of the sizes of the newest versions of files. (Excluding the oldest file)
def space_to_free(files):
    total_size = 0
    for inner_list in files:
        for file in inner_list[1:]:
            total_size += int(file["size"])
    return total_size


# Converts file size in bytes to the largest unit.
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


# Saves the list of duplicate files into a csv as a backup.
# Currently not being utilized but lays the groundwork
# for potential future expansions involving large datasets.
def save_to_csv(input_data, mode="a"):
    data = copy.deepcopy(input_data)
    # If csv is does not exist, create scanned_data.csv
    header = list(data[0][0].keys())
    header.remove("content")
    if data:
        with open(backup_csv, mode, encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, header)
            if mode == "w":
                writer.writeheader()
            for inner_list in data:
                for d in inner_list:
                    # Make sure 'd' does not contain the key 'content'
                    if "content" in d:
                        del d["content"]
                    writer.writerow(d)


# Deletes the duplicate files except the oldest of the files.
def del_duplicates(duplicates):
    d = c = 0
    print("*Please take note that deleted files are removed permanently.*")
    confirm = input("Enter 'C' to confirm command to delete: ").strip().lower()
    print("")
    if confirm == "c":
        for inner_list in duplicates:
            for file in inner_list[1:]:
                if os.path.exists(file["path"]):
                    os.remove(file["path"])
                    d += 1
                else:
                    c += 1
        if d == 1:
            return (f"\nDeleted: {d} file.\n", False)
        elif c > 0:
            return ((
                f"\nDeleted: {d} files."
                + f"\nSome path does not exists anymore. Please try to scan again.\n"
            ),  False
            )
        else:
            return (f"\nDeleted: {d} files.\n", False)
    else:
        return (f"\nDeleted: 0 files.\n", True)


if __name__ == "__main__":
    main()
