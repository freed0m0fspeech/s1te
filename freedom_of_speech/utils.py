import requests
import os

from math import sqrt


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.get(image_url)

    if r.headers["content-type"] in image_formats:
        return True

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
