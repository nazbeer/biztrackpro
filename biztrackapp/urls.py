from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('',login_view,name='login' ),
    path('logout/',logout_view,name='logout' ),
    path('home/',HomeView.as_view(),name='home' ),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)