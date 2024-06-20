from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("toggle_follow/<int:follow_id>/", views.toggle_follow, name="toggle_follow"),
    path("posting", views.posting, name="posting"),
    path("allP", views.allP, name="allP"),
     path('update_post/<int:post_id>/', views.update_post, name='update_post'),
     path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path("following",views.following, name="following"),
    path("profile/<int:user_id>/", views.profile, name="profile"),  
]
