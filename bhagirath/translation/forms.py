from django import forms
from django.contrib.auth import authenticate
from django.contrib.admin import widgets  
from captcha.fields import ReCaptchaField
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from bhagirath.translation.models import *

class SplitDateTimeJSField(forms.SplitDateTimeField):
    def __init__(self, *args, **kwargs):
        super(SplitDateTimeJSField, self).__init__(*args, **kwargs)
        self.widget.widgets[0].attrs = {'class': 'vDateField'}
        self.widget.widgets[1].attrs = {'class': 'vTimeField'}  

class DateJSField(forms.SplitDateTimeField):
    def __init__(self, *args, **kwargs):
        super(DateJSField, self).__init__(*args, **kwargs)
        self.widget.widgets[0].attrs = {'class': 'vDateField'}
      
class LoginForm(forms.models.ModelForm):
    class Meta:
        model = User
        
    username = forms.CharField(max_length=50)
    password = forms.CharField( widget=forms.PasswordInput)  
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct username and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

class SignUpForm(forms.models.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {'date_of_birth':DateJSField(required=False,), 
                   'translator':forms.CheckboxInput,
                   'contributor':forms.CheckboxInput,
                   'evaluator':forms.CheckboxInput,
                 }
    EXPERTISE_CHOICES = (('1', '1'),
                         ('2', '2'),
                         ('3', '3'))

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField( widget=forms.PasswordInput)
    confirm_password = forms.CharField( widget=forms.PasswordInput)
    district = forms.ModelChoiceField(queryset=Master_GeographicalRegion.objects.all(),widget=forms.Select)
    language = forms.ModelMultipleChoiceField(queryset=Master_LanguageExpertise.objects.all())
    interests = forms.ModelMultipleChoiceField(queryset=Master_InterestTags.objects.all())
    education_qualification = forms.ModelChoiceField(queryset=Master_EducationQualification.objects.all(),widget=forms.Select)
    domain = forms.ModelChoiceField(queryset=Master_EducationDomain.objects.all(),widget=forms.Select)
    medium_of_education_during_school = forms.ModelChoiceField(queryset=Master_Language.objects.all(),widget=forms.Select)
    #competence_for_each_language      
    captcha = ReCaptchaField(label="Please enter text you see or hear")
    
   
    
    def __init__(self, *args, **kwargs):      
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = widgets.AdminDateWidget()
    
    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        city = self.cleaned_data.get('city')
        translator = self.cleaned_data.get('translator')
        contributor = self.cleaned_data.get('contributor')
        evaluator = self.cleaned_data.get('evaluator')
        interests = self.cleaned_data.get('interests')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password') 
        language = self.cleaned_data.get('language')     
        
        if password == confirm_password:
            if username and email and first_name and last_name and date_of_birth and city:
                pass 
                if not translator:
                    self.cleaned_data.setdefault('translator')
                if not contributor:
                    self.cleaned_data.setdefault('contributor')
                if not evaluator:
                    self.cleaned_data.setdefault('evaluator')    
            else:
                raise forms.ValidationError("Please enter all * marked fields are case-sensitive.") 
        else:
            raise forms.ValidationError("Please confirm password correctly.")
        
        return self.cleaned_data
                  
class UploadForm(forms.models.ModelForm):
    UPLOAD_CHOICES = (('external', 'Provide URL'), ('internal', 'Attach a File'))
    SPECIFICATION_CHOICES = (('default', 'Default'), ('Specify', 'Specify'))
    CONTEXT_SIZE_CHOICES = (('1', 'One sentence'), ('2', 'Two sentences'),
                            ('3', 'Three sentences'), ('4', 'Four sentences'))

    class Meta:
        model = Task
        exclude = ('upload_timestamp','budget','dampening_factor','current_average_stability')
        widgets = {

                   'time_to_publish': SplitDateTimeJSField(required=False,)
                  }
    html_doc_content = forms.FileField(help_text="Task"),
    html_doc_name = forms.CharField(max_length=1000)
    upload_type = ChoiceField(widget=RadioSelect, choices=UPLOAD_CHOICES)         
    specifications = ChoiceField(widget=RadioSelect, choices=SPECIFICATION_CHOICES)
    context_size = forms.ChoiceField(widget=forms.Select, choices=CONTEXT_SIZE_CHOICES)
    age_group_tag = forms.ModelChoiceField(queryset=Master_AgeGroup.objects.all(),widget=forms.Select)
    interest_tags = forms.ModelMultipleChoiceField(queryset=Master_InterestTags.objects.all(), widget=forms.CheckboxSelectMultiple())   
    geographical_region = forms.ModelChoiceField(Master_GeographicalRegion.objects.all(),widget=forms.Select)
    #source_language = forms.ModelChoiceField(queryset=Master_Language.objects.all(), widget=forms.Select())
    #source_language = forms.TextInput(default="Hindi",widget=forms.Select())
    target_language = forms.ModelMultipleChoiceField(queryset=Master_Language.objects.all().exclude(language='English'), widget=forms.CheckboxSelectMultiple())    
   
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['time_to_publish'].widget = widgets.AdminSplitDateTime()
      
class TranslateForm(forms.models.ModelForm):
    class Meta:
        model = UserHistory
       
    def __init__(self, *args, **kwargs):
        super(TranslateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
            self.fields[key].widget.attrs['readonly'] = 'readonly'
                   
class UpdateProfileForm(forms.models.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {'date_of_birth':DateJSField(required=False,), 
                   'translator':forms.CheckboxInput,
                   'contributor':forms.CheckboxInput,
                   'evaluator':forms.CheckboxInput,
                }
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField( widget=forms.PasswordInput)
    confirm_password = forms.CharField( widget=forms.PasswordInput)
    district = forms.ModelChoiceField(queryset=Master_GeographicalRegion.objects.all().order_by('geographical_region'),widget=forms.Select)
    language = forms.ModelMultipleChoiceField(queryset=Master_LanguageExpertise.objects.all(), widget=forms.CheckboxSelectMultiple())
    interests = forms.ModelMultipleChoiceField(queryset=Master_InterestTags.objects.all(), widget=forms.CheckboxSelectMultiple())
    education_qualification = forms.ModelChoiceField(queryset=Master_EducationQualification.objects.all(),widget=forms.Select)
    domain = forms.ModelChoiceField(queryset=Master_EducationDomain.objects.all(),widget=forms.Select)
    medium_of_education_during_school = forms.ModelChoiceField(queryset=Master_Language.objects.all(),widget=forms.Select)
    #competence_for_each_language      

    def __init__(self, *args, **kwargs):      
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = widgets.AdminDateWidget()
        self.fields['username'].widget.attrs['readonly'] = True

            