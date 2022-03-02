import uuid
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model, get_user
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import DecimalField
from django.db.models.query import QuerySet
from django.urls import reverse
# from smart_selects.db_fields import ChainedForeignKey


class Currency(models.Model):
    code = models.CharField(max_length=5, unique=True, db_index=True)
    charactercode = models.CharField(max_length=5, blank=True, null=True)
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return self.charactercode


class Wallet(models.Model):
    title = models.CharField(max_length=150)
    currency = models.ForeignKey(
        Currency, on_delete=PROTECT, verbose_name='Валюта')
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.title + ' (' + str(self.currency) + ')'

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"


typeIncome = 'Доход'
typeExpense = 'Расход'
typeTransfer = 'Перевод'

type_choices = [
    (typeExpense, 'Расход'),
    (typeIncome, 'Доход'),
]

type_choices_operation = [
    (typeExpense, 'Расход'),
    (typeIncome, 'Доход'),
    (typeTransfer, 'Перевод'),
]


class Category(models.Model):
    title = models.CharField('Название', max_length=150)
    type = models.CharField(
        max_length=10, choices=type_choices, default=typeExpense)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категория"
        ordering = ['type', 'title']

    def __str__(self):
        return self.title

    # def chained_relation(self):
    #     return self.operation_set.filter(user = self.request.user)


class Operation(models.Model):
    type = models.CharField('Тип', max_length=10,
                            choices=type_choices_operation, default=typeExpense)
    user = models.ForeignKey(get_user_model(), on_delete=CASCADE)
    # category = ChainedForeignKey(
    #     'Category',
    #     on_delete=PROTECT,
    #     chained_field="type",
    #     chained_model_field="type",
    #     show_all=False,
    #     auto_choose=True,
    #     verbose_name='Категория'
    # )
    category = models.ForeignKey(
        'Category',
        on_delete=PROTECT,
        verbose_name='Категория',
        blank=True,
        null=True)
    date = models.DateTimeField('Дата', default=datetime.now)
    wallet = models.ForeignKey(Wallet, on_delete=PROTECT, verbose_name='Кошелек', related_name='wallet')
    wallet_recipient = models.ForeignKey(
        Wallet, 
        on_delete=PROTECT, 
        verbose_name='На кошелек', 
        related_name='wallet_recipient',
        blank=True,
        null=True)
    sum = models.DecimalField('Сумма', max_digits=15, decimal_places=2)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        str_type = ': -' if self.type == typeExpense else ': +'
        return str(self.category) + str_type + str(self.sum)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        ordering = ['-date']
