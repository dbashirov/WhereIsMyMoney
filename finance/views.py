from django.http.response import JsonResponse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from dateutil.relativedelta import relativedelta
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import json
import datetime

from .forms import OperationCreateForm
from .calcOfBalances import calculation_of_balances, expenses_by_category
from .addFunctions import MonthInWords

from .models import (
    Category,
    Operation,
    Wallet,
    typeIncome
)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        
        # Определеяем период для вывода
        today = datetime.datetime.today()
        datePrevMonth = today - relativedelta(months=1)
        date2PrevMonth = today - relativedelta(months=2)
        date3PrevMonth = today - relativedelta(months=3)

        # Определяем общий остаток
        rezult = calculation_of_balances(self.request.user, date3PrevMonth, today)
        context['start_date'] = date3PrevMonth.strftime('%Y-%m-%d')
        context['income_list'] = json.dumps(rezult['income_list'])
        context['expense_list'] = json.dumps(rezult['expense_list'])
        context['balance_list'] = json.dumps(rezult['balance_list'])

        # Опредлеям расходы по категориям за препредущий месяц
        expenses2PrevMonth = expenses_by_category(self.request.user, date2PrevMonth)
        context['showExpenses2PrevMonth'] = len(expenses2PrevMonth) > 0
        context['expenses2PrevMonth'] = json.dumps(expenses2PrevMonth)
        context['name2PrevMonth'] = json.dumps(MonthInWords(date2PrevMonth))
        
        # Опредлеям расходы по категориям за предущий месяц
        expensesOfPrevMonth = expenses_by_category(self.request.user, datePrevMonth)
        context['showExpensesPrevMonth'] = len(expensesOfPrevMonth) > 0
        context['expensesPrevMonth'] = json.dumps(expensesOfPrevMonth)
        context['namePrevMonth'] = json.dumps(MonthInWords(datePrevMonth))

        # Опредлеям расходы по категориям за текущий месяц
        expensesOfCurrentMonth = expenses_by_category(self.request.user, today)
        context['expensesOfCurrentMonth'] = json.dumps(expensesOfCurrentMonth)

        # Отображение остатков по каждому кошельку
        wallets = Wallet.objects.filter(user=self.request.user)
        list_wallets = []
        for currentWallet in wallets:
            rezult = calculation_of_balances(self.request.user, datePrevMonth, today, currentWallet)
            list_wallets.append({
                'id': currentWallet.id, 
                'title': currentWallet.title,
                'income_list': rezult['income_list'],
                'expense_list': rezult['expense_list'],
                'balance_list': rezult['balance_list'],
            })
        
        context['wallets'] = wallets
        context['list_wallets'] = json.dumps(list_wallets)
        
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        return queryset


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['title', 'type']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('categories')

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class CategoryCreateView(CreateView):
    model = Category
    fields = ['title', 'type']
    context_object_name = 'category'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    context_object_name = 'category'
    success_url = reverse_lazy('categories')

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class OperationListView(LoginRequiredMixin, ListView):
    model = Operation
    context_object_name = 'Operations'
    paginate_by = 30

    def get_queryset(self):
        user = self.request.user
        try:
            # search_text = self.kwargs['search_text']
            search_text = self.request.GET.get('search_text')
        except:
            search_text = ''
        if search_text != '' and search_text != None:
            queryset = Operation.objects.filter(
                (Q(category__title__icontains=search_text) 
                    | Q(wallet__title__icontains=search_text) 
                    | Q(wallet_recipient__title__icontains=search_text)
                    | Q(description__icontains=search_text)),
                user=user)
        else:
            queryset = Operation.objects.filter(user=user)
        
        return queryset

class OperationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Operation
    fields = ['sum', 'wallet', 'type',
              'category', 'wallet_recipient', 'date', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('operations')
    context_object_name = 'operation'

    def get_context_data(self, **kwargs):
        context = super(OperationUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['wallet'].queryset = Wallet.objects.filter(user=self.request.user)
        context['form'].fields['wallet_recipient'].queryset = Wallet.objects.filter(user=self.request.user)
        return context

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user

class OperationCreateView(CreateView):
    model = Operation
    # fields = ['sum', 'wallet', 'type', 'category', 'date', 'description']
    context_object_name = 'operation'
    form_class = OperationCreateForm
    success_url = reverse_lazy('operations')
    template_name_suffix = '_form'

    def get_context_data(self, **kwargs):
        context = super(OperationCreateView, self).get_context_data(**kwargs)
        context['form'].fields['wallet'].queryset = Wallet.objects.filter(user=self.request.user)
        context['form'].fields['wallet_recipient'].queryset = Wallet.objects.filter(user=self.request.user)
        
        # Передаем на форму куда вернуться, если нажали "Назад"
        if 'operations' in self.request.GET.get('next', '/'):
            context['next'] = '/operations'
            self.success_url = reverse_lazy('operations')
        else:
            context['next'] = '/'
            self.success_url = reverse_lazy('home')
        return context

    def post(self, request, *args, **kwargs):
        if "addMore" in request.POST:
            self.success_url = reverse_lazy('operations-add')
            if 'operations' in request.GET.get('next', '/'):
                self.success_url += '?next=operations'
            else:
                self.success_url += '?next=home'
            if 'addIncome' in request.GET:
                self.success_url += '&addIncome'
            return super(OperationCreateView, self).post(request, *args, **kwargs)
        else:
            if 'operations' in request.GET.get('next', '/'):
                self.success_url = reverse_lazy('operations')
            else:
                self.success_url = reverse_lazy('home')
            return super(OperationCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        # Тест. Здесь тоже работает, но не знаю где лучше использовать, пока оставлю в post
        # if "addMore" in self.request.POST:
        #     self.success_url = reverse_lazy('operations-add')
        #     return super(OperationCreateView, self).form_valid(form)
        # else:
        #     return super(OperationCreateView, self).form_valid(form)
        return super(OperationCreateView, self).form_valid(form)

    # def get_success_url(self):
    #     print(f"HTTP_REFERER = {self.request.POST}")
    #     return self

class OperationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Operation
    context_object_name = 'operation'
    success_url = reverse_lazy('operations')

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class WalletListView(LoginRequiredMixin, ListView):
    model = Wallet
    context_object_name = 'wallets'

    def get_queryset(self):
        user = self.request.user
        queryset = Wallet.objects.filter(user=user)
        return queryset

class WalletCreateView(CreateView):
    model = Wallet
    fields = ['title', 'currency', 'description']
    context_object_name = 'wallet'
    success_url = reverse_lazy('wallets')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(WalletCreateView, self).form_valid(form)

class WalletUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Wallet
    fields = ['title', 'currency', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('wallets')

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user

class WalletDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Wallet
    context_object_name = 'wallet'
    success_url = reverse_lazy('wallets')

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


def returnListCategory(request):

    if request.method == "POST":
        
        post_data = json.loads(request.body.decode("utf-8"))

        qs = Category.objects.all()
        qs = qs.filter(type=post_data['type'], user=request.user)
        # qs_json = serializers.serialize('json', qs)
        qs_json = list(qs.values())
        
    else:
        qs_json = { }

    return JsonResponse(qs_json, safe=False)
    # return HttpResponse(qs_json, content_type='application/json')

def returnListWallet(request):

    if request.method == "POST":
        
        post_data = json.loads(request.body.decode("utf-8"))
        # print(f'wallet={post_data}')
        # print(post_data['wallet']=='')
        qs = Wallet.objects.all()
        if post_data['wallet'] == '':
            qs = qs.filter(user=request.user)
        else:
            qs = qs.filter(user=request.user).exclude(id=post_data['wallet'])
        qs_json = list(qs.values())
        
    else:
        qs_json = { }

    return JsonResponse(qs_json, safe=False)

