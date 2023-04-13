from django.urls import path
from django .contrib.auth import views as auth_views
from .import views

urlpatterns = [
#register/login paths
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

#main paths
    path('', views.home,name="home"),
    path('user/', views.userPage, name="user-page"),
    path('students/', views.students,name="students"),
    path('teacher/<str:pk_test>/', views.teachers,name="teacher"),
    path('units/', views.units,name="unit"),

#units creation paths
    path('create_unit/<str:pk>/',views.createUnit,name="create_unit"),
    path('update_unit/<str:pk>/', views.updateUnit, name="update_unit"),
    path('delete_unit/<str:pk>/', views.deleteUnit, name="delete_unit"),

#notes upload paths
    path('books/upload/', views.upload_book, name='upload_book'),
    path('book_list/', views.book_list, name="book_list"),
    path('books/<int:pk>/', views.delete_book, name='delete_book'),


#reset password paths
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="events/password_reset.html"),name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="events/password_reset_sent.html"),name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="events/password_reset_form.html"),name="password_reset_confrim"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="events/password_reset_done.html"),name="password_reset_complete"),

#chatbot paths
    path('/', views.chat, name='chat'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),


]

#continue video 20
