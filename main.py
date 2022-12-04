import os
import random
import requests

from pprint import pprint
from urllib.parse import urlparse

from dotenv import load_dotenv


def save_image(filename, image_url, headers={}, params={}):
    response = requests.get(image_url, headers=headers, params=params)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_total_comics():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_random_comic(total_comics):
    num = random.randint(1, total_comics)
    url = f'https://xkcd.com/{num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_upload_url(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    payload = {
        'access_token': access_token,
        'group_id': -217501442,
        'v': '5.131',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    json_content = response.json()
    return json_content['response']['upload_url']


def get_comic_filename(image_url):
    parsed_image_url = urlparse(image_url).path
    path, extension = os.path.splitext(parsed_image_url)
    return comic_content['title'] + extension


def save_photo_for_wall(access_token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'v': '5.131',
        'group_id': -217501442,
        'photo': photo,
        'server': server,
        'hash': hash,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['response']


def post_on_wall(owner_id, media_id):
    url = 'https://api.vk.com/method/wall.post'
    photo = {
        'access_token': os.environ['vk_access_token'],
        'v': '5.131',
        'owner_id': -217501442,
        'message': image_comment,
        'attachments': f'photo{owner_id}_{media_id}',
    }
    response = requests.post(url, data=photo)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    access_token = os.environ['vk_access_token']

    total_comics = get_total_comics()
    comic_content = get_random_comic(total_comics)
    image_url = comic_content['img']
    image_comment = comic_content['alt']

    filename = get_comic_filename(image_url)
    save_image(filename, image_url)

    upload_url = get_upload_url(access_token)

    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        json_content = response.json()
    
    os.remove(filename)

    photo, hash, server = json_content['photo'], json_content['hash'], json_content['server']
    
    json_content = save_photo_for_wall(access_token)

    owner_id = json_content[0]['owner_id']
    media_id = json_content[0]['id']

    pprint(post_on_wall(owner_id, media_id))

