from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import RegisterUserForm, UpdateOrderForm
from django.urls import reverse_lazy
from .models import User, Order
from django.views.generic.base import TemplateView
from django.views import generic
import datetime


# Create your views here.


def index(request):
    num_order = Order.objects.filter(status__exact='c')[:4]
    num_status = Order.objects.filter(status__exact='a').count()
    return render(
        request,
        'index.html',
        context={'num_order': num_order, 'num_status': num_status},
    )


class OrderDetailView(generic.DetailView):
    model = Order


class UserProfile(generic.DetailView):
    model = User


class LoanedOrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'studio/order_list_customer_user.html'
    paginate_by = 10
    status = None

    def get(self, request, *args, **kwargs):
        # print(request.GET.get('status'))
        if request.GET.get('status'):
            self.status = request.GET.get('status')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(LoanedOrdersByUserListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['status_list'] = Order.LOAN_STATUS
        # print(Order.LOAN_STATUS)
        return context

    def get_queryset(self):
        if self.status:
            return Order.objects.filter(customer_order=self.request.user, status=self.status)
        return Order.objects.filter(customer_order=self.request.user).order_by('-day_add')


class LoanedOrdersAllListView(PermissionRequiredMixin, generic.ListView):
    model = Order
    permission_required = 'studio.can_mark_returned'
    template_name = 'studio/order_list_customer_all.html'
    paginate_by = 10
    status = None

    def get(self, request, *args, **kwargs):
        # print(request.GET.get('status'))
        if request.GET.get('status'):
            self.status = request.GET.get('status')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(LoanedOrdersAllListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['status_list'] = Order.LOAN_STATUS
        # print(Order.LOAN_STATUS)
        return context

    def get_queryset(self):
        return Order.objects.all()


class OrderCreate(CreateView):
    model = Order
    fields = ['name', 'summary', 'category', 'photo_file']

    def form_valid(self, form):
        form.instance.customer_order = self.request.user
        form.instance.day_add = datetime.date.today()
        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    form_class = UpdateOrderForm
    permission_required = 'studio.can_mark_returned'

    def post(self, request, *args, **kwargs):
        print(request)
        return super().post(request, *args, **kwargs)


class OrderUserDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('my-order')

    def get(self, request, *args, **kwargs):
        if self.get_object().status == 'n':
            return super().get(request, *args, **kwargs)
        return redirect('my-order')


class OrderAdminDelete(PermissionRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('all-order')
    permission_required = 'studio.can_mark_returned'


class StudioLoginView(LoginView):
    template_name = 'registrations/login.html'


class StudioLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registrations/login.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

# class RegisterDoneView(TemplateView):
#     template_name = 'registration/register_done.html'
