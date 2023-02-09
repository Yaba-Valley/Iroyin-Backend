import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sqlalchemy import create_engine

#ssh-keygen -t ed25519 -C "ikpeleambroseobinna@gmail.com" 

host=os.environ['DBHOST']
username=os.environ['DBUSER']
dbname=os.environ['DBNAME']
password=os.environ['DBPASS']
port=os.environ['DBPORT']

path = f'mysql+mysqldb://{username}:{password}@{host}:{port}/{dbname}'

engine = create_engine(path)

def get_interacted_and_new_news(id):

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
            WHERE id NOT IN (SELECT news_id
                            FROM authentication_user_newInteractedWith
                            WHERE user_id = {id})
                        AND id NOT IN (SELECT news_id
                                        FROM authentication_user_newsSeen
                                        WHERE user_id = {id})
                        AND time_added >= now() - INTERVAL 7 DAY
            ORDER BY time_added DESC
            LIMIT 50
            '''
    last_24_hours_uninteracted_by_user= pd.read_sql_query(query, engine)

    return interacted, last_24_hours_uninteracted_by_user



def Machine(id, page):
    train, test = get_interacted_and_new_news(id)
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,2), stop_words='english', max_df=0.95, min_df=0.01)

    train_array= vectorizer.fit_transform(train['title'] ).toarray().mean(axis=0) #.apply(lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))

    test_array= vectorizer.transform(test['title']) #.apply(lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))
    similarity= cosine_similarity(train_array.reshape(1, -1), test_array)
    test['similarity']= similarity.T
    test.sort_values(by=['similarity'], inplace=True, ascending=False)
    test.drop(['similarity'], axis=1, inplace= True)
    test= test.head(page)
    seen=pd.DataFrame({'user_id':[id]*page, 'news_id':test['id'].values})
    seen.to_sql(name='authentication_user_newsSeen', con=engine, if_exists='append', index=False)
    return list(test.T.to_dict().values())
