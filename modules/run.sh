#!/bin/sh

V=../dataset/vocab-15kws.txt
Vc=../dataset/vocab-5k.txt
wiki=../dataset/wiki-1per*.txt
men=../dataset/men*
simlex=../dataset/simlex*

mkdir $1/
touch $1/summary.log

for w in 1 3 6
do
   for file in $Vc $V
   do
        echo "Input setting: w = $w, context file = $V, $file"
        echo "\nInput setting: w = $w, context file = $V, $file" >> foo/summary.log
        echo "Running distCounter.py..."
        python distCounter.py $V $file $wiki $w
        echo "Running idfCounter.py..."
        python idfCounter.py $V $file distCountOp.txt $wiki
        echo "Running pmiCounter.py..."
        python pmiCounter.py $V $file distCountOp.txt
        echo "EvalWS comparison..."
        python EvalWS.py $V $file distCountOp.txt $men $simlex $1/summary.log
        python EvalWS.py $V $file pmiCountOp.txt $men $simlex $1/summary.log
        python EvalWS.py $V $file idfCountOp.txt $men $simlex $1/summary.log
        echo "Done!"
   done
done
