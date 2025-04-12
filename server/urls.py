from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/book', include('book.urls')),
    path('api/v1/articles_essays', include('Articles_Essays.urls')),
    path('api/v1/miscellaneous', include('Miscellaneous.urls')),
    path('api/v1/about_author', include('About_Author.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)