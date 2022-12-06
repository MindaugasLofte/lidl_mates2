from django.shortcuts import render, redirect
from .models import MyUser, Krautuvas, Darbo_zona_sandelyje, Notes,Darbo_laiko_irasai
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfilisUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

# Create your views here.

# tikriname ar viskas veikia, nekuriant  template
def index(request):

# testuojame be html
# return HttpResponse('Starting LIDL MATES!')

    num_working_zones = Darbo_zona_sandelyje.objects.all().count()
    num_workers = MyUser.objects.all().count()
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
    paginator = Paginator(Krautuvas.objects.all(), 9)
    page_number = request.GET.get('page')
    paged_working_machines_list = paginator.get_page(page_number)

    # working_machines_list=Krautuvas.objects.all()
    context = {
        'working_machines_list': paged_working_machines_list
        # 'working_machines_list': working_machines_list
    }
    # print(working_machines_list)
    return render(request, 'lm/working_machines_list.html', context=context)

def workers(request):
    paginator = Paginator(MyUser.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_workers = paginator.get_page(page_number)
    # workers = MyUser.objects.all()
    context = {
        'workers': paged_workers
        # 'workers': workers
    }
    # print(workers)
    return render(request, 'lm/workers.html', context=context)

def work_records(request):
    paginator = Paginator(Darbo_laiko_irasai.objects.all(), 10)
    page_number = request.GET.get('page')
    paged_work_records = paginator.get_page(page_number)

    # work_records = Darbo_laiko_irasai.objects.all()
    context = {
        'work_records': paged_work_records
        # 'work_records': work_records
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
        picker_code = request.POST['picker_code']
        date_of_birth = request.POST['date_of_birth']
        email = request.POST ['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if MyUser.objects.filter(picker_code=picker_code).exists():
                messages.error(request, _('Username %s already exists!') % picker_code)
                return redirect('register')
            else:
                if MyUser.objects.filter(email=email).exists():
                    messages.error(request, _('Username with %s already exists!') % email)
                    return redirect('register')
                else:
                    MyUser.objects.create_user(picker_code=picker_code, email=email, password=password, date_of_birth=date_of_birth)
                    return render(request, 'lm/welcome.html')
        else:
            messages.error(request, _('Passwords do no match!'))
            return redirect('register')
    return render(request, 'lm/register.html')


class SearchResultsView(ListView):
    model = Krautuvas
    template_name = "lm/working_machines_list_search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("query")
        object_list = Krautuvas.objects.filter(
            Q(krautuvo_id__icontains=query)
        )
        return object_list

# @login_required
# def profilis(request):
#     return render(request, 'lm/profilis.html')


@login_required
def profilis(request):

    if request.method == 'POST':
        # u_form - user formas atnaujins
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # # p_form - profilio formas atnaujins
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        # if u_form.is_valid():
        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()
            #  sios zinutes bus atvaozduotos per profilis.html zr 7-13 eilutes
            messages.success(request, f'Profilis atnaujintas')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'lm/profilis.html', context)

class NotesListView(LoginRequiredMixin, generic.ListView):
    model = Notes
    template_name = 'lm/worker_notes.html'
    context_object_name = 'my_notes'
    paginate_by = 2
    def get_queryset(self):
        return Notes.objects.filter(darbuotojas=self.request.user).order_by('data')
class WorkersWorkingRecordsListView(LoginRequiredMixin, generic.ListView):
    model = Darbo_laiko_irasai
    template_name = 'lm/worker_working_records.html'
    context_object_name = 'my_working_records'
    paginate_by = 2
    def get_queryset(self):
        return Darbo_laiko_irasai.objects.filter(darbuotojas=self.request.user).order_by('data')

class WorkersUsedMachinesListView(LoginRequiredMixin, generic.ListView):
    model = Krautuvas
    template_name = 'lm/worker_used_machines.html'
    context_object_name = 'my_used_machines'
    paginate_by = 2
    def get_queryset(self):
        return Krautuvas.objects.filter(darbuotojas=self.request.user).order_by('data_taken')