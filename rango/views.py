from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    top_pages_list = Page.objects.order_by('-views')[:5]

    for category in category_list:
        category.url = encode_url(category.name)

    context_dict = {'categories': category_list,
                    'pages': top_pages_list,}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'file_name': "Vdul.jpg"}
    return render(request, 'rango/about.html', context_dict)


def category_view(request, category_name_url):
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name,
                    'category_name_url': category_name_url}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_url):
    category_name = decode_url(category_name_url)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            try:
                page.category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                return render(request, 'rango/add_category.html', {})

            page.save()

            return category_view(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html',
                              {'category_name_url': category_name_url,
                               'category_name': category_name,
                               'form': form})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            # Django way of hashing password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                              {'user_form': user_form,
                               'profile_form': profile_form,
                               'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


def encode_url(name):
    return name.replace(' ', '_')


def decode_url(url):
    return url.replace('_', ' ')
