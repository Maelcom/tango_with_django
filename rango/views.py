from django.http import HttpResponse

def index(request):
    return HttpResponse('Rango says hello world!'
                        'View <a href="about">"About"</a> page.')

def about(request):
    return HttpResponse('Rango Says: Here is the about page.'
                        'Go back to <a href="/rango">"Rango"</a> page.')
