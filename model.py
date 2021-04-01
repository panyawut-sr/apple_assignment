from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pickle

class NLUModel:
  def __init__(self, alpha=1.0, fit_prior=True):
    self.nb = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', MultinomialNB(alpha = alpha, fit_prior=fit_prior)),
                       ])

  def train(self, X, y, filename="model.sav"):
    self.nb.fit(X, y)
    pickle.dump(self.nb, open(filename, 'wb'))
  
  def load_model(self, filename="model.sav"):
    self.nb = pickle.load(open(filename, 'rb'))

  def test(self, X):
    return self.nb.predict(X)  

  def evaluate(self, y_true, y_pred):
    print(classification_report(y_true, y_pred))
    
