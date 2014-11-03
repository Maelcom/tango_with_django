from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from utils.decorators import ajax_login_required
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, MailerForm
from registration.backends.simple.views import RegistrationView
from rango.bing_search import run_query
from rango.mailer import sendphish, get_provs


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
    context_dict = {'file_name': "img/Vdul.jpg",
                    'visits': request.session.get('visits', 0)}
    return render(request, 'rango/about.html', context_dict)


# Category/Page views (TODO: split into separate file)
def category_view(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
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


def ajax_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return JsonResponse({'login_success': 'ok'})
    return render(request, 'rango/ajax_login.html', {'form': form})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def search(request):
    results = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            results = run_query(query)
    return render(request, 'rango/search.html', {'results': results})


def mailer(request):
    form = MailerForm()
    context = {'provs': get_provs()}
    if request.method == 'POST':
        form = MailerForm(data=request.POST)
        if form.is_valid():
            alert = sendphish(fromaddr=form.cleaned_data['login'],
                              toaddr=form.cleaned_data['to'],
                              pwd=form.cleaned_data['pwd'])
            if alert:
                context['alert'] = alert
            else:
                context['success'] = True
    context['form'] = form
    return render(request, 'rango/mailer.html', context)


def track_url(request):
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        if page_id:
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)
        else:
            return redirect('index')


@ajax_login_required
def like_category(request):
    if request.method == 'GET':
        cat_id = request.GET.get('cat_id')
        cat = Category.objects.get_or_none(id=int(cat_id))
        if cat:
            cat.likes += 1
            cat.save()
        return JsonResponse({'likes': cat.likes})


# Accessory function for 'suggest_category' view
def get_cat_list(q='', max_results=0):
    cats = None
    if q:
        cats = Category.objects.filter(name__istartswith=q)
        if max_results > 0:
            cats = cats[:max_results]
    return cats


def suggest_category(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        return render(request, 'rango/cats.html', {'cats': get_cat_list(q)})


class RangoRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'


class ProfileUpdate(UpdateView):
    model = UserProfile
    fields = ('picture', 'website')
    template_name_suffix = ""
    template_name = 'rango/profile.html'
    success_url = '.'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)
