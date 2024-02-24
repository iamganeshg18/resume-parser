from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from app import views
from django.conf import settings
from django.conf.urls.static import static



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('fileUpload',csrf_exempt(views.fieUpload),name="file"),
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('resumeparser/',csrf_exempt(views.parse_resume)),
]