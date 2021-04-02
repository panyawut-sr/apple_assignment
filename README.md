# apple_assignment

## How does it work

The program contains the two main systems.

1. Intent Classification (createAlarm, deleteAlarm, addLabel, updateAlarm)

   - Tokenization using the tokenizer from PyThaiNLP (an efficient tool for Thai language)
   - Fix mispelled words based on my own dictionary
   - Normalize integer text to thai text
   - Use tf-idf as the feature
   - Use Multinomial Naive Bayes as the model

2. Find the user's intents (Label, Device, Time)
   - Apply regex (regular expression) to find the intent keywords of label, device, and time
   - Use a rule-based algorithm to extract the time intent (based on common Thai grammar knowledge)
   - Handle cases where the user's intent does not match the algorithm's assumptions

This system supports the Thai hour unit of "โมง", "นาฬิกา", "ทุ่ม", "ยาม", and "บ่าย", including the minute units such as "นาที", "ครึ่ง", "ตรง". I also provide <config.py> for adjusting the parameters.

## Current accuracy

I split 10% of the data from "th_dataset.txt" as the validation set, and the remaining 90% of the data as the training set.

The current accuracy is as follows:

|              | precision | recall   | f1-score | support  |
| ------------ | --------- | -------- | -------- | -------- |
| addLabel     | 1.00      | 1.00     | 1.00     | 28       |
| createAlarm  | 0.97      | 0.95     | 0.96     | 39       |
| deleteAlarm  | 0.92      | 0.96     | 0.94     | 25       |
| updateAlarm  | 1.00      | 1.00     | 1.00     | 35       |
| --------     | --------  | -------- | -------- | -------- |
| accuracy     |           |          | 0.98     | 127      |
| macro avg    | 0.97      | 0.98     | 0.98     | 127      |
| weighted avg | 0.98      | 0.98     | 0.98     | 127      |

- Number of evaluation samples: 127 sentences
- Accuracy: 98%
- Macro recall: 0.98
- You can evaluate the model using your own file by using the command "python main.py --mode=Evaluate" --evaluate_data=<evaluate_file>

## How to feed input and get output

There are 4 modes for this program.

1. Train

   - This mode is used for retraining the model with a new dataset.
   - The input is named <train_file>, containing the sentence and ground truth pair for training.
   - The output is named <model_file>, containing the pipeline of the feature extraction and the model.
   - Example: "python main.py --mode=Train --train_data=<train_file> --save_model_path=<model_file>"

2. Evaluate

   - This mode is used for evaluating the model with the selected evaluation dataset.
   - The input is named <evaluate_file>, containing the sentence and ground truth pair for evaluation.
   - The program will print a report of the performance of the model (in the command line).
   - Example: "python main.py --mode=Evalute --train_data=<evaluate_file>"

3. TestSample

   - This mode is used for testing individual sentences.
   - The input is named <sentence>, which is typed in the command line.
   - The program will print the output of classification and user's intent based on the <sentence> (in the command line).
   - Example: "python main.py --mode=TestSample --sentence=<sentence>"
   - Note that this function required the input without spacing

4. TestFile
   - This mode is used for testing a set of sentences.
   - The input is named <test_file>, containing the input sentences.
   - The output is named <results_file>, containing the results for each input sentence.
   - Example: "python main.py --mode=TestSample --test_data=<test_file> --result_path=<results_file>"

example of <train.txt>

```
<sentence> <label>
<sentence> <label>
```

example of <evaluate.txt>

```
<sentence> <label>
<sentence> <label>
```

example of <test.txt>

```
<sentence>
<sentence>
```

## How to improve in the future

1. The simplest approach is to collect more data and apply a deep learning approach for this task. Many researchers have shown empirical evidence that a deep learning methods significantly outperform traditional machine learning methods, when a large dataset is available.

2. A semi-supervised learning approach can be used to address the high cost of collecting ground truth for data. Recent works have achieved the better results after applying methods such as "Meta Pseudo Labels" and "Noisy Student". We can apply these techniques to improve the performance of the classification model or the semantic parsing model in the future.

3. Ideally, we would like to avoid the scenario where the program performs the wrong actions. In such a case, we can ask the user to provide another input. We can introduce the idea of "confidence" or "uncertainty" to judge whether the user should be asked again.

4. When considering the extension of the program for additional scenarios, we can consider two approaches. If the number of possible scenarios does not increase significantly, a rule-based algorithm with additional rules can be used. On the other hand, once the set of scenarios becomes too large, it would be better to convert natural language utterances to a logical form, using methods such as "Semantic Parsing".

## Thought process

1. Considering the limited amount of data and time, I decided to use a third-party library called PyThaiNLP. This library is known to perform efficiently for preprocessing tasks for the Thai language, such as tokenization.

2. For feature extraction, I chose "tf-idf" considering the relatively small scale of both the task scope and the vocabulary size. "tf-idf" as a feature should be more efficient and precise than a deep learning approach, which requires a large amount of training data.

3. For the model, I chose "Naive Bayes" considering the same reasons as feature extraction.

4. For the finding user's intent, I made a rule-based algorithm because the variation in sentences should be quite small.
