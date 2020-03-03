from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import sys
sys.path.append('..')
from auto.main import main

@api_view(["POST"])
def current_location(request):
    
    apiKey = request.data.get("key","")
    
    get_headers = {
        "Authorization": f"Token {apiKey}"
    }
    move_headers = {
        "Authorization": f"Token {apiKey}",
        "content-type": "application/json"
    }
    info_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"

    r = requests.get(url = info_url, headers = get_headers)
    data = r.json()
    print(data)
    return Response(data)

@api_view(["POST"])
def start(request):
    main()
    return Response('done son')