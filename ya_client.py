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
    
    def upload_file(self, path, filename):
        url = f'{self.url}/resources/upload'
        params = {'path': path, 'overwrite': 'true'}
        files = {'file': open(filename, 'rb')}
        response = requests.post(url, headers=self.headers, params=params, files=files)
        return response    
