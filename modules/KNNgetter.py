from EvalWS import EvalWS
import sys

class KNN(EvalWS):

    def __init__(self, V, Vc, source):
        super().__init__(V, Vc)
        self.wordEmbedding(source)

    def get(self, query, K):
        if (query not in self.V):
            return []
        lst = list(zip(self.M[self.V[query], :].flatten().tolist(), [*self.V]))
        return sorted(lst, key=lambda f: f[0], reverse=True)[1:K + 1]


############################################################

if __name__ == "__main__":

    assert (len(sys.argv) ==
            7), "Required files sequence: V.txt, Vc.txt, xxCountOp.txt, queryWordFile, K, output.log"

    operator = KNN(sys.argv[1], sys.argv[2], sys.argv[3])
    res = {}

    with open(f"{sys.argv[4]}", "r") as f:
        for word in f:
            word = word.strip()
            buf = operator.get(word, int(sys.argv[5]))
            res[word] = [b[1] for b in buf]

    with open(f"{sys.argv[6]}", "w") as f:
        for key in res:
            f.write(f"{key}:{res[key]}\n")
