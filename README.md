# apple_assignment

## How does it work

The program contains the two main systems.

1. Intent Classification (createAlarm, deleteAlarm, addLabel, updateAlarm)

   - Tokenization by using the tokenizer from PythaiNLP
   - Fix the miss spell word based on my own dictionary
   - Normalize from the integer text to thai text
   - Use tf-idf as the feature
   - Use Multinomial Naive Bayes as the model

2. Find the user's intents

## Current accuracy

I split the 10% of the data from "th_dataset.txt" to be validation set, and the remaining 90% of the data to be training set

The current accuracy is follow as:

- number of evaluation samples: 127 sentences
- accuracy: 98%
- Macro recall: 0.98
- You can evalaute the model by using your own file by using command "python main.py --mode=Evaluate" --evaluate_data=<evaluate_file>

## How to feed input and get output

There are 4 main functions for this program.

1.

train.txt
<sentence> <label>
<sentecen> <label>

evaluate.txt
<sentence> <label>
<sentecen> <label>

test.txt
<sentence>
<sentence>

## How to improve in the future
