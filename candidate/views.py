from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView
from .forms import CandidateForm, ExperienceForm, EducationForm
from django.forms import formset_factory
from .models import CandidateModel, ExperienceModel, EducationModel
from home.models import ServiceModel, BlogModel, StatusModel
from django.core import mail
from django.utils.translation import gettext as _

# Create your views here.

class CvView(View):
    template_name = "admin/cv.html"
    context={}

    def get(self, request, *args, **kwargs):
        self.context["info"] = CandidateModel.objects.get(pk=kwargs["pk"])
        self.context["experiences"] = ExperienceModel.objects.get(candidate=kwargs["pk"])
        self.context["education"] = EducationModel.objects.get(candidate=kwargs["pk"])

        return render(request, self.template_name, self.context)


class HomeView(View):
    template_name="customer/home.html"
    context={}

    def get(self, request):
        if "candidate" in request.get_full_path(): 
            self.context['services'] = ServiceModel.objects.filter(role=False)
            self.context['blog'] = BlogModel.objects.filter(role=True)
        else:
            self.context['services'] = ServiceModel.objects.filter(role=True)
            self.context['blog'] = BlogModel.objects.filter(role=False)
        return render(request, self.template_name, self.context)
    
class CandidateServicesView(View):
    template_name="services-detail.html"
    model=ServiceModel

    def get(self, request, *args, **kwargs):
        if "candidate" in request.get_full_path():
            services = self.model.objects.filter(role=False).first()
        else:
            services = self.model.objects.filter(role=True).first()

        return render(request, self.template_name, {'services': services})

class CandidateServiceDetailsView(View):
    template_name="services-detail.html"

    def get(self, request):
        if "candidate" in request.get_full_path():
            services = self.model.objects.filter(role=False).first()
        else:
            services = self.model.objects.filter(role=True).first()

        return render(request, self.template_name, {'services': services})

class CandidateFormView(View):
    template_name="customer/form.html"
    success_url="/success/"

    candidate_form=CandidateForm
    experiences_form=formset_factory(ExperienceForm, max_num=3)
    educations_form=EducationForm

    def get(self, request):

        return render(request, self.template_name, {'forms': {
            'candidate_form': self.candidate_form, 'experiences_form': self.experiences_form, 'educations_form':self.educations_form
        }})
    
    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            name = request.POST["name"]
            surname = request.POST["surname"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            tc = request.POST["tc"]
            children = request.POST["children"]
            birthday =request.POST['birthday_year']  + "-" + request.POST['birthday_month'] + "-" + request.POST["birthday_day"]
            martial_status = request.POST["martial_status"] == 0 if False else True
            city = request.POST["city"]
            postcode = request.POST["postcode"]
            address = request.POST["address"]
            photo = request.POST["photo"]
            
            institution_name=request.POST['form-0-institution_name']
            position=request.POST['form-0-position']
            work_address=request.POST['form-0-work_address']
            ref_name=request.POST['form-0-ref_name']
            institution_email=request.POST['form-0-institution_email']
            institution_phone=request.POST['form-0-institution_phone']
            entry_date= request.POST['form-0-entry_date_year'] + "-" + request.POST['form-0-entry_date_month'] + "-" + request.POST['form-0-entry_date_day']
            quit_date= request.POST['form-0-quit_date_year'] + "-" + request.POST['form-0-quit_date_month'] + "-" + request.POST['form-0-quit_date_day']

            new_candidate = CandidateModel(
                name=name,
                surname=surname,
                email=email,
                phone=phone,
                tc=tc,
                children=children,
                birthday=birthday,
                martial_status=martial_status,
                city=city,
                postcode=postcode,
                address=address,
                photo=photo,
                status=0
            )

            new_experience = ExperienceModel(
                institution_name=institution_name,
                position=position,
                work_address=work_address,
                ref_name=ref_name,
                institution_email=institution_email,
                institution_phone=institution_phone,
                entry_date=entry_date,
                quit_date=quit_date,
                candidate=new_candidate
            )

            new_candidate.save()
            new_experience.save()
            
            if request.POST.get('form-1-institution_name', False):
                institution_name1=request.POST['form-1-institution_name']
                position1=request.POST['form-1-position']
                work_address1=request.POST['form-1-work_address']
                ref_name1=request.POST['form-1-ref_name']
                institution_email1=request.POST['form-1-institution_email']
                institution_phone1=request.POST['form-1-institution_phone']
                entry_date1=request.POST['form-1-entry_date_year'] + "-" + request.POST['form-1-entry_date_month'] + "-" + request.POST['form-1-entry_date_day']
                quit_date1=request.POST['form-1-quit_date_year'] + "-" + request.POST['form-1-quit_date_month'] + "-" + request.POST['form-1-quit_date_day']
                
                new_experience1 = ExperienceModel(
                    institution_name=institution_name1,
                    position=position1,
                    work_address=work_address1,
                    ref_name=ref_name1,
                    institution_email=institution_email1,
                    institution_phone=institution_phone1,
                    entry_date=entry_date1,
                    quit_date=quit_date1,
                    candidate=new_candidate
                )

                new_experience1.save()

            if request.POST.get('form-2-institution_name', False):
                institution_name2=request.POST['form-2-institution_name']
                position2=request.POST['form-2-position']
                work_address2=request.POST['form-2-work_address']
                ref_name2=request.POST['form-2-ref_name']
                institution_email2=request.POST['form-2-institution_email']
                institution_phone2=request.POST['form-2-institution_phone']
                entry_date2=request.POST['form-2-entry_date_year'] + "-" + request.POST['form-2-entry_date_month'] + "-" + request.POST['form-2-entry_date_day']
                quit_date2=request.POST['form-2-quit_date_year'] + "-" + request.POST['form-2-quit_date_month'] + "-" + request.POST['form-2-quit_date_day']
                
                new_experience2 = ExperienceModel(
                    institution_name=institution_name2,
                    position=position2,
                    work_address=work_address2,
                    ref_name=ref_name2,
                    institution_email=institution_email2,
                    institution_phone=institution_phone2,
                    entry_date=entry_date2,
                    quit_date=quit_date2
                )

                new_experience2.save()

            # EDUCATION
            university_name=request.POST['university_name']
            departman=request.POST['departman']
            doctorate=request.POST['doctorate']
            degree=request.POST['degree']
            phd=request.POST['phd']
            uni_entry_date=request.POST['entry_date_year'] + "-" + request.POST['entry_date_month'] + "-" + request.POST['entry_date_day']
            uni_graduated_at=request.POST['graduated_at_year'] + "-" + request.POST['graduated_at_month'] + "-" + request.POST['graduated_at_day']
            

            new_education = EducationModel(
                university_name=university_name,
                departman=departman,
                doctorate=doctorate,
                degree=degree,
                phd=phd,
                entry_date=uni_entry_date,
                graduated_at=uni_graduated_at,
                candidate=new_candidate
            )

            new_education.save()

            if request.POST.get('form-1-university_name'):
                university_name1=request.POST['form-1-university_name']
                departman1=request.POST['form-1-departman']
                doctorate1=request.POST['form-1-doctorate']
                degree1=request.POST['form-1-degree']
                phd1=request.POST['form-1-phd']
                uni_entry_date1=request.POST['form-1-entry_date_year'] + "-" + request.POST['form-1-entry_date_month'] + "-" + request.POST['form-1-entry_date_day']
                uni_graduated_at1=request.POST['form-1-graduated_at_year'] + "-" + request.POST['form-1-graduated_at_month'] + "-" + request.POST['form-1-graduated_at_day']
                
                new_education1 = EducationModel(
                    university_name=university_name1,
                    departman=departman1,
                    doctorate=doctorate1,
                    degree=degree1,
                    phd=phd1,
                    entry_date=uni_entry_date1,
                    graduated_at=uni_graduated_at1,
                    candidate=new_candidate
                )

                new_education1.save()

            if request.POST.get('form-2-university_name'):
                university_name2=request.POST['form-2-university_name']
                departman2=request.POST['form-2-departman']
                doctorate2=request.POST['form-2-doctorate']
                degree2=request.POST['form-2-degree']
                phd2=request.POST['form-2-phd']
                uni_entry_date2=request.POST['form-2-entry_date_year'] + "-" + request.POST['form-2-entry_date_month'] + "-" + request.POST['form-2-entry_date_day']
                uni_graduated_at2=request.POST['form-2-graduated_at_year'] + "-" + request.POST['form-2-graduated_at_month'] + "-" + request.POST['form-2-graduated_at_day']
                
                new_education2 = EducationModel(
                    university_name=university_name2,
                    departman=departman2,
                    doctorate=doctorate2,
                    degree=degree2,
                    phd=phd2,
                    entry_date=uni_entry_date2,
                    graduated_at=uni_graduated_at2,
                    candidate=new_candidate
                )

                new_education2.save()


            newStatus = StatusModel(candidates=new_candidate, status="0")

            html="Yeni bir başvuru geldi!\nisim:"+name+"\neposta: "+email+"\nTelefon: "+phone+"\n<a href='https://türfa.de' target='_blank'>Buradan</a> düzenleyebilirsin."
            newStatus.save()
           
            mail.send_mail(_("Başvuru"), html, 'postmaster-web@tuerfa.de', ['kilavuz.berker@tuerfa.de','kulke.nikko@tuerfa.de'], fail_silently=False)

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'forms': {
           'candidate_form': self.candidate_form, 'experiences_form': self.experiences_form, 'educations_form':self.educations_form
        }})