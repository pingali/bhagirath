from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth.models import Group
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from bhagirath.translation.forms import *
from bhagirath.translation.models import *
from bhagirath.centoid_score.SSDistance import SSDistance
import simplejson
import traceback
import logging

log = logging.getLogger("translation.views")

def bhagirath_404_view(request):
    data = {}
    return render_to_response('404.html',data,context_instance=RequestContext(request))

def bhagirath_error_view(request):
    data = {}
    return render_to_response('500.html',data,context_instance=RequestContext(request))

def home(request):
    """
    This function displays some information about bhagirath project,  
    weekly and overall top users and provides login facility to the user. 
    """
    overall_leaderboard = get_overall_leaderboard()
    weekly_leaderboard = get_weekly_leaderboard()
    data = {
            'overall_leaderboard':overall_leaderboard,
            'weekly_leaderboard':weekly_leaderboard,
        }
    return render_to_response('login/home.html',data,context_instance=RequestContext(request))

def about_us(request):
    """
    This function gives detailed information about bhagirath along with statistics and leaderboards.
    """
    user = request.user
    if user.is_authenticated():
        logged_in = True 
        uid = user.pk
        data = {
            'form': LoginForm(),
            'username':user,
            'logged_in':logged_in,
            'uid':uid 
        }
    else:
        logged_in = False
        data = {
            'form': LoginForm(),
            'logged_in':logged_in
        }
    return render_to_response('login/about_us.html',data,context_instance=RequestContext(request))      

def contact_us(request):
    user = request.user
    if user.is_authenticated():
        logged_in = True 
        uid = user.pk
        u = User.objects.get(pk=uid)
        if u.email:
            email_id = u.email
            form = ContactUsForm(initial={'email':email_id})
        else:
            email_id = ""
            form = ContactUsForm()
        data = {'email_id':email_id,'username':user, 'logged_in':logged_in,'form':form,'uid':uid }
    else:
        logged_in = False
        email_id = ""
        form = ContactUsForm()
        data = {'email_id':email_id,'username':user, 'logged_in':logged_in,'form':form }
    return render_to_response('login/contact_us.html',data,context_instance=RequestContext(request))

def feedback(request):
    c = request.POST.pop('comment')
    e = request.POST.pop('email')
    try:
        a = Feedback()
        if request.POST.has_key('feedback_suggestion'):
            a.type = "suggestion"
            if c[0] and e[0]:
                a.comment = c[0]
                a.email = e[0]
                a.save()
                messages.success(request,"Thanks for feedback!!!")
            else:
                messages.error(request,"Please enter all fields.")
                log.error("All fields not entered correctly while user feedback.")
    
        elif request.POST.has_key('feedback_collaboration'):
            a.type = "collaboration"
            if c[1] and e[1]:
                a.comment = c[1]
                a.email = e[1]
                a.save()
                messages.success(request,"Thanks for feedback!!!")
            else:
                messages.error(request,"Please enter all fields.")
                log.error("All fields not entered correctly while user feedback.")
    
        elif request.POST.has_key('feedback_copyright_issues'):
            a.type = "copyright_issue"
            if c[2] and e[2]:
                a.comment = c[2]
                a.email = e[2]
                a.save()
                messages.success(request,"Thanks for feedback!!!")
            else:
                messages.error(request,"Please enter all fields.")
                log.error("All fields not entered correctly while user feedback.")
    except:
        log.exception("Save user feedback failed for %s."%(request.POST['email']))
        messages.error(request,"User Feedback failed!!!Try again.")   
    next = "/contact_us/"
    return HttpResponseRedirect(next) 
                            
def sample_translations(request,id):
    """
    This function provides sample translations having english sentence, 
    its machine translation and user translation.  
    """
    if int(id) <= 15 and int(id) > 0:
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
    else:
        data = {}
        return render_to_response('404.html',data,context_instance=RequestContext(request))

def sign_up(request):
    """
    This function loads sign up form for new user's registration. 
    """
    data = { 'form': SignUpForm() }
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
        form = SignUpForm(request.POST)
        if form.is_valid():
            f_username = form.cleaned_data['username']
            f_password = form.cleaned_data['password']
            f_email = form.cleaned_data['email']           
            try:
                count = 0
                          
                #Check for unique email-id
                count = User.objects.filter(email=f_email).count()
                if count !=0:
                    data = {'form': SignUpForm(request.POST)}
                    messages.error(request,"EmailID already in use.Try another one!!!")
                    log.error("Exisiting email-id used while user-registration.")
                    return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                    
                #Check for unique username
                count = User.objects.all().filter(username = f_username).count()
                if count != 0:
                    data = {'form': SignUpForm(request.POST)}
                    messages.error(request,"Username already in use.Try another one!!!")
                    log.error("Exisiting username used while user-registration.")
                    return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                            
                u = User.objects.create_user(f_username, f_email, f_password)
                u.is_active = True
                u.save()
                u.set_password(f_password)
                u.save()
                                    
                user = User.objects.get(username__exact=f_username)
                                
                p = UserProfile()
                p.user = user
                p.ip_address = request.META['REMOTE_ADDR']
                p.save()
                                
                data = {'form': SignUpForm()}
                messages.success(request,"Registered successfully!!!")
                log.info("User registration successful for %s."%(f_username))
                next = "/sign_in/"
                return HttpResponseRedirect(next) 
            except:
                log.exception("User registration failed for %s."%(f_username))
                messages.error(request,"User Registration failed!!!")
                return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
        else:
            data = {'form': SignUpForm(request.POST)}
            messages.error(request,form._get_errors().as_text())
            log.error("All fields not entered correctly while user registration.")
            next = "/sign_up/"
            return HttpResponseRedirect(next) 
        
def sign_in(request):
    """
    This function loads sign form for user's login. 
    """

    overall_leaderboard = get_overall_leaderboard()
    weekly_leaderboard = get_weekly_leaderboard()
    data = {
            'form': LoginForm(),
            'overall_leaderboard':overall_leaderboard,
            'weekly_leaderboard':weekly_leaderboard,
        }
    return render_to_response('login/sign_in.html',data,context_instance=RequestContext(request))

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
        next = "/account/"
        log.info("%s logged in succesfully."%(user))  
    else:
        messages.error(request, "Incorrect username or password!!!")
        log.error("Login failed for user: %s."%(uname))
        next = "/sign_in/"
    return HttpResponseRedirect(next)    
    
def process_sign_out(request):
    """
    This function is used to logout user successfully from the site.
    """
    user=request.user
    s = Session.objects.filter(user=request.user,logout_timestamp=None)
    cnt = Session.objects.filter(user=request.user,logout_timestamp=None).count()
    s = s[cnt-1]
    s.logout_timestamp = datetime.datetime.now()
    s.save()

    auth.logout(request)
    
    try:
        request.session.flush()
    except:
        pass
    
    log.info("%s logged out succesfully."%(user))
    next = "/home/"
    return HttpResponseRedirect(next) 
    
def account(request):
    """
    This function provides information such as current statistics and user's contribution
    as total sentences translated, files uploaded and number of correct translations.
    """
    user = request.user
    uid = user.pk

    if user.is_authenticated():
        overall_leaderboard = get_overall_leaderboard()
        weekly_leaderboard = get_weekly_leaderboard()       
        user_pro = User.objects.get(pk = uid)
        try:
            user_profile = UserProfile.objects.get(user = user_pro)
            data = {
                'uid':uid,
                'total_translated_sentences':user_profile.total_translated_sentences,
                'no_of_perfect_translations': user_profile.no_of_perfect_translations,
                'total_uploaded_tasks':user_profile.total_uploaded_tasks,
                'total_evaluated_sentences':user_profile.total_evaluated_sentences,
                'username':user,
                'overall_leaderboard':overall_leaderboard,
                'weekly_leaderboard':weekly_leaderboard,
            } 
            log.info("%s visited its home page."%(user))
            return render_to_response('translation/account.html',data,context_instance=RequestContext(request))
        except:
            messages.error(request,"You have not registered!!!")
            log.error("%s made request before registration."%(user))
            next = "/home/"
            return HttpResponseRedirect(next) 
            
    else:
        data = {
                'form': LoginForm(),
                'uid':uid
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
        data = {
            'form': LoginForm(),
            'username':user,
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
            if request.POST.getlist('target_language') and request.FILES['html_doc_content'] and request.POST['time_to_publish_0'] and request.POST['time_to_publish_1'] and request.POST.getlist('interest_tags'):  
                all_language = request.POST.getlist('target_language')
                for l in all_language:
                    id = int(l)
                    target_language = Master_Language.objects.get(pk=id)
                    newtask = Task()
                    if request.POST.has_key('link'):
                        newtask.html_doc_name = request.POST['html_doc_name']
                        #newtask.html_doc_content = urllib2.urlopen(request.POST['html_doc_name'])
                    else:
                        newtask.html_doc_name = request.FILES['html_doc_content'].name
                        newtask.html_doc_content = request.FILES['html_doc_content']
                    
                   
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
                    
                    data = {
                            'form': UploadForm(),
                            'uid': uid,
                            'username':user
                        }
                    ta = TransactionAction.objects.filter(session = Session.objects.filter(user=user,logout_timestamp=None))[0]
                    ta.task = Task.objects.get(pk=newtask.id)
                    ta.action_timestamp = datetime.datetime.now()
                    ta.save()
                    messages.success(request,"File uploaded sucessfully!!!")
                    log.info("File %s uploaded succesfully"%(newtask.html_doc_name))
                    next = "/account/"
                    return HttpResponseRedirect(next) 
            else:
                messages.error(request,"Please fill in all fields!!!")
                log.error("All fields not entered correctly while file upload.")
                data = {
                        'form': UploadForm(),
                        'uid':  uid,
                        'username':user,
                }
                next = "/account/upload/"
                return HttpResponseRedirect(next) 
    except:
        log.exception("Upload Failed!!!")
        traceback.print_exc() 
   
def translate(request,uid):
    """
    This function provides sentences for translation to user.
    """
    log.info("Entered translate function - ") 
    
    user = request.user
    if user.is_authenticated():
        try:
            logged_in_user_id = uid
            i = 0
            c = 0
            hindi = " "
            # check for sentences previously done by user
            log.info("Search for available microtask STARTS - ") 
            
            
            available_sentences_done_by_user = UserHistory.objects.filter(user=logged_in_user_id)
            available_microtasks = Microtask.objects.filter(assigned = 0)
                
            #find sentences to be given                                             
            for j in available_sentences_done_by_user:
                available_microtasks = available_microtasks.exclude(original_sentence = available_sentences_done_by_user[i]).order_by('id')
                i +=1
            
            log.info("Search for available microtask ENDS - ") 
            
            
            for j in available_microtasks:
                c += 1
            #if no sentence available display message    
            if c==0:
                data = {
                    'form': TranslateForm(),
                    'uid':uid,
                    'username':user,
                }
                
                log.info("Make entry into TransactionAction if no microtask is available STARTS- ") 
                
                
                ta = TransactionAction()
                ta.session = Session.objects.filter(user=user,logout_timestamp=None)[0]
                ta.user = user
                ta.action = Master_Action.objects.filter(action="Translate")[0]
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
                
                log.info("Make entry into TransactionAction if no microtask is available ENDS- ") 
                
                
                messages.error(request,"No sentence available for translation!!")
                log.error("No sentence available for translation.")
                
                log.info("Entries made to log- ") 
                
                
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
            else:
                
                log.info("Bit array verification for experiment STARTS- ") 
                
                #get bit_array value for that sentence from static microtask table
                available_microtask = available_microtasks[0]
                s = StaticMicrotask.objects.filter(id=available_microtask.static_microtask_id)
                parent_static_microtask = StaticMicrotask.objects.get(id=s)
                x = Master_Experiment.objects.get(bit_array = parent_static_microtask.bit_array)
                z = x.bit_array
                prev_context_size = int(z[0:3],2)
                auto_correct =  int(z[10],2)
                reference_translation = int(z[11],2)
                
                log.info("Bit array verification for experiment ENDS- ") 
                
                #decide which features to be provided to user for a particular sentence
                
                log.info("Context loading STARTS- ")      
                (prev_context, meaning_list) = load_context(parent_static_microtask.id,prev_context_size)
                log.info("Context loading ENDS- ") 
                
                
                if auto_correct==0:
                    auto_correction = False
                else:
                    auto_correction = True
                
                log.info("Loading reference translations STARTS- ") 
                
                #get translations done by other users for that sentence
                if reference_translation == 1:
                    microtask_translation = parent_static_microtask.translated_sentence
                    machine_translation = parent_static_microtask.machine_translation
                
                    if microtask_translation == None:
                        hindi = machine_translation
                    else:
                        hindi = microtask_translation  
                        
                    other = UserHistory.objects.filter(original_sentence=available_microtask.original_sentence)
                    other_translations = ""

                    for i in other:
                        text = i.translated_sentence
                        if text:
                            other_translations = other_translations + "-> " + text + '\n'
                else:
                    microtask_translation = " "
                    machine_translation = " "
                    other_translations = " "
                
                log.info("Loading reference translation ENDS- ") 
                
                #take sentence from microtask make its entry in UserHistory with user as the one to whom this sentence is being assigned.
                
                log.info("Create record in UserHistory STARTS- ") 
                               
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
                
                log.info("Create record in UserHistory ENDS- ")
                log.info("Increase hop_count in StaticMicrotask STARTS- ") 
                  
                
                s = StaticMicrotask.objects.get(id=s)
                s.hop_count = s.hop_count + 1
                s.save()               
                                
                log.info("Increase hop_count in StaticMicrotask ENDS- ") 
                log.info("Loading dictionary- ")
       
                hindi_dictionary = []
                for i in meaning_list:
                    x = i[0]['fields']['meaning']
                    w = simplejson.loads(x)
                    for z in w:
                        log.info("Single Record")
                        log.info(z)
                        hindi_dictionary.append(z)
                        
                
                x = parent_static_microtask.meaning[0]['fields']['meaning']
                w = simplejson.loads(x)
                for z in w:
		    log.info(z)
                    hindi_dictionary.append(z)               
                    
                y = simplejson.dumps(hindi_dictionary)                     
                log.info("Dictionary loaded- ") 
                log.info(y)
                
                data = {
                        'form': TranslateForm(),
                        'curr_id':available_microtask,
                        'uid': uid,
                        'english': h.original_sentence,
                        'hindi': hindi,
                        'machine_translation': machine_translation,
                        'other_translations':other_translations,
                        'eng2hin_dict': y,
                        'username':user,
                        'prev_context':prev_context,
                        'auto_correction':auto_correction
                }
                                
                log.info("Update Microtask STARTS- ") 
                  
                                                
                #marking microtask entry as assigned  
                available_microtask.assigned=True
                available_microtask.save()
                
                log.info("Update Microtask ENDS- ") 
                  
                
                log.info("Create record in TransactionAction STARTS- ") 
                  
                
                ta = TransactionAction()
                ta.session = Session.objects.filter(user=user,logout_timestamp=None)[0]
                ta.user = user
                ta.action = Master_Action.objects.filter(action="Translate")[0]
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
                
                log.info("Create record in TransactionAction ENDS- ") 
                
                
                log.info("Microtask loaded for translation.")
            
                log.info("Template loading...- ")
                  
            
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
        except:
            log.exception("Load microtask for translation failed.")
            traceback.print_exc() 
    #if user is not logged in
    else:
        data = {
            'form': LoginForm()
        } 
        messages.error(request,"Please login.You're not logged in!!!")
        log.error("%s made request before login."%(user))
        next = "/home/"
        return HttpResponseRedirect(next) 
    return HttpResponse("Error!!!Please try reloading the page.")

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
                log.info("Search for record in UserHistory STARTS- ") 
                
                
                hist = UserHistory.objects.filter(microtask=eng)
                h = hist[0]
               
                if h.translated_sentence:
                    log.info("User has translated it previously so return back- ") 
                    
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
                    log.info("Update UserHistory record STARTS-") 
                    
                
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
                    
                    log.info("Update UserHistory record ENDS-") 
                    
                #micro = Microtask.objects.get (id=engl)
                #micro.delete()
              
                log.info("Make entry into TransactionAction STARTS-") 
                
                
                ta = TransactionAction.objects.filter(session = Session.objects.filter(user=user,logout_timestamp=None))[0]
                ta.task = h.task
                ta.subtask = h.subtask
                ta.static_microtask = h.static_microtask
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
             
                log.info("Make entry into TransactionAction ENDS-") 
                
                
                messages.success(request,"Translation saved sucessfully!!!")
                log.info("Microtask (id:%s) saved successfully after translation."%(id))
                next = "/account/translate/" + uid + "/"
                
                log.info("Calling translate()...")
                
                
                return HttpResponseRedirect(next) 
                
            except:
                log.exception("Save translated microtask failed.")
                traceback.print_exc() 
    else:
        log.error("%s made request before login."%(user))
        messages.error(request,"Please login.You're not logged in!!!")
        next = "/home/"
        return HttpResponseRedirect(next) 
    
    return HttpResponse("Error!!!")

def account_settings(request,uid):
    """
    This function provides user with his account information which is to be updated.
    """
    
    user = User.objects.get(pk=uid)
    u = UserProfile.objects.get(user = uid)
    
    all_groups = Group.objects.filter(user=user)
    if all_groups:
        groups = all_groups[0].name
    else:
        groups = ""
    l = find()
    
    form =  UpdateProfileForm(instance=u)
    form1 = UpdateProfileForm(instance=user,initial={'groups':groups}) 
    
    data = {
        'form': form,
        'form1':form1,
        'uid':uid,
        'list':l,
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
        form = UpdateProfileForm(request.POST)
        
        if form.is_valid():
            if form.cleaned_data.has_key('password'):
                f_password = form.cleaned_data['password']
            else:
                f_password = ""
            f_email = form.cleaned_data['email']
            f_first_name = form.cleaned_data['first_name']
            f_last_name = form.cleaned_data['last_name']
            f_date_of_birth = form.cleaned_data['date_of_birth']
            f_gender = form.cleaned_data['gender']
            f_district = form.cleaned_data['district']
            f_education_qualification = form.cleaned_data['education_qualification']
            f_domain = form.cleaned_data['domain']  
            f_medium_of_education_during_school = form.cleaned_data['medium_of_education_during_school']
            f_grp = form.cleaned_data['groups'].upper()
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
                #Check for unique email-id
                count = User.objects.exclude(username=request.user).filter(email=f_email).count() 
                if count !=0:
                    data = {'form': UpdateProfileForm(request.POST)}
                    messages.error(request,"EmailID already in use.Try another one!!!")
                    log.error("%s changed email-id to an existing one while updating profile."%(user))
                    return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
                    
                else:
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
                    userpro.gender = f_gender
                    userpro.district = f_district
                    userpro.domain = f_domain
                    userpro.education_qualification = f_education_qualification
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
                    
                    u.groups.clear()        
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
                    
       
                    data = {
                        'form': UpdateProfileForm(request.POST), 
                        'username':user
                    }
                    messages.success(request,"Profile updated successfully!!.")
                    log.info("Profile updated successfully for user: %s."%(user))
                    next = "/account/"
                    return HttpResponseRedirect(next) 
            except:
                log.exception("Profile Update Failed!!!")
                traceback.print_exc() 
                return render_to_response('translation/account_settings.html',context_instance=RequestContext(request))
        else:   
            if form._get_errors().has_key('confirm_password'):
                form._get_errors().pop('confirm_password')
            
            if form._get_errors().has_key('password'):
                form._get_errors().pop('password')
                        
            a = form._get_errors().as_text()
            user = User.objects.get(pk=uid)
            u = UserProfile.objects.get(user = uid)
            form =  UpdateProfileForm(instance=u)
            form1 = UpdateProfileForm(instance=user) 
            all_groups = Group.objects.filter(user=user)
            if all_groups:
                groups = all_groups[0].name
            else:
                groups = ""
            l = find()
   
            data = {
                    'form': form,
                    'form1':form1,
                    'uid':uid,
                    'list':l,
                    'username':request.user,
                    'groups':groups
                }
                       
            messages.error(request,a)
            log.error("All fields not entered correctly while user registration.")
            return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
    return HttpResponse("Some error occured!!!") 

def evaluate(request):
    """to be done"""
    messages.success(request, "This feature is coming soon!!!")
    return HttpResponseRedirect(reverse('account'))
    
def process_evaluate(request):
    """to be done"""
    return HttpResponseRedirect(reverse('account'))

def autocomplete(request,uid,prefix_val):
    word_list = []

    try:
        list = Master_HindiWords.objects.filter(original__startswith=prefix_val).values()
        for i in list:
            word_list.append(i['original'])    
        return HttpResponse(word_list)
    except:
        return HttpResponse("  ")

def autocorrect(request,word):
    auto = []
    prefix_val = word[:1]
    li = Master_HindiWords.objects.filter(original__startswith=prefix_val).values()
    for i in li:
        l = i['original']
        l = l.rstrip()
        a = SSDistance.getSimilarity(word, l)
        if a > 0.8:
            l = l + ' '
            auto.append(l)
    return HttpResponse(auto)


def load_context(sid,prev_context_count):
    """
    This function returns sentences before the sentence
    to be translated for giving context to user.
    """
    log.info("Entered load_context function")
    meaning_list = []
    
    if int(sid)==1:
        prev_context = ""
    else:
        a = int(sid) - int(prev_context_count)
        prev_context = ""
        while int(a) < int(sid):
            st = StaticMicrotask.objects.get(id=a)
            if st:
                prev_context = prev_context + st.original_sentence + ". "
                meaning_list.append(st.meaning)
            a += 1
    log.info("Exited load_context function")
    return prev_context, meaning_list

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
    return u

def get_weekly_leaderboard():
    u = WeeklyLeaderboard.objects.all().order_by('points_earned_this_week')[:10]
    return u
