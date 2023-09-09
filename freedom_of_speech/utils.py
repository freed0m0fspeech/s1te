import requests
import os

from math import sqrt


def is_url_image(image_url):
    try:
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.get(image_url, timeout=1)
        # timeout=(0.5, 1)

        if r.headers["content-type"] in image_formats:
            return True

        return False
    except Exception as e:
        print(e)
        return False


def exchange_code(code: str, redirect_uri: str):
    try:
        data = {
            "client_id": os.getenv('DISCORD_BOT_CLIENT_ID', ''),
            "client_secret": os.getenv('DISCORD_BOT_SECRET', ''),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "scope": "identify"
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
        credentials = response.json()
        access_token = credentials['access_token']

        response = requests.get("https://discord.com/api/v7/users/@me", headers={
            'Authorization': 'Bearer %s' % access_token
        })

        user = response.json()

        return user
    except Exception as e:
        print(e)
        return None


def calculate_lvl(xp, xp_factor):
    lvl = 0.5 + sqrt(1 + 8 * (xp) / (xp_factor)) / 2
    lvl = int(lvl) - 1

    xp_for_level = lvl / 2 * (2 * xp_factor + (lvl - 1) * xp_factor)

    xp_have = int(xp - xp_for_level)
    xp_need = (lvl + 1) * xp_factor

    return lvl, xp_have, xp_need


def update_cached_data(mongoDataBase):
    query = {'_id': 0, 'constitution': 1, 'laws': 1, 'users': 1, 'president': 1, 'testimonials': 1,
             'tlaws': 1,
             'start_vote': 1, 'judge': 1, 'referendum': 1, 'social': 1, 'parliament': 1, 'telegram': 1,
             'discord': 1,
             'xp': 1}
    return mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                      query=query)
