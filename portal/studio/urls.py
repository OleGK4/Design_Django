from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    # path('profile/', views.UserProfile.as_view(), name='user-profile'),
    path('myorders/', views.LoanedOrdersByUserListView.as_view(), name='my-order'),
    path('myorders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path(r'customer/', views.LoanedOrdersAllListView.as_view(), name='all-order'),
    path('order/create/', views.OrderCreate.as_view(), name='order-create'),
    path('myorders/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('myorders/<int:pk>/delete/', views.OrderUserDelete.as_view(), name='order-delete'),
    path('myorders/<int:pk>/delete/', views.OrderAdminDelete.as_view(), name='order-delete'),
]
