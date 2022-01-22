from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer



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



class Machine:
    def __init__(self, data):
        
        self.data = data

        self.model= Pipeline(steps=[('count_vector', CountVectorizer(ngram_range=(1,1), lowercase=True, stop_words='english')), ('tfid', TfidfTransformer()), ('model', MultinomialNB()) ])

    def recommend(self, data):
        scrape= pd.DataFrame(data)
        try:
            self.data= pd.DataFrame(self.data)

            lst_stopwords = nltk.corpus.stopwords.words("english")

            #self.data["text_clean"] = self.data["text"].apply(lambda x: utils_preprocess_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=lst_stopwords))

            #self.data.to_csv('news.csv', index = False)
            
            self.model.fit(self.data['titles'], self.data['interactions'])
            probability=self.model.predict_proba(scrape['titles'])[:,1]
            scrape['probability']= probability
            recommended_item= scrape.sort_values(by=['probability'], ascending=False).drop(['probability'], axis=1)
            recommended_item= recommended_item.iloc[:20, :]
            print('\n\n\n\n\n')
            print('ml', recommended_item)
            return recommended_item.to_dict(orient='list')
        except Exception as e:
            print(e)
            return scrape.iloc[:20, :].to_dict(orient = 'list')

        