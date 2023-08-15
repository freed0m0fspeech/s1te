import random

# from portfolio.utils import update_cached_data
from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
from django.views.generic import TemplateView
from utils import dataBases, cache

mongoDataBase = dataBases.mongodb_client

class HomePageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        context = {

        }

        # query = {'_id': 0, 'testimonials': 1}
        #
        # document = mongoDataBase.get_document(database_name='site', collection_name='portfolio', query=query)

        document = cache.portfolio

        if not document:
            testimonials = []
        else:
            testimonials = document.get('testimonials', [])

        testimonials_count = len(testimonials)
        max_testimonials = 10
        testimonials = random.sample(testimonials, min(testimonials_count, max_testimonials))

        context['testimonials'] = testimonials

        return render(request=request, template_name='portfolio/index.html', context=context)


class AddTestimonialPageView(TemplateView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    async def post(self, request, *args, **kwargs):
        data = request.POST

        if not data:
            return HttpResponse(status=422)

        testimonial = data.get('testimonial', '')
        # name = data.get('name', '')
        # role = data.get('role', '')

        if not testimonial:
            return HttpResponse(status=422)

        query = {'testimonials': {'text': testimonial}}

        mongoUpdate = mongoDataBase.update_field(database_name='site', collection_name='portfolio', action='$push', query=query)

        if mongoUpdate is None:
            return HttpResponse(status=500)
        else:
            cache.portfolio = mongoUpdate

        return HttpResponse(status=200)
