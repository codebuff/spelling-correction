##### options
```python
python -m spell-correction.MED.normal_MED
python -m spell-correction.MED.backtrace_MED
python -m spell-correction.MED.weighted_MED
python -m spell-correction.MED
python -m spell-correction.task0
python -m spell-correction.task1
python -m spell-correction.task2
```

***

##### Options' details and expected outputs

```python
python -m spell-correction.MED.normal_MED
```
```
Enter the string to be changed
xyzd
Enter the desired string
ayrd
MED by normal method: 4
```
---
```python
python -m spell-correction.MED.backtrace_MED
```
```
Enter the string to be changed
intention
Enter the desired string
execution
MED with backtracing  8
  === Alignment ===  
i n t e * * * * n t i o n
| | | | | | | | | | | | | 
* * * e x e c u * t i o n
  === Steps ===  
Step 1 delete i
Step 2 delete n
Step 3 delete t
Step 4 substitute/copy e with e (NO OP)
Step 5 insert x
Step 6 insert e
Step 7 insert c
Step 8 insert u
Step 9 delete n
Step 10 substitute/copy t with t (NO OP)
Step 11 substitute/copy i with i (NO OP)
Step 12 substitute/copy o with o (NO OP)
Step 13 substitute/copy n with n (NO OP)
```
---
```python
python -m spell-correction.MED.weighted_MED
```
```
creating confusion matrices
Enter the string to be changed
intention
Enter the desired string
execution
Weighted MED 0
  === Alignment ===  
i n t e n t i o n
| | | | | | | | | 
e x e c u t i o n
  === Steps ===  
Step 1 substitute i with e
Step 2 substitute n with x
Step 3 substitute t with e
Step 4 substitute e with c
Step 5 substitute n with u
Step 6 substitute/copy t with t (NO OP)
Step 7 substitute/copy i with i (NO OP)
Step 8 substitute/copy o with o (NO OP)
Step 9 substitute/copy n with n (NO OP)
```
---
```python
python -m spell-correction.MED
```
```
executes all the MEDs
```
---
*Note for tasks listed below:* 

In every task , 300 sentences are chosen randomly.Everything is converted to lowercase first and anything except alphanumeric is removed.

---

```python
python -m spell-correction.task0
```
```
  === In order to increase search speed, it has been assumed
that user types first character of word correctly ===  
32198 unique words found in /home/deepankar/workspace/nlp/spell-correction/preprocessing/big.txt
Iteration: 0
Taking 300 sentences from line no 984 to 1284 from /home/deepankar/workspace/nlp/spell-correction/preprocessing/holbrook-tagged.dat.txt
128 tagged erroneous words found in randomly selected 300 sentences
checking for every incorrect word
Dictionary approach accuracy %ages {'detection_accuracy_percentage': 96.74818418071567, 'correction_accuracy_percentage': 36.71875}
```
---
```python
python -m spell-correction.task1
```
Comment : in this task only detection accuracy have been calculated , for calculating correction accuracy one approach could be to try out all the permutation and see if it crosses threshold and compare against actual correct word, another approach would be to use frequencies from confusion matrices, however could not decide on which one thus it has been avoided.
```
32198 unique words found in /home/deepankar/workspace/nlp/spell-correction/preprocessing/big.txt
generating trigrams
Iteration 0
Taking 300 sentences from line no 1041 to 1341 from /home/deepankar/workspace/nlp/spell-correction/preprocessing/holbrook-tagged.dat.txt
106 tagged erroneous words found in randomly selected 300 sentences
Trigram approach accuracy 66.98113207547169 %
```
---
```python
python -m spell-correction.task2
```
Comment : if it is taking long don't kill the process, it takes around 200 seconds ( see benchmark for details )
```
32198 unique words found in /home/deepankar/workspace/nlp/spell-correction/preprocessing/big.txt
32198 unique words found
Saving all the words in hashmap
Taking 300 sentences from line no 515 to 815 from /home/deepankar/workspace/nlp/spell-correction/preprocessing/holbrook-tagged.dat.txt
126 tagged erroneous words found in randomly selected 300 sentences
checking for every incorrect word
{'correction_accuracy_percentage': 41.269841269841265, 'detection_accuracy_percentage': 96.76731320402587}
```
---
```python
python -m spell-correction.MED.normal_MED
```
```
=== Comparing Trigram approach against Dictionary approach ===  
32198 unique words found in /home/deepankar/workspace/nlp/spell-correction/preprocessing/big.txt
Taking 300 sentences from line no 1113 to 1413 from /home/deepankar/workspace/nlp/spell-correction/preprocessing/holbrook-tagged.dat.txt
  === Dictionary approach ===  
Dictionary approach accuracy 96.81200187529302 %
  === Trigram approach ===  
Iteration 0
90 tagged erroneous words found in randomly selected 300 sentences
Trigram approach accuracy  58.88888888888889 %
  === Comparison ===  
Dictionary approach: 96.81200187529302 % || Trigram approach 58.88888888888889 %
```
---
*Comparison of performance (execution speed) between Linear Dictionary / Brute Force Approach and Hashed Dictionary / Bit map Approach*

A custom hashmap has been implemented which does increase the detection speed, however correction speed is still slower than dictionary approach likely due to assumption while searching in dictionary approach .

Correcting by dictionary approach takes around 30 seconds and with bitmap approach takes around 200 seconds on same test data 
In order to increase the speed in bitmap searching one suggestion is only look for string of same length as incorrect word instead of length , length + 1 and length - 1 but that would bring down the correction accuracy of bitmap approach which is higher than dictionary approach.

---

##### Notes about MED outputs

###### BackTraceMED output
*Multiple paths are not taken into account*

While calculating MED if there are multiple possible paths with same score then order of preference is deletion > insertion > substitution

that's why

when alignment or steps is printed in output,most of the times they will be entirely composed of insertion and deletion only

###### WeightedMED output
*Generation of Confusion Matrices*

Multiple paths are not taken into account

While calculating MED if there are multiple possible paths with same score then order of preference is deletion > insertion > substitution

that's why

The counts in substitution matrix will be updated far less times than deletion or insertion matrices

As a result of this

when alignment or steps is printed in output,most of the times they will be composed of substitution only since every count in all the matrices are initialized with zero and substitution matrices is highly likely to contain zeroes leading to substitution path being chosen when path is selected by algorithm dynamically.
