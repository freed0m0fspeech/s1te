import asyncio
import datetime
import json
import os
import random
import secrets
from math import sqrt

import requests
from bson import json_util
# import uuid
# import OpenSSL

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from dotenv import load_dotenv
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

# load_dotenv()


class HomePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        cockies = request.COOKIES

        context = {

        }

        query = {'_id': 0, 'constitution': 1, 'laws': 1, 'tlaws': 1, 'users': 1, 'testimonials': 1, 'president': 1,
                 'parliament': 1, 'judge': 1}

        document = mongoDataBase.get_document(database_name='site', collection_name='freedom_of_speech', query=query)

        constitution = document.get('constitution', '')
        laws = document.get('laws', '')
        tlaws = document.get('tlaws', '')
        testimonials = document.get('testimonials', [])

        # Government in database is links to telegram accounts
        president = document.get('president', '')
        parliament = document.get('parliament', '')
        judge = document.get('judge', '')

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
        try:
            testimonials = random.sample(testimonials, 10)
        except ValueError:
            pass

        testimonials_html = ""
        for testimonial in testimonials:
            testimonial_text = testimonial.get('text', '')
            testimonial_username = testimonial.get('username', '')
            testimonial_role = testimonial.get('role', '')

            div = "<div class='testimonial__content swiper-slide'>"
            p = "<p class='testimonial__description'>"
            # Testimonial
            p_end = "</p>"
            h3 = "<div><h3 class='testimonial__name'>"
            # Username
            h3_end = "</h3>"
            span = "<span class='testimonial__subtitle'>"
            # Role
            span_end = "</span></div>"
            div_end = "</div>"

            testimonials_html += f"{div}{p}\"{testimonial_text}\"{p_end}{h3}{testimonial_username}{h3_end}{span}" \
                                 f"{testimonial_role}{span_end}{div_end}"

        if user:
            permissions = user.get('permissions', {'administrator': False, 'moderator': False})
        else:
            permissions = {}

        chat = 'freed0m0fspeech'
        chat = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/chat/{chat}")
        members_count = ''
        if chat:
            member = chat.json()
            chat_parameters = member.get('chat_parameters', '')
            if chat_parameters:
                members_count = chat_parameters.get('members_count', '')

        context['president'] = president
        context['parliament'] = parliament
        context['judge'] = judge
        context['constitution'] = constitution
        context['members_count'] = members_count
        context['username'] = username
        context['laws'] = laws
        context['tlaws'] = tlaws
        context['administrator'] = permissions.get('administrator', False)
        context['moderator'] = permissions.get('administrator', permissions.get('moderator', False))
        context['testimonials_html'] = testimonials_html
        context['members_count'] = members_count

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

            expires = datetime.now() + timedelta(days=7)
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
        expires = datetime.now() + timedelta(days=7)
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
            query = {'_id': 0, 'users': 1, 'parliament': 1, 'president': 1}
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
            query = {'_id': 0, 'users': 1}
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

        query = {'_id': 0, 'users': 1}
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
                mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                           query=query)
            else:
                return HttpResponse(status=500)

            response = HttpResponse(status=200)

            # if 'username' in cookies:
            #     response.cookies['username'] = new_username

            expires = datetime.now() + timedelta(days=7)
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
            chat = 'freed0m0fspeech'

            member = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat}/{username}")
            if member:
                member = member.json()
                member_parameters = member.get('member_parameters', '')
                if member_parameters:
                    role = member_parameters.get('custom_title', 'Member')
        else:
            username = 'Аноним'

        query = {'testimonials': {'text': testimonial, 'username': username, 'role': role}}

        mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$push',
                                   query=query, )

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
                query = {'_id': 0, 'users': 1, 'president': 1, 'parliament': 1, 'judge': 1}

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
                    tusername = telegram.get('username')
                    if tusername == newtusername:
                        if username == tusername:
                            # Unlinking telegram account
                            query = {f'users.{username}.telegram': ''}

                            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                       action='$unset', query=query)

                            return HttpResponse(status=200)

            query = {f'users.{username}.telegram.first_name': data.get('first_name', ''),
                     f'users.{username}.telegram.last_name': data.get('last_name', ''),
                     f'users.{username}.telegram.photo_url': data.get('photo_url', ''),
                     f'users.{username}.telegram.username': data.get('username', '')}

            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech', action='$set',
                                       query=query)

            chat = 'freed0m0fspeech'

            member = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat}/{username}")
            if member:
                member = member.json()
                member_parameters = member.get('member_parameters', '')
                if member_parameters:
                    role = member_parameters.get('custom_title', '')
                    if role:
                        role = role.lower()

                        if role == 'судья':
                            query = {f"judge": username}
                            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                       action='$set', query=query)

                        if role == 'президент':
                            query = {f"president": username}
                            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                       action='$set', query=query)
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

                        if role == 'парламент':
                            query = {f"parliament": username}
                            mongoDataBase.update_field(database_name='site', collection_name='freedom_of_speech',
                                                       action='$set', query=query)
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

        query = {'_id': 0, 'users': 1}
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
                users = document.get('users', {})

                if users.get(username, ''):
                    if users[username].get('sessionid', ''):
                        if sessionid == users[username]['sessionid']:
                            # user = users[username]
                            context['authorized'] = True

        if username:
            if users:
                user = users.get(username, '')
                if user:
                    context['username'] = username
                    telegram = user.get('telegram', '')
                    if telegram:
                        telegram_username = telegram.get('username', '')
                        context['telegram_username'] = telegram_username
                        context['telegram_first_name'] = telegram.get('first_name', '')
                        context['telegram_last_name'] = telegram.get('last_name', '')
                        context['telegram_photo_url'] = telegram.get('photo_url', '')
                        context['telegram_link_status'] = True

                        chat = 'freed0m0fspeech'
                        member = requests.get(f"https://telegram-bot-freed0m0fspeech.fly.dev/member/{chat}/{telegram_username}")
                        if member:
                            member = member.json()
                            member_parameters = member.get('member_parameters', '')
                            context['messages_count'] = member.get('messages_count', '')
                            context['lvl'] = member.get('lvl', '')
                            context['xp_have'] = member.get('xp_have', '')
                            context['xp_need'] = member.get('xp_need', '')
                            context['hours_in_voice_channel'] = member.get('hours_in_voice_channel', '')
                            if member_parameters:
                                context['role'] = member_parameters.get('custom_title', 'Участник')

                                joined_date = member_parameters.get('joined_date', '')
                                if joined_date:
                                    date = json.loads(joined_date, object_hook=json_util.object_hook)
                                    if date:
                                    #date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                                        context['joined_date'] = date.strftime('%b %e, %Y')
                    else:
                        context['telegram_link_status'] = False
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)

        return render(request, template_name='freedom_of_speech/profile.html', context=context)

    async def post(self, request, *args, **kwargs):
        return HttpResponse(status=404)
