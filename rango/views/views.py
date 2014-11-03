from datetime import datetime
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import MailerForm
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
