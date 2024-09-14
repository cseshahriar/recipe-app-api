from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    # Optional UI:
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'
    ),
    path('api/user/', include('user.urls')),
]
