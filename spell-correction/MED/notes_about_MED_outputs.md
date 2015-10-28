####  Notes about MED outputs

##### BackTraceMED output
**Multiple paths are not taken into account**  
While calculating MED if there are multiple possible paths with same score  
then order of preference is deletion > insertion > substitution  

that's why  
when alignment or steps is printed in output,  
most of the times they will be entirely composed of insertion and deletion only  

---  

##### WeightedMED output  
**Generation of Confusion Matrices**  

*Multiple paths are not taken into account*  

While calculating MED if there are multiple possible paths with same score  
then order of preference is deletion > insertion > substitution

that's why  
the counts in substitution matrix will be updated far less times than deletion or insertion
matrices  

*As a result of this*  
when alignment or steps is printed in output,  
most of the times they will be mostly composed of substitution only since every count in all the  
matrices are initialized with zero and substitution matrices is highly likely to contain zeroes  
leading to substitution path being chosen when path is selected by algorithm dynamically
