import EvalWS
import sys

class idfCounter:

    def __init__(self, V, Vc):
        self.V, self.Vc = EvalWS.fileReader(V, Vc)

    def getCounting(self, sourceFile, targetFile):

        hm = {}
        S = 0

        with open(targetFile, "r") as f:
            for sentence in f:
                S += 1
                tokens = sentence.strip().split()
                for token in tokens:
                    if (token in self.Vc):
                        hm[token] = hm.get(token, 0) + 1
        for key in hm:
            hm[key] = S / hm[key]

        source = EvalWS.sourceReader(sourceFile)

        for key in source:
            v, vc = key
            if (vc in hm):
                source[key] *= hm[vc]

        return source


############################################################

if __name__ == "__main__":

    assert (len(sys.argv) ==
            5), "Required file sequence: V.txt, Vc.txt, distCountOp.txt and wiki.txt"

    operator = idfCounter(sys.argv[1], sys.argv[2])
    res = operator.getCounting(sys.argv[3], sys.argv[4])

    print("Exporting results in idfCountOp.txt")

    with open("idfCountOp.txt", "w") as f:
        f.write(" x@y | tf-idf \n")
        for key in res:
            f.write(f"{key[0]}@{key[1]} {res[key]} \n")
