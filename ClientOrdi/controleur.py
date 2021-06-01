import requests
#from evdev import InputDevice, categorize, ecodes


token =""

def connexion(login="",password=""):
    global token
    r = requests.get('http://192.168.0.18:8123/login', auth=(login, password))
    print(r.status_code)
    if r.status_code == 200:
        if 'token' in r.json():
            token=r.json()['token']
            print("connection OK")
            return
    else:
        print("Erreur de connexion")


def envoiCommande():
    if token != "":
        r = requests.get('http://192.168.0.18:8123/stop', headers={'x-access-token': token})
        print(r.status_code)
        if r.status_code == 200:
            print(r.json())
    else:
        print('Non connecté')

if __name__ == '__main__':
     connexion('admin','azerty')
     envoiCommande()