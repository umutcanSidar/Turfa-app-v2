from django.urls import path, include
from .views import CandidateFormView, CandidateServiceDetailsView, HomeView
from home.views import ContactView, AboutView, BlogView, BlogDetailView, ServiceDetailsView

urlpatterns = [
    path("", HomeView.as_view(), name="candidate_home"),
    path("form/", CandidateFormView.as_view(), name="candidate_form"),

    path("contact/",ContactView.as_view(), name="candidate_contact"),
    path("about/",AboutView.as_view(), name="candidate_about"), 


    path("blog/",BlogView.as_view(), name="candidate_blog"),
    path("blog/<slug:slug>/",BlogDetailView.as_view(), name="candidate_blog_detail"),


    path("services/<slug:slug>/",ServiceDetailsView.as_view(), name="candidate_services_detail"),
    
]
