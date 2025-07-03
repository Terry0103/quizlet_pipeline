import requests
from bs4 import BeautifulSoup
import csv
import time
import datetime
import logging




def get_cambridge_entry(word):
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    return BeautifulSoup(res.text, "html.parser")

def get_cambridge_zh_translation(word):
    url = f"https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    trans_tag = soup.find("span", class_="trans dtrans dtrans-se break-cj")
    return trans_tag.text.strip() if trans_tag else "無翻譯"

def extract_definitions_and_examples(soup, max_defs=3):
    entries = soup.find_all("div", class_="pr entry-body__el")
    pos_dict = {}

    for entry in entries:
        pos_tag = entry.find("span", class_="pos dpos")
        def_tags = entry.find_all("div", class_="def ddef_d db")
        example_tags = entry.find_all("div", class_="examp dexamp")

        if pos_tag and def_tags:
            pos = pos_tag.text.strip()
            defs = [d.text.strip().rstrip(":").replace(",", ";") for d in def_tags[:max_defs]]
            examples = [e.text.strip().rstrip(":").replace(",", ";") for e in example_tags[:2]]  # max 2 examples
            if pos not in pos_dict:
                pos_dict[pos] = {"defs": [], "examples": []}
            pos_dict[pos]["defs"].extend(defs)
            pos_dict[pos]["examples"].extend(examples)

    return pos_dict

def get_cambridge_collocations(word):
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Look for word combination phrases — these show collocations
    colloc_tags = soup.find_all("span", class_="phrase-title dphrase-title")

    collocations = [tag.text.strip() for tag in colloc_tags]
    return collocations if collocations else []


def format_entry(word):
    soup_en = get_cambridge_entry(word)
    zh_translation = get_cambridge_zh_translation(word)
    pos_dict = extract_definitions_and_examples(soup_en)
    collocations = get_cambridge_collocations(word)


    lines = [f"{word},{zh_translation}"]

    for pos, content in pos_dict.items():
        defs = content["defs"][:MAX_DEFS]
        if defs:
            line = f"({pos}) • " + " • ".join(defs)
            lines.append(line)

    # Add example sentences
    for pos, content in pos_dict.items():
        for ex in content["examples"][:MAX_EXPS]:
            lines.append(f"e.g., {ex}")

    if collocations:
        m = min(len(collocations), 3)
        lines.append("Collocations: " + "\n" + "\n".join(collocations[: m]))

    return "\n".join(lines)

if __name__ == "__main__":
    VOCAB_TXT: str = "temp.txt"
    STR_DATETIME: str = datetime.datetime.now().strftime("%Y-%m-%d")
    FINE_NAME: str = f"./vocab_csv/{STR_DATETIME}_{VOCAB_TXT}.csv"
    MAX_DEFS: int = 2
    MAX_EXPS: int = 1


    logging.basicConfig(
    filename = f'./log/{STR_DATETIME}_vocab',
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

    # Your word list
    words: list[str] = []
    with open(f"./vocabulary_list/{VOCAB_TXT}", "r") as f:
        for w in f:
            words.append(w.strip())

    # Save output
    with open(FINE_NAME, "a", encoding="utf-8") as f:
        for word in words:
            entry_text = format_entry(word)
            f.write(entry_text + "\n\n")  # double newline between words
            time.sleep(1)  # be respectful when scraping

