from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from utils.decorators import ajax_login_required


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


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
