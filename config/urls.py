from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from api.auth.auth import RegisterViewSet, LoginViewSet, RefreshViewSet
from api.v1.user.views import UserViewSet
from api.v1.post.views import PostViewSet

apirouter = routers.SimpleRouter()
apirouter.register(r'user', UserViewSet, basename='user')
apirouter.register(r'post', PostViewSet, basename='post')

authrouter = routers.SimpleRouter()
authrouter.register(r'register', RegisterViewSet, basename='auth-register')
authrouter.register(r'login', LoginViewSet, basename='auth-login')
authrouter.register(r'refresh', RefreshViewSet, basename='auth-refresh')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(apirouter.urls)),
    path('auth/', include(authrouter.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
