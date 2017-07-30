import requests
from bs4 import BeautifulSoup
import json

def get_20_items(data):
    lastid = ''
    for i in data['items']:
        lastid = str(i['id'])
        insta_url = 'https://www.instagram.com/p/' + (i['code'])
        res = requests.get(insta_url)
        soup = BeautifulSoup(res.text, "lxml")
        json_part = soup.find_all("script", type="text/javascript")[1].string

        # as json
        json_part = json_part[json_part.find('=') + 2:-1]
        data = json.loads(json_part)

        if (str(data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['is_video']) == 'False'):
            image_url = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
            img_data = requests.get(image_url).content
            print("Start downloading.")
            with open(i['code'] + '.jpg', 'wb') as handler:
                handler.write(img_data)
            print("Done.")
        else:
            print("Not a photo!")

    return lastid

def refresh_url(origin_url, lastid):
    return str(origin_url+'?max_id='+lastid)

def main():
    user_id = 'siliconhbo'

    origin_urll = 'https://www.instagram.com/'+user_id+'/media/'
    urll = origin_urll
    data = requests.get(urll).json()
    not_last = True
    while(not_last):
        urll = refresh_url(origin_urll, get_20_items(data))
        data = requests.get(urll).json()
        if(len(data['items']) < 20):
            break
    # Last items
    # test
    get_20_items(data)

if __name__ == '__main__':
    main()
