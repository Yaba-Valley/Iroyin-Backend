from django.http import FileResponse
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import requests
from io import BytesIO
import textwrap
from datetime import datetime

def generate_screenshot(favicon_link, thumbnail_link, newssource, headline, date):
    wrapper= textwrap.TextWrapper(width=30)
    gap=15
    start_position_x= 60 #0
    start_position_y=20 #10
    favicon_radius=20
    
    readnews = Image.open('readnewslogo-dark-mode.png').convert('RGBA')
    readnews_width= 80
    readnews_height= readnews_width//4
    readnews = readnews.resize((readnews_width, readnews_height))

    # Download the favicon image from the link
    response = requests.get(favicon_link)
    favicon = Image.open(BytesIO(response.content)).convert('RGBA')
    # Create a circular mask of size 100x100
    mask = Image.new('L', (favicon_radius, favicon_radius), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, favicon_radius, favicon_radius), fill=255)
    
    # Apply the circular mask to the favicon
    favicon = favicon.resize((favicon_radius, favicon_radius))
    favicon.putalpha(mask)
    

    # Calculate the position of headline based on the height of the font
    new_headline=''
    word_list= wrapper.wrap(text=headline)
    for elements in word_list:
        new_headline=new_headline+elements+'\n'

    headline_font = ImageFont.truetype("Blatant-Bold.otf", 25)
    headline_width, headline_height = headline_font.getsize(new_headline)
    height_of_new_headline= headline_height*(new_headline.count('\n'))
    width_of_new_headline= headline_width//(new_headline.count('\n'))
    headline_x = start_position_x
    headline_y = start_position_y+ readnews_height+ gap-5
 
    # Download the thumbnail image from the link
    response = requests.get(thumbnail_link)
    thumbnail = Image.open(BytesIO(response.content)).convert('RGBA')
    original_thumbnail_width, original_thumbnail_height= thumbnail.size
    
    if new_headline.count('\n')>=2:
        thumbnail_width= width_of_new_headline+25

    elif new_headline.count('\n')<2:
        thumbnail_width= max(450, width_of_new_headline)
    thumbnail_width=350
    thumbnail_height= int((original_thumbnail_height/original_thumbnail_width)*thumbnail_width) #int(thumbnail_width*0.75)
    thumbnail = thumbnail.resize((thumbnail_width, thumbnail_height))

    # Calculate the position of the thumbnail based on the height of
    thumbnail_x = start_position_x
    thumbnail_y = headline_y+ height_of_new_headline+gap
    print(height_of_new_headline)
    #Calculate the position of favicon
    favicon_x = start_position_x
    favicon_y = thumbnail_y + thumbnail_height+gap

    # Calculate the position of newssource, on top of headline and below the favicon
    new_newssource=f'  {newssource} • '
    newssource_font = ImageFont.truetype("ARIAL.TTF", 15)
    newssource_width, newssource_height = newssource_font.getsize(new_newssource)
    
    newssource_x = favicon_x+favicon_radius
    newssource_y = favicon_y+(favicon_radius//5)-3
    
    # Create a black background image of size 600x400
    image_width=500 #thumbnail_x+thumbnail_width+ start_position_x
    image_height=500 # newssource_y+favicon_radius+gap
    bg_image = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    

    # Draw the headline in white color on the image
    draw = ImageDraw.Draw(bg_image)
    draw.text((headline_x, headline_y), new_headline.strip(), fill=(255, 255, 255), font=headline_font)

    # Paste the thumbnail on the top left corner of the background image
    bg_image.paste(thumbnail, (thumbnail_x, thumbnail_y), thumbnail)

    # Paste the favicon on the top left corner of the background image
    bg_image.paste(favicon, (favicon_x, favicon_y), favicon)
        
    # Draw the news source in white color on the image, on top of the favicon and headline
    draw.text((newssource_x, newssource_y), new_newssource, fill=(255, 255, 255), font=newssource_font)
    
    # Draw the date
    date_font = ImageFont.truetype("arial.ttf", 15)
    draw.text((newssource_x+newssource_width, newssource_y),date, fill=(255, 255, 255), font=date_font)
    

    
    # Paste the ReadNews icon
    bg_image.paste(readnews, (start_position_x, start_position_y), readnews)

    #bg_image.save('trial.jpg')
    #bg_image.show()
    return bg_image

#generate_screenshot('https://external-content.duckduckgo.com/ip3/gazettengr.com.ico', 'https://gazettengr.com/wp-content/uploads/WhatsApp-Image-2023-03-01-at-11.37.18-PM.jpeg', 'Peoples Gazette', 'Nigerian stocks fall on Tinubu’s emergence as president-elect', 'Thur Mar 2, 2023' )


def get_image(favicon, img, website, title, date):
    # Get the screenshot
    #favicon=https://external-content.duckduckgo.com/ip3/gazettengr.com.ico&img=https://gazettengr.com/wp-content/uploads/WhatsApp-Image-2023-03-01-at-11.37.18-PM.jpeg&website=Peoples Gazette&title=Nigerian stocks fall on Tinubu’s emergence as president-elect&date=Thur Mar 2, 2023
    #image= generate_screenshot('https://external-content.duckduckgo.com/ip3/gazettengr.com.ico', 'https://gazettengr.com/wp-content/uploads/WhatsApp-Image-2023-03-01-at-11.37.18-PM.jpeg', 'Peoples Gazette', 'Nigerian stocks fall on Tinubu’s emergence as president-elect', 'Thur Mar 2, 2023' )
    image = generate_screenshot(favicon, img, website, title, date) #pass parameter

    # Convert the image to a file object
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    filename= str(datetime.today())
    filename= filename.replace(' ', '').replace('-', '').replace(':', '').replace('.', '')
    filename='Newsway_image_'+filename+'.png'
    # Return the file object as a file response
    return FileResponse(buffer, as_attachment=True, filename=filename)
