import json
import sys

errors_file_name = sys.argv[1]
urls_file_name = sys.argv[2]


def read_file(file_name):
	with open(file_name, 'r') as file:
		data = json.load(file)
	return data


def save_file(data):
	with open("output.json", "w") as file:
		json.dump(data, file)
	return None


def extract_errors(errors_file, urls_file):
	data = []
	for url in urls_file:
		if url['url'] in errors_file:
			data.append(url)
	return data


def main():
	errors_file = read_file(errors_file_name)
	urls_file = read_file(urls_file_name)
	data = extract_errors(errors_file, urls_file)
	save_file(data)


if __name__ == '__main__':
	main()
