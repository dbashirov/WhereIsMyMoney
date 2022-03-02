from django.db import models
from django.urls import path
from django.conf.urls import url
from .models import Category
from .views import (
    # Общее
    HomePageView, 
    AboutPageView, 
    
    # Категории
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    # Операции
    OperationListView, 
    OperationUpdateView, 
    OperationCreateView, 
    OperationDeleteView,

    # Кошелек
    WalletListView,
    WalletCreateView,
    WalletUpdateView,
    WalletDeleteView,

    returnListCategory,
    returnListWallet
)


urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),

    # DAL
    url(r'^operations/add/category-ajax/$', returnListCategory, name='returnListCategory'),
    url(r'^operations/update/category-ajax/$', returnListCategory, name='returnListCategory'),

    url(r'^operations/add/wallet_recipient-ajax/$', returnListWallet, name='returnListWallet'),
    url(r'^operations/update/wallet_recipient-ajax/$', returnListWallet, name='returnListWallet'),

    # Журная операций
    path('operations', OperationListView.as_view(), name='operations'),
    path('operations/update/<int:pk>', OperationUpdateView.as_view(), name='operations-update'),
    path('operations/add/', OperationCreateView.as_view(), name='operations-add'),
    path('operations/delete/<int:pk>', OperationDeleteView.as_view(), name='operations-delete'),

    # Категории
    path('categories', CategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>', CategoryUpdateView.as_view(), name='categories-update'),
    path('categories/add/', CategoryCreateView.as_view(), name='categories-add'),
    path('categories/delete/<int:pk>', CategoryDeleteView.as_view(), name='categories-delete'),

    # Кошельки
    path('wallets', WalletListView.as_view(), name='wallets'),
    path('wallets/update/<int:pk>', WalletUpdateView.as_view(), name='wallets-update'),
    path('wallets/add/', WalletCreateView.as_view(), name='wallets-add'),
    path('wallets/delete/<int:pk>', WalletDeleteView.as_view(), name='wallets-delete'),
]