import EvalWS
import sys
import numpy as np

class pmiCounter:

    def __init__(self, V, Vc):
        buf1, buf2 = EvalWS.fileReader(V, Vc)
        self.V = {}
        self.Vc = {}
        for i, v in enumerate(buf1):
            self.V[v] = 0
        for i, vc in enumerate(buf2):
            self.Vc[vc] = 0

    def getCounting(self, sourceFile):
        source = EvalWS.sourceReader(sourceFile)
        pmi = {}
        N = 0
        for key in source:
            N += source[key]
            v, vc = key
            self.V[v] += source[key]
            self.Vc[vc] += source[key]
            pmi[key] = 0

        for key in pmi:
            v, vc = key
            pmi[key] = np.log2(source[key] * N / (self.V[v] * self.Vc[vc]))

        return pmi


############################################################

if __name__ == "__main__":

    assert (len(sys.argv) ==
            4), "Required file sequence: V.txt, Vc.txt, distCoutOp.txt"

    operator = pmiCounter(sys.argv[1], sys.argv[2])
    res = operator.getCounting(sys.argv[3])

    print("Exporting result to pmiCountOp.txt")

    save = {}

    with open("pmiCountOp.txt", "w") as f:

        f.write("x@y | pmi \n")

        for key in res:
            v, vc = key
            if (v == "coffee"):
                save[vc] = res[key]
            f.write(f"{v}@{vc} {res[key]} \n")

    # print("Top 10 highest PMI context word to 'Coffee': \n")

    # for i, key in enumerate(sorted(save, key=save.get, reverse=True)):
    #     if (i > 9):
    #         break
    #     print(f"PMI [{key}] = {save[key]}")

    # print("Top 10 lowest PMI context word to 'Coffee': \n")

    # for i, key in enumerate(sorted(save, key=save.get, reverse=False)):
    #     if (i > 9):
    #         break
    #     print(f"PMI [{key}] = {save[key]}")
