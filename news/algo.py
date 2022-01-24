## for data
import json
import pandas as pd
import numpy as np## for plotting
from sklearn.naive_bayes import MultinomialNB
import seaborn as sns## for processing
import re
import nltk## for bag-of-words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction, model_selection, naive_bayes, pipeline, manifold, preprocessing

'''
try:
    nltk.download('stopwords')
    nltk.download('wordnet')
except:
    pass
'''


def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and   
    ##characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text




data= pd.read_csv('news.csv')
lst_stopwords = nltk.corpus.stopwords.words("english")

data["text_clean"] = data["titles"].apply(lambda x: utils_preprocess_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=lst_stopwords))

""" 
corpus = data["text_clean"]
vectorizer.fit(corpus)
X_train = vectorizer.transform(corpus)
dic_vocabulary = vectorizer.vocabulary_

 """
model= pipeline.Pipeline(steps=[('tfid', TfidfVectorizer()), ('model', MultinomialNB()) ])


model.fit(data['text_clean'], data['interactions'])
probability=model.predict_proba(data['text_clean'])[:,1]
data['probability']= probability
recommended_item= data.sort_values(by=['probability'], ascending=False).drop(['probability'], axis=1)
recommended_item= recommended_item.iloc[:20, :]
print('\n\n\n\n\n')
print('ml', recommended_item)