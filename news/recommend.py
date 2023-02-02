import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sqlalchemy import create_engine


def get_interacted_and_new_news(id):
    host=os.environ['DBHOST']
    username=os.environ['DBUSER']
    dbname=os.environ['DBNAME']
    password=os.environ['DBPASS']
    port=os.environ['DBPORT']

    path = f'mysql+mysqldb://{username}:{password}@{host}:{port}/{dbname}'
    print(path)
    engine = create_engine(path)
    query = f"""SELECT 
	                news_news.title
                    , news_news.id         
                FROM news_news
                INNER JOIN authentication_user_newInteractedWith        
                    ON news_news.id=authentication_user_newInteractedWith.news_id
                WHERE authentication_user_newInteractedWith.user_id={id}"""

    interacted = pd.read_sql_query(query, engine)


    query=  f'''
            SELECT news_news.*
            FROM news_news
            LEFT OUTER JOIN authentication_user_newInteractedWith ON news_news.id= authentication_user_newInteractedWith.news_id
            WHERE (authentication_user_newInteractedWith.user_id <> {id} OR authentication_user_newInteractedWith.user_id IS NULL) AND time_added >= now() - INTERVAL 1 DAY
            ORDER BY time_added DESC
            '''
    last_24_hours_uninteracted_by_user= pd.read_sql_query(query, engine)

    return interacted, last_24_hours_uninteracted_by_user



def Machine(id, page):
    train, test = get_interacted_and_new_news(id)
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,2), stop_words='english')

    train_array= vectorizer.fit_transform(train['title'] ).toarray().mean(axis=0) #.apply(lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))

    test_array= vectorizer.transform(test['title']) #.apply(lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))
    similarity= cosine_similarity(train_array.reshape(1, -1), test_array)
    test['similarity']= similarity.T
    test.sort_values(by=['similarity'], inplace=True, ascending=False)
    test.drop(['similarity'], axis=1, inplace= True)

    return list(test.head(page).T.to_dict().values())