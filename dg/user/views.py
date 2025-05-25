from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
# from django.http import HttpResponse
import datetime
from django.http import Http404


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def login(request):
    ...
def logout(request):
    ...


def my_view(request):
    # ...
    if 'foo':
        return HttpResponseNotFound("<h1>Page not found</h1>")
    else:
        return HttpResponse("<h1>Page was found</h1>")
    # Return a "created" (201) response code.
    return HttpResponse(status=201)


def detail(request, poll_id):
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404("Poll does not exist")
    return render(request, "polls/detail.html", {"poll": p})

async def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)