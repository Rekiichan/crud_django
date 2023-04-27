from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from django.contrib import admin
from django.urls import path, include

schema_view = swagger_get_schema_view(
    openapi.Info(
    title="CRUD API",
    default_version='1.0.0',
    description="API Document of A"
    ), 
    public = True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("app.urls")),

    # authen process

    # auth/jwt/create POST   ==> used for login, need: username, password
    # auth/users/     POST   ==> used for create user: need username, password, email

    # path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),

    # authen end

    # swagger region
    path('api/v1/', 
         include([
    # path('api/', include(('app.urls','app'), namespace='app')),
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
         ])),

]
