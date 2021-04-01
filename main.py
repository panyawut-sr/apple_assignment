from config import get_config
from userintent import UserIntent
from preprocess_text import PreProcessingText
from postprocess_text import PostProcessingText
from model import NLUModel
from rule import label_regex_list, device_list, time_regex_list
import configparser
import pandas as pd

def run(config):
    
    if(config.mode == "Train"):
      df = pd.read_csv(config.train_data, delimiter="\t", header=None)
      df.columns = ["text", "label"]

      pre = PreProcessingText()
      custom_dictionary = pre.create_dict()
      
      df_train, vocab_to_idx, idx_to_vocab, cnt_vocab, maxlen = pre.make_vocab_and_tokenize(df, custom_dictionary)
      model = NLUModel(config.alpha, config.fit_prior)
      model.train(df_train["text"], df_train["label"], config.save_model_path)
    
    elif(config.mode == "Evaluate"):
      pre = PreProcessingText()
      custom_dictionary = pre.create_dict()
      intent = UserIntent(label_regex_list, device_list, time_regex_list)
      post = PostProcessingText()

      df_test = pd.read_csv(config.evaluate_data, delimiter="\t", header=None)
      df_test.columns = ["text", "label"]
      df_test = pre.preprocess_test(df_test, custom_dictionary)

      model = NLUModel(config.alpha, config.fit_prior)
      model.load_model(config.load_trained_model_path)
      predict = model.test(df_test["text"])
      model.evaluate(df_test["label"].values, predict)

    elif(config.mode == "TestSample"):
      t = config.sentence
      pre = PreProcessingText()
      post = PostProcessingText()
      custom_dictionary = pre.create_dict()
      intent = UserIntent(label_regex_list, device_list, time_regex_list)
      t = pre.preprocess_sample(t, custom_dictionary)

      model = NLUModel(config.alpha, config.fit_prior)
      model.load_model(config.load_trained_model_path)
      predict = model.test([t])
      user_intent = intent.find_user_intent([t])
      ans = post.post_processing_user_intent([t], user_intent, predict[0])
      print("".join(t.split()))
      print(str(ans))

    elif(config.mode == "TestFile"):
      pre = PreProcessingText()
      custom_dictionary = pre.create_dict()
      intent = UserIntent(label_regex_list, device_list, time_regex_list)
      post = PostProcessingText()

      df_test = pd.read_csv(config.test_data, delimiter="\t", header=None)
      df_test.columns = ["text"]
      df_test = pre.preprocess_test(df_test, custom_dictionary)

      model = NLUModel(config.alpha, config.fit_prior)
      model.load_model(config.load_trained_model_path)
      predict = model.test(df_test["text"])
      
      with open("results.txt", "w") as f:
        for i in range(len(df_test)):
          t = df_test["text"].iloc[i].split()
          user_intent = intent.find_user_intent(t)
          ans = post.post_processing_user_intent(t, user_intent, predict[i])
          f.write(str(i)+": "+"".join(t)+"\n")
          f.write(str(ans)+"\n")
          f.write("\n")    
    else:
      print("Please, select the mode")
      print("1. Train")
      print("2. Evaluate")
      print("3. TestSample")
      print("4. TestFile")
      
if __name__ == '__main__':
    config, unparsed = get_config()
    run(config)

