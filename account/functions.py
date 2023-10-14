import requests
from .models import Config, History

def sendMessage(message):
    config = Config.objects.get(id=1)
    msg = message.replace(' ','+')
    url = f'https://api.callmebot.com/whatsapp.php?phone={config.whatsapp_number}&text={msg}&apikey=2600741'
    x = requests.post(url)

def extract_lat_lng():
    ip_url = 'https://api.ipify.org?format=json'
    ip_res = requests.get(ip_url)
    ip = eval(str(ip_res.text))
    url = f"http://ip-api.com/json/{ip.get('ip')}"
    x = requests.get(url)
    data = eval(str(x.text))
    print(data)
    return data

def addHistory(request, action):
    ip = extract_lat_lng()
    History.objects.create(action=action, user=request.user, ip_address=ip.get('query'))