from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


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
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)


def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)


def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.views = 0
            try:
                page.category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html', {}, context)

            page.save()

            return category_view(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html',
                              {'category_name_url': category_name_url,
                               'category_name': category_name,
                               'form': form},
                              context)


def encode_url(name):
    return name.replace(' ', '_')


def decode_url(url):
    return url.replace('_', ' ')
