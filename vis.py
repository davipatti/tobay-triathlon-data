#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year")
args = parser.parse_args()

plt.style.use("seaborn-v0_8-whitegrid")


def _classify_sex(division):
    d = division.lower()
    if "female" in d:
        return "f"
    elif "male" in d:
        return "m"
    else:
        return d[0]


def classify_sex(df):
    df["sex"] = [_classify_sex(division) for division in df["Division"]]
    return df


def mung_age(df):
    df["age"] = df["age"].str.replace("Age ", " ").astype(float)
    return df


df_inds = (
    pd.read_csv(f"csv/{args.year}-individuals.csv")
    .query("bib != 'error_not_found'")
    .astype({"bib": int})
    .set_index("bib")
    .pipe(mung_age)
)


def mung_chip_time(df):
    ct = ["00:" + ct if ct.count(":") == 1 else ct for ct in df["Chip Time"]]
    df["Chip Time"] = pd.to_timedelta(ct)
    df["minutes"] = df["Chip Time"].dt.seconds / 60.0
    return df


df = (
    pd.read_csv(f"csv/{args.year}-main.csv", index_col="Bib")
    .dropna(subset="Chip Time")
    .pipe(mung_chip_time)
    .join(df_inds)
    .pipe(classify_sex)
)


fig, axes = plt.subplots(ncols=2, sharey=True, sharex=True, figsize=(12, 3))

for sex, ax in zip("mf", axes):
    sub_df = df.query("sex == @sex")
    ax.scatter(sub_df["age"], sub_df["minutes"], label=sex, s=15, lw=0.5, ec="white")
    ax.set(title=f"sex = {sex}", xlabel="Age (years)", ylabel="Time (mins)")
    plt.suptitle(args.year)

for format in "png", "pdf":
    plt.savefig(f"img/{args.year}-age-vs-time.{format}", bbox_inches="tight")
