from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('zadmin/', admin.site.urls),
    path('', include("place.urls")),
    path('blog/', include("blog.urls")),
    path('user/', include("user.urls")),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)