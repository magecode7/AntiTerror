from math import fabs
import re
import nltk
from nltk.probability import FreqDist
nltk.download('stopwords')
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

#patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-–]+"
patterns = "[^а-яА-Яa-zA-Z0-9]"
stopwords_ru = stopwords.words("russian") + stopwords.words("english")
morph = MorphAnalyzer()

def tokenize(text: str) -> list[str]:
    text = re.sub(patterns, ' ', text)

    tokens = []
    for token in text.split():
        token = token.lower()
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            if not token:
                continue
            tokens.append(token)
    return tokens

def lemmatize(text: str) -> str:
    t = tokenize(text)
    if t == None: t = ''
    return ' '.join(t)

def top_tokens(text: str):
    fdist = FreqDist(text)
    return fdist.most_common()

def main():
    print(lemmatize(input()))

if __name__ == "__main__":
    main()