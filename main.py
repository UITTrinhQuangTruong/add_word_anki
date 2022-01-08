import argparse

from src import get_content


def main():
    parser = argparse.ArgumentParser(description="Get word for Anki application")
    parser.add_argument("--dictionary", type=str, default="longman")
    parser.add_argument("--input_file", type=str, default=None)
    parser.add_argument("--save_dir", type=str, default=".")
    parser.add_argument("--output_file", type=str, default="dictionary.csv")

    get_content(
        parser.dictionary, parser.input_file, parser.save_dir, parser.output_file
    )
