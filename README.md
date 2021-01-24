Tokenization/Word Embedding
=======
# README.md

> Python version - 3.8.5
> 

## 1. Tokenization

**Tokenization.py** contains four tokenization methods: *whiteSpace, NTLK, SpaCy* and *BPE*. 

To acquire output, there are two required arguements, **data.txt** and **train.raw** both are "content" column in **IRAhandle_tweets_1.csv** used as input source data. 

```python
python tokenization.py data.txt train.raw
```

The **output.log** file are tokenized results answering first three questions. 

## 2. Word Counting/Embedding

### 2.1 Counting script

Three word counting/embedding methods are packaged into: **distCounter.py** /distributional counting; **idfCounter.py**/tf-idf counting; **pmiCounter.py** /PMI counting. 

Both **idfCounter.py** and **pmiCounter.py** requires input data file from the output of **distCountOp.txt** as source file. Indeed, the parameter setting of *window_size* should be done in **distCounter.py** and the center/context word file required to be consistant to **distCounter.py** on others.

> format of getting distribution counting output
```python
python distCounter.py centerWord.txt contextWord.txt targetFile.txt windowSize
```

> The output of distCounter.py saved in distCountOp.txt

> example
```
python distCounter.py vocab-15kws.txt Vc = vocab-15kws.txt wiki-1percent.txt 6

head -n 10 distCountOp.txt

x@y | tf | w= 6 | V = vocab-15kws.txt Vc = vocab-15kws.txt 
they@encouraged 12
they@playing 72
they@with 2284
they@sexual 17
they@roles 18
they@and 8170
encouraged@they 12
encouraged@playing 2
encouraged@with 32
```

The formats of **idfCounter.py** and **pmiCounter.py** are similar to **distCounter.py** except requires output of **distCounter.py** as source file.

> format of getting tf-idf counting output
```
python idfCounter.py centerWord.txt contextWord.txt source.txt targetFile.txt 
python pmiCounter.py centerWord.txt contextWord.txt source.txt
```

> The output of distCounter.py/pmiCounter.py saved in idfCountOp.txt/pmiCountOp.txt
> 
> example
```
python idfCouter.py vocab-15kws.txt vocab-15kws.txt distCountOp.txt wiki-1percent.txt
python pmiCounter.py vocab-15kws.txt vocab-15kws.txt distCountOp.txt

head -n 10 pmiCountOp.txt

x@y | pmi | window = 6
they@encouraged 0.29142617272133425 
they@playing 0.33361365128863174 
they@with 0.09450506732157941 
they@sexual 0.17631284241651715 
they@roles -0.006463674152033827 
they@and -0.13044860509714454 
encouraged@they 0.29142617272133425 
encouraged@playing 1.0551886479628758 
encouraged@with -0.17134186992470699 
```

### 2.2 Similarity Score

To evaluate the performance of various word counting/embedding methods. We can use the output files *..CountOp.txt* as source file and compared it with gold standard (*MEN, SimLex-999*) through similarity score (spearman correlation coefficient). 

The module to get score is EvalWS.py. 

> format of EvalWS.py
```
python EvalWS.py centerWord.txt contextWord.txt xxCountOp.txt goldStandard.txt output.log
```

> example
> compute similarity score of distributional counting (winodow size = 6) result to MEN and SimLex-999
```
python EvalWs.py vocab-15kws.txt vocab-15kws.txt distCountOp.txt men.txt simlex-999.txt save.log

cat save.log 

spearmanr correlation for distCountOp.txt:
men.txt: 0.24106664963215607, simlex-999.txt: 0.04469576384051759
```

### 2.3 Quantitative Comparison

The quantitative comparison script for **W = (1,3,6)** and context word file as **(vocab-15kws.txt, vocab-5k.txt)** is written in shell script **run.sh**. Run shell script in terminal and results are saved as **summary.log** in target file.

> example
```
./run.sh foo/

head -n 10 foo/summary.log

Input setting: w = 1, context file = dataset/vocab-15kws.txt, dataset/vocab-5k.txt

For distCountOp.txt:
spearmanr correlation with dataset/men.txt: 0.209091543574558
spearmanr correlation with dataset/simlex-999.txt: 0.06778569953818134

For pmiCountOp.txt:
spearmanr correlation with dataset/men.txt: 0.433603129702521
spearmanr correlation with dataset/simlex-999.txt: 0.22749770004854117

...
```

### 2.4 Qualitative Analysis (KNN)

The **KNNgetter.py** is written to acquire the KNN of query word list. It requires the center/context/source files of specific word counting/embedding method (center/context file should be consistant with embedding output paramters) and the results are saved in output file. 

> format
```
python KNNgetter.py centerWord.txt contextWord.txt sourceFile queryWord K output
```

> example get 10 NN of query words (apple and bank)
```
python KNNgetter.py vocab-15kws.txt vocab-15kws.txt pmiCountOp.txt query.txt 10 output.log

cat output.log

apple:['os', 'microsoft', 'macintosh', 'mac', 'ios', 'software', 'desktop', 'computers', 'linux', 'iphone']
bank:['corporation', 'banks', 'company', 'railway', 'river', 'capital', 'west', 'central', 'east', 'northern']
```
>>>>>>> 15387be... init repo
