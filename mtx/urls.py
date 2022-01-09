from django.contrib import admin
from django.urls import path
from basketball.views import show_app_home, show_app_features, show_app_about, classify_video

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_app_home, name='home'),
    path('skynet/features/', show_app_features, name='features'),
    path('skynet/about/', show_app_about, name='about'),
    path('skynet/features/classify', classify_video, name='classify'),
]
