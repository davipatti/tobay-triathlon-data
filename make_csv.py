#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import pandas as pd
import re


def clean_str(s: str) -> str:
    s = s.strip()
    # remove multiple consecutive " " and "\n" chars
    s = re.sub(r"(\n)+", " ", s)
    s = re.sub(r"( )+", " ", s)
    return s


soup = BeautifulSoup(sys.stdin, "html.parser")


def process_row(row) -> list[str]:
    elements = row.find_all("td")
    if not elements:
        elements = row.find_all("th")
    return [clean_str(element.text) for element in elements]


pd.DataFrame(
    [process_row(row) for row in soup.css.select("tbody > tr")],
    columns=process_row(soup.css.select("thead > tr")[0]),
).rename(columns={"Finish Time": "Chip Time"}).to_csv(sys.stdout, index=False)
