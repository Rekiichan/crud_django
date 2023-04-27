from django.urls import path
from . import views

urlpatterns = [
    # path('get', views.ApiTest.as_view(), name = 'get-data'),
    # path('get/<int:pk>', views.ApiTest.as_view(), name = 'get-data-pk'),
    # path('post', views.ApiTest.as_view(), name = 'post-data'),
    # path('put/<int:pk>', views.ApiTest.as_view(), name = 'put-data'),
    # path('delete/<int:pk>', views.ApiTest.as_view(), name = 'delete-data'),

    # item CRUD region
    path('item/', views.get_item, name='get-or-post-item'), # GET, POST
    path('item-upsert/<pk>', views.update_and_delete_items, name='update-or-delete-item'),

    # user retreive
    path('users/', views.view_users, name='view_users'), # GET
    path('get-user/', views.get_user, name='get-user'),

    # auth
    path('auth/me', views.CheckMyAuth.as_view(), name = 'check-me'),
    path('auth/login', views.AuthenLogin.as_view(), name = 'login'),


    path('auth/signup-client', views.AuthenSignupClient.as_view(), name = 'signup-client'),
    path('auth/signup-admin', views.AuthenSignupAdmin.as_view(), name = 'signup-admin'),
    

]




