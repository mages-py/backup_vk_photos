import requests
import os
import json

class FileUtilities:

    def read_file(self,filename):
        with open(filename, 'r') as f:
            return f.read()
        
    def download_file(self, url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
            
    def is_exists(self, path):
        return os.path.exists(path) or os.path.isdir(path)
    
    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)
    
    def create_json_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4, skipkeys=True)
    def delete_folder(self, path):
        os.rmdir(path)
    def delete_file(self, path):
        os.remove(path)
        
        
if __name__ == '__main__':
    utils = FileUtilities()
    utils.delete_folder('images')