import datetime
from django.db.models import Sum, Q
import random

from .models import (
    Operation,
    Category,
    typeIncome,
    typeExpense,
    typeTransfer
)


def calculation_of_balances(user, bedinDate, endDate, wallet=None):

    income_list = []
    expense_list = []
    balance_list = []

    # Получаем баланс на начало периода
    if wallet == None:
        # Сумма поступлений на начало периода
        income_beg = Operation.objects.filter(
            type=typeIncome,
            user=user,
            date__lte=bedinDate.date()
        ).aggregate(all_sum_beg=Sum("sum"))
        # Сумма списаний на начало периода
        expense_beg = Operation.objects.filter(
            type=typeExpense,
            user=user,
            date__lte=bedinDate.date()
        ).aggregate(all_sum_beg=Sum("sum"))
    else:
        # Сумма поступлений на начало периода
        income_beg = Operation.objects.filter(
            (Q(type=typeIncome) & Q(wallet=wallet)) | (Q(type=typeTransfer) & Q(wallet_recipient=wallet)),
            user=user,
            date__lte=bedinDate.date()
        ).aggregate(all_sum_beg=Sum("sum"))
        # Сумма списаний на начало периода
        expense_beg = Operation.objects.filter(
            Q(type=typeExpense) | Q(type=typeTransfer),
            user=user,
            wallet=wallet,
            date__lte=bedinDate.date()
        ).aggregate(all_sum_beg=Sum("sum"))

    balance = (income_beg['all_sum_beg'] if income_beg['all_sum_beg'] != None else 0) - \
        (expense_beg['all_sum_beg'] if expense_beg['all_sum_beg'] != None else 0)

    # print(f'wallet = {wallet},  income_beg = {income_beg["all_sum_beg"]}, expense_beg = {expense_beg["all_sum_beg"]}, balance={balance}')

    for iday in range(abs((endDate - bedinDate).days) + 1, 0, -1):

        # Определям текущую дату для расчета
        current_date = (endDate - datetime.timedelta(days=iday-1))

        if wallet == None:
            
            # Определям сумму доходов за текущий день
            result_income = Operation.objects.filter(
                type=typeIncome,
                user=user,
                date__date=current_date.date()
            ).aggregate(all_sum_day=Sum("sum"))
            
            # Определяем суммы расходов за текущий день
            result_expense = Operation.objects.filter(
                type=typeExpense,
                user=user,
                date__date=current_date.date()
            ).aggregate(all_sum_day=Sum("sum"))

        else:
            
            # Определям сумму доходов за текущий день
            result_income = Operation.objects.filter(
                (Q(type=typeIncome) & Q(wallet=wallet)) | (Q(type=typeTransfer) & Q(wallet_recipient=wallet)),
                user=user,
                date__date=current_date.date()
            ).aggregate(all_sum_day=Sum("sum"))

            # Определяем суммы расходов за текущий день
            result_expense = Operation.objects.filter(
                Q(type=typeExpense) | Q(type=typeTransfer),
                user=user,
                wallet=wallet,
                date__date=current_date.date()
            ).aggregate(all_sum_day=Sum("sum"))

        sum_income = result_income['all_sum_day'] if result_income['all_sum_day'] != None else 0
        sum_expence = result_expense['all_sum_day'] if result_expense['all_sum_day'] != None else 0

        # Определяем остаток
        balance = balance + sum_income - sum_expence

        income_list.append(str(sum_income))
        expense_list.append(str(sum_expence))
        balance_list.append(str(balance))

    return {'income_list': income_list, 'expense_list': expense_list, 'balance_list': balance_list}

def expenses_by_category(user, datePrevMonth, Wallet=None):
    
    expensesByCategory = []
    categories = Category.objects.filter(user=user, type=typeExpense)

    for category in categories:
        result_expense = Operation.objects.filter(
                type=typeExpense,
                user=user,
                category=category,
                date__year=datePrevMonth.year,
                date__month=datePrevMonth.month
            ).aggregate(sum=Sum("sum"))
        sum = result_expense['sum'] if result_expense['sum'] != None else 0
        if sum > 0:
            expensesByCategory.append({'name': str(category), 'y': str(sum), 'z': random.randrange(50, 150)})

    return expensesByCategory

def incomes_by_category(user, datePrevMonth, Wallet=None):
    
    incomesByCategory = []
    categories = Category.objects.filter(user=user, type=typeIncome)
    print(f'{categories=}')

    for category in categories:
        result_income = Operation.objects.filter(
                type=typeIncome,
                user=user,
                category=category,
                date__year=datePrevMonth.year,
                date__month=datePrevMonth.month
            ).aggregate(sum=Sum("sum"))
        sum = result_income['sum'] if result_income['sum'] != None else 0
        if sum > 0:
            incomesByCategory.append({'name': str(category), 'y': str(sum), 'z': random.randrange(50, 150)})

    return incomesByCategory