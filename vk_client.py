from config import VK_TOKEN
from pprint import pprint
import requests

class VKClient:
    PARAMS = {
            'access_token': VK_TOKEN,
            'v': '5.131',
        }
    def __init__(self, user_id = 0):
        self.user_id = user_id
    
    def get_data(self, url, params=None):
        """
        Get data from the VK.com.
        :param user_id: The ID of the user whose data is being retrieved.
        :return: The response containing the data as a JSON object.
        """
        if params:
            params.update(self.PARAMS)
        else:
            params = self.PARAMS
            
        response = requests.get(url, params=params).json()
        return response
        
    def get_albums(self):
        """
        Get albums for a specific user from the VK.com.
        :return: The response containing the albums for the user specified by owner_id as a JSON object.
        """
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = {
                'owner_id': self.user_id,
                'need_system': 1,
            }
        
        return self.get_data(url=url, params=params)
    
    def get_photos(self, album_id):
        """
        Get photos from the VK.com.
        :return: The response containing the photos as a JSON object.
        """
        url = 'https://api.vk.com/method/photos.get'
        params = {
                'owner_id': self.user_id,
                'album_id': album_id,
                'extended': 1,
                'photo_sizes': 1,
            }
        
        return self.get_data(url=url, params=params)

if __name__ == '__main__':        
    vk = VKClient(user_id=2688868)
    albums = vk.get_albums()
    # print(albums['response']['count'])
    pprint(albums['response']['items'])
    # print(albums)