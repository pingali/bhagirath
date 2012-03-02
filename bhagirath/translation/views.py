from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth.models import Group,Permission
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core import serializers
from bhagirath.translation.forms import *
from bhagirath.translation.models import *
from bhagirath.translation.subtask_parser import subtaskParser
from bhagirath.translation.microtask_parser import microtaskParser
from bhagirath.centoid_score.CentroidFinder import CentroidFinder 
import captcha
import traceback
import logging
import os

def findpath(path):
    parent_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(parent_dir,path))

log = logging.getLogger("translation.views")
path = 'rolling_log'
rolling_handler = logging.handlers.RotatingFileHandler(path, maxBytes=52428800)
log.addHandler(rolling_handler)


def home(request):
    """
    This function displays some information about bhagirath project, current statistics, 
    weekly and overall top users and provides login facility to the user. 
    """
    (u,a,s) = stats()
    overall_leaderboard = get_overall_leaderboard()
    weekly_leaderboard = get_weekly_leaderboard()
    data = {
            'form': LoginForm(),
            'registered_users':u,
            'translated_sentences':s,
            'published_articles':a,
            'overall_leaderboard':overall_leaderboard,
            'weekly_leaderboard':weekly_leaderboard,
        }
    return render_to_response('login/home.html',data,context_instance=RequestContext(request))

def about_us(request):
    """
    This function gives detailed information about bhagirath along with statistics and leaderboards.
    """
    (u,a,s) = stats()
    overall_leaderboard = get_overall_leaderboard()
    weekly_leaderboard = get_weekly_leaderboard()
    data = {
            'form': LoginForm(),
            'registered_users':u,
            'translated_sentences':s,
            'published_articles':a,
            'overall_leaderboard':overall_leaderboard,
            'weekly_leaderboard':weekly_leaderboard,
        }
    return render_to_response('login/about_us.html',data,context_instance=RequestContext(request))
          
def sample_translations(request,id):
    """
    This function provides sample translations having english sentence, 
    its machine translation and user translation.  
    """
    sample_translations = Master_SampleTranslations.objects.get(pk=id)
    original_sentence = sample_translations.original_sentence;
    google_translation = sample_translations.google_translation;
    user_translation = sample_translations.user_translation;
    
    count = Master_SampleTranslations.objects.all().count()
 
    if int(id) == int(count):
        next_id = 1
    else:
        next_id = int(id) + 1
    
    if int(id) == 1:
        prev_id = int(count)
    else:
        prev_id = int(id) - 1
        
    data = {
            'original_sentence':original_sentence,
            'google_translation':google_translation,
            'user_translation':user_translation,
            'next_id':next_id,
            'prev_id':prev_id
        }
    return render_to_response('login/sample_translations.html',data,context_instance=RequestContext(request))

def sign_up(request):
    """
    This function loads sign up form for new user's registration. 
    """
    l = find()
    data = {
        'form': SignUpForm(),
        'list':l,
        'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
    }
    return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
    
def process_sign_up(request):
    """
This function is used to process information provided by user while registration.
It performs several checks over the data entered by user like the entered recaptcha,
password as well as confirmed password, unique username and email-id. If all entries
are valid and all checks are passed it registers the user by creating a record in User and UserProfile models.
"""
    user = request.user
    if request.method == 'POST':
        check_captcha = captcha.client.submit(request.POST['recaptcha_challenge_field'],
                                       request.POST['recaptcha_response_field'],
                                       settings.RECAPTCHA_PRIVATE_KEY,
                                       request.META['REMOTE_ADDR'])
        
        if check_captcha.is_valid:
            f_password = request.POST['password']
            f_confirm_password = request.POST['confirm_password']
            f_email = request.POST['email']
            f_username = request.POST['username']
            f_first_name = request.POST['first_name']
            f_last_name = request.POST['last_name']
            f_gender = request.POST['gender']
            f_date_of_birth = request.POST['date_of_birth']
            f_grp = request.POST['groups'].upper()
                 
            if request.POST.has_key('translator'):
                f_translator = request.POST['translator']
            else:
                f_translator = False
            if request.POST.has_key('contributor'):
                f_contributor = request.POST['contributor']
            else:
                f_contributor = False
            if request.POST.has_key('evaluator'):
                f_evaluator = request.POST['evaluator']
            else:
                f_evaluator = False
                      
            try:
                count = 0
                if f_password == f_confirm_password:
                    if f_email and f_username and f_first_name and f_last_name and f_gender and f_date_of_birth and f_grp:
                        count = User.objects.filter(email=f_email).count()
                        if count !=0:
                            data = {
                                'form': SignUpForm(request.POST),
                                'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False),
                                }
                            messages.error(request,"EmailID already in use.Try another one!!!")
                            log.error("Exisiting email-id used while user-registration.")
                            return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                        
                        count = User.objects.all().filter(username = f_username).count()
                                
                        if count != 0:
                            data = {
                                'form': SignUpForm(request.POST),
                                'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False),
                                }
                            messages.error(request,"Username already in use.Try another one!!!")
                            log.error("Exisiting username used while user-registration.")
                            return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                        
                        u = User.objects.create_user(f_username, f_email, f_password)
                        u.is_active = True
                        u.first_name =f_first_name
                        u.last_name = f_last_name
                        u.save()
                        u.set_password(f_password)
                        u.save()
                        try:
                            g = Group.objects.get(name=f_grp)
                            u.groups.add(g)
                            u.save()
                        except:
                            g = Group.objects.filter(name=f_grp)
                            if g:
                                u.groups.add(g)
                                u.save()  
                            else:
                                g = Group()
                                g.name = f_grp
                                g.save()
                                u.groups.add(g)
                                u.save()
                            
                        user = User.objects.get(username__exact=f_username)
                        
                        #user.userprofile_set.create(date_of_birth=f_date_of_birth,ip_address=request.META['REMOTE_ADDR'],gender=f_gender,
                        #                           translator=f_translator,contributor=f_contributor,evaluator=f_evaluator)
                        p = UserProfile()
                        p.user = user
                        p.date_of_birth = f_date_of_birth
                        p.ip_address = request.META['REMOTE_ADDR']
                        p.gender = f_gender
                        p.translator = f_translator
                        p.contributor = f_contributor
                        p.evaluator = f_evaluator
                        p.save()
                        
                        userpro = UserProfile.objects.get(user=user)
                        
                        if request.POST.getlist('language'):
                            all_language = request.POST.getlist('language')
                            
                            for l in all_language:
                                id = int(l)
                                f_language = Master_Language.objects.get(pk=id)
                                userpro.language.add(f_language)
                        
                        if request.POST.has_key('medium_of_education_during_school'):
                            medium_of_education_during_school = request.POST['medium_of_education_during_school']
                            
                            for l in medium_of_education_during_school:
                                id = int(l)
                                f_medium_of_education_during_school = Master_Language.objects.get(pk=id)
                                userpro.medium_of_education_during_school = f_medium_of_education_during_school
                                userpro.save()
                              
                        if request.POST.has_key('district'):
                            district = request.POST['district']
                            
                            for l in district:
                                id = int(l)
                                f_district = Master_GeographicalRegion.objects.get(pk=id)
                                userpro.district = f_district
                                userpro.save()

                        if request.POST.has_key('education_qualification'):
                            education_qualification = request.POST['education_qualification']
                            
                            for l in education_qualification:
                                id = int(l)
                                f_education_qualification = Master_EducationQualification.objects.get(pk=id)
                                userpro.education_qualification = f_education_qualification
                                userpro.save()
                                
                        if request.POST.has_key('domain'):
                            domain = request.POST['domain']
                            
                            for l in domain:
                                id = int(l)
                                f_domain = Master_EducationDomain.objects.get(pk=id)
                                userpro.domain = f_domain
                                userpro.save()
                        
                        if request.POST.getlist('interests'):
                            all_interests = request.POST.getlist('interests')
                            for i in all_interests:
                                id = int(i)
                                f_interests = Master_InterestTags.objects.get(pk=id)
                                userpro.interests.add(f_interests)
                            
                        data = {
                            'form': SignUpForm(),
                            'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False),
                            }
                        messages.success(request,"Record saved successfully!!!")
                        log.info("User registration successful for %s."%(f_username))
                        return render_to_response('login/home.html',data,context_instance=RequestContext(request))
                    else:
                        data = {
                            'form': SignUpForm(request.POST),
                            'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False),
                            }
                        messages.error(request,"Please fill in all fields!!!")
                        log.error("All fields not entered correctly while user registration.")
                        return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
    
                else:
                    data = {
                        'form': SignUpForm(request.POST),
                        'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False),
                        }
                    messages.error(request,"Confirm password correctly!!!")
                    log.error("Password not confirmed correctly.")
                    return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                return HttpResponseRedirect(reverse('home'))
            except:
                log.exception("User registration failed for %s."%(f_username))
                traceback.print_exc()
                messages.error(request, "Registration Failed!!!Try again.")
               
        else:
            data = {
                'form': SignUpForm(),
                'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False),
                }
            messages.error(request, "Recaptcha entered incorrectly!!!")
            log.error("Recaptcha entered incorrectly while user registration.")
            return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
    return HttpResponse("Registration Failed - Some error occurred!!!")

def process_sign_in(request):
    """
    This function authenticates the user with username and password provided 
    by him and allows login if and only if the user is active.
    """
    uname = request.POST['username']
    passwd = request.POST['password']
    user = auth.authenticate(username=uname, password=passwd)
    if user is not None and user.is_active:
        auth.login(request, user)
        s = Session()
        s.user = user
        s.login_timestamp = datetime.datetime.now()
        s.save()
        msg = "Welcome,%s"%(request.user)   
        next = "/account/"
        messages.success(request,msg)
        log.info("%s logged in succesfully."%(user)) 
        return HttpResponseRedirect(next) 
    else:
        messages.error(request, "Incorrect username or password!!!")
        log.error("Login failed for user: %s."%(uname))   
    return HttpResponseRedirect(reverse('home'))
    
def process_sign_out(request):
    """
    This function is used to logout user successfully from the site.
    """
    user=request.user
    s = Session.objects.filter(user=request.user,logout_timestamp=None)[0]
    s.logout_timestamp = datetime.datetime.now()
    s.save()
    auth.logout(request)
    
    (u,a,s) = stats()
    overall_leaderboard = get_overall_leaderboard()
    weekly_leaderboard = get_weekly_leaderboard()
    data = {
        'form': LoginForm(),
        'registered_users':u,
        'translated_sentences':s,
        'published_articles':a,
        'overall_leaderboard':overall_leaderboard,
        'weekly_leaderboard':weekly_leaderboard,
        } 
    messages.success(request,"Thanks for spending some quality time with the Website today.")
    log.info("%s logged out succesfully."%(user))
    return render_to_response('login/home.html',data,context_instance=RequestContext(request))   

def account(request):
    """
    This function provides information such as current statistics and user's contribution
    as total sentences translated, files uploaded and number of correct translations.
    """
    user = request.user
    uid = user.pk

    if user.is_authenticated():
        (u,a,s) = stats()   
        overall_leaderboard = get_overall_leaderboard()
        weekly_leaderboard = get_weekly_leaderboard()       
        user_pro = UserProfile.objects.filter(user = uid)
        user_profile = user_pro[0]
        data = {
                'uid':uid,
                'total_translated_sentences':user_profile.total_translated_sentences,
                'no_of_perfect_translations': user_profile.no_of_perfect_translations,
                'total_uploaded_tasks':user_profile.total_uploaded_tasks,
                'total_evaluated_sentences':user_profile.total_evaluated_sentences,
                'registered_users':u,
                'translated_sentences':s,
                'published_articles':a,
                'username':user,
                'overall_leaderboard':overall_leaderboard,
                'weekly_leaderboard':weekly_leaderboard,
        } 
        log.info("%s visited its home page."%(user))
        return render_to_response('translation/account.html',data,context_instance=RequestContext(request))
    else:
        data = {
        'form': LoginForm(),
        'uid':uid,
        'registered_users':u,
        'translated_sentences':s,
        'published_articles':a,
        } 
        messages.error(request,"You're not logged in!!!")
        log.error("%s made request before login."%(user))
        return render_to_response('login/home.html',data,context_instance=RequestContext(request)) 

def upload(request):   
    """
    This function is used for uploading files for translation. 
    User has to provide information about file,language in which it is to be translated,
    interest tags, age group and region of people by whom it is to be translated, 
    number of sentences that should be given at a time for translation.
    """
    user = request.user
    uid = user.pk
    if user.is_authenticated():
        data = {
            'form': UploadForm(),
            'uid':  uid,
            'username':user,
             }
        ta = TransactionAction()
        ta.session = Session.objects.filter(user=user,logout_timestamp=None)[0]
        ta.user = user
        ta.action = Master_Action.objects.filter(action="Upload")[0]
        ta.action_timestamp = datetime.datetime.now()
        ta.save()
        log.info("%s visited upload form."%(user))
        return render_to_response('translation/upload.html',data,context_instance=RequestContext(request))
    else:
        (u,a,s) = stats()
        data = {
        'form': LoginForm(),
        'username':user,
        'registered_users':u,
        'translated_sentences':s,
        'published_articles':a
        } 
    messages.error(request,"You're not logged in!!!")
    log.error("%s made request before login."%(user))
    return render_to_response('login/home.html',data,context_instance=RequestContext(request)) 

def process_upload(request):
    """
    Stores file and its text part in Task model.
    """
    user = request.user
    uid = user.pk
    try:
        if request.method == 'POST':
            if request.POST.getlist('target_language') and request.POST['html_doc_name'] and request.FILES['html_doc_content'] and request.POST['time_to_publish_0'] and request.POST['time_to_publish_1'] and request.POST.getlist('interest_tags'):  
                all_language = request.POST.getlist('target_language')
                for l in all_language:
                    id = int(l)
                    target_language = Master_Language.objects.get(pk=id)
                    newtask = Task()
                    if request.POST.has_key('link'):
                        newtask.html_doc_name = request.POST['html_doc_name']
                    else:
                        newtask.html_doc_name = request.FILES['html_doc_content'].name
                    if request.POST.has_key('file'):
                        newtask.html_doc_content = request.FILES['html_doc_content']
                    else:
                        pass
                        #newtask.html_doc_content = urllib2.urlopen(request.POST['html_doc_name'])
                    newtask.upload_timestamp = datetime.datetime.now()
                    upload_ts = newtask.upload_timestamp
                    dt = datetime.datetime.strptime(request.POST['time_to_publish_0'],'%Y-%m-%d')   
                    tm = datetime.datetime.strptime(request.POST['time_to_publish_1'],'%H:%M:%S')   
                    tm = datetime.datetime.time(tm)
                    timestamp = datetime.datetime.combine(dt, tm)
                    newtask.time_to_publish = timestamp
                    newtask.source_language = Master_Language.objects.get(language="English")
                    newtask.target_language = target_language                 
                    if newtask.source_language == newtask.target_language:
                        data = {
                                'form' : UploadForm(),
                                'uid':uid,
                                'username':user,
                                }
                        messages.error(request,"Select different target language!!!")
                        log.error("%s selected same language as source and target while uploading document for translation."%(user))
                        return render_to_response('translation/upload.html',data,context_instance=RequestContext(request))
                    if request.POST['context_size']:
                        newtask.context_size = request.POST['context_size']
                    else:
                        newtask.context_size = 1
                        
                    if request.POST['age_group_tag']:
                        newtask.age_group_tag = Master_AgeGroup.objects.get(pk=request.POST['age_group_tag'])
                    if request.POST['geographical_region']:
                        newtask.geographical_region = Master_GeographicalRegion.objects.get(pk=request.POST['geographical_region'])
                    newtask.budget = 1
                    newtask.dampening_factor = 0.5
                    newtask.user = user
                    newtask.save()
                    
                    newtask = Task.objects.get(upload_timestamp=upload_ts)
                    if request.POST.getlist('interest_tags'):
                            all_interests = request.POST.getlist('interest_tags')                
                            
                            for i in all_interests:
                                id = int(i)
                                f_interests = Master_InterestTags.objects.get(pk=id)
                                newtask.interest_tags.add(f_interests)
                    newtask.save()
                    (u,a,s) = stats()
                    data = {
                            'form': UploadForm(),
                            'uid': uid,
                            'username':user,
                            'registered_users':u,
                            'translated_sentences':s,
                            'published_articles':a
                        }
                    ta = TransactionAction.objects.filter(session = Session.objects.filter(user=user,logout_timestamp=None))[0]
                    ta.task = Task.objects.get(pk=newtask.id)
                    ta.action_timestamp = datetime.datetime.now()
                    ta.save()
                    messages.success(request,"File uploaded sucessfully!!!")
                    log.info("File %s uploaded succesfully"%(newtask.html_doc_name))
                    return render_to_response('translation/account.html',data,context_instance=RequestContext(request))
            else:
                messages.error(request,"Please fill in all fields!!!")
                log.error("All fields not entered correctly while file upload.")
                data = {
                        'form': UploadForm(),
                        'uid':  uid,
                        'username':user,
                }
                return render_to_response('translation/upload.html',data,context_instance=RequestContext(request))
    except:
        log.exception("Upload Failed!!!")
        traceback.print_exc() 
        messages.error(request, "Upload Failed")
   
def translate(request,uid):
    """
    This function provides sentences for translation to user.
    """
    user = request.user
    if user.is_authenticated():
        try:
            logged_in_user_id = uid
            i = 0
            c = 0
            # check for sentences previously done by user
            
            available_sentences_done_by_user = UserHistory.objects.filter(user=logged_in_user_id)
            available_microtasks = Microtask.objects.filter(assigned = 0)
                
            #find sentences to be given                                             
            for j in available_sentences_done_by_user:
                available_microtasks = available_microtasks.exclude(original_sentence = available_sentences_done_by_user[i]).order_by('id')
                i +=1
            
            for j in available_microtasks:
                c += 1
            #if no sentence available display message    
            if c==0:
                data = {
                    'form': TranslateForm(),
                    'uid':uid,
                    'username':user,
                }
                
                ta = TransactionAction()
                ta.session = Session.objects.filter(user=user,logout_timestamp=None)[0]
                ta.user = user
                ta.action = Master_Action.objects.filter(action="Translate")[0]
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
                
                messages.error(request,"No sentence available for translation!!")
                log.error("No sentence available for translation.")
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
            else:
                #get bit_array value for that sentence from static microtask table
                available_microtask = available_microtasks[0]
                s = StaticMicrotask.objects.filter(id=available_microtask.static_microtask_id)
                parent_static_microtask = StaticMicrotask.objects.get(id=s)
                x = Master_Experiment.objects.get(bit_array = parent_static_microtask.bit_array)
                z = x.bit_array
                prev_context_size = int(z[0:3],2)
                auto_correct =  int(z[10],2)
                reference_translation = int(z[11],2)
                
                #decide which features to be provided to user for a particular sentence
                prev_context = load_context(parent_static_microtask.id,prev_context_size)
                
                if auto_correct==0:
                    auto_correction = False
                else:
                    auto_correction = True
                
                #get translations done by other users for that sentence
                if reference_translation == 1:
                    microtask_translation = parent_static_microtask.translated_sentence
                    machine_translation = parent_static_microtask.machine_translation
                
                    other = UserHistory.objects.filter(original_sentence=available_microtask.original_sentence)
                    other_translations = ""

                    for i in other:
                        text = i.translated_sentence
                        if text:
                            other_translations = other_translations + "-> " + text + '\n'
                else:
                    microtask_translation = ""
                    machine_translation = ""
                    other_translations = ""
                                  
                #take sentence from microtask make its entry in UserHistory with user as the one to whom this sentence is being assigned.  
                h = UserHistory()
                h.task = available_microtask.task
                h.subtask = available_microtask.subtask
                h.static_microtask = available_microtask.static_microtask
                h.microtask =  available_microtask
                h.user = user
                h.original_sentence = available_microtask.original_sentence 
                h.assign_timestamp = datetime.datetime.now()
                h.current_active_tag = 0
                h.correction_episode = [{}]
                h.save()
                
                s = StaticMicrotask.objects.get(id=s)
                s.hop_count = s.hop_count + 1
                s.save()               
                                
                (word,hindi_dictionary) = dict(h)               
                                
                data = {
                        'form': TranslateForm(),
                        'curr_id':available_microtask,
                        'uid': uid,
                        'english': h.original_sentence,
                        'hindi': microtask_translation,
                        'machine_translation': machine_translation,
                        'other_translations':other_translations,
                        'dictionary': hindi_dictionary,
                        'word':word,
                        'username':user,
                        'prev_context':prev_context,
                        'auto_correction':auto_correction
                }
                                
                #marking microtask entry as assigned  
                available_microtask.assigned=True
                available_microtask.save()
                ta = TransactionAction()
                ta.session = Session.objects.filter(user=user,logout_timestamp=None)[0]
                ta.user = user
                ta.action = Master_Action.objects.filter(action="Translate")[0]
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
                log.info("Microtask loaded for translation.")
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
        except:
            log.exception("Load microtask for translation failed.")
            traceback.print_exc() 
            messages.error(request, "Load microtask for translation failed!!!")
    #if user is not logged in
    else:
        (u,a,s) = stats()
        data = {
            'form': LoginForm(),
            'registered_users':u,
            'translated_sentences':s,
            'published_articles':a
        } 
        messages.error(request,"Please login.You're not logged in!!!")
        log.error("%s made request before login."%(user))
        return render_to_response('login/home.html',data,context_instance=RequestContext(request))
    return HttpResponse("Error!!!")

def process_translate(request,id,uid):
    """
    This function store translation submitted by user.
    """
    user = request.user    
    if user.is_authenticated():
        if request.method == 'POST':
            try:
                #take translation search for user in userHistory
                correction_episode = request.POST['cmd']
                list = correction_episode.split('here')
                           
                
                engl = Microtask.objects.filter(pk=id)
                eng = engl[0]
                #search for english sentence and store in userHistory
                hist = UserHistory.objects.filter(microtask=eng)
                h = hist[0]
                if h.translated_sentence:
                    data = {
                        'form': TranslateForm(),
                        'uid': uid,
                        'curr_id':h.microtask_id,
                        'english': h.original_sentence,
                        'hindi':"",
                        'username':user,
                    }
                    messages.success(request,"You have already translated that sentence!!!")
                    return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
                else:
                    h.translated_sentence = request.POST['translated_sentence']
                    h.submission_timestamp = datetime.datetime.now()
                    h.stability = 0.0
                    h.current_active_tag = 1
                    h.change_flag = 1
                    h.status_flag = 'Reviewed'
                    h.correction_episode = list 
                    h.save() 
                    #convert history of key press in json and store
                    dat = serializers.serialize('json', UserHistory.objects.filter(pk=h.id), fields=('correction_episode'), ensure_ascii=False)
                    h.correction_episode = dat
                    h.save()
                
                #micro = Microtask.objects.get (id=engl)
                #micro.delete()
              
                ta = TransactionAction.objects.filter(session = Session.objects.filter(user=user,logout_timestamp=None))[0]
                ta.task = h.task
                ta.subtask = h.subtask
                ta.static_microtask = h.static_microtask
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
                
                data = {
                        'form': TranslateForm(),
                        'uid': uid,
                        'curr_id':h.microtask_id,
                        'english': h.original_sentence,
                        'hindi':"",
                        'username':user,
                    }
                messages.success(request,"Record saved sucessfully!!!")
                log.info("Microtask (id:%s) saved successfully after translation."%(id))
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
            except:
                log.exception("Save translated microtask failed.")
                traceback.print_exc() 
                messages.error(request, "Save translated microtask Failed!!!")
    else:
        log.error("%s made request before login."%(user))
        return HttpResponse("Please login.You're not logged in!!!")

def account_settings(request,uid):
    """
    This function provides user with his account information which is to be updated.
    """
    user = User.objects.get(pk=uid)
    u = UserProfile.objects.get(user = uid)
    form =  UpdateProfileForm(instance=u)
    form1 = UpdateProfileForm(instance=user) 
    
    data = {
        'form': form,
        'form1':form1,
        'uid':uid,
        'username':request.user
    }
    log.info("%s visited account_settings form."%(user))
    return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))    

def process_account_settings(request,uid):
    """
    This function saves the changes made by user in his profile
    except his username cannot be changed.
    """
    user = request.user 
    if request.method == 'POST':
        f_password = request.POST['password']
        f_confirm_password = request.POST['confirm_password']
        f_email = request.POST['email']
        f_first_name = request.POST['first_name']
        f_last_name = request.POST['last_name']
        f_date_of_birth = request.POST['date_of_birth']
        f_district = request.POST['district']
        f_education_qualification = request.POST['education_qualification']
        f_domain = request.POST['domain']  
        f_medium_of_education_during_school = request.POST['medium_of_education_during_school']
            
        if request.POST.has_key('translator'):
            f_translator = request.POST['translator']
        else:
            f_translator = False
        if request.POST.has_key('contributor'):
            f_contributor = request.POST['contributor']
        else:
            f_contributor = False
        if request.POST.has_key('evaluator'):           
            f_evaluator = request.POST['evaluator']
        else:
            f_evaluator = False
                
        try:
            #find user record
            if f_password == f_confirm_password:
                if f_email and f_first_name and f_last_name:
                    count = User.objects.exclude(username=request.user).filter(email=f_email).count() 
                                            
                    if count !=0:
                        data = {
                            'form': SignUpForm(request.POST), 
                        }
                        messages.error(request,"EmailID already in use.Try another one!!!")
                        log.error("%s changed email-id to an existing one while updating profile."%(user))
                        return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
                    #update record
                    u = User.objects.get(username = request.user)
                    u.first_name =f_first_name
                    u.last_name = f_last_name
                    u.email = f_email
                    u.save()
                    if f_password:
                        u.set_password(f_password)
                        u.save()

                    userpro = UserProfile.objects.get(user=user)
                        
                    userpro.date_of_birth = f_date_of_birth
                    userpro.district = Master_GeographicalRegion.objects.get(pk=f_district)
                    userpro.domain = Master_EducationDomain.objects.get(pk=f_domain)
                    userpro.education_qualification = Master_EducationQualification.objects.get(pk=f_education_qualification)
                    userpro.translator = f_translator
                    userpro.evaluator = f_evaluator
                    userpro.contributor = f_contributor
                    userpro.save()
                    
                    if request.POST.getlist('language'):     
                        all_language = request.POST.getlist('language')            
                            
                        for l in all_language:
                            id = int(l)
                            f_language = Master_Language.objects.get(pk=id)
                            userpro.language.add(f_language)
                        
                    if request.POST.has_key('medium_of_education_during_school'):     
                        medium_of_education_during_school = request.POST['medium_of_education_during_school']            
                            
                        for l in medium_of_education_during_school:
                            id = int(l)
                            f_medium_of_education_during_school = Master_Language.objects.get(pk=id)
                            userpro.medium_of_education_during_school = f_medium_of_education_during_school
                            userpro.save()
                                                     
                    if request.POST.getlist('interests'):
                        all_interests = request.POST.getlist('interests')                
                            
                        for i in all_interests:
                            id = int(i)
                            f_interests = Master_InterestTags.objects.get(pk=id)
                            userpro.interests.add(f_interests)
                    
                    (u,a,s) = stats()
       
                    data = {
                        'form': SignUpForm(), 
                        'username':user,
                        'registered_users':u,
                        'translated_sentences':s,
                        'published_articles':a
                    }
                    messages.success(request,"Record saved successfully!!.")
                    log.info("Profile updated successfully for user: %s."%(user))
                    return render_to_response('translation/account.html',data,context_instance=RequestContext(request))                              
                else:
                    data = {
                        'form': SignUpForm(request.POST),
                        }
                    messages.error(request,"Please fill in all fields!!!")
                    log.error("All fields not entered correctly while updating user profile.")
                    return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
    
            else:
                data = {
                    'form': SignUpForm(request.POST),
                } 
                messages.error(request,"Confirm password correctly!!!")
                log.error("Password not confirmed correctly.")
                return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
            return HttpResponseRedirect(reverse('home')) 
        except:
            log.exception("Update Failed!!!")
            traceback.print_exc() 
            messages.error(request, "Account update Failed!!!Try again.")
            return render_to_response('translation/account_settings.html',context_instance=RequestContext(request))
    return HttpResponse("Error!!!") 
    
def evaluate(request):
    print "to be done"
    ta = TransactionAction()
    ta.session = Session.objects.filter(user=request.user,logout_timestamp=None)[0]
    ta.user = request.user
    ta.action = Master_Action.objects.filter(action="Evaluate")[0]
    ta.action_timestamp = datetime.datetime.now()
    ta.save()
    return HttpResponseRedirect(reverse('account'))
    
def process_evaluate(request):
    print "to be done"
    return HttpResponseRedirect(reverse('account'))


def load_context(sid,prev_context_count):
    """
    This function returns sentences before the sentence
    to be translated for giving context to user.
    """
    if int(sid)==1:
        prev_context = ""
    else:
        a = int(sid) - int(prev_context_count)
        prev_context = ""
        while int(a) < int(sid):
            st = StaticMicrotask.objects.get(id=a)
            if st:
                prev_context = prev_context + st.original_sentence + ". "
            a += 1
    return prev_context

def dict(h):
    """
    This function returns the hindi meaning of all the words in english sentence.
    """
    dict = h.original_sentence.split(' ')
    count = len(dict)
    k = 0
    word = ''
    hindi_dictionary = ''
    meaning = ''
    while k < count:
        mean = Master_English2Hindi.objects.filter(english_word = dict[k])            
        if mean:
            i = Master_English2Hindi.objects.filter(english_word = dict[k]).count()
            m = 0
            while m < i:
                meaning = mean[m].hindi_word + '--' + meaning
                m += 1
            if meaning:
                hindi_dictionary = hindi_dictionary + ',' + meaning 
                word = word + ',' + dict[k]    
        k += 1
    return (word,hindi_dictionary)

def stats():
    """
    This function returns statistics - no. of registered users, sentences and articles translated.
    """
    sta = StatCounter.objects.all().order_by('created_on')
    count = StatCounter.objects.all().count()
    
    if sta:
        st = sta[count- 1]
        u = st.registered_users
        s = st.translated_sentences
        a = st.published_articles
    else:
        u = 0
        a = 0
        s = 0
    print (u,a,s)    
    return (u,a,s)

def find():
    u = Group.objects.all()
    l = "" 
    count = Group.objects.all().count()
    i = 0
    if count>0:
        l = u[i].name
        i+=1
        while i < count:
            l = l + ',' + u[i].name
            i += 1
    return l

def get_overall_leaderboard():
    u = OverallLeaderboard.objects.all().order_by('overall_points_earned')[:10]
    print u
    return u

def get_weekly_leaderboard():
    u = WeeklyLeaderboard.objects.all().order_by('points_earned_this_week')[:10]
    return u