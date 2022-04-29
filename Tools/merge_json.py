import json
import sys

json_file_names = sys.argv[1:]


def read_files(file_names):
	all_json = []
	for name in file_names:
		with open(name, 'r') as file:
			all_json.append(json.load(file))
	return all_json


def save_file(data):
	with open("final.json", "w") as file:
		json.dump(data, file)
	return None


def merge(json_data):
	main_json = []
	for json_item in json_data:
		main_json.extend(json_item)
	return main_json


def main():
	json_data = read_files(json_file_names)
	all_json = merge(json_data)
	save_file(all_json)


if __name__ == '__main__':
	main()
