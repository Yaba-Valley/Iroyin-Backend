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

path = f'postgresql+pyscopg2://{username}:{password}@{host}:{port}/{dbname}'

engine = create_engine(path)


def get_interacted_and_new_news(id):

    query = f"""
                SELECT 
                    n.*, 
                    COALESCE(l.likes, 0) AS likes, 
                    COALESCE(i.interactions, 0) AS interactions, 
                    COALESCE(s.saves, 0) AS saves,
                    COALESCE(d.dislikes, 0) AS dislikes
                FROM 
                    news_news n 
                LEFT JOIN (
                    SELECT news_id, COUNT(CASE WHEN user_id = {id} THEN 1 END) AS likes
                    FROM authentication_user_liked_news
                    GROUP BY news_id
                ) l ON n.id = l.news_id
                LEFT JOIN (
                    SELECT news_id, COUNT(CASE WHEN user_id = {id} THEN 1 END) AS interactions
                    FROM authentication_user_newInteractedWith
                    GROUP BY news_id
                ) i ON n.id = i.news_id
                LEFT JOIN (
                    SELECT news_id, COUNT(CASE WHEN user_id = {id} THEN 1 END) AS saves
                    FROM authentication_user_saved_news
                    GROUP BY news_id
                ) s ON n.id = s.news_id
                LEFT JOIN (
                    SELECT news_id, COUNT(CASE WHEN user_id = {id} THEN 1 END) AS dislikes
                    FROM authentication_user_disliked_news
                    GROUP BY news_id
                ) d ON n.id = d.news_id
                WHERE 
                    COALESCE(l.likes, 0) + COALESCE(i.interactions, 0) + COALESCE(s.saves, 0) + COALESCE(d.dislikes, 0) > 0
            """
    interacted = pd.read_sql_query(query, engine)
    

    query = f'''
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
            '''
    last_7_days_uninteracted_by_user = pd.read_sql_query(query, engine)

    return interacted, last_7_days_uninteracted_by_user

def Machine(id, page):
    train, test = get_interacted_and_new_news(id)
    if train.shape[0]>5:
        vectorizer = TfidfVectorizer(
            lowercase=True, ngram_range=(1, 2), stop_words='english')

        # .apply(lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))
        train_array = vectorizer.fit_transform(
            train['title']).toarray()
        train['count']= (0.3*train['saves'].fillna(0))+ (0.5*train['likes'].fillna(0))+ (0.2*train['interactions'].fillna(0)) + (0*train['dislikes'].fillna(0))
        
        #train['count']= (train['count']-train['count'].mean())/train['count'].std()
        
        train_array=train_array*train['count'].values.reshape(-1,1)
        
        train_array= train_array.mean(axis=0)
        #print(train_array)
        # .apply(lambda x: clean_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))
        test_array = vectorizer.transform(test['title'])
        similarity = cosine_similarity(train_array.reshape(1, -1), test_array)
        test['similarity'] = similarity.T
        test.sort_values(by=['similarity'], inplace=True, ascending=False)
        test.drop(['similarity'], axis=1, inplace=True)
        test= test.head(page)
        seen=pd.DataFrame({'user_id':[id]*page, 'news_id':test['id'].values})
        seen.to_sql(name='authentication_user_newsSeen', con=engine, if_exists='append', index=False)

        return list(test.T.to_dict().values())
    
    else:
        query='''
                SELECT 
                    news_news.*,
                COUNT(authentication_user_liked_news.news_id) AS likes,
                COUNT(authentication_user_newInteractedWith.news_id) AS interactions,
                COUNT(authentication_user_saved_news.news_id) AS saves
                FROM news_news
                LEFT JOIN authentication_user_liked_news ON news_news.id = authentication_user_liked_news.news_id
                LEFT JOIN authentication_user_newInteractedWith ON news_news.id = authentication_user_newInteractedWith.news_id
                LEFT JOIN authentication_user_saved_news ON news_news.id = authentication_user_saved_news.news_id
                WHERE time_added >= now() - INTERVAL 7 DAY
                GROUP BY news_news.id, news_news.title
              '''
        table = pd.read_sql_query(query, engine)
        table['saves']= table['saves']*3
        table['likes']= table['likes']*2

        table['importance']= table[['saves', 'likes', 'interactions']].sum(axis=0)

        table.sort_values(by=['importance'], ascending=False, inplace=True)
        table.drop(['importance', 'saves', 'likes', 'interactions'], axis=1, inplace=True)
        table= table.head(page)
        print(table)
        seen=pd.DataFrame({'user_id':[id]*page, 'news_id':table['id'].values})
        seen.to_sql(name='authentication_user_newsSeen', con=engine, if_exists='append', index=False)

        return list(table.T.to_dict().values())



