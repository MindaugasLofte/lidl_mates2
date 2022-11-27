from django.shortcuts import render,get_object_or_404, reverse, redirect
from .models import Darbuotojas, Krautuvas, Darbo_zona_sandelyje
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from django.views.generic import TemplateView, ListView

# Create your views here.

# tikriname ar viskas veikia, nekuriant  template
def index(request):

# testuojame be html
# return HttpResponse('Starting LIDL MATES!')
    return render(request, 'lm/index.html')

def working_zones(request):
    working_zones = Darbo_zona_sandelyje.objects.all()
    context = {
        'working_zones': working_zones
    }
    # print(working_zones)
    return render(request, 'lm/working_zones.html', context=context)

def working_machines_list(request):
    working_machines_list=Krautuvas.objects.all()
    context = {
        'working_machines_list': working_machines_list
    }
    # print(working_machines_list)
    return render(request, 'lm/working_machines_list.html', context=context)

def workers(request):
    workers = Darbuotojas.objects.all()
    context = {
        'workers': workers
    }
    # print(workers)
    return render(request, 'lm/workers.html', context=context)

def about(request):
    return render(request, 'lm/about.html')

def dashboard(request):
    return render(request, 'lm/dashboard.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        #pasiimti duomenis iš formos
        username = request.POST['username']
        email = request.POST ['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %s already exists!') % username)
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Username with %s already exists!') % email)
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    return render(request, 'lm/welcome.html')
        else:
            messages.error(request, _('Passwords do no match!'))
            return redirect('register')
    return render(request, 'lm/register.html')


class SearchResultsView(ListView):
    model = Krautuvas
    template_name = "search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("query")
        object_list = Krautuvas.objects.filter(
            Q(krautuvo_id__icontains=query)
        )
        return object_list


