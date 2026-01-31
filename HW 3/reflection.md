# Reflection for HW 3
## Benjamin Adovasio

### Did you have any trouble installing the plotext library? If so, what problems, and how did you address?

I had never used plotext library before, however I have used pip in the past to install libraries so it was fairly smooth. 

### Briefly summarize your algorithmic approach for building the dictionary returned by parseWords. Don’t show your algorithm or discuss it line-by-line — briefly summarize in your own words, in high-level English terms.
My initial thought when reading the assignment was to do a for loop for each line, similar to:
```python
with open(filename, "r") as input_file:
    for line in input_file:
        ...
```
However the instructions stated to read the file line by line, similar to Homework 2. At first I made the dictionary remove all punctuation and capitalization so the dictionary was the count of all words, however I realized that I would need capitalization for the 3rd function, so I went back and added a count of capitalizations for each word:

```python
key = word.lower()

if key not in word_dict:
    word_dict[key] = [0, 0]  # [uppercase_count, lowercase_count]

if word[0].isupper():
    word_dict[key][0] += 1
else:
    word_dict[key][1] += 1
```

### [Visit the plotext GitHub page](https://github.com/piccolomo/plotext) and identify and briefly describe one additional plotting function of interest to you that is available in the library.
I thought the image plot function was really interesting, as I had never seen an image plot before. I would like to try to use that on a future asignment. 

### Discuss your use of any LLM (ChatGPT, Claude, MetaAI, etc.) in completing this assignment, if any. What prompts did you ask of the LLM? How did you ensure the results were correct? (Personally, Claude gave me a number of errors related to the library.)

The way I usually code, I start by typing out in psuedo-code, before going back and actually coding. Personally I prefer [StackOverflow Python](https://stackoverflow.com/questions/tagged/python?tab=Newest) to any LLM's, and I used it to research the best way to count the capitalization of words in the dictionary, and I leared I can just use:
```python 
word_dict[key] = [0, 0]  # [uppercase_count, lowercase_count]
```

I did, however, use ChatGPT to generate the test txt files for my code. I chose to use ChatGPT for this because ChatGPT generated a handful of different types of words and strings to really test my function and make sure it worked properly. 
