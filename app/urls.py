from django.urls import path
from . import views

urlpatterns = [
    path('get', views.ApiTest.as_view(), name = 'get-data'),
    path('get/<int:pk>', views.ApiTest.as_view(), name = 'get-data-pk'),
    path('post', views.ApiTest.as_view(), name = 'post-data'),
    path('put/<int:pk>', views.ApiTest.as_view(), name = 'put-data'),
    path('delete/<int:pk>', views.ApiTest.as_view(), name = 'delete-data'),
]




