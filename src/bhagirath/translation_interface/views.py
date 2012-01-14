from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.forms import save_instance
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from forms import UploadForm,LoginForm,TranslateForm
from models import Task,Microtask,UserHistory
import datetime

def home(request): 
    data = {
        'form': LoginForm(),
    } 
    return render_to_response('translation_interface/login/login.html',data,context_instance=RequestContext(request))
 
def processSignin(request):
    uname = request.POST['login_username']
    passwd = request.POST['login_password']
    user = auth.authenticate(username=uname, password=passwd)
    if user is not None and user.is_active:
        auth.login(request, user)
        data = {
                'form': LoginForm(),
                'uid':user.id,
                'message':"You're logged in successfully!!!",
        }   
        return render_to_response('translation_interface/translate/userhome.html',data,context_instance=RequestContext(request))
    else:
        data = {
             'form': LoginForm(),
             'message':"Incorrect username or password!!!",
        }       
        return render_to_response('translation_interface/login/uname_passwd_incorrect.html',data,context_instance=RequestContext(request))
 
def processSignout(request):     
    auth.logout(request)
    data = {
        'form': LoginForm(),
        'message':"You're logged out successfully!!!",
    } 
    return render_to_response('translation_interface/login/login.html',data,context_instance=RequestContext(request))
 
       
def processSignup(request): 
    if request.method == 'POST':
        count = 0
        passwd1 = request.POST['password']
        passwd2 = request.POST['cpasswd']
        nemail = request.POST['email']
        nuname = request.POST['username']
        nfname = request.POST['first_name']
        nlname = request.POST['last_name']
        

        a = User.objects.all()
        if passwd1 == passwd2:
            if nemail and nuname and nfname and nlname:
                for j in a:
                    em = a.filter(email=request.POST['email'])
                    for j in em:
                        count +=1
                    if count !=0:
                        data = {
                                'form': LoginForm(),
                        }
                        return render_to_response('translation_interface/login/unique_email_error.html',data,context_instance=RequestContext(request))
                a = User.objects.all()
                count = 0
                for j in a:
                    us = a.filter(username = nuname)
                    for j in us:
                        count +=1
                    if count != 0:
                        data = {
                                'form': LoginForm(),
                        }
                        return render_to_response('translation_interface/login/unique_uname_error.html',data,context_instance=RequestContext(request))
                
                u = User(username=request.POST['username'], is_active=True, email=request.POST['email'], first_name=request.POST['first_name'], last_name = request.POST['last_name'])
                u.save()
                u.set_password(request.POST['password'])
                u.save()
                user = User.objects.get(username=request.POST['username'])
                user.userprofile_set.create(language=request.POST['language'],ip_address = request.META['REMOTE_ADDR'],current_load=0)
            else:
                data = {
                    'form': LoginForm(),
                    }
                return render_to_response('translation_interface/login/signup_null_error.html',data,context_instance=RequestContext(request))
        else:
            data = {
                    'form': LoginForm(),
                    'message':"Confirm password correctly!!!",
            } 
            return render_to_response('translation_interface/login/confirm_passwd_error.html',data,context_instance=RequestContext(request))
        data = {
                    'form': LoginForm(),
        }
        return render_to_response('translation_interface/login/success.html',data,context_instance=RequestContext(request))
  
    
def upload(request):   
    user = request.user
    uid = user.pk
    data = {
        'form': UploadForm(),
        'uid': uid,
    }
    return render_to_response('translation_interface/translate/upload.html',data,context_instance=RequestContext(request))

def processUpload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newtask = Task()
            newtask.html_doc_name = request.FILES['html_doc_content'].name
            newtask.upload_timestamp = datetime.datetime.now()
            newtask.interest_tags = " "
            newtask.budget = 1
            newtask.time_to_publish = datetime.datetime.now()+datetime.timedelta(365/12)
            newtask.dampening_factor = 0.5
            newtask.current_average_stability = 0.0
            save_instance(form, newtask)
    return HttpResponseRedirect(reverse('upload'))
   
def translate(request,uid):
    user = request.user
    if user.is_authenticated():
        logged_in_user_id = uid 
        available_sentences_not_done_by_user = UserHistory.objects.filter(current_active_tag=1).exclude(user=logged_in_user_id)
        available_sentences_done_by_user = UserHistory.objects.filter(current_active_tag=1,user=logged_in_user_id)
        available_sentences = UserHistory.objects.filter(current_active_tag=1).exclude(user=logged_in_user_id)
        
        u = User.objects.filter(id=logged_in_user_id)
        count = 0
        c = 0
        i = 0
        
        for j in available_sentences_done_by_user:
            available_sentences = available_sentences.exclude(original_sentence = available_sentences_done_by_user[i])
            i +=1
        
        for j in available_sentences:
            count +=1
       
        if count==0:
            i = 0
            microtasks = Microtask.objects.filter(assigned = 0)
            for j in available_sentences_done_by_user:
                microtasks = microtasks.exclude(original_sentence = available_sentences_done_by_user[i])
                i +=1
            for j in microtasks:
                c += 1
            if c==0:
                return render_to_response('translation_interface/translate/nodata.html',context_instance=RequestContext(request))
            else:
                m = microtasks[0]
                h = UserHistory()
                h.task = m.task
                h.subtask = m.subtask
                h.microtask = m
                h.original_sentence = m.original_sentence
                h.translated_sentence = m.translated_sentence
                h.current_active_tag = 0
                h.user = u[0]
                h.hop_count = 1
                h.save()
                data = {
                        'form': TranslateForm(instance=h),
                        'curr_id':h.id,
                        'uid': uid,
                        'english': m.original_sentence,
                        'hindi': m.translated_sentence,
               }
                m.assigned=True
                m.save()
                return render_to_response('translation_interface/translate/translate.html',data,context_instance=RequestContext(request))
        else:
            m = available_sentences[0]
            sid = m.id
            new_userhistory = UserHistory()
            new_userhistory.subtask = m.subtask
            new_userhistory.task = m.task
            new_userhistory.microtask = m.microtask
            new_userhistory.original_sentence = m.original_sentence
            new_userhistory.stability = m.stability
            new_userhistory.hop_count = m.hop_count + 1
            new_userhistory.change_flag = 0
            new_userhistory.time_to_live = m.time_to_live
            new_userhistory.status_flag = "Raw"
            new_userhistory.current_active_flag = 0
            new_userhistory.user = u[0]
            new_userhistory.save()
            data = {
                'form': TranslateForm(instance=m),
                'curr_id':sid,
                'uid': uid,
                'english': m.original_sentence,
                'hindi':m.transliterated_sentence,
            }
            return render_to_response('translation_interface/translate/translate.html',data,context_instance=RequestContext(request))
    else:
        return HttpResponse("Please login.You're not logged in!!!")
 
def translationDone(request,id,uid):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            english =request.POST['original_sentence']
            hist = UserHistory.objects.filter(user = uid, original_sentence = english)
            h = hist[0]
            transliterated_text = request.POST['output']
            h.translated_sentence = transliterated_text
            h.transliterated_sentence = request.POST['input']
            h.current_active_tag = 1
            h.change_flag = 1
            h.status_flag = 'Reviewed'
            h.save()
            data = {
                    'form': TranslateForm(),
                    'uid': uid,
                    'curr_id':h.id,
                    'english': h.original_sentence,
                    'hindi':h.transliterated_sentence,
                    }
        
    return render_to_response('translation_interface/translate/translate.html',data,context_instance=RequestContext(request))
    