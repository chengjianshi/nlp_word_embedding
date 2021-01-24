from nltk.tokenize import WordPunctTokenizer
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import spacy
import numpy
import sys

class tokenizer:

    def __init__(self, document):
        self.document = [d.lower() for d in document]

    def whiteSpaceTokenizer(self):
        return [d.split() for d in self.document]

    def nltkTokenizer(self):
        tk = WordPunctTokenizer()
        return [tk.tokenize(d) for d in self.document]

    def spacyTokenizer(self):
        nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner"])
        res = []
        for doc in self.document:
            sentence = nlp(doc)
            res.append([d.text for d in sentence])
        return res

    def bpeTokenizer(self, rawTrainFile):
        tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
        tokenizer.pre_tokenizer = Whitespace()
        trainer = BpeTrainer(
            special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
        tokenizer.train([rawTrainFile], trainer)
        return [tokenizer.encode(d).tokens for d in self.document]


def getResult(documents):
    # print first 3 tweets
    print("First three tweets:")
    for i in range(3):
        print(documents[i], end="\n")
    # types/tokens, top10 words
    hm = {}
    count = 0
    for document in documents:
        for token in document:
            count += 1
            hm[token] = hm.get(token, 0) + 1
    return count, len(hm), sorted(hm, key=hm.get, reverse=True)[:10]


def fileReader(fileRoute):
    with open(fileRoute, "r") as f:
        content = [l.strip() for l in f]
    return content

###############################################################


if __name__ == "__main__":

    assert len(sys.argv) == 3, "Two raw files routes are required."

    data = fileReader(sys.argv[1])

    operator = tokenizer(data)

    with open("output.log", "w") as f:

        numToken1, numType1, topWord1 = getResult(
            operator.whiteSpaceTokenizer())
        f.write(f"Q_1.1. WhiteSpace tokenizer:\n Number of Tokens: {numToken1}, Number of Types: {numType1}, Ratio: {numType1/numToken1}\n Top 10 words:{topWord1}\n")

        numToken2, numType2, topWord2 = getResult(operator.nltkTokenizer())
        f.write(f"Q_1.2. NLTK tokenizer:\n Number of Tokens: {numToken2}, Number of Types: {numType2}, Ratio: {numType2/numToken2}\n Top 10 words:{topWord2}\n")

        numToken3, numType3, topWord3 = getResult(operator.spacyTokenizer())
        f.write(f"Q_1.3. SpaCy tokenizer:\n Number of Tokens: {numToken3}, Number of Types: {numType3}, Ratio: {numType3/numToken3}\n Top 10 words:{topWord3}\n")

        numToken4, numType4, topWord4 = getResult(
            operator.bpeTokenizer(sys.argv[2]))
        f.write(f"Q_1.4. BPE tokenizer:\n Number of Tokens: {numToken4}, Number of Types: {numType4}, Ratio: {numType3/numToken4}\n Top 10 words:{topWord4}\n")
