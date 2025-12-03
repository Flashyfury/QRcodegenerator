from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history, name='history'),
    path('qr/<int:pk>/', views.qr_detail, name='qr_detail'),
    path('qr/<int:pk>/download/', views.download_qr, name='qr_download'),
    path('preview/', views.preview_image, name='preview_image'),  # optional server-side preview endpoint
]
