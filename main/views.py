from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import AdvUser, SubRubric, AK
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm, AKForm, AIFormSet
from .utilities import signer

def index(request):
    aks = AK.objects.filter(is_active=True)[:10]
    context = {'aks': aks}
    return render(request, 'main/index.html', context)

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class AKLoginView(LoginView):
    template_name = 'main/login.html'

@login_required
def profile(request):
    aks = AK.objects.filter(author=request.user.pk)
    context = {'aks': aks}
    return render(request, 'main/profile.html', context)

class AKLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class AKPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    aks = AK.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        aks = aks.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(aks, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'aks': page.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)

def detail(request, rubric_pk, pk):
    ak = get_object_or_404(AK, pk=pk)
    ais = ak.additionalimage_set.all()
    context = {'ak': ak, 'ais': ais}
    return render(request, 'main/detail.html', context)

@login_required
def profile_ak_detail(request, rubric_pk, pk):
    ak = get_object_or_404(AK, pk=pk)
    ais = ak.additionalimage_set.all()
    context = {'ak': ak, 'ais': ais}
    return render(request, 'main/profile_ak_detail.html', context)

@login_required
def profile_ak_add(request):
    if request.method == 'POST':
        form = AKForm(request.POST, request.FILES)
        if form.is_valid():
            ak = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=ak)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
                return redirect('main:profile')
    else:
        form = AKForm(initial={'author': request.user.pk})
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_ak_add.html', context)

@login_required
def profile_ak_change(request, pk):
    ak = get_object_or_404(AK, pk=pk)
    if request.method == 'POST':
        form = AKForm(request.POST, request.FILES ,instance=ak)
        if form.is_valid():
            ak = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=ak)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS , 'Объявление исправлено')
                return redirect('main:profile')
    else:
        form = AKForm(instance=ak)
        formset = AIFormSet(instance=ak)
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_ak_change.html', context)

@login_required
def profile_ak_delete(request, pk):
    ak = get_object_or_404(AK, pk=pk)
    if request.method == 'POST':
        ak.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect('main:profile')
    else:
        context = {'ak': ak}
        return render(request, 'main/profile_ak_delete.html', context)

