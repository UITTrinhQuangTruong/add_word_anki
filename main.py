import argparse

from src import get_content

path_default = "/mnt/c/Users/quang/AppData/Roaming/Anki2/Truongdz/collection.media"


def main():
    parser = argparse.ArgumentParser(
        description="Get word for Anki application")
    parser.add_argument("--dictionary", type=str, default="longman")
    parser.add_argument("--input_file", type=str, default=None)
    parser.add_argument("--save_dir", type=str, default=path_default)
    parser.add_argument("--output_file", type=str, default="dictionary.csv")

    args = parser.parse_args()
    get_content(args.dictionary, args.input_file,
                args.save_dir, args.output_file)


if __name__ == "__main__":
    main()
