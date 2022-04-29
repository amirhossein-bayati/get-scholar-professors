import json
import sys

json_file_name = sys.argv[1]


def read_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def main():
    json_data = read_file(json_file_name)
    print(len(json_data))


if __name__ == '__main__':
    main()
