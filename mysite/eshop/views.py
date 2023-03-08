
from .models import Preke, Uzsakymas, Uzsakymo_eilute, Siuntimas
from django.http import HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import UserUpdateForm, ProfilisUpdateForm, UserUzsakymasCreateForm, UzsakymasReviewForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext as _

def index(request):
    return render(request, 'index.html')

class PrekeListView(generic.ListView):
    model = Preke
    template_name = 'preke_list.html'


class PrekeDetailView(generic.DetailView):
    model = Preke
    template_name = 'preke_detail.html'

class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 4
    template_name = 'uzsakymai.html'
    context_object_name = "uzsakymai"


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas.html'
    context_object_name = "uzsakymas"
    form_class = UzsakymasReviewForm


    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.vartotojas = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get('query')
    search_results = Preke.objects.filter(Q(pavadinimas__icontains=query))
    return render(request, 'search.html', {'prekes': search_results, 'query': query})


class UzsakymasByUserListView(LoginRequiredMixin,generic.ListView):
    model = Uzsakymas
    template_name ='mano_uzsakymai.html'
    paginate_by = 10

    def get_queryset(self):
        return Uzsakymas.objects.filter(uzsakovas=self.request.klientas).filter(status__exact='p')


class UserUzsakymasListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 4
    template_name = 'user_uzsakymai.html'
    context_object_name = "uzsakymai"

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user)

class UzsakymasByUserCreateView(LoginRequiredMixin, CreateView):
    model = Uzsakymas
    # fields = ['preke_id', 'kiekis']
    success_url = "/eshop/manouzsakymai/"
    template_name = 'user_uzsakymas_form.html'
    form_class = UserUzsakymasCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

class UzsakymasByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Uzsakymas
    fields = ['preke_id']
    success_url = "/eshop/manouzsakymai/"
    template_name = 'user_uzsakymas_form.html'

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas

class UzsakymasByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Uzsakymas
    success_url = "/eshop/manouzsakymai/"
    template_name = 'user_uzsakymas_delete.html'

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas

@csrf_protect
def registracija(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %s already exists!') % username)
                return redirect('registracija')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('User email %s already exist!') % email)
                    return redirect('registracija')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, _('User %s registered!') % username)
                    return redirect('login')
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('registracija')
    return render(request, 'registration/registracija.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)


class SiuntimasListView(generic.DetailView):
    model = Siuntimas
    template_name = 'siuntimas.html'