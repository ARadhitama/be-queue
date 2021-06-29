import requests

api_token = "rY31CW7Jujq8QKYhfFR22EYcl0mcbNcT5rFvOj5VWuQtcXkFnr" # GET https://x.rajaapi.com/poe
api_url = "https://x.rajaapi.com/"
jakarta_id = 31


def get_provinsi():
    url = api_url + "MeP7c5ne" + api_token + "/m/wilayah/provinsi"
    r = requests.get(url)
    data = r.json()

    if data['code'] == 200:
        return data['data']
    else:
        return []


def get_kabupaten():
    url = api_url + "MeP7c5ne" + api_token + "/m/wilayah/kabupaten?idpropinsi=" + str(jakarta_id)
    r = requests.get(url)
    data = r.json()

    if data['code'] == 200:
        return data['data']
    else:
        return []


def get_kecamatan(kabupaten_id):
    url = api_url + "MeP7c5ne" + api_token + "/m/wilayah/kecamatan?idkabupaten=" + str(kabupaten_id)
    r = requests.get(url)
    data = r.json()

    if data['code'] == 200:
        return data['data']
    else:
        return []


def get_kelurahan(kecamatan_id):
    url = api_url + "MeP7c5ne" + api_token + "/m/wilayah/kelurahan?idkecamatan=" + str(kecamatan_id)
    r = requests.get(url)
    data = r.json()

    if data['code'] == 200:
        return data['data']
    else:
        return []