import os
import random
import requests

from urllib.parse import urlparse

from dotenv import load_dotenv


def get_comics_count():
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
    return f"{comic_content['title']}{extension}"


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


def upload_photo_to_server(filename, upload_url):
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


def post_on_wall(group_id, owner_id, media_id):
    url = 'https://api.vk.com/method/wall.post'
    group_id = -int(group_id)
    photo = {
        'owner_id': group_id,
        'message': image_comment,
        'attachments': f'photo{owner_id}_{media_id}',
    }
    response = session.post(url, data=photo)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    comics_count = get_comics_count()
    comic_content = get_random_comic(comics_count)
    image_url, image_comment = comic_content['img'], comic_content['alt']
    filename = get_comic_filename(image_url)
    save_image(filename, image_url)

    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = os.environ['VK_GROUP_ID']
    vk_version_api = os.environ['VK_VERSION_API']

    with requests.Session() as session:
        session.params.update(
            {
            'access_token': access_token,
            'v': vk_version_api,
        })
        upload_url = get_upload_url()

        try:
            server_photo_content = upload_photo_to_server(filename, upload_url)
        finally:    
            os.remove(filename)

        photo = server_photo_content['photo']
        photo_hash = server_photo_content['hash']
        server =  server_photo_content['server']
    
        wall_photo_content = save_wall_photo(photo, photo_hash, server)
        owner_id = wall_photo_content[0]['owner_id']
        media_id = wall_photo_content[0]['id']
        post_on_wall(group_id, owner_id, media_id)
