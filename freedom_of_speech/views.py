import asyncio
import datetime
import json
import os
import random
import secrets
import rsa
import requests
# import uuid
# import OpenSSL

from math import sqrt

from apscheduler.jobstores.base import JobLookupError
from bson import json_util
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from dotenv import load_dotenv
from pytz import utc

from .forms import HomeForm
from django.contrib.auth.models import User
from utils import mongoDataBase
from .utils import *
from datetime import datetime, timedelta
from django_telegram_login.authentication import (
    verify_telegram_authentication
)
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)
from pymongo import (
    errors,
    ReturnDocument
)


class HomePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        cockies = request.COOKIES

        context = {

        }

        query = {'_id': 0, 'constitution': 1, 'laws': 1, 'tlaws': 1, 'users': 1, 'testimonials': 1, 'president': 1,
                 'parliament': 1, 'judge': 1, 'start_vote': 1, 'end_vote': 1, 'chat': 1, 'candidates': 1, 'votes': 1,
                 'referendum': 1}

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

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

        # testimonials_html = ""
        # for testimonial in testimonials:
        #     testimonial_text = testimonial.get('text', '')
        #     testimonial_username = testimonial.get('username', '')
        #     testimonial_role = testimonial.get('role', '')
        #
        #     div = "<div class='testimonial__content swiper-slide'>"
        #     p = "<p class='testimonial__description'>"
        #     # Testimonial
        #     p_end = "</p>"
        #     h3 = "<div><h3 class='testimonial__name'>"
        #     # Username
        #     h3_end = "</h3>"
        #     span = "<span class='testimonial__subtitle'>"
        #     # Role
        #     span_end = "</span></div>"
        #     div_end = "</div>"
        #
        #     testimonials_html += f"{div}{p}\"{testimonial_text}\"{p_end}{h3}{testimonial_username}{h3_end}{span}" \
        #                          f"{testimonial_role}{span_end}{div_end}"

        if user:
            permissions = user.get('permissions', {'administrator': False, 'moderator': False})
        else:
            permissions = {}

        chat = document.get('chat', {})
        members_count = ''

        if chat:
            chat_parameters = chat.get('chat_parameters', '')
            if chat_parameters:
                members_count = chat_parameters.get('members_count', '')

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
        context['members_count'] = members_count
        context['date_updated'] = document.get('chat', {}).get('date', '')
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

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

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

        query = {'_id': 0, 'users': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

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
        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                   query=query, upsert=False)

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

        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')

        if not old_password or not new_password:
            return HttpResponse(status=422)

        if old_password == new_password:
            return HttpResponse(status=401)

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
                            if users[username]['password'] == old_password:
                                user = users[username]
                            else:
                                return HttpResponse(status=401)
        else:
            return HttpResponse(status=422)

        if user:
            query = {f'users.{username}.password': new_password}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

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

        parliament = document.get('parliament')
        president = document.get('president')

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

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

            response = HttpResponse(laws)

            url = "https://telegram-bot-freed0m0fspeech.fly.dev/send/freed0m0fspeech"

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

                tresponse = requests.post(url, data=data, headers={'Origin': origin})

            return response
        else:
            if is_parliament:
                query = {'tlaws': laws}

                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                           query=query)

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

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

            response = HttpResponse(constitution)

            url = "https://telegram-bot-freed0m0fspeech.fly.dev/send/freed0m0fspeech"

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

                tresponse = requests.post(url, data=data, headers={'Origin': origin})

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
        password = data.get('password', '')

        if not new_username or not password:
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
                            if users[username]['password'] == password:
                                user = users[username]

                                if username == new_username:
                                    return HttpResponse(status=200)
                            else:
                                return HttpResponse(status=401)  # Worng credentials
        else:
            return HttpResponse(status=422)

        if user:
            if users[username]:
                # Delete old account info
                query = {f'users.{username}': ''}
                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$unset',
                                           query=query)
                # Add new account info
                query = {f'users.{new_username}': users[username]}

                if username == document.get('judge', {}).get('judge', ''):
                    query['judge.judge'] = username
                if username == document.get('president', ''):
                    query['president'] = username
                if username == document.get('parliament', ''):
                    query['parliament'] = username

                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                           query=query)
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
                query = {'_id': 0, 'users': 1}

                document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                      query=query)

                users = document.get('users', {})
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            user = users[username]

        role = 'Незнакомец'
        if user:
            member = user.get('member', {})
            if member:
                member_parameters = member.get('member_parameters', {})
                if member_parameters:
                    role = member_parameters.get('custom_title', 'Участник')

                    # If user has no role in chat
                    if not role:
                        role = 'Участник'
        else:
            username = 'Аноним'

        query = {'testimonials': {'text': testimonial, 'username': username, 'role': role}}

        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$push',
                                   query=query)

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
                query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'candidates': 1, 'chat': 1}

                document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                                      query=query)

                users = document.get('users', {})
                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            user = users[username]
        else:
            return HttpResponse(status=422)
        # data = {'id', 'first_name', 'last_name', 'username', 'photo_url', 'auth_date', 'hash'}
        role = ''
        if user:
            newtusername = data.get('username', '')
            for tuser in users.values():
                telegram = tuser.get('telegram', '')
                if telegram:
                    tusername = telegram.get('username', '')
                    if tusername == newtusername:
                        if user.get('telegram', {}).get('username', '') == tusername:
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
                                query = {f'users.{username}.telegram': '', f'users.{username}.member': '',
                                         f'users.{username}.date': '', f'referendum.votes.{username}': ''}

                                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                           action='$unset', query=query)

                                return HttpResponse(status=200)

            query = {f'users.{username}.telegram.first_name': data.get('first_name', ''),
                     f'users.{username}.telegram.last_name': data.get('last_name', ''),
                     f'users.{username}.telegram.photo_url': data.get('photo_url', ''),
                     f'users.{username}.telegram.username': data.get('username', '')}

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

            chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')

            # publicKeyReloaded = rsa.PublicKey.load_pkcs1(os.getenv('RSA_PUBLIC_KEY', '').encode('utf8'))

            data = {
                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
            }

            data = json.dumps(data)

            origin = os.getenv('HOSTNAME', '')
            # origin = rsa.encrypt(origin, publicKeyReloaded)

            member = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat_username}/{newtusername}",
                                  data=data, headers={'Origin': origin})
            if member and member.status_code == 200:
                member = member.json()

                query = {f'users.{username}.member': member}
                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                           action='$set', query=query)

                # member_parameters = member.get('member_parameters', {})
                # if member_parameters:
                #     role = member_parameters.get('custom_title', '')
                #     if role:
                #         role = role.lower()
                #
                #         if role == 'судья':
                #             if document.get('judge', {}).get('judge', '') != username:
                #                 query = {f"judge.judge": username, f'referendum.votes.{username}': ''}
                #                 mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                #                                            action='$set', query=query)
                #
                #         if role == 'президент':
                #             if document.get('president', '') != username:
                #                 query = {f"president": username, f'referendum.votes.{username}': ''}
                #                 mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                #                                            action='$set', query=query)
                            # users = document.get('users', '')
                            # if users:
                            #     old_username = document.get('president', '')
                            #
                            #     if old_username:
                            #         if old_username == username:
                            #             return HttpResponse(status=200)
                            #
                            #         query = {f"president": username, f'users.{username}.permissions.moderator': True,
                            #                  f'users.{old_username}.permissions.moderator': False}
                            #     else:
                            #         query = {f"president": username, f'users.{username}.permissions.moderator': True}
                            #
                            #     mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                            #                                action='$set', query=query)

                        # if role == 'парламент':
                        #     if document.get('parliament', '') != username:
                        #         query = {f"parliament": username, f'referendum.votes.{username}': ''}
                        #         mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                        #                                    action='$set', query=query)
                            # users = document.get('users', '')
                            # if users:
                            #     old_username = document.get('parliament', '')
                            #
                            #     if old_username:
                            #         if old_username == username:
                            #             return HttpResponse(status=200)
                            #
                            #         query = {f"parliament": username, f'users.{username}.permissions.moderator': True,
                            #                  f'users.{old_username}.permissions.moderator': False}
                            #     else:
                            #         query = {f"parliament": username, f'users.{username}.permissions.moderator': True}
                            #
                            #     mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                            #                                action='$set', query=query)
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

        query = {'_id': 0, 'users': 1, 'candidates': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech',
                                              query=query)

        users = document.get('users', '')
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
                    telegram = user.get('telegram', '')
                    if telegram:
                        telegram_username = telegram.get('username', '')
                        context['telegram_username'] = telegram_username
                        context['telegram_first_name'] = telegram.get('first_name', '')
                        context['telegram_last_name'] = telegram.get('last_name', '')

                        telegram_photo_url = telegram.get('photo_url', '')
                        if is_url_image(telegram_photo_url):
                            context['telegram_photo_url'] = telegram_photo_url

                        context['telegram_link_status'] = True

                        member = user.get('member', {})
                        if member:
                            member_parameters = member.get('member_parameters', '')
                            context['messages_count'] = member.get('messages_count', '')
                            context['lvl'] = member.get('lvl', '')
                            context['xp_have'] = member.get('xp_have', '')
                            context['xp_need'] = member.get('xp_need', '')
                            context['hours_in_voice_channel'] = member.get('hours_in_voice_channel', '')
                            context['member_status'] = True
                            if member_parameters:
                                context['role'] = member_parameters.get('custom_title', 'Участник')
                                if not context['role']:
                                    candidate = document.get('candidates', {}).get(username, '')
                                    if candidate:
                                        context['role'] = 'Кандидат'
                                    else:
                                        context['role'] = 'Участник'

                                joined_date = member_parameters.get('joined_date', '')
                                if joined_date:
                                    date = json.loads(joined_date, object_hook=json_util.object_hook)
                                    if date:
                                        # date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                                        # context['joined_date'] = date.strftime('%b %e, %Y')
                                        # print(date.strftime('%Y-%m-%d %H:%M:%S'))
                                        context['joined_date'] = date.strftime('%Y-%m-%d %H:%M:%S')

                        context['date_updated'] = user.get('date', '')
                    else:
                        context['telegram_link_status'] = False
                        context['role'] = 'Аноним'
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)

        return render(request, template_name='freedom_of_speech/profile.html', context=context)

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

        query = {'_id': 0, 'users': 1, 'votes': 1, 'candidates': 1}
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

        if not users.get(username, {}).get('member', {}):
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
            joined_date = users.get(username, {}).get('member', {}).get('member_parameters', {}).get('joined_date', '')
            if joined_date:
                date = json.loads(joined_date, object_hook=json_util.object_hook)
                if date:
                    # timedelta in group
                    freedom = datetime.now() - date
                    if freedom.days >= 30:
                        query = {f'votes.president.{username}': president}
                        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                   action='$set',
                                                   query=query)

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

        query = {'_id': 0, 'users': 1, 'votes': 1, 'candidates': 1}
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

        if not users.get(username, {}).get('member', {}):
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
            joined_date = users.get(username, {}).get('member', {}).get('member_parameters', {}).get('joined_date', '')
            if joined_date:
                date = json.loads(joined_date, object_hook=json_util.object_hook)
                if date:
                    # timedelta in group
                    freedom = datetime.now() - date
                    if freedom.days >= 30:
                        query = {f'votes.parliament.{username}': parliament}
                        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                   action='$set',
                                                   query=query)

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

        query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1, 'chat': 1, 'candidates': 1}
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

        if not users.get(judge, {}).get('member', {}) and judge:
            # Not member of group
            return HttpResponse(status=401)

        if judge:
            tjudge = users.get(judge, {}).get('telegram', {}).get('username', '')
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
                        text = f"{text}Судья [{judge_info.get('judge', '')}](t.me/{tjudge}) был(а) снят(а) со своего поста"

                        # Demote judge in chat
                        chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                        origin = os.getenv('HOSTNAME', '')
                        data = {
                            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                            'action': 'demote_chat_member',
                        }
                        data = json.dumps(data)
                        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                      data=data, headers={'Origin': origin})
                    else:
                        return HttpResponse(status=404)
                else:
                    # New Judge
                    tjudge = users.get(judge, {}).get('telegram', {}).get('username', '')
                    if tjudge:
                        text = f"{text}Новый Судья: [{judge}](t.me/{tjudge})"

                        # Promote new judge (tjudge)
                        chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                        origin = os.getenv('HOSTNAME', '')
                        data = {
                            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                            'action': 'promote_chat_member',
                            'parameters': {'custom_title': 'Cудья'},
                        }
                        data = json.dumps(data)
                        requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                      data=data, headers={'Origin': origin})

                        ojudge = judge_info.get('judge', '')
                        if ojudge:
                            # Demote old judge
                            chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                            origin = os.getenv('HOSTNAME', '')
                            data = {
                                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                'action': 'demote_chat_member',
                            }
                            data = json.dumps(data)
                            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{ojudge}",
                                          data=data, headers={'Origin': origin})
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
                        tjudge = users.get(judge_info.get('judge', ''), {}).get('telegram', {}).get('username', '')
                        if tjudge:
                            text = f"{text}Судья [{judge_info.get('judge', '')}](t.me/{tjudge}) был(а) снят(а) со своего поста"

                            chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                            origin = os.getenv('HOSTNAME', '')
                            data = {
                                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                'action': 'demote_chat_member',
                            }
                            data = json.dumps(data)
                            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                          data=data, headers={'Origin': origin})
                        else:
                            return HttpResponse(status=404)
                    else:
                        # New Judge
                        tjudge = users.get(judge, {}).get('telegram', {}).get('username', '')
                        if tjudge:
                            text = f"{text}Новый Судья: [{judge}](t.me/{tjudge})"

                            # Promote new judge (tjudge)
                            chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                            origin = os.getenv('HOSTNAME', '')
                            data = {
                                'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                'action': 'promote_chat_member',
                                'parameters': {'custom_title': 'Cудья'},
                            }
                            data = json.dumps(data)
                            requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{tjudge}",
                                          data=data, headers={'Origin': origin})

                            ojudge = judge_info.get('judge', '')
                            if ojudge:
                                # Demote old judge
                                chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                                origin = os.getenv('HOSTNAME', '')
                                data = {
                                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                                    'action': 'demote_chat_member',
                                }
                                data = json.dumps(data)
                                requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/manage/{chat_username}/{ojudge}",
                                              data=data, headers={'Origin': origin})
                        else:
                            return HttpResponse(status=404)
            else:
                return HttpResponse(status=422)

        if judge_info.get('judge', '') == judge:
            query = {f'judge.{role}': judge}

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

            response = HttpResponse(judge)

            return response
        else:
            if not query:
                query = {f'judge.{role}': judge}
            else:
                chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
                origin = os.getenv('HOSTNAME', '')
                data = {
                    "text": text,
                    'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
                }

                data = json.dumps(data)

                requests.post(f"https://telegram-bot-freed0m0fspeech.fly.dev/send/{chat_username}", data=data,
                              headers={'Origin': origin})

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

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

        query = {'_id': 0, 'users': 1, 'votes': 1, 'end_vote': 1}
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

        if not users.get(username, {}).get('member', {}):
            # Not member of group
            return HttpResponse(status=401)

        if document.get('end_vote', ''):
            # Cannot stand during vote
            return HttpResponse(status=409)

        # Users with freedom less than 30 days can't stand
        joined_date = users.get(username, {}).get('member', {}).get('member_parameters', {}).get('joined_date', '')
        if joined_date:
            date = json.loads(joined_date, object_hook=json_util.object_hook)
            if date:
                # timedelta in group
                freedom = datetime.now() - date
                if freedom.days >= 30:
                    if role == 'president':
                        query = {f'candidates.{username}': 'president'}
                        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                                   query=query)
                    else:
                        if role == 'parliament':
                            query = {f'candidates.{username}': 'parliament'}
                            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                                       query=query)
                        else:
                            if role == 'judge':
                                query = {f'candidates.{username}': 'judge'}
                                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                                           query=query)
                            else:
                                query = {f'candidates.{username}': ''}
                                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                           action='$unset', query=query)

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

        query = {'_id': 0, 'users': 1, 'end_vote': 1, 'president': 1, 'parliament': 1, 'judge': 1}
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

        if not users.get(username, {}).get('member', {}):
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
        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                   query=query)

        return HttpResponse(opinion)

class UpdateChatPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        query = {'_id': 0, 'chat': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        last_update = document.get('chat', {}).get('date', '')

        if last_update:
            # update only every 30 minutes
            if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')).seconds < 1800:
                # Too many requests
                return HttpResponse(status=429)
        else:
            return HttpResponse(status=422)

        chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }
        data = json.dumps(data)
        origin = os.getenv('HOSTNAME', '')
        chat = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/chat/{chat_username}", data=data,
                            headers={'Origin': origin})

        if chat and chat.status_code == 200:
            chat = chat.json()

            date = datetime.now(tz=utc)
            date = date.strftime('%Y-%m-%d %H:%M:%S')

            query = {'chat.chat_parameters': chat.get('chat_parameters', {}), 'chat.date': date}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                       action='$set', query=query)

            return HttpResponse()
        else:
            return HttpResponse(status=422)


class UpdateMemberPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        username = data.get('username', '')

        if not username:
            # No username to update member info
            return HttpResponse(status=422)

        query = {'_id': 0, 'users': 1, 'chat': 1}
        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        user = document.get('users', {}).get(username, {})

        last_update = user.get('date', '')

        if last_update:
            # update only every 30 minutes
            if (datetime.now(tz=utc).replace(tzinfo=None) - datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')).seconds < 1800:
                # Too many requests
                return HttpResponse(status=429)
        else:
            return HttpResponse(status=422)

        telegram_username = user.get('telegram', {}).get('username', '')

        if not telegram_username:
            # No telegram username to update member info
            return HttpResponse(status=422)

        chat_username = document.get('chat', {}).get('chat_parameters', {}).get('username', '')
        data = {
            'publicKey': os.getenv('RSA_PUBLIC_KEY', ''),
        }
        data = json.dumps(data)
        origin = os.getenv('HOSTNAME', '')

        member = requests.get(
            f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat_username}/{telegram_username}",
            data=data, headers={'Origin': origin})

        if member and member.status_code == 200:
            member = member.json()

            date = datetime.now(tz=utc)
            date = date.strftime('%Y-%m-%d %H:%M:%S')

            query = {f'users.{username}.member': member, f'users.{username}.date': date}
            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                       action='$set', query=query)

            return HttpResponse()
        else:
            if member.status_code == 422:
                # if not member or not user or not chat:
                #     return Response(status=422)

                date = datetime.now(tz=utc)
                date = date.strftime('%Y-%m-%d %H:%M:%S')

                query = {f'users.{username}.member': '', f'users.{username}.date': date, f'referendum.votes.{username}': ''}
                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                           action='$set', query=query)

            return HttpResponse()
