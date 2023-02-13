""" import requests
from bs4 import BeautifulSoup

# Make a request to the BBC News website
response = requests.get('https://www.bbc.com/news')

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the article elements on the page
    articles = soup.find_all('a', class_='gs-c-promo-heading')

    # Iterate over each article
    for article in articles:
        title = article.text.strip()
        link = article['href']
        print(f'{title} - {link}')
        
        # Get the content of the article page
        article_response = requests.get(f'https://www.bbc.com{link}')
        
        # Check if the request for the article was successful
        if article_response.status_code == 200:
            # Parse the HTML content of the article page
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            
            # Find the image element on the article page
            image = article_soup.find('img')
            
            # Check if an image was found
            if image:
                # Get the URL of the image
                image_url = image['src']
                
                # Get the image data
                image_response = requests.get(image_url)
                
                # Check if the request for the image was successful
                if image_response.status_code == 200:
                    print(image_url)
                    # Save the image to a file
                   # with open(f'{title}.jpg', 'wb') as f:
                        #f.write(image_response.content)
                else:
                    print(f'Failed to retrieve image for {title}')
            else:
                print(f'No image found for {title}')
        else:
            print(f'Failed to retrieve article for {title}')
else:
    print('Failed to retrieve page content')
 """