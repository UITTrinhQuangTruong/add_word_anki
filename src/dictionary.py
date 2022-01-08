import os
from deep_translator import GoogleTranslator

from src.helper import get_page_content


class LongMan:
    def __init__(self, dir) -> None:
        self.translater = GoogleTranslator(source="en", target="vi")
        self.dir = dir

        if not os.path.isdir(dir):
            os.makedirs(dir)

    def _preprocess(self):
        url = f"https://www.ldoceonline.com/dictionary/{self.word.replace(' ', '-')}"
        self.lm_page_content = get_page_content(url)

        # remove unnecessary tags
        self.lm_page_content.find("head").decompose()
        for i in self.lm_page_content.findAll("script"):
            i.decompose()
        for i in self.lm_page_content.findAll("noscript"):
            i.decompose()
        classes = ["header", "footer", "responsive_cell2", "topslot-container"]
        for class_ in classes:
            self.lm_page_content.find("div", class_=class_).decompose()
        classes = [
            "ColloExa",
            "Thesref",
            "assetlink",
            "asset div",
            "dictionary_intro span",
            "PhrVbEntry",
            "PICCAL",
            "Tail",
            "am-dictionary",
            "ORIGIN",
            "LANG",
        ]
        for class_ in classes:
            for i in self.lm_page_content.findAll("span", class_=class_):
                i.decompose()

        content_of_word = self.lm_page_content.findAll("span", class_="dictlink")
        for i in content_of_word:
            if i.find("span", class_="Sense") == None:
                i.decompose()

        # Fix link to longman dictionary
        for i in self.lm_page_content.findAll("a"):
            i["href"] = "https://www.ldoceonline.com" + i["href"]

    def _change_voice(self, voice="uk"):
        heads_of_word = self.lm_page_content.findAll("span", class_="frequent Head")

        class_ = (
            "speaker brefile fas fa-volume-up hideOnAmp"
            if voice == "uk"
            else "speaker amefile fas fa-volume-up hideOnAmp"
        )

        for idx, head in enumerate(heads_of_word):
            name_of_file = f"{self.word}_{voice}_{idx}.mp3"
            audio = head.find("span", class_=class_)
            string = f"[sound:{name_of_file}]"
            os.system(f"wget {audio['data-src-mp3']} -O {name_of_file}")
            new_tag = self.lm_page_content.new_tag("span", **{"class": "us_au"})
            new_tag.string = string
            audio.decompose()
            head.append(new_tag)

    def _get_examples(self):
        list_examples = self.lm_page_content.findAll("span", class_="EXAMPLE")
        idx = 0
        while idx < len(list_examples):
            parent = list_examples[idx].parent
            for j in parent.findChildren("span", class_="EXAMPLE", recursive=False)[1:]:
                j.decompose()
            idx += 1
            list_examples = self.lm_page_content.findAll("span", class_="EXAMPLE")

        # Change link to audio example
        self.example = ""
        for idx, i in enumerate(self.lm_page_content.findAll("span", class_="EXAMPLE")):
            try:
                name_of_file = f"{self.word}_example_{idx}.mp3"
                audio = i.find(
                    "span", class_="speaker exafile fas fa-volume-up hideOnAmp"
                )
                string = f"{i.text} [sound:{name_of_file}]"
                if self.example == "":
                    self.example = i.text.strip()

                # Download file audio
                os.system(f"wget {audio['data-src-mp3']} -O {name_of_file}")
                audio.decompose()
                i.string = string
            except:
                pass

    def _get_suggest(self):
        list_of_words = self.word.split(" ")
        classes = ["PASTTENSE", "PASTPART", "T3PERSSING"]
        for i in classes:
            word_ = self.lm_page_content.find("span", class_=i)
            if word_ != None:
                list_of_words.append(word_.text)
        example_ = self.example
        for i in list_of_words:
            if i in example_:
                example_ = example_.replace(
                    i, f"  {' '.join(['__' for _ in range(len(i))])}  "
                )

        def_of_word = self.lm_page_content.find("span", class_="DEF").text
        self.suggestion = f"<div><span class='english'>{def_of_word} - </span><span class='vietnamese'>{self.translater.translate(def_of_word)}</span></div><div><span class='english'>{example_} - </span><span class='vietnamese'>{self.translater.translate(self.example)}</span></div>"

    def _get_content(self):

        self._preprocess()
        self._change_voice()
        self._get_examples()
        self._get_suggest()

        name_img = f"{self.word}.jpg"
        self.image = f"<img scr='{name_img}'></img>"
        self.vietnamese = self.translater.translate(self.word)

    def get_word(self, word):
        self.word = word.lower().strip()
        self._get_content()

        return [
            self.word,
            self.suggestion,
            self.vietnamese,
            f"{self.lm_page_content}",
            self.image,
        ]