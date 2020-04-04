from django.urls import path, include
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.PhotoWall.as_view(), name='indexpage'),
    path('accounts/register/',views.register,name='register'),
    path('download/images/<int:id>/',views.download_image,name='download_image'),
    path('user/dashboard/',views.Dashboard.as_view(),name='dashboard'),
    path('upload/<str:room_code>/', views.UploadPhoto.as_view(), name='upload_photo'),
    path('photowall/<str:photo_room>/', views.PhotoWallIndex.as_view(), name='photo_wall'),
    path('photowall/<str:photo_room>/slideshow/', views.Photowallslideshow.as_view(), name='photo_wall_slideshow'),
    path('search_photo_room/', views.SearchPhotoRoom.as_view(), name='search_photo_room'),
    path('create_party_room/', views.CreatePhotoRoom.as_view(), name='create_party_room'),
    ]
