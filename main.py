import os
import random
import requests

from urllib.parse import urlparse

from dotenv import load_dotenv


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


def get_comic_filename(image_url):
    parsed_image_url = urlparse(image_url).path
    path, extension = os.path.splitext(parsed_image_url)
    return comic_content['title'] + extension


def save_image(filename, image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_upload_url():
    url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    response = session.get(url)
    response.raise_for_status()
    json_content = response.json()
    return json_content['response']['upload_url']


def download_photo_to_server(filename, upload_url):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return response.json()


def save_wall_photo(photo, hash, server):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'photo': photo,
        'hash': hash,
        'server': server,
    }
    response = session.post(url, data=payload)
    response.raise_for_status()
    return response.json()['response']


def post_on_wall(owner_id, media_id):
    url = 'https://api.vk.com/method/wall.post'
    photo = {
        'owner_id': -217501442,
        'message': image_comment,
        'attachments': f'photo{owner_id}_{media_id}',
    }
    response = session.post(url, data=photo)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    
    total_comics = get_total_comics()
    comic_content = get_random_comic(total_comics)
    image_url = comic_content['img']
    image_comment = comic_content['alt']
    filename = get_comic_filename(image_url)
    save_image(filename, image_url)

    access_token = os.environ['vk_access_token']
    vk_version_api = 5.131
    with requests.Session() as session:
        session.params.update(
            {
            'access_token': access_token,
            'v': vk_version_api,
        })

        upload_url = get_upload_url()
        server_photo_content = download_photo_to_server(filename, upload_url)
        os.remove(filename)

        photo = server_photo_content['photo']
        hash = server_photo_content['hash']
        server =  server_photo_content['server']
    
        wall_photo_content = save_wall_photo(photo, hash, server)
        owner_id = wall_photo_content[0]['owner_id']
        media_id = wall_photo_content[0]['id']
        post_on_wall(owner_id, media_id)
