#!/usr/bin/env python3

import argparse
import sys
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

parser = argparse.ArgumentParser()
parser.add_argument("--event_id", default=482363)
args = parser.parse_args()


def make_soup(url: str) -> BeautifulSoup:
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return BeautifulSoup(driver.page_source, "html.parser")


def find_class(class_: str, soup: BeautifulSoup) -> str:
    try:
        return soup.css.select("." + class_)[1].text.strip()
    except IndexError:
        return "error_not_found"


soup = make_soup(
    f"https://runsignup.com/Race/Results/131115#resultSetId-{args.event_id};perpage:5000"
)
sys.stdout.write(soup.prettify())


# Write individual details
data = []
for row in soup.css.select("tbody > tr"):

    if suffix := row.attrs.get("data-result-url") is not None:

        url = "https://runsignup.com" + suffix
        soup = make_soup(url)
        data.append(
            {
                _class: find_class(_class, soup)
                for _class in (
                    "eventName",
                    "gender",
                    "age",
                    "location",
                    "bibDisplay__bibNum",
                )
            }
        )
        data[-1]["url"] = url

pd.DataFrame(data).rename(columns=dict(bibDisplay__bibNum="bib")).to_csv(
    sys.stderr, index=False
)
