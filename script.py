import pandas as pd
import re
from collections import Counter


# 1) Charger les données
df = pd.read_csv("Headphone_Dataset.csv")

# 2) Fonctions d'extraction depuis la colonne "Comment"

def extract_title(text):
    lines = text.splitlines()
    return lines[0].strip() if lines else None

def extract_country(text):
    match = re.search(r"Reviewed in (.*?) on", text)
    return match.group(1).strip() if match else None

def extract_date(text):
    match = re.search(r"Reviewed in .*? on (.*)", text)
    if match:
        line = match.group(1).splitlines()[0]
        return line.strip()
    return None

def extract_color(text):

    match = re.search(r"Color:\s*(.*?)(Verified Purchase|$)", text, flags=re.DOTALL)
    return match.group(1).strip() if match else None

def extract_verified(text):
    return "Verified Purchase" in text

def extract_useful_votes(text):
    match = re.search(r"(\d+)\s+people found this helpful", text)
    return int(match.group(1)) if match else 0

def extract_review_text(text):
    lines = text.splitlines()
    if len(lines) <= 3:
        return None

    body_lines = []
    for line in lines[3:]:
        if re.search(r"\d+\s+people found this helpful", line):
            break
        if line.strip() in ("Helpful", "Report"):
            break
        if line.strip() == "":
            continue
        body_lines.append(line.strip())

    return " ".join(body_lines) if body_lines else None

# 3) Création des nouvelles colonnes

df["title"] = df["Comment"].apply(extract_title)
df["country"] = df["Comment"].apply(extract_country)
df["date"] = df["Comment"].apply(extract_date)
df["color"] = df["Comment"].apply(extract_color)
df["verified"] = df["Comment"].apply(extract_verified)
df["useful_votes"] = df["Comment"].apply(extract_useful_votes)
df["review_text"] = df["Comment"].apply(extract_review_text)

print(df[["title", "country", "date", "color", "verified", "useful_votes"]].head())

print("\n--- APERÇU COMMENTAIRE ---")
print(df[["title", "review_text"]].head())


###Structure du dataset

print("\n--- DIMENSIONS ---")
print(df.shape)

print("\n--- TYPES ---")
print(df.dtypes)


###Qualité des données

print("\n--- MISSING VALUES ---")
print(df.isna().sum())

###Distribution des notes
print("\n--- STAR DISTRIBUTION ---")
print(df["Star"].value_counts().sort_index())


###Répartition par pays
print("\n--- TOP COUNTRIES ---")
print(df["country"].value_counts().head(10))

####Répartition couleur

print("\n--- COLORS ---")
print(df["color"].value_counts())

###Longueur des commentaires
df["comment_length"] = df["review_text"].apply(lambda x: len(str(x)))

print("\n--- COMMENT LENGTH STATS ---")
print(df["comment_length"].describe())


###Mots les plus fréquents 
import re
from collections import Counter

def clean_for_freq(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return text

df["clean_text"] = df["review_text"].apply(clean_for_freq)

all_words = " ".join(df["clean_text"]).split()
counter = Counter(all_words)

print("\n--- MOST COMMON WORDS ---")
print([w for w in counter.most_common(30) if len(w[0])>3])
