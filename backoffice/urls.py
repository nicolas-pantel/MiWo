from django.urls import path, include

from rest_framework.documentation import include_docs_urls

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('demo', views.DemoView.as_view(), name='demo'),
    path('demo/<channel>', views.DemoServerView.as_view(), name="demo_server"),

    ### API ###
    path('api/docs/', include_docs_urls(title='Miwo API')),
    path('api/', include('rest_auth.urls')),
    path('api/registration/', include('rest_auth.registration.urls')),
]
