from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page


def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[:5]
    top_pages_list = Page.objects.order_by('-views')[:5]

    for category in category_list:
        category.url = encode_url(category.name)

    context_dict = {'categories': category_list,
                    'pages': top_pages_list}
    return render_to_response('rango/index.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    context_dict = {'file_name': "Vdul.jpg"}
    return render_to_response('rango/about.html', context_dict, context)


def category_view(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_ulr(category_name_url)
    context_dict = {'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)


def encode_url(name):
    return name.replace(' ', '_')


def decode_ulr(url):
    return url.replace('_', ' ')
