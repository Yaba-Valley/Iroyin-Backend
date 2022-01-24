from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import nltk
import re
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score



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


""" def objective(trial):
    percentile = trial.suggest_float("feature-selection__percerntile", 0, 10)
    #intercept = trial.suggest_categorical("fit_intercept", [True, False])
    #tol = trial.suggest_float("tol", 0.001, 0.01, log=True)
    #solver = trial.suggest_categorical("solver", ["auto", "svd","cholesky", "lsqr", "saga", "sag"])

    ## Create Model
    model = Pipeline(steps=[('tfid-vectorizer', TfidfVectorizer(lowercase = True)), ('feature-selection', SelectPercentile(score_func= chi2, percentile=90)), ('model', MultinomialNB()) ])

    ## Fit Model
    model.fit(X_train, Y_train)

    return mean_squared_error(Y_test, regressor.predict(X_test)) """


class Machine:
    def __init__(self, data):
        
        self.data = data

        self.model= Pipeline(steps=[('tfid-vectorizer', TfidfVectorizer(lowercase = True)), ('feature-selection', SelectPercentile(score_func= chi2, percentile=90)), ('classifier', RandomForestClassifier())])

    def recommend(self, data):
        scrape= pd.DataFrame(data)
        try:
            self.data= pd.DataFrame(self.data)


            #self.data["text_clean"] = self.data["text"].apply(lambda x: utils_preprocess_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=lst_stopwords))

            #self.data.to_csv('news.csv', index = False)
            param_grid = {'feature-selection__percentile': (50, 60, 70)}
            model_grid_search = GridSearchCV(self.model, param_grid=param_grid,
                                 n_jobs=2, cv=2)
            model_grid_search.fit(self.data['titles'], self.data['interactions'])
            #self.model.fit(self.data['titles'], self.data['interactions'])

            probability=model_grid_search.predict_proba(scrape['titles'])[:,1]

            print('f1 :', f1_score(self.data['interactions'],model_grid_search.predict(self.data['titles'])))

            print(f"The best set of parameters is: "f"{model_grid_search.best_params_}")

            scrape['probability']= probability

            recommended_item= scrape.sort_values(by=['probability'], ascending=False).drop(['probability'], axis=1)

            recommended_item= recommended_item.iloc[:20, :]
            print('\n\n\n\n\n')
            #print('ml', recommended_item)
            return recommended_item.to_dict(orient='list')
        except Exception as e:
            return scrape.sample(frac = 1).iloc[:20, :].to_dict(orient = 'list')

        