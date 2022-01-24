def prepareDataForModel (data, newsInteracted):
    
    titles, urls,interactions,imgs=[],[],[],[]
        
    for i in range(len(data)):
        titles.append(data[i]['title'])
        urls.append(data[i]['url'])
        imgs.append(data[i]['img'])
        
        
        if newsInteracted is not None:
            if data[i] in newsInteracted:
                interactions.append(1)
            else:
                interactions.append(0)
        
    if newsInteracted is not None:
        return {'titles': titles, 'urls': urls, 'interactions': interactions, 'imgs': imgs}
    
    return {'titles': titles, 'urls': urls, 'imgs': imgs }
