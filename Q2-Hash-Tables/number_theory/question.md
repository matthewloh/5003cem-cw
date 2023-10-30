Question 2: Hash Tables
Devise an experiment that will determine which of the two hash function defined below is “better”.
You first need to define your 2 hash functions. Start by choosing 2 random numbers 𝑎𝑎 and 𝑏𝑏 such that
𝑎𝑎 < 𝑏𝑏. We will also assume that the table will have a size of 5500. For a key of 𝑖𝑖, the 2 functions will be:
• ℎ(𝑖𝑖) = (𝑎𝑎𝑖𝑖 + 𝑏𝑏) 𝑚𝑚𝑚𝑚𝑚𝑚 5500
• ℎ(𝑖𝑖) = 𝑓𝑓𝑓𝑓𝑚𝑚𝑚𝑚𝑓𝑓 �5500 ∗ ��𝑖𝑖 ∗ 𝑎𝑎
𝑏𝑏� 𝑚𝑚𝑚𝑚𝑚𝑚 1��
Write a program that will insert 5000 unique and randomly generated numbers into two separate hash
tables using the functions define above. In the case of a collision use open addressing linear probing to
handle it. Use suitable methods to investigate which function performs better. Your experiment should
be repeated at least 10 times.
Using the observations and results obtained, write an argument to support your findings. You may use
other additional methods of investigation as well to make a more compelling argument.
