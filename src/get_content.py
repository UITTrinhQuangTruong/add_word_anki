import os
import sys

import pandas as pd

from src.dictionary import LongMan


def get_content(dictionary, input_file, save_dir, output_file):
    if dictionary == "longman":
        model = LongMan(dir=save_dir)

    else:
        print("--dictionary not available!!!")
        sys.exit(1)

    if input_file != None:
        try:
            with open(input_file, "w") as f:
                list_of_words = f.read().split("\n")
        except:
            print(f"{input_file} not exists!!!")
            sys.exit(1)
    else:
        word = [input("Type your word:\t")]

    if os.path.isfile(output_file):
        df = pd.read_csv(output_file, header=None)
    else:
        df = pd.DataFrame(columns=range(5))

    for word in list_of_words:
        result = dictionary.get_word(word)
        df_length = len(df)
        df.loc[df_length] = result

    df.to_csv(output_file, header=False, index=False)
