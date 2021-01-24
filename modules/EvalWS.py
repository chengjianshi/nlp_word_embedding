import numpy as np
import sys
from scipy import stats

class EvalWS:

    def __init__(self, V, Vc):
        buf1, buf2 = fileReader(V, Vc)
        self.V = {}
        self.Vc = {}
        for i, v in enumerate(buf1):
            self.V[v] = i
        for i, vc in enumerate(buf2):
            self.Vc[vc] = i

    def wordEmbedding(self, sourceFile):
        source = sourceReader(sourceFile)
        M = np.zeros((len(self.Vc), len(self.V)))
        for i, key in enumerate(source):
            v, vc = key
            M[self.Vc[vc], self.V[v]] = source[key]
        for i in range(len(self.V)):
            norm = np.linalg.norm(M[:, i])
            if (norm == 0):
                pass
            else:
                M[:, i] /= norm
        self.M = np.dot(M.T, M)
        return

    def EvalWS(self, targetFile):

        target = sourceReader(targetFile, target=True)

        lst1 = np.zeros(len(target))
        lst2 = np.zeros(len(target))

        for i, key in enumerate(target):
            v1, v2 = key
            if ((v1 not in self.V) or (v2 not in self.V)):
                sim = 0
            else:
                sim = self.M[self.V[v1], self.V[v2]]
            lst1[i] = sim
            lst2[i] = target[key]
        corr, _ = stats.spearmanr(lst1, lst2)
        return corr

def sourceReader(file, target=False):

    source = {}

    print(f"\nPouring source file {file}:\n")

    with open(file, "r") as f:
        for i, line in enumerate(f):
            print(f"read lines: {i} ", end="\r")
            if (i == 0):
                continue
            line = line.strip().split()
            if (target):
                v, vc, val = line
            else:
                keys, val = line
                v, vc = keys.split("@")
            source[(v, vc)] = float(val)

    print("Done!")
    return source


def fileReader(file1, file2):

    print(f"\nPouring center words from {file1} and context words from {file2}\n")

    with open(file1, "r") as f1:
        V = [l.strip() for l in f1]
    with open(file2, "r") as f2:
        Vc = [l.strip() for l in f2]

    print("Done!")

    return set(V), set(Vc)

############################################################


if __name__ == "__main__":

    assert (len(sys.argv) ==
            7), "Required files sequence: V.txt, Vc.txt, xxCountOp.txt, MEN.txt, SimLex-999.txt, logfile.txt."

    operator = EvalWS(sys.argv[1], sys.argv[2])
    operator.wordEmbedding(sys.argv[3])
    corr1 = operator.EvalWS(sys.argv[4])
    corr2 = operator.EvalWS(sys.argv[5])

    with open(f"{sys.argv[6]}", "a") as f:
        f.write(f"\nspearmanr correlation for {sys.argv[3]}:\n")
        f.write(f"{sys.argv[4]}: {corr1}, {sys.argv[5]}: {corr2}\n")
