import datetime
import json
import os
import random
import secrets
from math import sqrt

import requests

from bson import json_util
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from pytz import utc
from utils import dataBases
from freedom_of_speech.utils import is_url_image, exchange_code, calculate_lvl
from datetime import (
    datetime,
    timedelta,
)
from django_telegram_login.authentication import (
    verify_telegram_authentication
)
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)

mongoDataBase = dataBases.mongodb_client


class HomePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        cockies = request.COOKIES

        context = {

        }

        query = {'_id': 0, 'constitution': 1, 'laws': 1, 'tlaws': 1, 'users': 1, 'testimonials': 1, 'president': 1,
                 'parliament': 1, 'judge': 1, 'start_vote': 1, 'end_vote': 1, 'telegram': 1, 'candidates': 1,
                 'votes': 1,
                 'referendum': 1, 'social': 1, 'discord': 1}

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            # DataBase error
            return HttpResponse(status=500)

        constitution = document.get('constitution', '')
        laws = document.get('laws', '')
        tlaws = document.get('tlaws', '')
        testimonials = document.get('testimonials', [])

        start_vote = document.get('start_vote', '')
        end_vote = document.get('end_vote', '')

        # Government in database is usernames of telegram accounts
        president = document.get('president', '')
        parliament = document.get('parliament', '')
        judge_info = document.get('judge', {})

        if not cockies:
            user = {}
            username = ''
        else:
            user = {}
            sessionid = cockies.get('sessionid', '')
            username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            user = users[username]

                            if username == president:
                                context['is_president'] = True
                                if tlaws:
                                    laws = tlaws
                                    tlaws = True
                            else:
                                context['is_president'] = False

                            if username == parliament:
                                context['is_parliament'] = True
                                if tlaws:
                                    laws = tlaws
                                    tlaws = True
                            else:
                                context['is_parliament'] = False

        # 10 random testimonials
        testimonials_count = len(testimonials)
        max_testimonials = 10
        testimonials = random.sample(testimonials, min(testimonials_count, max_testimonials))

        if user:
            permissions = user.get('permissions', {'administrator': False, 'moderator': False})
        else:
            permissions = {}

        telegram = document.get('telegram', {})
        discord = document.get('discord', {})
        # members_count = 0

        telegram_members_count = int(telegram.get('chat_parameters', {}).get('members_count', 0))
        discord_members_count = int(discord.get('guild_parameters', {}).get('member_count', 0))

        if context.get('is_president', ''):
            context['judge'] = judge_info.get('president', '')
        else:
            if context.get('is_parliament', ''):
                context['judge'] = judge_info.get('parliament', '')
            else:
                context['judge'] = judge_info.get('judge', '')

        context['referendum'] = document.get('referendum', {}).get('votes', {}).get(username, False)
        context['president'] = president
        context['parliament'] = parliament
        context['constitution'] = constitution
        context['telegram_members_count'] = telegram_members_count
        context['discord_members_count'] = discord_members_count
        date_updated = max(telegram.get('chat_parameters', {}).get('date', ''),
                           discord.get('guild_parameters', {}).get('date', ''))
        context['date_updated'] = date_updated

        if document.get('users', {}).get(username, {}):
            context['username'] = username

        context['laws'] = laws
        context['tlaws'] = tlaws
        context['administrator'] = permissions.get('administrator', False)
        context['moderator'] = permissions.get('administrator', permissions.get('moderator', False))
        context['testimonials'] = testimonials
        context['start_vote'] = start_vote
        context['end_vote'] = end_vote
        context['candidates'] = document.get('candidates', {})
        context['candidate'] = document.get('candidates', {}).get(username, {})
        context['users'] = document.get('users', {}).keys()
        context['parliament_voted'] = document.get('votes', {}).get('parliament', {}).get(username, '')
        context['president_voted'] = document.get('votes', {}).get('president', {}).get(username, '')
        context['social'] = document.get('social', {})
        context['users_count'] = len(document.get('users', {}))

        response = render(request=request, template_name='freedom_of_speech/index.html', context=context)

        return response


class SignInPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        # if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        #     username = request.COOKIES['username']
        #
        #     last_connection = request.COOKIES['last_connection']
        #     last_connection_time = datetime.datetime.strptime(last_connection[:-7],
        #                                                       "%Y-%m-%d %H:%M:%S")
        #
        #     if (datetime.datetime.now() - last_connection_time).seconds < 10:
        #         response = HttpResponse(str(username) + ' last connection < 10 seconds')
        #     else:
        #         response = HttpResponse(str(username) + ' last connection > 10 seconds')
        #
        # else:
        #     response = HttpResponse('not logged in')
        #
        # return response

        context = {

        }

        response = render(request=request, template_name='freedom_of_speech/signin.html', context=context)

        return response

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        username = data.get('username', '')
        password = data.get('password', '')

        if not username or not password:
            return HttpResponse(status=422)

        try:
            username.encode('latin-1')
        except UnicodeEncodeError:
            return HttpResponse(status=422)

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        try:
            sessionid = ''
            users = document['users']

            if users[username]:
                user = users[username]
                if user['password'] == password:
                    sessionid = user['sessionid']
        except (IndexError, KeyError, TypeError):
            return HttpResponse(status=401)

        if sessionid:

            context = {

            }

            # response = render(request=request, template_name='freedom_of_speech/index.html', context=context)

            response = HttpResponse(status=200)

            expires = datetime.now(tz=utc) + timedelta(days=7)

            response.set_cookie(key='username', value=username, secure=True, samesite='None', expires=expires)
            response.set_cookie(key='sessionid', value=sessionid, secure=True, samesite='None', expires=expires)

            # expires = datetime.datetime.now() + datetime.timedelta(days=7)
            # sessionid = secrets.token_urlsafe(24)

            # response.set_cookie(key='last_connection', value=datetime.datetime.now(), secure=True, samesite='None',
            #                     expires=expires)
            # response.set_cookie('username', username, expires=expires)
            # session_num_bytes = 24
            # response.set_cookie('sessionID', uuid.UUID(bytes=M2Crypto.m2.rand_bytes(session_num_bytes)))
            # response.set_cookie('sessionID', uuid.UUID(bytes=OpenSSL.rand.bytes(session_num_bytes)))

            return response
        else:
            return HttpResponse(status=401)


class SignTelegramPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        # cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        try:
            verify_telegram_authentication(bot_token=os.getenv('TELEGRAM_BOT_TOKEN', ''), request_data=data)
        except (TelegramDataIsOutdatedError, NotTelegramDataError):
            return HttpResponse(status=422)

        username = ''

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        try:
            sessionid = ''
            users = document.get('users', {})

            for user in users:
                user_telegram = users.get(user, {}).get('telegram', {})

                if user_telegram.get('id', '') == data.get('id', ''):
                    username = user
                    sessionid = users.get(user, {}).get('sessionid', '')

        except (IndexError, KeyError, TypeError):
            return HttpResponse(status=401)

        if sessionid:
            query = {f'users.{username}.telegram': data}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set', query=query, upsert=False)

            context = {

            }

            response = HttpResponse(status=200)

            expires = datetime.now(tz=utc) + timedelta(days=7)

            response.set_cookie(key='username', value=username, secure=True, samesite='None', expires=expires)
            response.set_cookie(key='sessionid', value=sessionid, secure=True, samesite='None', expires=expires)

            return response
        else:
            # register new user
            tid = data.get('id', '')
            username = f"telegram@{tid}"

            if not username:
                return HttpResponse(status=422)

            try:
                username.encode('latin-1')
            except UnicodeEncodeError:
                return HttpResponse(status=422)

            query = {'_id': 0, 'users': 1}
            document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                  query=query)

            if not document:
                return HttpResponse(status=500)

            users = document.get('users', '')
            user = ''
            if users:
                user = users.get(username, '')

            if user:
                return HttpResponse(status=409)  # Already registered username

            response = HttpResponse(status=201)

            session_num_bytes = 24
            sessionid = secrets.token_urlsafe(session_num_bytes)
            expires = datetime.now(tz=utc) + timedelta(days=7)
            response.set_cookie(key='username', value=username, secure=True, samesite='None', expires=expires)
            response.set_cookie(key='sessionid', value=sessionid, secure=True, samesite='None', expires=expires)

            query = {f'users.{username}.sessionid': sessionid, f'users.{username}.telegram': data}
            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                     action='$set', query=query, upsert=False) is None:
                return HttpResponse(status=500)

            return response


class SignDiscordPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')

        if not code:
            return HttpResponse(status=422)

        redirect_uri = f"{os.getenv('HOSTNAME')}freedom_of_speech/sign/discord/"
        data = exchange_code(code, redirect_uri)

        # data = request.POST
        # cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        username = ''

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        try:
            sessionid = ''
            users = document.get('users', {})

            for user in users:
                user_discord = users.get(user, {}).get('discord', {})

                if user_discord.get('id', '') == data.get('id', ''):
                    username = user
                    sessionid = users.get(user, {}).get('sessionid', '')

        except (IndexError, KeyError, TypeError):
            return HttpResponse(status=401)

        if sessionid:
            query = {f'users.{username}.discord': data}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set', query=query, upsert=False)

            context = {

            }

            response = render(request=request, template_name='freedom_of_speech/popup_success.html', context={})

            expires = datetime.now(tz=utc) + timedelta(days=7)

            response.set_cookie(key='username', value=username, secure=True, samesite='None', expires=expires)
            response.set_cookie(key='sessionid', value=sessionid, secure=True, samesite='None', expires=expires)

            return response
        else:
            # register new user
            did = data.get('id', '')
            username = f"discord@{did}"

            if not username:
                return HttpResponse(status=422)

            try:
                username.encode('latin-1')
            except UnicodeEncodeError:
                return HttpResponse(status=422)

            query = {'_id': 0, 'users': 1}
            document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                  query=query)

            if not document:
                return HttpResponse(status=500)

            users = document.get('users', '')
            user = ''
            if users:
                user = users.get(username, '')

            if user:
                return HttpResponse(status=409)  # Already registered username

            response = render(request=request, template_name='freedom_of_speech/popup_success.html', context={})

            session_num_bytes = 24
            sessionid = secrets.token_urlsafe(session_num_bytes)
            expires = datetime.now(tz=utc) + timedelta(days=7)
            response.set_cookie(key='username', value=username, secure=True, samesite='None', expires=expires)
            response.set_cookie(key='sessionid', value=sessionid, secure=True, samesite='None', expires=expires)

            query = {f'users.{username}.sessionid': sessionid, f'users.{username}.discord': data}
            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                          action='$set', query=query, upsert=False) is None:
                return HttpResponse(status=500)

            return response


class SignUpPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        # if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        #     username = request.COOKIES['username']
        #
        #     last_connection = request.COOKIES['last_connection']
        #     last_connection_time = datetime.datetime.strptime(last_connection[:-7],
        #                                                       "%Y-%m-%d %H:%M:%S")
        #
        #     if (datetime.datetime.now() - last_connection_time).seconds < 10:
        #         response = HttpResponse(str(username) + ' last connection < 10 seconds')
        #     else:
        #         response = HttpResponse(str(username) + ' last connection > 10 seconds')
        #
        # else:
        #     response = HttpResponse('not logged in')
        #
        # return response

        context = {

        }

        response = render(request=request, template_name='freedom_of_speech/signup.html', context=context)

        return response

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        username = data.get('username', '')
        password = data.get('password', '')
        repeat_password = data.get('repeat_password', '')

        if not username or not password or not repeat_password:
            return HttpResponse(status=422)

        try:
            username.encode('latin-1')
        except UnicodeEncodeError:
            return HttpResponse(status=422)

        if any(char in "#/@" for char in username):
            return HttpResponse(status=422)

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        users = document.get('users', '')
        user = ''
        if users:
            user = users.get(username, '')

        if user:
            return HttpResponse(status=409)  # Already registered username
        if password != repeat_password:
            return HttpResponse(status=422)  # Passwords mismatches

        # context = {
        #
        # }

        # response = render(request=request, template_name='freedom_of_speech/index.html', context=context)

        response = HttpResponse(status=201)

        session_num_bytes = 24
        sessionid = secrets.token_urlsafe(session_num_bytes)
        expires = datetime.now(tz=utc) + timedelta(days=7)
        response.set_cookie(key='username', value=username, secure=True, samesite='None', expires=expires)
        response.set_cookie(key='sessionid', value=sessionid, secure=True, samesite='None', expires=expires)

        query = {f'users.{username}.password': password, f'users.{username}.sessionid': sessionid}
        updateMongo = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                 action='$set', query=query, upsert=False)

        if updateMongo is None:
            return HttpResponse(status=500)

        # try:
        #     user = document['users'][username]
        #     password_check = user['password']
        #     sessionid_check = user['sessionid']
        # except (IndexError, KeyError, TypeError):
        #     user = ''
        #     password_check = ''
        #     sessionid_check = ''
        #
        # if not password == password_check or not sessionid == sessionid_check:
        #     return HttpResponse(status=500)

        # expires = datetime.datetime.now() + datetime.timedelta(days=365)
        # response.set_cookie(key='last_connection', value=datetime.datetime.now(), secure=True, samesite='None')
        # response.set_cookie('username', username, expires=expires)
        # response.set_cookie('sessionID', uuid.UUID(bytes=M2Crypto.m2.rand_bytes(session_num_bytes)))
        # response.set_cookie('sessionID', uuid.UUID(bytes=OpenSSL.rand.bytes(session_num_bytes)))

        return response


class SignOutPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        # data = request.POST
        cookies = request.COOKIES

        if 'username' or 'sessionid' in cookies:
            response = HttpResponse(status=200)

            response.delete_cookie('username')
            response.delete_cookie('sessionid')

            return response
        else:
            return HttpResponse(status=422)


class EditPasswordPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        # old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')

        if not new_password:
            return HttpResponse(status=422)

        # if old_password == new_password:
        #     return HttpResponse(status=401)

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        user = {}
        if cookies:
            sessionid = cookies.get('sessionid', '')
            username = cookies.get('username', '')

            if 'sessionid' and 'username' in cookies:
                users = document.get('users', {})
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            if not users.get(username, {}).get('password', '') == new_password:
                                user = users.get(username, {})
                            else:
                                return HttpResponse(status=200)
        else:
            return HttpResponse(status=422)

        if user:
            query = {f'users.{username}.password': new_password}
            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                     action='$set', query=query) is None:
                return HttpResponse(status=500)

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=422)


class EditLawsPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        cockies = request.COOKIES

        if not data or not cockies:
            return HttpResponse(status=422)

        laws = data.get('laws', '')

        if not laws:
            return HttpResponse(status=422)

        user = {}
        sessionid = cockies.get('sessionid', '')
        username = cockies.get('username', '')

        if 'sessionid' and 'username' in cockies:
            query = {'_id': 0, 'users': 1, 'parliament': 1, 'president': 1, 'laws': 1}
        else:
            return HttpResponse(status=422)

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        parliament = document.get('parliament', '')
        president = document.get('president', '')

        is_president = False
        is_parliament = False

        users = document.get('users', {})
        if users.get(username, ''):
            if users[username].get('sessionid', ''):
                if sessionid == users[username]['sessionid']:
                    user = users[username]

                    if president == username:
                        is_president = True

                    if parliament == username:
                        is_parliament = True

        if user:
            permissions = user.get('permissions', {'administrator': False, 'moderator': False})
        else:
            permissions = {}

        if permissions.get('administrator', False) or permissions.get('moderator', False) or is_president:
            if is_president:
                query = {'laws': laws, 'tlaws': ''}
            else:
                query = {'laws': laws}

            updateMongo = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                     action='$set', query=query)

            if updateMongo is None:
                return HttpResponse(status=500)

            response = HttpResponse(laws)

            laws_old = document.get('laws', '')

            added_lines = ''
            deleted_lines = ''
            laws_old_splitlines = laws_old.splitlines()
            laws_splitlines = laws.splitlines()

            for line in laws_splitlines:
                if line not in laws_old_splitlines:
                    added_lines = f"{added_lines}\n{line}"

            for line in laws_old_splitlines:
                if line not in laws_splitlines:
                    deleted_lines = f"{deleted_lines}\n{line}"

            if not deleted_lines and not added_lines:
                return response
            else:
                if added_lines:
                    added_lines = f"||{added_lines[1::]}||"
                if deleted_lines:
                    deleted_lines = f"||~~{deleted_lines[1::]}~~||"

                text = f"**Внесены изменения в [законы]({os.getenv('HOSTNAME', '')}freedom_of_speech/#laws) Freedom of speech:**"

                if added_lines and deleted_lines:
                    text = f"{text}\n\n{added_lines}\n\n{deleted_lines}"
                else:
                    text = f"{text}\n\n{added_lines}{deleted_lines}"

                # 4096
                # ttext = textwrap.shorten(ttext, width=300, placeholder='..', replace_whitespace=False)
                if len(text) > 4096:
                    text = f"{text[0:4093]}.."

                # publicKeyReloaded = rsa.PublicKey.load_pkcs1(os.getenv('RSA_PUBLIC_KEY', '').encode('utf8'))

                data = {
                    "text": text,
                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                }

                data = json.dumps(data)

                origin = os.getenv('HOSTNAME', '')
                # origin = rsa.encrypt(origin, publicKeyReloaded)

                tresponse = requests.post("https://telegram-bot-freed0m0fspeech.fly.dev/send/freed0m0fspeech",
                                          data=data, headers={'Origin': origin, 'Host': origin})

            return response
        else:
            if is_parliament:
                query = {'tlaws': laws}

                updateMongo = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                         action='$set', query=query)

                if updateMongo is None:
                    return HttpResponse(status=500)

                response = HttpResponse(laws)

                return response

        return HttpResponse(status=422)


class EditConstitutionPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        cockies = request.COOKIES

        if not data or not cockies:
            return HttpResponse(status=422)

        constitution = data.get('constitution', '')
        if not constitution:
            return HttpResponse(status=422)

        user = {}
        sessionid = cockies.get('sessionid', '')
        username = cockies.get('username', '')

        if 'sessionid' and 'username' in cockies:
            query = {'_id': 0, 'users': 1, 'constitution': 1}
        else:
            return HttpResponse(status=422)

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        users = document.get('users', {})
        if users.get(username, ''):
            if users[username].get('sessionid', ''):
                if sessionid == users[username]['sessionid']:
                    user = users[username]

        if user:
            permissions = user.get('permissions', {'administrator': False, 'moderator': False})
        else:
            permissions = {}

        if permissions.get('administrator', False) or permissions.get('moderator', False):
            query = {'constitution': constitution}

            updateMongo = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                     action='$set', query=query)

            if updateMongo is None:
                return HttpResponse(status=500)

            response = HttpResponse(constitution)

            constitution_old = document.get('constitution', '')

            added_lines = ''
            deleted_lines = ''
            constitution_old_splitlines = constitution_old.splitlines()
            constitution_splitlines = constitution.splitlines()

            for line in constitution_splitlines:
                if line not in constitution_old_splitlines:
                    added_lines = f"{added_lines}\n{line}"

            for line in constitution_old_splitlines:
                if line not in constitution_splitlines:
                    deleted_lines = f"{deleted_lines}\n{line}"

            if not deleted_lines and not added_lines:
                return response
            else:
                if added_lines:
                    added_lines = f"||{added_lines[1::]}||"
                if deleted_lines:
                    deleted_lines = f"||~~{deleted_lines[1::]}~~||"

                text = f"**Внесены изменения в [конституцию]({os.getenv('HOSTNAME', '')}freedom_of_speech/#constitution) Freedom of speech:**"

                if added_lines and deleted_lines:
                    text = f"{text}\n\n{added_lines}\n\n{deleted_lines}"
                else:
                    text = f"{text}\n\n{added_lines}{deleted_lines}"

                # 4096
                # ttext = textwrap.shorten(ttext, width=300, placeholder='..', replace_whitespace=False)
                if len(text) > 4096:
                    text = f"{text[0:4093]}.."

                # publicKeyReloaded = rsa.PublicKey.load_pkcs1(os.getenv('RSA_PUBLIC_KEY', '').encode('utf8'))

                data = {
                    "text": text,
                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                }

                data = json.dumps(data)

                origin = os.getenv('HOSTNAME', '')
                # origin = rsa.encrypt(origin, publicKeyReloaded)

                tresponse = requests.post("https://telegram-bot-freed0m0fspeech.fly.dev/send/freed0m0fspeech",
                                          data=data, headers={'Origin': origin, 'Host': origin})

                return response

        return HttpResponse(status=422)


class EditUsernamePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        new_username = data.get('username', '')
        # password = data.get('password', '')

        if not new_username:
            return HttpResponse(status=422)

        query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        user = {}
        if cookies:
            sessionid = cookies.get('sessionid', '')
            username = cookies.get('username', '')

            users = document.get('users', {})

            if 'sessionid' and 'username' in cookies:
                if users.get(new_username, ''):
                    return HttpResponse(status=409)  # Already registered username
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # if not users[username]['password'] == password:
                            user = users[username]

                            if username == new_username:
                                return HttpResponse(status=200)

                            if any(char in "#/@" for char in new_username):
                                return HttpResponse(status=401)
                            # else:
                            #     return HttpResponse(status=401)  # Worng credentials
        else:
            return HttpResponse(status=422)

        if user:
            if users[username]:
                # Delete old account info
                query = {f'users.{username}': ''}
                if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$unset',
                                          query=query) is None:
                    return HttpResponse(status=500)
                # Add new account info
                query = {f'users.{new_username}': users[username]}

                if username == document.get('judge', {}).get('judge', ''):
                    query['judge.judge'] = username
                if username == document.get('president', ''):
                    query['president'] = username
                if username == document.get('parliament', ''):
                    query['parliament'] = username

                if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                         action='$set', query=query) is None:
                    return HttpResponse(status=500)
            else:
                return HttpResponse(status=500)

            response = HttpResponse(status=200)

            # if 'username' in cookies:
            #     response.cookies['username'] = new_username

            expires = datetime.now(tz=utc) + timedelta(days=7)
            response.set_cookie(key='username', value=new_username, secure=True, samesite='None', expires=expires)

            return response
        else:
            return HttpResponse(status=422)


class AddTestimonialPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        testimonial = data.get('testimonial', '')
        if not testimonial:
            return HttpResponse(status=422)

        user = {}
        username = ''
        if cookies:
            sessionid = cookies.get('sessionid', '')
            username = cookies.get('username', '')

            if 'sessionid' and 'username' in cookies:
                query = {'_id': 0, 'users': 1, 'telegram': 1}

                document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                      query=query)

                if not document:
                    return HttpResponse(status=500)  # DataBase Error

                users = document.get('users', {})
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            user = users[username]

        role = 'Незнакомец'
        if user:
            # member = user.get('member', {})
            member_parameters = document.get('telegram', {}).get('members_parameters', {}).get(
                users.get(username, {}).get('telegram', {}).get('id', ''), {})
            if member_parameters:
                role = member_parameters.get('custom_title', 'Участник')

                # If user has no role in chat
                if not role:
                    role = 'Участник'
        else:
            username = 'Аноним'

        query = {'testimonials': {'text': testimonial, 'username': username, 'role': role}}

        updateMongo = mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                 action='$push', query=query)

        if updateMongo is None:
            return HttpResponse(status=500)

        return HttpResponse(status=200)


class AuthTelegramPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST
        cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        try:
            verify_telegram_authentication(bot_token=os.getenv('TELEGRAM_BOT_TOKEN', ''), request_data=data)
        except (TelegramDataIsOutdatedError, NotTelegramDataError):
            return HttpResponse(status=422)

        user = {}
        users = {}
        document = {}
        if cookies:
            sessionid = cookies.get('sessionid', '')
            username = cookies.get('username', '')

            if 'sessionid' and 'username' in cookies:
                query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'candidates': 1,
                         'telegram': 1}

                document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                      query=query)

                if not document:
                    return HttpResponse(status=500)  # DataBase Error

                users = document.get('users', {})
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            user = users[username]
        else:
            return HttpResponse(status=422)
        # data = {'id', 'first_name', 'last_name', 'username', 'photo_url', 'auth_date', 'hash'}
        if user:
            # newtusername = data.get('username', '')
            newtid = data.get('id', '')
            for tuser in users.values():
                user_telegram = tuser.get('telegram', '')
                if user_telegram:
                    tid = user_telegram.get('id', '')
                    if tid == newtid:
                        if user.get('telegram', {}).get('id', '') == tid:
                            # Unlinking telegram account
                            # Unlink rules prevent from unlink
                            if (
                                    document.get('president', '') == username or
                                    document.get('parliament', '') == username or
                                    document.get('judge', {}).get('judge', '') == username or
                                    username in document.get('candidates', {})
                            ):
                                return HttpResponse(status=409)
                            else:
                                if not user.get('discord', {}):
                                    if not user.get('password', ''):
                                        return HttpResponse(status=409)
                                    else:
                                        if any(char in "#/@" for char in username):
                                            return HttpResponse(status=409)

                                query = {f'users.{username}.telegram': '', f'referendum.votes.{username}': ''}

                                if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                              action='$unset', query=query) is None:
                                    return HttpResponse(status=500)

                                return HttpResponse(status=200)

            for user in users:
                if users.get(user, {}).get('telegram', {}).get('id', '') == newtid:
                    # Found user with telegram linked
                    return HttpResponse(status=409)

            query = {f'users.{username}.telegram': data}

            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                          query=query) is None:
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=422)

        return HttpResponse(status=200)


class ProfilePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        # access self.args, self.kwargs
        # kwargs: {'username': '01eh'}
        if not self.kwargs:
            username = ''
        else:
            username = self.kwargs.get('username', '')

        cockies = request.COOKIES

        query = {'_id': 0, 'users': 1, 'candidates': 1, 'telegram': 1, 'xp': 1, 'discord': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        if not document:
            # DataBase error
            return HttpResponse(status=500)

        users = document.get('users', '')
        telegram = document.get('telegram', {})
        discord = document.get('discord', {})
        context = {

        }
        if not cockies:
            context['authorized'] = False
        else:
            context['authorized'] = False
            sessionid = cockies.get('sessionid', '')
            if not username:
                username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                # users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True

        if username:
            if users:
                user = users.get(username, '')
                if user:
                    permissions = user.get('permissions', {'administrator': False, 'moderator': False})
                    context['administrator'] = permissions.get('administrator', False)
                    context['moderator'] = permissions.get('administrator', permissions.get('moderator', False))

                    context['username'] = username
                    # context['candidate'] = document.get('candidates', {}).get(username, {})
                    user_telegram = user.get('telegram', {})
                    user_discord = user.get('discord', {})
                    xp = 0
                    messages_count = 0
                    # members_count = 0
                    voicetime = 0
                    if user_telegram:
                        context['telegram_id'] = user_telegram.get('id', '')
                        context['telegram_username'] = user_telegram.get('username', '')
                        context['telegram_first_name'] = user_telegram.get('first_name', '')
                        context['telegram_last_name'] = user_telegram.get('last_name', '')

                        telegram_photo_url = user_telegram.get('photo_url', '')
                        # if is_url_image(telegram_photo_url):
                        context['telegram_photo_url'] = telegram_photo_url

                        context['telegram_link_status'] = True

                        member_parameters = telegram.get('members_parameters', {}).get(context.get('telegram_id', ''),
                                                                                       {})
                        if member_parameters:
                            messages_count += member_parameters.get('messages_count', 0)

                            # xp_factor = telegram.get('xp_factor', 100)  # threshold
                            xp += member_parameters.get('xp', 0)

                            # lvl, xp_have, xp_need = calculate_lvl(xp, xp_factor)

                            # context['telegram_lvl'] = lvl
                            # context['telegram_xp_have'] = xp_have
                            # context['telegram_xp_need'] = xp_need
                            # context['xp'] = member_parameters.get('xp', '')
                            voicetime += round(member_parameters.get('voicetime', 0) / 3600, 1)
                            context['telegram_role'] = member_parameters.get('custom_title', 'Участник')
                            context['telegram_position'] = member_parameters.get('position', '')
                            context['telegram_members_count'] = int(
                                telegram.get('chat_parameters', {}).get('members_count', 0))
                            context['telegram_date_updated'] = member_parameters.get('date', '')
                            context['telegram_member_status'] = True

                            if not context['telegram_role']:
                                candidate = document.get('candidates', {}).get(username, '')
                                if candidate:
                                    context['telegram_role'] = 'Кандидат'
                                else:
                                    context['telegram_role'] = 'Участник'

                            joined_date = member_parameters.get('joined_date', '')
                            if joined_date:
                                date = json.loads(joined_date, object_hook=json_util.object_hook)
                                if date:
                                    # date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                                    # context['joined_date'] = date.strftime('%b %e, %Y')
                                    # print(date.strftime('%Y-%m-%d %H:%M:%S'))
                                    context['telegram_joined_date'] = date.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        context['telegram_link_status'] = False
                        context['telegram_role'] = 'Аноним'

                    if user_discord:
                        context['discord_link_status'] = True

                        context['discord_id'] = user_discord.get('id', '')
                        context['discord_username'] = user_discord.get('username', '')
                        context['discord_global_name'] = user_discord.get('global_name', '')
                        context['discord_discriminator'] = user_discord.get('discriminator', '')
                        context['discord_public_flags'] = user_discord.get('public_flags', '')
                        context['discord_flags'] = user_discord.get('flags', '')
                        context['discord_banner'] = user_discord.get('banner', '')
                        context['discord_accent_color'] = user_discord.get('accent_color', '')
                        context['discord_avatar'] = user_discord.get('avatar', '')
                        context['discord_avatar_decoration'] = user_discord.get('avatar_decoration', '')
                        context['discord_banner_color'] = user_discord.get('banner_color', '')
                        # Multi - Factor Authentication
                        context['discord_mfa_enabled'] = user_discord.get('mfa_enabled', '')
                        context['discord_locale'] = user_discord.get('locale', '')
                        context['discord_premium_type'] = user_discord.get('premium_type', '')

                        # discord_photo_url = user_discord.get('photo_url', '')
                        # if is_url_image(telegram_photo_url):
                        # context['discord_photo_url'] = discord_photo_url

                        member_parameters = discord.get('members_parameters', {}).get(context.get('discord_id', ''), {})
                        if member_parameters:
                            messages_count += member_parameters.get('messages_count', 0)

                            # xp_factor = discord.get('xp_factor', 100)  # threshold
                            xp += member_parameters.get('xp', 0)

                            # context['xp'] += member_parameters.get('xp', '')
                            voicetime += round(member_parameters.get('voicetime', 0) / 3600, 1)
                            # context['discord_role'] = member_parameters.get('custom_title', 'Участник')
                            context['discord_position'] = member_parameters.get('position', '')
                            context['discord_members_count'] = int(
                                discord.get('guild_parameters', {}).get('member_count', 0))
                            context['discord_date_updated'] = member_parameters.get('date', '')
                            context['discord_member_status'] = True

                            joined_date = member_parameters.get('joined_at', '')
                            if joined_date:
                                date = json.loads(joined_date, object_hook=json_util.object_hook)
                                if date:
                                    # date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                                    # context['joined_date'] = date.strftime('%b %e, %Y')
                                    # print(date.strftime('%Y-%m-%d %H:%M:%S'))
                                    context['discord_joined_date'] = date.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        context['discord_link_status'] = False

                    # context['members_count'] = members_count
                    context['messages_count'] = messages_count
                    context['voicetime'] = voicetime
                    xp_factor = document.get('xp', {}).get('xp_factor', 100)  # threshold
                    lvl, xp_have, xp_need = calculate_lvl(xp, xp_factor)

                    context['lvl'] = lvl
                    context['xp_have'] = xp_have
                    context['xp_need'] = xp_need
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)

        return render(request, template_name='freedom_of_speech/profile/profile.html', context=context)

    async def post(self, request, *args, **kwargs):
        return HttpResponse(status=404)


class VotePresidentPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        cockies = request.COOKIES

        query = {'_id': 0, 'users': 1, 'votes': 1, 'candidates': 1, 'telegram': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        users = document.get('users', '')
        context = {

        }
        username = ''
        if not cockies:
            return HttpResponse(status=422)
        else:
            context['authorized'] = False
            sessionid = cockies.get('sessionid', '')
            if not username:
                username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                # users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True
            else:
                return HttpResponse(status=422)

        if context.get('authorized', False) and username:
            president = data.get('candidate', '')
        else:
            return HttpResponse(status=422)

        if president not in document.get('candidates', {}):
            # Voting for not candidate
            return HttpResponse(status=409)

        telegram_id = users.get(username, {}).get('telegram', {}).get('id', '')

        if not document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}):
            # Not member of group
            return HttpResponse(status=401)

        if not document.get('votes', {}).get('president', {}).get(username):
            if not users.get(username, {}).get('telegram', {}):
                # Users without telegram account can't vote
                return HttpResponse(status=404)

            # synch_date = users.get(username, {}).get('date', '')
            #
            # if not synch_date:
            #     # Date of synch is not known
            #     return HttpResponse(status=409)
            #
            # if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(synch_date,
            #                                                                   '%Y-%m-%d %H:%M:%S')).days >= 1:
            #     # Data synched with telegram is older than 1 day
            #     return HttpResponse(status=409)

            # Users with freedom less than 30 days can't vote
            joined_date = document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}).get(
                'joined_date', '')
            if joined_date:
                date = json.loads(joined_date, object_hook=json_util.object_hook)
                if date:
                    # timedelta in group
                    freedom = datetime.now() - date
                    if freedom.days >= 30:
                        query = {f'votes.president.{username}': president}
                        if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                      action='$set',
                                                      query=query) is None:
                            return HttpResponse(status=500)

                        response = HttpResponse(president)

                        return response
        else:
            return HttpResponse(status=403)

        return HttpResponse(status=409)


class VoteParliamentPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        cockies = request.COOKIES

        query = {'_id': 0, 'users': 1, 'votes': 1, 'candidates': 1, 'telegram': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        users = document.get('users', '')
        context = {

        }
        username = ''
        if not cockies:
            return HttpResponse(status=422)
        else:
            context['authorized'] = False
            sessionid = cockies.get('sessionid', '')
            if not username:
                username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                # users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True
            else:
                return HttpResponse(status=422)

        if context.get('authorized', False) and username:
            parliament = data.get('candidate', '')
        else:
            return HttpResponse(status=422)

        if parliament not in document.get('candidates', {}):
            # Voting for not candidate
            return HttpResponse(status=409)

        telegram_id = users.get(username, {}).get('telegram', {}).get('id', '')

        if not document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}):
            # Not member of group
            return HttpResponse(status=401)

        if not document.get('votes', {}).get('parliament', {}).get(username):
            if not users.get(username, {}).get('telegram', {}):
                # Users without telegram account can't vote
                return HttpResponse(status=404)

            # synch_date = users.get(username, {}).get('date', '')
            #
            # if not synch_date:
            #     # Date of synch is not known
            #     return HttpResponse(status=409)
            #
            # if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(synch_date,
            #                                                                   '%Y-%m-%d %H:%M:%S')).days >= 1:
            #     # Data synched with telegram is older than 1 day
            #     return HttpResponse(status=409)

            # Users with freedom less than 30 days can't vote
            joined_date = document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}).get(
                'joined_date', '')
            if joined_date:
                date = json.loads(joined_date, object_hook=json_util.object_hook)
                if date:
                    # timedelta in group
                    freedom = datetime.now() - date
                    if freedom.days >= 30:
                        query = {f'votes.parliament.{username}': parliament}
                        if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                      action='$set',
                                                      query=query) is None:
                            return HttpResponse(status=500)

                        response = HttpResponse(parliament)

                        return response
        else:
            HttpResponse(status=403)

        return HttpResponse(status=409)


class VoteJudgePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        cockies = request.COOKIES

        query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'telegram': 1, 'candidates': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        users = document.get('users', '')
        context = {

        }
        username = ''
        if not cockies:
            return HttpResponse(status=422)
        else:
            context['authorized'] = False
            sessionid = cockies.get('sessionid', '')
            if not username:
                username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                # users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True
            else:
                return HttpResponse(status=422)

        if context.get('authorized', False) and username:
            judge = data.get('candidate', '')
        else:
            return HttpResponse(status=422)

        if judge not in document.get('candidates', {}) and judge:
            # Voting for not candidate
            return HttpResponse(status=409)

        telegram_id = users.get(username, {}).get('telegram', {}).get('id', '')
        if not document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}) and judge:
            # Not member of group
            return HttpResponse(status=401)

        if judge:
            tjudge = users.get(judge, {}).get('telegram', {}).get('id', '')
            if not tjudge:
                return HttpResponse(status=404)

            if judge == document.get('president', ''):
                # President can't be judge
                return HttpResponse(status=404)
            if judge == document.get('parliament', ''):
                # Parliament can't be judge
                return HttpResponse(status=404)

        judge_info = document.get('judge', {})
        query = ''
        text = ''
        if username == document.get('president', '') and document.get('president', ''):
            role = 'president'

            if judge_info.get('parliament', '') == judge:
                # Set new judge
                query = {'judge.judge': judge, f'judge.{role}': judge, f'referendum.votes.{username}': ''}

                text = f"**Изменения [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech:\n\n**"

                if not judge:
                    # Remove Judge
                    tjudge = users.get(judge_info.get('judge', ''), {}).get('telegram', {}).get('username', '')
                    if tjudge:
                        text = f"{text}Судья [{judge_info.get('judge', '')}](tg://user?id={tjudge}) был(а) снят(а) со своего поста"

                        # Demote judge in chat
                        chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                        origin = os.getenv('HOSTNAME', '')
                        data = {
                            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                            'action': 'demote_chat_member',
                        }
                        data = json.dumps(data)
                        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                      data=data, headers={'Origin': origin, 'Host': origin})
                    else:
                        return HttpResponse(status=404)
                else:
                    # New Judge
                    tjudge = users.get(judge, {}).get('telegram', {}).get('id', '')
                    if tjudge:
                        text = f"{text}Новый Судья: [{judge}](tg://user?id={tjudge})"

                        # Promote new judge (tjudge)
                        chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                        origin = os.getenv('HOSTNAME', '')
                        data = {
                            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                            'action': 'promote_chat_member',
                            'parameters': {'custom_title': 'Cудья'},
                        }
                        data = json.dumps(data)
                        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                      data=data, headers={'Origin': origin, 'Host': origin})

                        ojudge = judge_info.get('judge', '')
                        if ojudge:
                            tojudge = users.get(ojudge, {}).get('telegram', {}).get('id', '')
                            # Demote old judge
                            chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                            origin = os.getenv('HOSTNAME', '')
                            data = {
                                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                'action': 'demote_chat_member',
                            }
                            data = json.dumps(data)
                            requests.post(
                                f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tojudge}",
                                data=data, headers={'Origin': origin, 'Host': origin})
                    else:
                        return HttpResponse(status=404)
        else:
            if username == document.get('parliament', '') and document.get('parliament', ''):
                role = 'parliament'

                if judge_info.get('president', '') == judge:
                    # Set new judge
                    query = {'judge.judge': judge, f'judge.{role}': judge, f'referendum.votes.{username}': ''}

                    text = f"**Изменения [Правительства]({os.getenv('HOSTNAME', '')}freedom_of_speech/#government) Freedom of speech:\n\n**"

                    if not judge:
                        # Remove Judge
                        tjudge = users.get(judge_info.get('judge', ''), {}).get('telegram', {}).get('id', '')
                        if tjudge:
                            text = f"{text}Судья [{judge_info.get('judge', '')}](tg://user?id={tjudge}) был(а) снят(а) со своего поста"

                            chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                            origin = os.getenv('HOSTNAME', '')
                            data = {
                                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                'action': 'demote_chat_member',
                            }
                            data = json.dumps(data)
                            requests.post(
                                f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                data=data, headers={'Origin': origin, 'Host': origin})
                        else:
                            return HttpResponse(status=404)
                    else:
                        # New Judge
                        tjudge = users.get(judge, {}).get('telegram', {}).get('id', '')
                        if tjudge:
                            text = f"{text}Новый Судья: [{judge}](t.me/{tjudge})"

                            # Promote new judge (tjudge)
                            chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                            origin = os.getenv('HOSTNAME', '')
                            data = {
                                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                'action': 'promote_chat_member',
                                'parameters': {'custom_title': 'Cудья'},
                            }
                            data = json.dumps(data)
                            requests.post(
                                f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                data=data, headers={'Origin': origin, 'Host': origin})

                            ojudge = judge_info.get('judge', '')
                            if ojudge:
                                tojudge = users.get(ojudge, {}).get('telegram', {}).get('id', '')
                                # Demote old judge
                                chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username',
                                                                                                            '')
                                origin = os.getenv('HOSTNAME', '')
                                data = {
                                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                    'action': 'demote_chat_member',
                                }
                                data = json.dumps(data)
                                requests.post(
                                    f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tojudge}",
                                    data=data, headers={'Origin': origin, 'Host': origin})
                        else:
                            return HttpResponse(status=404)
            else:
                return HttpResponse(status=422)

        if judge_info.get('judge', '') == judge:
            query = {f'judge.{role}': judge}

            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                          query=query) is None:
                return HttpResponse(status=500)

            response = HttpResponse(judge)

            return response
        else:
            if not query:
                query = {f'judge.{role}': judge}
            else:
                chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                origin = os.getenv('HOSTNAME', '')
                data = {
                    "text": text,
                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                }

                data = json.dumps(data)

                requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat_username}", data=data,
                              headers={'Origin': origin, 'Host': origin})

            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                          query=query) is None:
                return HttpResponse(status=500)

            response = HttpResponse(judge)

            return response


class VoteCandidatePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        cockies = request.COOKIES

        query = {'_id': 0, 'users': 1, 'votes': 1, 'end_vote': 1, 'telegram': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        users = document.get('users', {})
        context = {

        }
        username = ''
        if not cockies:
            return HttpResponse(status=422)
        else:
            context['authorized'] = False
            sessionid = cockies.get('sessionid', '')
            if not username:
                username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                # users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True
            else:
                return HttpResponse(status=422)

        if context.get('authorized', False) and username:
            role = data.get('role', '')
        else:
            return HttpResponse(status=422)

        if not users.get(username, {}).get('telegram', {}):
            # Users without telegram account can't stand
            return HttpResponse(status=404)

        telegram_id = users.get(username, {}).get('telegram', {}).get('id', '')
        if not document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}):
            # Not member of group
            return HttpResponse(status=401)

        if document.get('end_vote', ''):
            # Cannot stand during vote
            return HttpResponse(status=409)

        # Users with freedom less than 30 days can't stand
        joined_date = document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}).get('joined_date',
                                                                                                          '')
        if joined_date:
            date = json.loads(joined_date, object_hook=json_util.object_hook)
            if date:
                # timedelta in group
                freedom = datetime.now() - date
                if freedom.days >= 30:
                    if role == 'president':
                        query = {f'candidates.{username}': 'president'}
                        if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                      action='$set',
                                                      query=query) is None:
                            return HttpResponse(status=500)
                    else:
                        if role == 'parliament':
                            query = {f'candidates.{username}': 'parliament'}
                            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                          action='$set',
                                                          query=query) is None:
                                return HttpResponse(status=500)
                        else:
                            if role == 'judge':
                                query = {f'candidates.{username}': 'judge'}
                                if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                              action='$set',
                                                              query=query) is None:
                                    return HttpResponse(status=500)
                            else:
                                query = {f'candidates.{username}': ''}
                                if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                              action='$unset', query=query) is None:
                                    return HttpResponse(status=500)

                    response = HttpResponse(role)
                    return response

        return HttpResponse(status=409)


class VoteReferendumPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        cockies = request.COOKIES

        query = {'_id': 0, 'users': 1, 'end_vote': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'telegram': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        users = document.get('users', {})
        context = {

        }
        username = ''
        if not cockies:
            return HttpResponse(status=422)
        else:
            context['authorized'] = False
            sessionid = cockies.get('sessionid', '')
            if not username:
                username = cockies.get('username', '')

            if 'sessionid' and 'username' in cockies:
                # users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True
            else:
                return HttpResponse(status=422)

        if not context.get('authorized', False) and username:
            return HttpResponse(status=422)

        if document.get('end_vote', ''):
            # Cannot vote for referendum during vote
            return HttpResponse(status=409)

        president = document.get('president', '')
        parliament = document.get('parliament', '')
        judge = document.get('judge', {}).get('judge', '')

        if president == username:
            # President can't vote for referendum
            return HttpResponse(status=409)

        if parliament == username:
            # Parliament can't vote for referendum
            return HttpResponse(status=409)

        if judge == username:
            # Judge can't vote for referendum
            return HttpResponse(status=409)

        telegram_id = users.get(username, {}).get('telegram', {}).get('id', '')
        if not document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}):
            # Not member of group
            return HttpResponse(status=409)

        # synch_date = users.get(username, {}).get('date', '')
        #
        # if not synch_date:
        #     # Date of synch is not known
        #     return HttpResponse(status=409)
        #
        # if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(synch_date,'%Y-%m-%d %H:%M:%S')).days >= 1:
        #     # Data synched with telegram is older than 1 day
        #     return HttpResponse(status=409)

        opinion = data.get('opinion', False)

        if opinion == 'true':
            opinion = True
        else:
            opinion = False

        query = {f'referendum.votes.{username}': opinion}
        if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                      query=query) is None:
            return HttpResponse(status=500)

        return HttpResponse(opinion)


class UpdateChatPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        query = {'_id': 0, 'telegram': 1, 'discord': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return

        last_update_telegram = document.get('telegram', {}).get('chat_parameters', {}).get('date', '')
        last_update_discord = document.get('discord', {}).get('guild_parameters', {}).get('date', '')

        if last_update_telegram:
            # update only every 30 minutes
            if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update_telegram,
                                                                              '%Y-%m-%d %H:%M:%S')).seconds >= 1800:
                chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
                data = {
                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                }
                data = json.dumps(data)
                origin = os.getenv('HOSTNAME', '')
                chat = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/chat/{chat_username}", data=data,
                                    headers={'Origin': origin, 'Host': origin})

                if chat and chat.status_code == 200:
                    chat = chat.json()

                    query = {'telegram.chat_parameters': chat.get('chat_parameters', {}),
                             'telegram.members_parameters': chat.get('members_parameters', {})}
                    if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                  action='$set', query=query) is None:
                        return HttpResponse(status=500)
                else:
                    return HttpResponse(status=422)

        if last_update_discord:
            # update only every 30 minutes
            if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update_discord,
                                                                              '%Y-%m-%d %H:%M:%S')).seconds >= 1800:
                guild_id = document.get('discord', {}).get('guild_parameters', {}).get('id', '')
                data = {
                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                }
                data = json.dumps(data)
                origin = os.getenv('HOSTNAME', '')
                guild = requests.get(f"https://discord-bot-freed0m0fspeech.fly.dev/guild/{guild_id}", data=data,
                                     headers={'Origin': origin, 'Host': origin})

                if guild and guild.status_code == 200:
                    guild = guild.json()

                    query = {'discord.guild_parameters': guild.get('guild_parameters', {}),
                             'discord.members_parameters': guild.get('members_parameters', {})}
                    if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                  action='$set', query=query) is None:
                        return HttpResponse(status=500)
                else:
                    return HttpResponse(status=422)

        return HttpResponse(status=200)


# class UpdateMemberPageView(TemplateView):
#     async def get(self, request, *args, **kwargs):
#         return HttpResponse(status=404)
#
#     async def post(self, request, *args, **kwargs):
#         data = request.POST
#
#         if not data:
#             return HttpResponse(status=422)
#
#         username = data.get('username', '')
#
#         if not username:
#             # No username to update member info
#             return HttpResponse(status=422)
#
#         query = {'_id': 0, 'users': 1, 'telegram': 1}
#         document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)
#
#         user = document.get('users', {}).get(username, {})
#         telegram_id = user.get('telegram', {}).get('id', '')
#
#         last_update_chat = document.get('telegram', {}).get('chat_parameters', {}).get('date', '')
#         last_update = document.get('telegram', {}).get('members_parameters', {}).get(telegram_id, {}).get('date',
#                                                                                                           last_update_chat)
#
#         if last_update:
#             # update only every 30 minutes
#             if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update,
#                                                                               '%Y-%m-%d %H:%M:%S')).seconds < 1800:
#                 # Too many requests
#                 return HttpResponse(status=429)
#         else:
#             return HttpResponse(status=422)
#
#         telegram_id = user.get('telegram', {}).get('id', '')
#
#         if not telegram_id:
#             # No telegram username to update member info
#             return HttpResponse(status=422)
#
#         chat_username = document.get('telegram', {}).get('chat_parameters', {}).get('username', '')
#         data = {
#             'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
#         }
#         data = json.dumps(data)
#         origin = os.getenv('HOSTNAME', '')
#
#         telegram_member = requests.get(
#             f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat_username}/{telegram_id}",
#             data=data, headers={'Origin': origin, 'Host': origin})
#
#         if telegram_member and telegram_member.status_code == 200:
#             telegram_member = telegram_member.json()
#
#             query = {}
#             for member_parameter in telegram_member:
#                 query[f'telegram.members_parameters.{telegram_id}.{member_parameter}'] = telegram_member.get(member_parameter, '')
#
#             if query:
#                 if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
#                                               action='$set', query=query) is None:
#                     return HttpResponse(status=500)
#
#             return HttpResponse()
#         else:
#             if telegram_member.status_code == 422:
#                 # if not member or not user or not chat:
#                 #     return Response(status=422)
#
#                 # date = datetime.now(tz=utc)
#                 # date = date.strftime('%Y-%m-%d %H:%M:%S')
#
#                 query = {f'telegram.members_parameters.{telegram_id}': '', f'referendum.votes.{username}': ''}
#                 if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
#                                               action='$unset', query=query) is None:
#                     return HttpResponse(status=500)
#             else:
#                 return HttpResponse(status=telegram_member.status_code)
#
#             return HttpResponse(status=200)


class MembersPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        # cockies = request.COOKIES

        context = {

        }

        query = {'_id': 0, 'users': 1, 'telegram': 1, 'xp': 1, 'discord': 1}

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        members = []

        telegram_members_parameters = document.get('telegram', {}).get('members_parameters', {})
        discord_members_parameters = document.get('discord', {}).get('members_parameters', {})
        xp_factor = document.get('xp', {}).get('xp_factor', 100)  # threshold

        for username, user_parameters in document.get('users', {}).items():
            telegram_member_parameters = telegram_members_parameters.get(
                user_parameters.get('telegram', {}).get('id', ''), {})
            xp = 0
            voicetime = 0
            messages_count = 0

            if telegram_member_parameters:
                xp += telegram_member_parameters.get('xp', 0)
                voicetime += round(telegram_member_parameters.get('voicetime', 0) / 3600, 1)
                messages_count += telegram_member_parameters.get('messages_count', 0)

            discord_member_parameters = discord_members_parameters.get(user_parameters.get('discord', {}).get('id', ''),
                                                                       {})
            if discord_members_parameters:
                xp += discord_member_parameters.get('xp', 0)
                voicetime += round(discord_member_parameters.get('voicetime', 0) / 3600, 1)
                messages_count += discord_member_parameters.get('messages_count', 0)

            lvl, xp_have, xp_need = calculate_lvl(xp, xp_factor)

            parameters = {}
            parameters['lvl'] = lvl
            parameters['xp_have'] = xp_have
            parameters['xp_need'] = xp_need
            parameters['voicetime'] = voicetime
            parameters['messages_count'] = messages_count

            # position = member_parameters.get('position', float('inf'))
            # if not is_url_image(user_parameters.get('telegram', {}).get('photo_url')):
            #     user_parameters['telegram']['photo_url'] = ''

            member = (username, xp, parameters, user_parameters.get('telegram', {}), user_parameters.get('discord', {}))
            members.append(member)

        # Sort members by xp
        # If you just need a number that's bigger than all others, you can use float('inf')
        # in similar fashion, a number smaller than all others float('-inf')

        # x[1].get('position', float('inf'))
        members.sort(reverse=True, key=lambda x: x[1])

        # Max 100 members
        context['members'] = members[:100]
        # Slice dict
        # dict_name = dict(list(dict_name.items())[:100])

        # for member in members:
        #     print(member[0])

        response = render(request=request, template_name='freedom_of_speech/members/members.html', context=context)

        return response


class TelegramMembersPageView(TemplateView):
    # async def get(self, request, *args, **kwargs):
    #     return HttpResponse(status=404)

    async def get(self, request, *args, **kwargs):
        # cockies = request.COOKIES

        context = {

        }

        query = {'_id': 0, 'users': 1, 'telegram': 1, 'xp': 1}

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        members = []

        telegram_members_parameters = document.get('telegram', {}).get('members_parameters', {})
        xp_factor = document.get('xp', {}).get('xp_factor', 100)  # threshold

        for username, user_parameters in document.get('users', {}).items():
            telegram_member_parameters = telegram_members_parameters.get(
                user_parameters.get('telegram', {}).get('id', ''), {})

            if telegram_member_parameters:
                xp = telegram_member_parameters.get('xp', 0)
                lvl, xp_have, xp_need = calculate_lvl(xp, xp_factor)

                parameters = {}
                parameters['lvl'] = lvl
                parameters['xp_have'] = xp_have
                parameters['xp_need'] = xp_need
                parameters['voicetime'] = round(telegram_member_parameters.get('voicetime', 0) / 3600, 1)
                parameters['messages_count'] = telegram_member_parameters.get('messages_count', 0)

                position = telegram_member_parameters.get('position', float('inf'))
                member = (username, position, parameters, user_parameters.get('telegram', {}))
                members.append(member)

        members.sort(reverse=False, key=lambda x: x[1])

        # Max 100 members
        context['members'] = members[:100]

        response = render(request=request, template_name='freedom_of_speech/members/telegram.html', context=context)

        return response


class DiscordMembersPageView(TemplateView):
    # async def get(self, request, *args, **kwargs):
    #     return HttpResponse(status=404)

    async def get(self, request, *args, **kwargs):
        # cockies = request.COOKIES

        context = {

        }

        query = {'_id': 0, 'users': 1, 'discord': 1, 'xp': 1}

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        if not document:
            return HttpResponse(status=500)

        members = []

        discord_members_parameters = document.get('discord', {}).get('members_parameters', {})
        xp_factor = document.get('xp', {}).get('xp_factor', 100)  # threshold

        for username, user_parameters in document.get('users', {}).items():
            discord_member_parameters = discord_members_parameters.get(user_parameters.get('discord', {}).get('id', ''),
                                                                       {})

            if discord_member_parameters:
                xp = discord_member_parameters.get('xp', 0)
                lvl, xp_have, xp_need = calculate_lvl(xp, xp_factor)

                parameters = {}
                parameters['lvl'] = lvl
                parameters['xp_have'] = xp_have
                parameters['xp_need'] = xp_need
                parameters['voicetime'] = round(discord_member_parameters.get('voicetime', 0) / 3600, 1)
                parameters['messages_count'] = discord_member_parameters.get('messages_count', 0)

                position = discord_member_parameters.get('position', float('inf'))
                member = (username, position, parameters, user_parameters.get('discord', {}))
                members.append(member)

        members.sort(reverse=True, key=lambda x: x[1])

        # Max 100 members
        context['members'] = members[:100]

        response = render(request=request, template_name='freedom_of_speech/members/discord.html', context=context)

        return response


class AuthDiscordPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')

        if not code:
            return HttpResponse(status=422)

        redirect_uri = f"{os.getenv('HOSTNAME')}freedom_of_speech/auth/discord/"
        data = exchange_code(code, redirect_uri)

        # data = request.POST
        cookies = request.COOKIES

        if not data:
            return HttpResponse(status=422)

        user = {}
        users = {}
        document = {}
        if cookies:
            sessionid = cookies.get('sessionid', '')
            username = cookies.get('username', '')

            if 'sessionid' and 'username' in cookies:
                query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'candidates': 1,
                         'telegram': 1, 'discord': 1}

                document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                      query=query)

                if not document:
                    return HttpResponse(status=500)  # DataBase Error

                users = document.get('users', {})
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            user = users[username]
        else:
            return HttpResponse(status=422)

        if user:
            newdid = data.get('id', '')
            for tuser in users.values():
                discord = tuser.get('discord', '')
                if discord:
                    did = discord.get('id', '')
                    if did == newdid:
                        if user.get('discord', {}).get('id', '') == did:
                            # Unlinking discord account
                            # Unlink rules prevent from unlink
                            if (
                                    document.get('president', '') == username or
                                    document.get('parliament', '') == username or
                                    document.get('judge', {}).get('judge', '') == username or
                                    username in document.get('candidates', {})
                            ):
                                return HttpResponse(status=409)
                            else:
                                if not user.get('telegram', {}):
                                    if not user.get('password', ''):
                                        return HttpResponse(status=409)
                                    else:
                                        if any(char in "#/@" for char in username):
                                            return HttpResponse(status=409)

                                query = {f'users.{username}.discord': ''}

                                if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                              action='$unset', query=query) is None:
                                    return HttpResponse(status=500)

                                return render(request=request, template_name='freedom_of_speech/popup_success.html',
                                              context={})
            for user in users:
                if users.get(user, {}).get('discord', {}).get('id', '') == newdid:
                    # Found user with discord linked
                    return HttpResponse(status=409)

            query = {f'users.{username}.discord': data}

            if mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                          query=query) is None:
                return HttpResponse(status=500)

        return render(request=request, template_name='freedom_of_speech/popup_success.html', context={})
