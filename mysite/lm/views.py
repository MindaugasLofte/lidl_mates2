from django.shortcuts import render, redirect
from .models import Darbuotojas, Krautuvas, Darbo_zona_sandelyje, Notes,Darbo_laiko_irasai
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from django.views.generic import ListView

# Create your views here.

# tikriname ar viskas veikia, nekuriant  template
def index(request):

# testuojame be html
# return HttpResponse('Starting LIDL MATES!')

    num_working_zones = Darbo_zona_sandelyje.objects.all().count()
    num_workers = Darbuotojas.objects.all().count()
    num_notes = Notes.objects.all().count()
    num_working_machines = Krautuvas.objects.all().count()
    num_work_records = Darbo_laiko_irasai.objects.all().count()



    context = {
        'num_working_zones':num_working_zones,
        'num_workers':num_workers,
        'num_notes':num_notes,
        'num_working_machines':num_working_machines,
        'num_work_records':num_work_records,

    }
    return render(request, 'lm/index.html', context=context)

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

def work_records(request):
    work_records = Darbo_laiko_irasai.objects.all()
    context = {
        'work_records': work_records
    }
    # print(work_records)
    return render(request, 'lm/work_records.html', context=context)

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


