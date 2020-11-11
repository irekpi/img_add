from django.urls import path
from rest_framework import routers
from img_upload import views_api, views

app_name = 'img'

router = routers.DefaultRouter()
router.register('img_list', views_api.ImagesViewSet)


urlpatterns = [
    path('<int:pk>/<int:height>/<int:width>/', views.ImgView.as_view(), name='img_url'),
]
urlpatterns += router.urls
