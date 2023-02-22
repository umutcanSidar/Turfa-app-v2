from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from .forms import ContactForm, LoginForm
from django.core import mail
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from .models import User, AboutModel, ContactModel, BlogModel, ServiceModel, StatusModel
from candidate.models import CandidateModel 
from .forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class StatusView(View,LoginRequiredMixin):
    template_name="status.html"
    context={}
    login_url="/login/"


    def post(self, request):   
        if request.method=="POST":
            status_pk = request.POST["id"]
            candidate_status = request.POST["status"]
            user = request.user

            if user.is_authenticated:
                if candidate_status == "1":
                    updateStatus = StatusModel.objects.filter(id=status_pk).update(user=None, status=candidate_status)
                else:
                    updateStatus = StatusModel.objects.filter(id=status_pk).update(status=candidate_status, user=user)
                return HttpResponseRedirect("/status/")            

        return render(request, self.template_name, self.context)

    def get(self, request):

        self.context["candidate_candidate"] = StatusModel.objects.filter(status=True)
        self.context["candidate_choosen"] = StatusModel.objects.filter(user=request.user, status=False)
       
        return render(request, self.template_name, self.context)
    
class ServiceDetailsView(View):
    template_name="services-detail.html"
    model=ServiceModel

    def get(self, request, *args, **kwargs):
        if "candidate" in request.get_full_path():
            services = self.model.objects.filter(role=False).first()
        else:
            services = self.model.objects.filter(role=True).first()

        return render(request, self.template_name, {'services': services})
    
class ErrorView(View):
    template_name="error.html"

    def get(self, request):
        return render(request, self.template_name)

class SuccesView(View):
    template_name="success.html"

    def get(self, request):
        return render(request, self.template_name)

# class ForgotPasswordView(View):
#     template_name="forgot-password.html"

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         return render(request, self.template_name)

class RegisterView(View):
    template_name="register.html"
    success_url="/success/"

    def get(self, request):

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name)

    def post(self, request):
        if request.method == "POST":

            email=request.POST['email']
            password=request.POST['password']
            role=request.POST['role']

            try:
                user = User.objects.filter(email=email).first()

                if user is not None:
                    return render(request, self.template_name, {'error':_("Kullanıcı mevcut")})
                else:
                    newuser = User.objects.create_user(email=email, password=password, role=role)
                    newuser.save()

                    login(request, newuser)

                    return HttpResponseRedirect("/")  
            except IntegrityError:
                # user already exists
                return render(request, self.template_name, {'error':_("Kullanıcı mevcut")})
        else:
            return HttpResponseRedirect("/error/")
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

class LoginView(View):
    template_name="login.html"
    success_url="/"
    form_class=LoginForm


    def get(self, request):

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name)

    def post(self, request):
        if request.method == "POST":
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.success_url)
            else:
                return render(request, self.template_name, {'error': _("Kullanıcı adı veya Parolayı kontrol ediniz!")})

        else:
            return HttpResponseRedirect("/error/")

class HomeView(View):
    template_name="home.html"
    context={}

    def get(self, request):
        if "candidate" in request.get_full_path(): 
            self.context['services'] = ServiceModel.objects.filter(role=False)
            self.context['blog'] = BlogModel.objects.filter(role=True)
        else:
            self.context['services'] = ServiceModel.objects.filter(role=True)
            self.context['blog'] = BlogModel.objects.filter(role=False)

        return render(request, self.template_name, self.context)
    
class AboutView(View):
    template_name="about.html"
    model=AboutModel

    def get(self, request):

        role_url=request.get_full_path()

        if "candidate" in role_url:
            about = self.model.objects.filter(isActive=True, role=False).first()
        else:
            about = self.model.objects.filter(isActive=True, role=True).first()

        return render(request, self.template_name, {'about': about})
    
class BlogView(View):
    template_name="blog-list.html"
    model=BlogModel

    def get(self, request):
        role_url=request.get_full_path()

        if "candidate" in role_url:
            all_blog = self.model.objects.all().filter(role=True)
        else:
            all_blog = self.model.objects.all().filter(role=False)

        return render(request, self.template_name, {'all_blog':all_blog})
    
class BlogDetailView(View):
    template_name="blog-detail.html"
    model=BlogModel

    def get(self, request, *args, **kwargs):
        role_url=request.get_full_path()

        if "candidate" in role_url:
            all_blog = self.model.objects.filter(role=True,slug=kwargs['slug']).first()
        else:
            all_blog = self.model.objects.filter(role=False,slug=kwargs['slug']).first()

        return render(request, self.template_name, {'all_blog':all_blog})
    
class ContactView(View):
    template_name="contact.html"
    form_class= ContactForm
    success_url="/success/"
    model=ContactModel
    
    def post(self, request):
        if request.method == "POST":
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            message=request.POST['message']


            html="isim:"+name+"\nemail: "+email+"\nphone: "+phone+"\nmessage: "+message

            mail.send_mail(_("İletişim"), html, 'from@example.com', ['umutcansidar@gmail.com'], fail_silently=False)
            assert len(mail.outbox) == 1

            return HttpResponseRedirect(self.success_url)
    
    def get(self, request):

        role_url=request.get_full_path()
        context={
            'form': self.form_class()
        }

        if "candidate" in role_url:
            context['contact'] = self.model.objects.filter(role=False).first()
        else:
            context['contact'] = self.model.objects.filter(role=True).first()

        # contact=self.model.objects.filter(role=)

        return render(request, self.template_name, context)