import requests
from pprint import pprint
from settings  import token


class YandexDisk:

    def __init__(self, token):
        self.token = token
        self.base_url = 'https://cloud-api.yandex.net/v1/disk'
        self.headers = {'Authorization': f"OAuth {token}"}
        
    def create_folder(self, path_disk):

        """Создаёт папку на вашем аккаунте по указанному адресу"""

        url = f'{self.base_url}/resources'
        self.path_disk = path_disk
        
        params = {'path': path_disk}
        response = requests.put(url, headers=self.headers, params=params) 

        if response.status_code == 201:
            print(f"{response.status_code}\nпапка {path_disk} успешно создана ")
            return path_disk
        elif response.status_code == 409:
            print(f'Папка {path_disk} уже существует')
            pass
        elif response.status_code == 404:
            print(f"{response.status_code} \nНекорректный запрос")
            return None
        elif response.status_code == 401:
            print(f'Токен {token[:6]}...{token[-6:]} недействителен')
            return None
        else:
            print('Error')
            return None
           

    def delete_folder(self, path_disk):

        """Удаляет папку по указанному адресу"""

        url = f'{self.base_url}/resources'
        self.path = path_disk
        params = {
            'path': path_disk,
            'permanently': True
        }
        
        response = requests.delete(url, params=params, headers=self.headers)
        if response.status_code == 204:
            print(f'Папка успешно удалена')
            return path_disk
        elif response.status_code == 401:
            print(f'Токен {token[:6]}...{token[-6:]} недействителен')
            return None
        elif response.status_code in range(400, 499):
            print(f"{response.status_code} \nНекорректный запрос")
            return None
        else:
            print('Error')
            return None
           

    def add_photo(self, photo_url: dict):

        """Загружает одно или несколько фото из интернета по ссылкам. 
        Данные необходимо передавать в формате словаря: {папка/название: url}"""
      
        if not isinstance(photo_url, dict):
            pprint('Введите данные в виде словаря')
            return None

        URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for folder, url in photo_url.items():
            params = {
                'path': folder,
                'url': url}
            
            response = requests.post(URL, params=params, headers=self.headers)
            if response.status_code == 202:
                print(f'Фото успешно загружено по адресу {folder}')
            elif response.status_code == 401:
                print(f'Токен {token[:6]}...{token[-6:]} недействителен')
                return None    
            else:
                print(f'Ошибка {response.status_code}')
           

class Dogs:
     
     def __init__(self, breed):
        self.breed = breed

     def get_photo(self): 
        
        """возвращает ссылки на фото из интернета"""

        url = 'https://dog.ceo/api/breeds/list/all'
        response = requests.get(url).json()
        url_dict = {}
        if self.breed in response['message']:
            if response['message'][self.breed]:
                
                for sub_breed in response['message'][f'{self.breed}']:
                    sub_url = f'https://dog.ceo/api/breed/{self.breed}/{sub_breed}/images/random'
                    new_resp = requests.get(sub_url).json()
                    url_dict[f'{self.breed}/{sub_breed}'] = new_resp['message']
            else:
                url_dict[f'{self.breed}/{self.breed}'] =  f'https://dog.ceo/api/breed/{self.breed}/images/random'
        
        else:
            print(f'Порода {self.breed} не найдена')
            return None
        
        if url_dict is not None:
            return url_dict  
           
          
        
    
          
Y = YandexDisk(token)
dog = Dogs("schnauzer")
p = dog.get_photo()
if p is not None:
   Y.create_folder(dog.breed)
   Y.add_photo(p)

