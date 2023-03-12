from django.http import FileResponse
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import textwrap

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def generate_image(favicon_link, thumbnail_link, newssource, headline, date, mode):
    
    wrapper= textwrap.TextWrapper(width=30)
    gap=15
    start_position_x= 20
    start_position_y=20 #10
    favicon_radius=25
    
    if mode=='dark':
        readnews = Image.open('readnewslogo-dark-mode.png').convert('RGBA')
    else:
        # put the light mode link here
        readnews = Image.open('readnewslogo-dark-mode.png').convert('RGBA')
    readnews_width= 80
    readnews_height= readnews_width//4
    readnews = readnews.resize((readnews_width, readnews_height))

    # Download the favicon image from the link
    response = requests.get(favicon_link, headers=headers)
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

    headline_font = ImageFont.truetype("Blatant.otf", 17)
    headline_width, headline_height = headline_font.getsize(new_headline)
    height_of_new_headline= headline_height*(new_headline.count('\n'))
    width_of_new_headline= headline_width//(new_headline.count('\n'))
    headline_x = start_position_x
    headline_y = start_position_y+ readnews_height+ gap-5

    # Download the thumbnail image from the link
    response = requests.get(thumbnail_link, headers=headers)
    thumbnail = Image.open(BytesIO(response.content)).convert('RGBA')
    original_thumbnail_width, original_thumbnail_height= thumbnail.size
    
    thumbnail_width= max(250, width_of_new_headline+50)
    thumbnail_height= int((original_thumbnail_height/original_thumbnail_width)*thumbnail_width) #int(thumbnail_width*0.75)
    thumbnail = thumbnail.resize((thumbnail_width, thumbnail_height))

    # Create a circular mask for thumbnail
    mask_thumb = Image.new('L', (thumbnail_width, thumbnail_height), 0)
    draw_thumb = ImageDraw.Draw(mask_thumb)
    draw_thumb.rounded_rectangle((0, 0, thumbnail_width, thumbnail_height), radius=15, fill=255)

    # Apply the circular mask to the thumbnail
    thumbnail.putalpha(mask_thumb)

    # Calculate the position of the thumbnail based on the height of
    thumbnail_x = start_position_x
    thumbnail_y = headline_y+ height_of_new_headline+gap
    print(height_of_new_headline)
    #Calculate the position of favicon
    favicon_x = start_position_x
    favicon_y = thumbnail_y + thumbnail_height+gap

    # Calculate the position of newssource, on top of headline and below the favicon
    new_newssource=f'  {newssource} • '
    newssource_font = ImageFont.truetype("arial.ttf", 12)
    newssource_width, newssource_height = newssource_font.getsize(new_newssource)
    
    newssource_x = favicon_x+favicon_radius
    newssource_y = favicon_y+(favicon_radius//5)+1
    
    # Create a black background image of size 600x400
    image_width=thumbnail_x+thumbnail_width+ start_position_x
    image_height=newssource_y+favicon_radius+gap
    if mode=='dark':
        bg_image = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    else:
        bg_image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
    

    # Draw the headline in white color on the image
    draw = ImageDraw.Draw(bg_image)
    if mode=='dark':
        draw.text((headline_x, headline_y), new_headline.strip(), fill=(255, 255, 255), font=headline_font)
    else:
        draw.text((headline_x, headline_y), new_headline.strip(), fill=(0, 0, 0), font=headline_font)

    # Paste the thumbnail on the top left corner of the background image
    bg_image.paste(thumbnail, (thumbnail_x, thumbnail_y), thumbnail)

    # Paste the favicon on the top left corner of the background image
    bg_image.paste(favicon, (favicon_x, favicon_y), favicon)
        
    # Draw the news source in white color on the image, on top of the favicon and headline
    if mode=='dark':
        draw.text((newssource_x, newssource_y), new_newssource, fill=(255, 255, 255), font=newssource_font)
    else:
        draw.text((newssource_x, newssource_y), new_newssource, fill=(0, 0, 0), font=newssource_font)
    
    # Draw the date
    date_font = ImageFont.truetype("arial.ttf", 12)
    if mode=='dark':
        draw.text((newssource_x+newssource_width, newssource_y),date, fill=(255, 255, 255), font=date_font)
    else:
        draw.text((newssource_x+newssource_width, newssource_y),date, fill=(0, 0, 0), font=date_font)

    
    # Paste the ReadNews icon
    bg_image.paste(readnews, (start_position_x, start_position_y), readnews)

    

    # Create a circular mask for image
    mask_img = Image.new('L', (image_width, image_height), 0)
    draw_img = ImageDraw.Draw(mask_img)
    draw_img.rounded_rectangle((0, 0, image_width, image_height), radius=15, fill=255)

    # Apply the circular mask to the image
    bg_image.putalpha(mask_img)

    bg_image= bg_image.resize( (1500,int(1500*bg_image.size[1]/bg_image.size[0])) )
    bg_image = bg_image.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=3))
    # Create a final background image of size 600x400
    final_image_width=2000
    final_image_height=bg_image.size[1]+500
    if mode=='dark':
        final_image = Image.new('RGB', (final_image_width, final_image_height), (30, 30, 30))
    else:
        final_image = Image.new('RGB', (final_image_width, final_image_height), (195, 195, 195))
    final_image.paste(bg_image, ((final_image_width-bg_image.size[0])//2, (final_image_height-bg_image.size[1])//2), bg_image)
    return final_image

#generate_screenshot('https://external-content.duckduckgo.com/ip3/gazettengr.com.ico', 'https://gazettengr.com/wp-content/uploads/WhatsApp-Image-2023-03-01-at-11.37.18-PM.jpeg', 'Peoples Gazette', 'Nigerian stocks fall on Tinubu’s emergence as president-elect', 'Thur Mar 2, 2023' )


def get_image(favicon, img, website, title, date):
    # Get the screenshot
    #favicon=https://external-content.duckduckgo.com/ip3/gazettengr.com.ico&img=https://gazettengr.com/wp-content/uploads/WhatsApp-Image-2023-03-01-at-11.37.18-PM.jpeg&website=Peoples Gazette&title=Nigerian stocks fall on Tinubu’s emergence as president-elect&date=Thur Mar 2, 2023
    #image= generate_screenshot('https://external-content.duckduckgo.com/ip3/gazettengr.com.ico', 'https://gazettengr.com/wp-content/uploads/WhatsApp-Image-2023-03-01-at-11.37.18-PM.jpeg', 'Peoples Gazette', 'Nigerian stocks fall on Tinubu’s emergence as president-elect', 'Thur Mar 2, 2023' )
    image = generate_image(favicon, img, website, title, date) #pass parameter

    # Convert the image to a file object
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    filename= str(datetime.today())
    filename= filename.replace(' ', '').replace('-', '').replace(':', '').replace('.', '')
    filename='Newsway_image_'+filename+'.png'
    # Return the file object as a file response
    return FileResponse(buffer, as_attachment=True, filename=filename)
