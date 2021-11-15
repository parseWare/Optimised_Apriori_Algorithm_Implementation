# Optimised_Apriori_Algorithm_Implementation
**Hash Based Apriori**<br><br>
We created a hash based algorithm in which there are mainly two stages :--<br>
● Creating the hash tree for each length ( it is the length of frequent itemset
currently).<br>
● Pruning the above build hash tree and the frequent_tuples that are
obtained in the hash tree with the help of support which will be given
externally.<br>
<br><br><br>
**Partition Apriori**<br><br>
Algorithm is having two scans –<br>
● For each smaller partition having the relative support (calculated on the basis of
number of partitions and main_support_count ) and finding the hash_tree for
each partition.<br>
● Second scan for the union of all the itemsets. This has been found using the
hash tree of each partition but now pruning is done with provided support (given
externally) to prue the itemset that are not so frequent and find the union of all of
them.<br>
