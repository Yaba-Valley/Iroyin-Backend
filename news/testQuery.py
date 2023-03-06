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
                            
                            UNION ALL
                            
                            (SELECT 
                                news_news.title
                                , news_news.id         
                            FROM news_news
                            INNER JOIN authentication_user_saved_news        
                                ON news_news.id=authentication_user_saved_news.news_id
                            WHERE authentication_user_saved_news.user_id={id} )
                            
                            UNION ALL
                            
                            (SELECT 
                                news_news.title
                                , news_news.id         
                            FROM news_news
                            INNER JOIN authentication_user_shared_news        
                                ON news_news.id=authentication_user_shared_news.news_id
                            WHERE authentication_user_shared_news.user_id={id} )
                            
                        ) AS Interact
                GROUP BY title
                ORDER BY count DESC
                """

    interacted = pd.read_sql_query(query, engine)
    


    return interacted #,  last_24_hours_uninteracted_by_user

def nearest_user_engagement(id):
    query=f'''
            WITH nearest_users AS (
                SELECT DISTINCT i1.user_id
                FROM authentication_user_interests i1
                WHERE i1.user_id != {id}
                AND NOT EXISTS (
                    SELECT *
                    FROM authentication_user_interests i2
                    WHERE i2.user_id = {id}
                    AND NOT EXISTS (
                        SELECT *
                        FROM authentication_user_interests i3
                        WHERE i3.user_id = i1.user_id
                        AND i3.interest_id = i2.interest_id
                    )
                )
            )

            SELECT 
                n.*, 
                COALESCE(l.likes, 0) AS likes, 
                COALESCE(i.interactions, 0) AS interactions, 
                COALESCE(s.saves, 0) AS saves,
                COALESCE(d.dislikes, 0) AS dislikes
            FROM 
                news_news n 
            LEFT JOIN (
                SELECT news_id, COUNT(CASE WHEN user_id IN (SELECT user_id FROM nearest_users) THEN 1 END) AS likes
                FROM authentication_user_liked_news
                GROUP BY news_id
            ) l ON n.id = l.news_id
            LEFT JOIN (
                SELECT news_id, COUNT(CASE WHEN user_id IN (SELECT user_id FROM nearest_users) THEN 1 END) AS interactions
                FROM authentication_user_newInteractedWith
                GROUP BY news_id
            ) i ON n.id = i.news_id
            LEFT JOIN (
                SELECT news_id, COUNT(CASE WHEN user_id IN (SELECT user_id FROM nearest_users) THEN 1 END) AS saves
                FROM authentication_user_saved_news
                GROUP BY news_id
            ) s ON n.id = s.news_id
            LEFT JOIN (
                SELECT news_id, COUNT(CASE WHEN user_id IN (SELECT user_id FROM nearest_users) THEN 1 END) AS dislikes
                FROM authentication_user_disliked_news
                GROUP BY news_id
            ) d ON n.id = d.news_id
            WHERE 
                COALESCE(l.likes, 0) + COALESCE(i.interactions, 0) + COALESCE(s.saves, 0) + COALESCE(d.dislikes, 0) > 0
    '''