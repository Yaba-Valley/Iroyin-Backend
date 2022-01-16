from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class Machine:
    def __init__(self, data):
        self.data= pd.DataFrame(data)
        self.model= Pipeline(steps=[('count_vector', CountVectorizer(ngram_range=(1,1), lowercase=True, stop_words='english')), ('tfid', TfidfTransformer()), ('model', MultinomialNB()) ])

    def recommend(self):
        
        try:
            self.model.fit(self.data['titles'], self.data['interactions'])
            probability=self.model.predict_proba(self.data['titles'])[:,1]
            self.data['probability']= probability
            recommended_item= self.data.sort_values(by=['probability'], ascending=False).drop(['probability', 'interactions'], axis=1)
            recommended_item= recommended_item.iloc[:20, :]
            #print('ml', recommended_item.to_dict(orient='list'))
            return recommended_item.to_dict(orient='list')
        except:
            return self.data

        