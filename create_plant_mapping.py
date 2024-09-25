import argparse
import json


def main(args):
    with open(args.input_file, "r") as file:
        data = json.load(file)

    mapping = {}
    counter = 0
    for _, value in data.items():
        mapping[counter] = value
        counter += 1

    with open(args.output_file, "w") as file:
        json.dump(mapping, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="store", dest="input_file")
    parser.add_argument("--output", action="store", dest="output_file")
    args = parser.parse_args()
    if not (args.input_file or args.output_file):
        parser.error("No input or output file")
    main(args)
