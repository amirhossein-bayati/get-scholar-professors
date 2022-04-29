import json
import sys

data_file_name = sys.argv[1]


def read_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def save_file(data):
    with open("removed_duplicate.json", "w") as file:
        json.dump(data, file)
    return None


def remove_duplicates(data_file):
    data = []
    unique = []

    for item in data_file:
        url = item['Google Scholar link of the author']
        if url not in unique:
            data.append(item)
            unique.append(url)
    return data


def number_of_removed_items(first_file, second_file):
    return f'{len(first_file)-len(second_file)} file(s) removed.'


def main():
    data_file = read_file(data_file_name)
    data = remove_duplicates(data_file)
    print(number_of_removed_items(data_file, data))
    save_file(data)


if __name__ == '__main__':
    main()
