from vk_client import VKClient
from pprint import pprint

def get_album_id(client_vk):
    albums = client_vk.get_albums()
    if 'error' in albums:
        print('Текст ошибки:', albums['error']['error_msg'])
        return
    albums_arr = [{'profile':'Фото профиля'}, {'wall': 'Фото со стены'}]
    albums_arr += [{album['id']: album['title']} for album in albums['response']['items'] if int(album['id']) > 0]
    print('Список альбомов:')
    print('===================================================================')
    for idx, album in enumerate(albums_arr, start=1):
        print(idx, list(album.values())[0])
    print('===================================================================')
    album_id = int(input('Введите номер альбома: '))
    if album_id <= 0 or album_id > len(albums_arr):
        print('Нет такого альбома')
        return
    return list(albums_arr[album_id-1].keys())[0]

def get_sorted_photos(vk_client, album_id):
    photos = vk_client.get_photos(album_id)
    if 'error' in photos:
        print('Текст ошибки:', photos['error']['error_msg'])
        return
    return sorted(photos['response']['items'], key=lambda photo: photo['likes']['count'], reverse=True)
    

def start(user_id, qty_photos=5):
    client_vk = VKClient(user_id=user_id)
    
    album_id = get_album_id(client_vk)
    if not album_id:
        print('Не выбран альбом')
        return
    
    photos = get_sorted_photos(client_vk, album_id)
    pprint(photos[0:qty_photos])
    # print('===================================================================')
    # photo_id = int(input('Введите ID фотографии: '))
    # if photo_id < 0:
    #     return
    # client.download_photo(photo_id, album_id)
    

if __name__ == '__main__':
    start(2688868)
    # start(6616826)