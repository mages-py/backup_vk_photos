import datetime
from vk_client import VKClient
from ya_client import YaClient
from file_utilities import FileUtilities

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
    
def get_qty_photos(max_qty):
    qty = input(f'Всего фотографий: {max_qty}. Сколько фотографий скачать? ({5 if max_qty > 5 else max_qty} по умолчанию): ')
    if qty.isdigit():
        return int(qty) if int(qty) <= max_qty else max_qty
    return 5 if max_qty > 5 else max_qty

def get_folder_name(client_ya: YaClient):
    folder_name = f'Backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
    user_folder_name = input(f'Укажите имя папки (по умолчанию: {folder_name}): ')
    ya_folder_name = user_folder_name if user_folder_name else folder_name
    if client_ya.is_exist('/BackupVKPhoto'):
        if client_ya.is_exist(f'/BackupVKPhoto/{ya_folder_name}'):
            print(f'Папка {ya_folder_name} уже существует. Придумайте другое имя.')
            get_folder_name(client_ya)
        else:
            client_ya.create_folder(f'/BackupVKPhoto/{ya_folder_name}')
    else:
        client_ya.create_folder('/BackupVKPhoto/')
        client_ya.create_folder(f'/BackupVKPhoto/{ya_folder_name}')
    return f'/BackupVKPhoto/{ya_folder_name}'

def print_progressbar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def backup_photos(user_id, ya_token):
    client_vk = VKClient(user_id=user_id)
    client_ya = YaClient(token=ya_token)
    utils = FileUtilities()
    
    album_id = get_album_id(client_vk)
    if not album_id:
        print('Не выбран альбом')
        return
    
    photos = get_sorted_photos(client_vk, album_id)
    qty_photos = get_qty_photos(len(photos))
    backup_photos = photos[0:qty_photos]
     
    if not backup_photos:
        print('Нет фотографий для сохранения.')
        return
    
    folder = get_folder_name(client_ya)
    json_photos = []
    
    print_progressbar(0, qty_photos, prefix = f'Прогресс: 0/{qty_photos}', suffix = 'Загружено', length = 50)
    for i, photo in enumerate(backup_photos):
        if not 'sizes' in photo:
            continue
        max_size = sorted(photo['sizes'], key=lambda x: x['width'] * x['height'], reverse=True)[0]
        url =max_size['url']
        ext = url.split('.')[-1][0:3]
        size = max_size['type']
        count_likes = photo['likes']['count']
        create_date = photo['date']
        file_name = f'{count_likes}.{ext}'
        if client_ya.is_exist(f'{folder}/{file_name}'):
            file_name = f'{count_likes}_{create_date}.{ext}'
            if client_ya.is_exist(f'{folder}/{file_name}'):
                file_name = f'{count_likes}_{create_date}_{i}.{ext}'
        utils.download_file(url, file_name)
        if client_ya.upload_file(folder + '/' + file_name, file_name, 'true'):
            json_photos.append({
                'file_name': file_name,
                'size': size
            })
        utils.delete_file(file_name)
        print_progressbar(i + 1, qty_photos, prefix = f'Загружено: {i+1}/{qty_photos}', suffix = 'загружено', length = 50)
    utils.create_json_file('VKBackup.json', json_photos)

if __name__ == '__main__':
    vk_user_id = int(input('ID пользователя VK: '))
    ya_token = input('Токен Яндекс.Диска: ')
    backup_photos(vk_user_id, ya_token)