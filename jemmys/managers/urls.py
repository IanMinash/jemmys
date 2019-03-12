from django.urls import path, include
from .views import dash, Login, Logout, ProductListView, ProductDetailView, update_product, new_product, OrderListView, view_order, variant_manager, CustomerListView, CustomerDetailView, IssueListView, IssueDetailView, issue_manager

app_name = 'managers'

urlpatterns = [
    path('', dash, name='dashboard'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('products', ProductListView.as_view(), name='products'),
    path('product/', include([
       path('create', new_product, name='new-product'),
       path('create-variant', variant_manager, name='new-variant'),
       path('<slug:slug>', ProductDetailView.as_view(), name='product'),
       path('update/<slug:slug>', update_product, name='update-product'),

    ])),
    path('orders', OrderListView.as_view(), name='orders'),
    path('order/<order_id>', view_order, name='view-order'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customer/<pk>', CustomerDetailView.as_view(), name='customer'),
    path('issues', IssueListView.as_view(), name='issues'),
    path('issue/<pk>', IssueDetailView.as_view(), name='issue'),
    path('issue/update/<pk>', issue_manager, name='issue-manager'),
]