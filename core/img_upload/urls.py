from django.urls import path
from img_upload import views

app_name = 'img'

urlpatterns = [
    path('<int:pk>/', views.ImgView.as_view(), name='img_url'),
]