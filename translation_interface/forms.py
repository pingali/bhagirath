from django import forms
from django.contrib.auth.models import User
from models import Task,UserHistory

class LoginForm(forms.models.ModelForm):
    class Meta:
        model = User
               
class UploadForm(forms.models.ModelForm):
    class Meta:
        model = Task
        exclude = ('upload_timestamp','html_doc_name','interest_tags','budget','duration','dampening_factor','current_average_stability')
      
class TranslateForm(forms.models.ModelForm):
    class Meta:
        model = UserHistory
       
    def __init__(self, *args, **kwargs):
        super(TranslateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
            self.fields[key].widget.attrs['readonly'] = 'readonly'
            
        
            
            