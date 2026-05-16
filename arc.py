import csv

filename = "results.csv"

with open(filename, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    header = next(reader)
    print(header)

    for row in reader:
        print(row)