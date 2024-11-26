import argparse
import csv
import os

def get_duplicates(host_list: list) -> list:
    duplicate_set: set = set()
    duplicate_list: list = list()

    [duplicate_set.add(host) for host in host_list if host_list.count(host) > 1]
    for host in duplicate_set:
        duplicate_list.append({"hostname":host, "count": host_list.count(host)})

    return duplicate_list

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="asset_info.py",
        description="Nexpose System Information")
    parser.add_argument("-f", "--File", type=str, required=True)
    parser.add_argument("-d", "--Duplicates", action="store_true")

    args = parser.parse_args()

    csv_file = args.File
    while True:
        if os.path.isfile(csv_file):
            break
        else:
            print("File Does Not Exist")
            csv_file = input("File Name: ")
    
    host_list: list = []

    with open(csv_file, newline="") as f:
        rows = csv.DictReader(f)
        for row in rows:
            if len(row["Name"]) > 0:
                host_list.append(row["Name"])
                #print(row["Name"], row["IP Address"])

    if args.Duplicates:
        duplicate_list: list = get_duplicates(host_list)
        with open("nexpose_duplicate_file.csv", "w", newline="") as dup_file:
            field_names = ["hostname", "count"]
            writer = csv.DictWriter(dup_file, fieldnames=field_names)

            writer.writeheader
            [writer.writerow(item) for item in duplicate_list]


if __name__ == "__main__":
    main()