from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView


#from utils import mongoDataBase




class HomePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        context = {

        }

        return render(request=request, template_name='portfolio/index.html', context=context)
