from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class Machine:
    def __init__(self, data):
        self.data = data
        self.model= Pipeline(steps=[('count_vector', CountVectorizer(ngram_range=(1,1), lowercase=True, stop_words='english')), ('tfid', TfidfTransformer()), ('model', MultinomialNB()) ])

    def recommend(self, data):
        scrape= pd.DataFrame(data)
        try:
            self.data= pd.DataFrame(self.data)
            
            self.data.to_csv('news.csv', index = False)
            
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

        