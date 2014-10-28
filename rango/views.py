from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserProfileForm  # , UserForm


def index(request):
    category_list = Category.objects.order_by('-likes')
    top_pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': top_pages_list}

    # Session-based data below
    visits = request.session.get('visits', 0)
    last_visit = request.session.get('last_visit')

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['visits'] = visits + 1
        request.session['last_visit'] = str(datetime.now())

    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'file_name': "Vdul.jpg",
                    'visits': request.session.get('visits', 0)}
    return render(request, 'rango/about.html', context_dict)


def category_view(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category_name'] = category_name_slug.replace('-', ' ').title()

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save()
            return redirect('category', cat.slug)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    cat = Category.objects.get_or_none(slug=category_name_slug)
    if not cat:
        return redirect('category', category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = cat
            page.save()
            return redirect('category', category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html',
                  {'category_name_slug': category_name_slug,
                   'form': form})

# Decomission of handmade login and register
# Switched to django-registration-redux
# def register(request):
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             # Django way of hashing password
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             # Auto-login the new user
#             user = authenticate(username=user_form.cleaned_data['username'],
#                                 password=user_form.cleaned_data['password'])
#             login(request, user)
#             return redirect('index')
#         else:
#             print user_form.errors, profile_form.errors
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'rango/register.html',
#                               {'user_form': user_form,
#                                'profile_form': profile_form,})
#
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             print "Invalid login details: {0}, {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
