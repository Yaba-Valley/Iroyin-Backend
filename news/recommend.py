from code import interact
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, f1_score
import nltk
import os
from sqlalchemy import create_engine


def get_df(id):
    path = os.getcwd()+'/db.sqlite3'

    engine = create_engine('sqlite:///'+path)
    query = f""" SELECT news_news.title, news_news.id         
    FROM news_news
    INNER JOIN news_user_newInteractedWith        
    ON news_news.id=news_user_newInteractedWith.news_id
    WHERE news_user_newInteractedWith.user_id={id}; """

    interacted = pd.read_sql_query(query, engine)
    
    interacted['interactions'] =  [1] * len(interacted)
    
    query = f""" SELECT news_news.title, news_news.id          
    FROM news_news
    INNER JOIN news_user_newsSeen        
    ON news_news.id=news_user_newsSeen.news_id
    WHERE news_user_newsSeen.user_id={id}; """

    seen = pd.read_sql(query, engine)
    merged=interacted.merge(seen, on=['id', 'title'], how='outer')
    merged.fillna(0, inplace=True)
    merged.sample(frac = 1)
    return merged.sample(frac = 1)


# dL
#from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer


def clean_text(text, flg_stemm=False, flg_lemm=False, lst_stopwords=None):
    # clean (convert to lowercase and remove punctuations and
    # characters and then strip)
    text = re.sub(r'^[0-9]|[0-9]$|\w+(-\w+)',
                  'GoalScoredMatch', str(text).lower().strip())
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

    # Tokenize (convert from string to list)
    lst_text = text.split()  # remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in
                    lst_stopwords]

    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]

    # Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    # back to string from list
    text = " ".join(lst_text)
    return text


"""
 def objective(trial):
    percentile = trial.suggest_float("feature-selection__percerntile", 0, 10)
    #intercept = trial.suggest_categorical("fit_intercept", [True, False])
    #tol = trial.suggest_float("tol", 0.001, 0.01, log=True)
    #solver = trial.suggest_categorical("solver", ["auto", "svd","cholesky", "lsqr", "saga", "sag"])

    ## Create Model
    model = Pipeline(steps=[('tfid-vectorizer', TfidfVectorizer(lowercase = True)), ('feature-selection', SelectPercentile(score_func= chi2, percentile=90)), ('model', MultinomialNB()) ])

    ## Fit Model
    model.fit(X_train, Y_train)

    return mean_squared_error(Y_test, regressor.predict(X_test))

"""


class Machine:
    def __init__(self, id):

        self.data = get_df(id)
        self.model = Pipeline(steps=[('tfid-vectorizer', TfidfVectorizer(lowercase=True)), ('feature-selection',
                              SelectPercentile(score_func=f_classif)), ('classifier', MultinomialNB())])

    def recommend(self, data):
        scrape = pd.DataFrame(data)
        print(scrape)
        #scrape= pdfrom_dict(data, orient='rows', dtype=None, columns=None)
        try:
            self.data["titles"] = self.data["titles"].apply(lambda x: clean_text(
                x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))

            #self.data.to_csv('news.csv', index = False)
            param_grid = {
                'feature-selection__percentile': (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)}

            model_grid_search = GridSearchCV(self.model,
                                             param_grid=param_grid,
                                             n_jobs=2,
                                             cv=StratifiedShuffleSplit(
                                                 n_splits=3, test_size=0.1),
                                             scoring='f1')

            model_grid_search.fit(
                self.data['titles'], self.data['interactions'])
            #self.model.fit(self.data['titles'], self.data['interactions'])

            probability = model_grid_search.predict_proba(scrape['titles'].apply(
                lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None)))[:, 1]

            print('f1 :', model_grid_search.best_score_)

            print(
                f"The best set of parameters is: "f"{model_grid_search.best_params_}")

            scrape['probability'] = probability

            recommended_item = scrape.sort_values(
                by=['probability'], ascending=False).drop(['probability'], axis=1)

            recommended_item = recommended_item.iloc[:20, :]
            print(recommended_item[['meta', 'probability']])
            print('\n\n\n\n\n')
            #print('ml', recommended_item)
            return recommended_item.to_dict(orient='list')
        except Exception as e:
            print(e)
            return scrape.sample(frac=1).iloc[:20, :].to_dict(orient='list')
