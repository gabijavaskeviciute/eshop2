

from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prekes/', views.PrekeListView.as_view(), name='preke_list'),
    path('prekes/<int:pk>', views.PrekeDetailView.as_view(), name='preke_detail'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas'),
    path('search/', views.search, name='search'),
    path('manouzsakymai/', views.UserUzsakymasListView.as_view(), name='manouzsakymai'),
    path('registracija/', views.registracija, name='registracija'),
    path('profilis/', views.profilis, name='profilis'),
    path('manouzsakymai/new', views.UzsakymasByUserCreateView.as_view(), name='manonaujiuzsakymai'),
    path('manouzsakymai/<int:pk>/update', views.UzsakymasByUserUpdateView.as_view(), name='mano-uzsakymas-update'),
    path('manouzsakymai/<int:pk>/delete', views.UzsakymasByUserDeleteView.as_view(), name='mano-uzsakymas-delete'),
    path('siuntimas/', views.SiuntimasListView.as_view(), name='siuntimas'),
]
