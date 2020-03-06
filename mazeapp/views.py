from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import sys
sys.path.append('..')
from auto.main import main, miner

@api_view(["POST"])
def current_location(request):
    
    apiKey = request.data.get("key","")
    
    get_headers = {
        "Authorization": f"Token {apiKey}"
    }
    
    info_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"

    r = requests.get(url = info_url, headers = get_headers)
    data = r.json()
    print(data)
    return Response(data)


@api_view(["GET"])
def start(request):
    main()
    return Response('done son')
