import itertools
import numpy as np
import EvalWS
import sys

class distCounter:

    def __init__(self, files):
        self.V, self.Vc = EvalWS.fileReader(files[0], files[1])

    def getCounting(self, target, window):

        hm = {}

        with open(target, "r") as f:
            for sentence in f:
                tokens = sentence.strip().split()
                for i in range(len(tokens)):
                    if (tokens[i] not in self.V):
                        continue
                    temp = [*tokens[max(0, i - window):i], *tokens[i + 1:min(len(tokens), i + window + 1)]]
                    for token in temp:
                        if (token not in self.Vc):
                            continue
                        key = (tokens[i], token)
                        hm[key] = hm.get(key, 0) + 1

        return hm


########################################################


if __name__ == "__main__":

    assert len(
        sys.argv) == 5, "Required files sequence: 'V.txt', 'Vc.txt', 'target.txt', window_size"

    operator = distCounter([sys.argv[1], sys.argv[2]])

    res = operator.getCounting(sys.argv[3], window=int(sys.argv[4]))

    print("Exporting results in distCountOp.txt")

    with open("distCountOp.txt", "w") as f:
        f.write(f" x@y | tf | w= {sys.argv[4]} | V = {sys.argv[1]} Vc = {sys.argv[2]} \n")
        for key in res:
            f.write(f"{key[0]}@{key[1]} {res[key]}\n")
