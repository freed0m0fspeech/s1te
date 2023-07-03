import requests

post_request_types = ('testimonial', 'auth')
get_request_types = ('testimonial', 'constitution')


async def verify_post_request(request):
    request_type_value = request.POST.get('type', '')

    if not request_type_value:
        return False

    for request_type in post_request_types:
        if request_type_value == request_type:
            return request_type

    return False


async def verify_get_request(request):
    request_type_value = request.POST.get('type', '')

    if not request_type_value:
        return False

    for request_type in get_request_types:
        if request_type_value == request_type:
            return request_type

    return False


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.get(image_url)

    if r.headers["content-type"] in image_formats:
        return True

    return False
