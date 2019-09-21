import requests
import wget

file_url = 'https://cs8.pikabu.ru/post_img/2016/02/14/10/1455468516121493345.jpg'

# file_response = requests.get(file_url)
#
# if file_response.status_code == 200:
#     with open(f'{file_url.split("/")[-1]}', 'wb') as file:
#         file.write(file_response.content)

wget.download(file_url, out='/Volumes/400/projects/GB_data_mining/')