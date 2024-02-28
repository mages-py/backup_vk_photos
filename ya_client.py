import requests

class YaClient:
    def __init__(self, token):
        self.url = 'https://cloud-api.yandex.net/v1/disk'
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}

    def is_exist(self, path):
        url = f'{self.url}/resources'
        params = {'path': path}
        response = requests.get(url, headers=self.headers, params=params)
        return response.status_code == 200
    
    def create_folder(self, path):
        url = f'{self.url}/resources'
        params = {'path': path}
        response = requests.put(url, headers=self.headers, params=params)
        return response.status_code
    
    def _get_upload_url(self, path, overwrite='false'):
        url = f'{self.url}/resources/upload'
        params = {'path': path, 'overwrite': overwrite}
        response = requests.get(url, headers=self.headers, params=params)
        return response
    
    def upload_file(self, path, filename, overwrite='false'):
        url = self._get_upload_url(path, overwrite).json().get('href', '')
        if not url:
            print('Ошибка получения ссылки для загрузки')
            return
        with open(filename, 'rb') as f:
            response = requests.put(url, headers=self.headers, data=f)
        return response
