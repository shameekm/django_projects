from django.urls import path, reverse_lazy
from . import views

app_name = 'bill'
urlpatterns = [
    path('', views.RecieptListView.as_view(), name='all'),
    # path('reciept/<int:pk>', views.RecieptDetailView.as_view(), name='reciept_detail'),
    # path('reciept/create', views.RecieptCreateView.as_view(), name='reciept_create'),
    # path('reciept/<int:pk>/update', views.RecieptUpdateView.as_view(), name='reciept_update'),
    # path('reciept/<int:pk>/delete', views.RecieptUpdateView.as_view(), name='reciept_delete'),
    # path('reciept/<int:pk>/item', views.ItemCreateView.as_view(), name='reciept_item_create'),
    # path('item/<int:pk>/delete', views.ItemDeleteView.as_view(), name='reciept_item_delete'),
]
