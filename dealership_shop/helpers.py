import requests
import requests_cache
import decimal 
import json 

requests_cache.install_cache(cache_name = 'image_cache', backend='sqlite', expire_after=900)


def get_image(search):

    url = "https://google-search72.p.rapidapi.com/imagesearch"

    querystring = {"q":search,"gl":"us","lr":"lang_en","num":"1","start":"0"}

    headers = {
        "X-RapidAPI-Key": "1df9712505msh8373f9c9de7bfc9p15cd94jsne1b94afb0dad",
        "X-RapidAPI-Host": "google-search72.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    img_url = data['items'][0]['originalImageUrl'] 
    return img_url

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)
    
    