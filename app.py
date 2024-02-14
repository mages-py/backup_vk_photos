from vk_client import VKClient
from pprint import pprint

def start(user_id):
    client = VKClient(user_id=user_id)
    albums = client.get_albums()
    if 'error' in albums:
        print('Текст ошибки:', albums['error']['error_msg'])
        return
    print('Список альбомов:')
    print('===================================================================')
    for album in albums['response']['items']:
        print(album['id'], album['title'])
    print('===================================================================')
    album_id = int(input('Введите ID альбома: '))
    if album_id == 0:
        return
    photos = client.get_photos(album_id)
    if 'error' in photos:
        print('Текст ошибки:', photos['error']['error_msg'])
        return
    print('Список фотографий:')
    print('===================================================================')
    save_photos = []
    for photo in photos['response']['items']:
        print(photo['id'], photo['sizes'][-1]['url'])
        pprint(photo)
    # print('===================================================================')
    # photo_id = int(input('Введите ID фотографии: '))
    # if photo_id < 0:
    #     return
    # client.download_photo(photo_id, album_id)
    

if __name__ == '__main__':
    start(2688868)
    # start(6616826)