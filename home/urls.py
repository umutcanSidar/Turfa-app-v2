from django.urls import path, include
from .views import HomeView, BlogView, ContactView, LoginView, RegisterView, SuccesView, LogoutView, AboutView,ServiceDetailsView, BlogDetailView, StatusView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("",HomeView.as_view(), name="home"),
    
    path("status/",login_required(StatusView.as_view()), name="status"),

    path("services/<slug:slug>/",ServiceDetailsView.as_view(), name="services_detail"),

    path("blog/",BlogView.as_view(), name="blog-list"),
    path("blog/<slug:slug>/",BlogDetailView.as_view(), name="blog_detail"),
   
    path("contact/",ContactView.as_view(), name="contact"),
    path("about/",AboutView.as_view(), name="about"), 

    # User
    path("login/",LoginView.as_view(), name="login"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("register/",RegisterView.as_view(), name="register"),
    
    path("reset_password/",auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    
    path("success/", SuccesView.as_view(), name="success"),
    path("error/", SuccesView.as_view(), name="error"),

    # CANDIDATE FORM
    path("candidate/", include("candidate.urls"))
]