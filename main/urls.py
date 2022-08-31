from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = [
    path('', include('shop.urls', namespace='shop')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)