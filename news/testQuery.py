import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sqlalchemy import create_engine


def get_interacted_and_new_news(id):
    host = os.environ['DBHOST']
    username = os.environ['DBUSER']
    dbname = os.environ['DBNAME']
    password = os.environ['DBPASS']
    port = os.environ['DBPORT']

    path = f'mysql+mysqldb://{username}:{password}@{host}:{port}/{dbname}'
    print(path)
    engine = create_engine(path)
    query = f"""SELECT title, COUNT(title) AS 'count'
                FROM    (   (SELECT 
	                        news_news.title
                            , news_news.id         
                            FROM news_news
                            INNER JOIN authentication_user_newInteractedWith        
                            ON news_news.id=authentication_user_newInteractedWith.news_id
                            WHERE authentication_user_newInteractedWith.user_id={id})
                            
                            UNION ALL
                            (SELECT 
                                news_news.title
                                , news_news.id         
                            FROM news_news
                            INNER JOIN authentication_user_liked_news        
                                ON news_news.id=authentication_user_liked_news.news_id
                            WHERE authentication_user_liked_news.user_id={id} )
                        ) AS Interact
                GROUP BY title
                WHERE  title LIKE '%Biden Admin Commits Over $300 Million to Support Kids\' Mental Health%'
                """

    interacted = pd.read_sql_query(query, engine)
    


    return interacted #,  last_24_hours_uninteracted_by_user

print(get_interacted_and_new_news(8))