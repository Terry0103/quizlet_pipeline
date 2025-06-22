import requests
from bs4 import BeautifulSoup
import csv
import time
import datetime
import logging

str_datetime: str = datetime.datetime.now().strftime("%Y-%m-%d")
logging.basicConfig(
    filename = f'./log/{str_datetime}_vocab',
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")



FINE_NAME: str = f"./vocab_csv/{str_datetime}_quizlet_vocabs.csv"

# def get_grouped_definitions(word):
#     url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     res = requests.get(url, headers=headers)
#     soup = BeautifulSoup(res.text, "html.parser")

#     entries = soup.find_all("div", class_="pr entry-body__el")
#     pos_dict = {}

#     for entry in entries:
#         pos_tag = entry.find("span", class_="pos dpos")
#         def_tags = entry.find_all("div", class_="def ddef_d db")

#         if pos_tag and def_tags:
#             pos = pos_tag.text.strip()
#             definitions = [d.text.strip().rstrip(":") for d in def_tags]
#             if pos not in pos_dict:
#                 pos_dict[pos] = []
#             pos_dict[pos].extend(definitions)

#     # Build single Quizlet-style definition string
#     if not pos_dict:
#         return "Definition not found"

#     parts = []
#     for pos, defs in pos_dict.items():
#         grouped = f"({pos}) • " + " • ".join(defs[:3]).replace("\"", '')  # limit to 3 defs per POS
#         parts.append(grouped)

#     return ("\n".join(parts) + "\n")

# Your word list
# words = ["run", "gregarious", "obfuscate", "benevolent"]

# # Write output CSV
# with open(FINE_NAME, "w", newline='', encoding="utf-8") as f:
#     writer = csv.writer(f)
#     for word in words:
#         definition = get_grouped_definitions(word)
#         if definition == "Definition not found":
#             logging.error(f"{word}, Definition not found")

#         time.sleep(3)
#         writer.writerow([word, definition])
#         logging.info(f"{word}, process work well")