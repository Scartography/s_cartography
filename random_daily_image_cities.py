


import os
import shutil
import random
from PIL import Image
from geopy.geocoders import Nominatim

import tweepy
from facepy import GraphAPI

#twitter access
consumer_key = 'fqvvqfJXSnQ5SC7LLwidtFHPZ'
consumer_secret = 'TpApBrzbSaBoIuRYen5WMXBJRBZx1pOGEKt4RSVt17wrGWh3Fo'

access_token = '792827976652054528-sMpjTievRwS4KKDrTtYRASSctqVu3Xn'
access_token_secret = 'PxAoffUdE8Gc4ymLlF1zbgF6cpQU2dx7GEetc4gFBBavw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#facebook acess
ACCESS_TOKEN = 'EAAGScQCf7wMBAChpJlWDU3dqiTrSWtcomTXC7goZBgFXlX9GH5KBZCoYNJkKm6hA5I5icvT7QlHXV2vy625YJ2GqFeS2cYclbCvscZCBZAZCauH7aFdxzV51wGb3A9EsfPDtDc63PKA9bKz6ODpQVDMGpJMhlZBKgZCd4KxCCWfwAZDZD'

graph = GraphAPI(ACCESS_TOKEN)

path_cities = os.getcwd()+'/_cities_web_export/'



def random_image(images_path_01, images_path_02):


    temp = os.getcwd() + '/temp/'
    if not os.path.exists(temp):
        os.makedirs(temp)



    image_list = []
    for files in os.listdir(images_path_01):
        image_list.append(files)
    if not images_path_02 == '':
        for files in os.listdir(images_path_02):
            image_list.append(files)

    rand_item = image_list[random.randrange(len(image_list))]
    a = "DO YOU WANT TO POST THIS:"+rand_item+'????? (Y/N)'

    while not a in ['y', 'Y', 'yes', 'yay']:
        rand_item = image_list[random.randrange(len(image_list))]
        a = raw_input("DO YOU WANT TO POST THIS: "+rand_item+'????? (y/n)')

    if rand_item in os.listdir(images_path_01):
        image = images_path_01 + rand_item
    else:
        image = images_path_02 + rand_item


    name = image.split('/')[-1]

    if 'SAR' in name or 'Sigma' in name or 'projectedLocalIncidenceAngle' in name:
        satellite = 'Sentinel-1'
    elif 'INFRARED' in name:
        satellite = 'Sentinel-2 Infrared'
    elif '3D' in name:
        satellite = 'Sentinel-2 #3D'
    else:
        satellite = 'Sentinel-2'


    basewidth = 2700
    img = Image.open(image)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(temp+name.replace('.jpg','')+'_small.jpg', "JPEG", quality=55)
    image = temp + name.replace('.jpg','')+'_small.jpg'
    print image

    name = name.split('_')[0]

    name_link = name.lower()
    name_link = name_link.replace(' ','-')



    message_twitter = '#'+name.replace(' ', '') + ' from #space by the @CopernicusEU '+satellite+'! Download at: https://sevcikcartography.wixsite.com/cartography/'+name_link



    if len(message_twitter) <= 126:
        message_twitter = message_twitter + ' #map #Geography'
    elif len(message_twitter) <= 137:
        message_twitter = message_twitter + ' #map'

    print message_twitter
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(name)
        print location.latitude, location.longitude
        status = api.update_with_media(image, message_twitter, location.latitude, location.longitude)
    except:
        location = 51.0504, 13.7373
        status = api.update_with_media(image, message_twitter, 51.0504, 13.7373)



    message_facebook = message_twitter.replace('@', '#') +' @[200540683688506]'
    print message_facebook

    graph.post(path= 'me/photos', message=message_facebook , source =open(image, 'rb'), location = location)


    #API.update_with_media(filename[, status][, in_reply_to_status_id][, lat][, long][, source][, place_id][, file])
    #status = api.update_with_media(image, message, location.latitude, location.longitude)

    shutil.rmtree(temp)


random_image(images_path_01=path_cities, images_path_02='')


#random_image_facebook(path_images)