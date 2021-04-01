import pandas as pd
from num_thai.thainumbers import NumThai
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus.common import thai_words
from pythainlp.util import dict_trie
from collections import defaultdict

class PreProcessingText():
  def __init__(self):
    self.new_words = {"iphone", "ไอโฟน", "ipad", "ไอแพด", "แมคบุ๊ค", "macbook", "โน๊ตบุ๊ค", "มือถือ", "เลเบล"}
    self.miss_spell = {"ตั้กปลุก":"ตั้งปลุก", "แปป":"แปบ"}
    self.norm_time = {"10": "สิบ",
              "11": "สิบเอ็ด",
              "12": "สิบสอง",
              "13": "สิบสาม",
              "14": "สิบสี่",
              "15": "สิบห้า",
              "16": "สิบหก",
              "17": "สิบเจ็ด",
              "18": "สิบแปด",
              "19": "สิบเก้า",
              "21": "ยี่สิบเอ็ด",
              "22": "ยี่สิบสอง",
              "23": "ยี่สิบสาม",
              "24": "ยี่สิบสี่",
              "20": "ยี่สิบ",
              "1": "หนึ่ง", 
              "2": "สอง",
              "3": "สาม", 
              "4": "สี่",
              "5": "ห้า", 
              "6": "หก",
              "7": "เจ็ด",
              "8": "แปด",
              "9": "เก้า"}

  def clean_text(self, text):
    for incor, cor in self.miss_spell.items():
      text = text.replace(incor, cor)
    for num, w in self.norm_time.items():
      text = text.replace(num, w)
    return text

  def create_dict(self):
    words = self.new_words.union(thai_words())
    custom_dict = dict_trie(words)
    return custom_dict

  def preprocess_test(self, df, vocab_to_idx=None, custom_dictionary=None):
    for idx, row in df.iterrows():
      t = self.clean_text(row["text"].lower())
      tokens = word_tokenize(t, custom_dict=custom_dictionary, engine="newmm")
      df["text"][idx] = " ".join(tokens)
    return df

  def preprocess_sample(self, t, vocab_to_idx=None, custom_dictionary=None):
    t = self.clean_text(t.lower())
    tokens = word_tokenize(t, custom_dict=custom_dictionary, engine="newmm")
    t = " ".join(tokens)
    return t
      
  def make_vocab_and_tokenize(self, df, custom_dictionary):
    vocab_to_idx = {"<start>":0, "<stop>":1,"<UNK>":2}
    cnt_vocab = defaultdict(int)
    corpus = []
    tokenized_words = []
    maxlen = 0
    for t in df["text"]:
      t = self.clean_text(t.lower())
      tokens = word_tokenize(t, custom_dict=custom_dictionary, engine="newmm")
      tmp = []
      for token in tokens:
        token = token.strip()
        if (len(token) == 0):
          continue

        tmp.append(token)
        cnt_vocab[token]+=1
        if(token not in vocab_to_idx.keys()):
          vocab_to_idx[token] = len(vocab_to_idx) 

      tokenized_words.append(tmp)
      corpus.append(" ".join(tmp))
      if(len(tokens) > maxlen):
        maxlen = len(tokens)

    df["tokenized"] = tokenized_words
    df["text"] = corpus
    idx_to_vocab = {v: k for k, v in vocab_to_idx.items()}
    return df, vocab_to_idx, idx_to_vocab, cnt_vocab, maxlen
