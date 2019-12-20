from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/page', views.sign_in_page, name='sign_in_page'),
    path('signin', views.sign_in, name='sign_in'),
    path('register/page', views.register_page, name='register_page'),
    path('register', views.register, name='register'),
    path('logoff', views.logoff, name='logoff'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('users/show/<int:user_id>', views.user_info, name='user_info'),
    path('post/create/<int:user_id>', views.new_post, name='new_post'),
    path('post/comment/<int:post_id>', views.new_post_comment, name='new_post_comment'),
]