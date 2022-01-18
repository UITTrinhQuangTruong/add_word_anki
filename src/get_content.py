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
            with open(input_file, "r") as f:
                list_of_words = [i for i in f.read().split("\n") if i != ""]
        except:
            print(f"{input_file} not exists!!!")
            sys.exit(1)
    else:
        list_of_words = [input("Type your word:\t")]

    output_path = os.path.join(save_dir, output_file)
    if os.path.isfile(output_path):
        df = pd.read_csv(output_path, header=None)
    else:
        df = pd.DataFrame(columns=range(5))

    flag = 0
    for word in list_of_words:
        if word in df[0].values:
            if flag < 2:
                print(
                    f"{word} exists in dictionary! Do you want to replace it? (y, ya, n, na)")
                ans = input().lower()
                if ans == "y":
                    flag = 1
                elif ans == "ya":
                    flag = 2
                elif ans == "na":
                    flag = 3
            if flag == 1 or flag == 2:
                result = model.get_word(word)
                index = df[0] == word
                df.loc[index] = [result]
            continue
        result = model.get_word(word)
        df_length = len(df)
        df.loc[df_length] = result

    df.to_csv(output_path, header=False, index=False)
