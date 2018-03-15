from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('demo', views.DemoView.as_view(), name='demo'),
    path('demo/<channel>', views.DemoServerView.as_view(), name="demo_server"),
]
