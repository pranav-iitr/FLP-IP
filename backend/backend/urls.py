
from django.contrib import admin
from django.urls import path , include
from users import urls as user_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(user_urls), name="api"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
