from django.template import RequestContext
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from bhagirath.translation.forms import *
from bhagirath.translation.models import *
from django.conf import settings
from django.contrib import messages
from django.core import serializers
import captcha
import traceback
import logging
from bhagirath.translation.subtask_parser import subtaskParser
from bhagirath.translation.microtask_parser import microtaskParser

log = logging.getLogger("translation.views")

def hindiwords(request):
    F = open("/home/ankita/Desktop/hindi_wordlist/noun_txt")
    line = F.read()
    parts = line.split('\n')
    for j in parts:
        p = Master_HindiWords()
        p.original = j
        p.pos = "Noun"
        p.save()
    return HttpResponse("DONE!!!") 

def english2hindi(request):
    F = open("/home/ankita/Desktop/enghin/a_new.txt")
    line = F.read()
    parts = line.split('\n')
    i = 0
    j = len(parts)
    
    while i < j:
        if parts[i]:
            part = parts[i].split(',')
            p = Master_English2Hindi()
            p.english_word = part[0]
            p.pos = part[1]
            p.hindi_word = part[2]
            p.save()
        i += 1
   
    return HttpResponse("DONE!!!")

def subtask(request):
    tasks = Task.objects.all()
    i = Task.objects.all().count()
    j = 0
    while  j< i:
        t = tasks[j]
        s = '/home/ankita/Desktop/TRDDC_Wikipedia/Sample_Wiki_Articles/' + t.html_doc_name
        subtaskParser(s,t.id)
        j +=1
    return HttpResponse("DONE!!!") 

def staticmicro(request):
    microtaskParser()    
    return HttpResponse("DONE!!!") 

def microtask(request):
    i = 0
    static = StaticMicrotask.objects.filter(assigned = 0)
    while i < 50:
        s = static[i]
        j = 0
        while j < 3:
            m = Microtask()
            m.task = s.task
            m.subtask = s.subtask
            m.static_microtask = s
            m.original_sentence = s.original_sentence
            m.assigned = 0
            m.assign_timestamp = datetime.datetime.now()
            m.save()
            j += 1
        #s.assigned = 1
        #s.save
        i += 1    
    return HttpResponse("DONE!!!") 
           
def home(request):
    sta = StatCounter.objects.all().order_by('created_on')
    if sta:
        st = sta[0]
        u = st.registered_users
        s = st.translated_sentences
        a = st.published_articles
    else:
        u = 0
        a = 0
        s = 0
    data = {
            'form': LoginForm(),
            'registered_users':u,
            'translated_sentences':s,
            'published_articles':a
        }
    return render_to_response('login/home.html',data,context_instance=RequestContext(request))

def about_us(request):
    sta = StatCounter.objects.all().order_by('created_on')
    if sta:
        st = sta[0]
        u = st.registered_users
        s = st.translated_sentences
        a = st.published_articles
    else:
        u = 0
        a = 0
        s = 0
    data = {
            'form': LoginForm(),
            'registered_users':u,
            'translated_sentences':s,
            'published_articles':a
        }
    return render_to_response('login/about_us.html',data,context_instance=RequestContext(request))
          
def sample_translations(request,id):
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
    data = {
        'form': SignUpForm(),
        'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
    }
    return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
 
def process_sign_up(request):
    user = request.user 
    if request.method == 'POST':
        check_captcha = captcha.client.submit(request.POST['recaptcha_challenge_field'], 
                                       request.POST['recaptcha_response_field'], 
                                       settings.RECAPTCHA_PRIVATE_KEY, 
                                       request.META['REMOTE_ADDR'])
        if check_captcha.is_valid is False:
            pass_captcha = False
        else:
            pass_captcha = True

        if pass_captcha :
            f_password = request.POST['password']
            f_confirm_password = request.POST['confirm_password']
            f_email = request.POST['email']
            f_username = request.POST['username']
            f_first_name = request.POST['first_name']
            f_last_name = request.POST['last_name']
            f_gender = request.POST['gender']
            f_date_of_birth = request.POST['date_of_birth']
                 
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
                    if f_email and f_username and f_first_name and f_last_name:
                        count = User.objects.filter(email=f_email).count()                     
                        if count !=0:
                            data = {
                                'form': SignUpForm(request.POST),
                                'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
                                }
                            messages.error(request,"EmailID already in use.Try another one!!!")
                            return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                        
                        count = User.objects.all().filter(username = f_username).count()
                                
                        if count != 0:
                            data = {
                                'form': SignUpForm(request.POST),
                                'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
                                }
                            messages.error(request,"Username already in use.Try another one!!!")
                            return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request)) 
                        
                        u = User.objects.create_user(f_username, f_email, f_password)
                        u.is_active = True
                        u.first_name =f_first_name
                        u.last_name = f_last_name
                        u.save()
                        u.set_password(f_password)
                        u.save()
                        
                        user = User.objects.get(username__exact=f_username)
                        user.userprofile_set.create(date_of_birth=f_date_of_birth,ip_address=request.META['REMOTE_ADDR'],gender=f_gender,
                                                    translator=f_translator,contributor=f_contributor,evaluator=f_evaluator)
                        
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
                        messages.success(request,"Record saved successfully!!.")
                        return render_to_response('login/home.html',data,context_instance=RequestContext(request))                              
                    else:
                        data = {
                            'form': SignUpForm(request.POST),
                            'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
                            }
                        messages.error(request,"Please fill in all fields!!!")
                        return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
    
                else:
                    data = {
                        'form': SignUpForm(request.POST),
                        'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
                        } 
                    messages.error(request,"Confirm password correctly!!!")
                    return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
                return HttpResponseRedirect(reverse('home')) 
            except:
                log.exception("Registration Failed!!!")
                traceback.print_exc() 
                messages.error(request, "Registration Failed!!!Try again.")
               
        else:
            data = {
                'form': SignUpForm(),
                'html_captcha':captcha.client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, attrs = {'theme' : 'red'}, use_ssl = False), 
                }
            messages.error(request, "Recaptcha entered incorrectly!!!")
           
            return render_to_response('login/sign_up.html',data,context_instance=RequestContext(request))
    return HttpResponse("Error!!!")

def process_sign_in(request):
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
        return HttpResponseRedirect(next) 
    else:
        messages.error(request, "Incorrect username or password!!!")   
    return HttpResponseRedirect(reverse('home'))
    
def process_sign_out(request):
    s = Session.objects.filter(user=request.user,logout_timestamp=None)[0]
    s.logout_timestamp = datetime.datetime.now()
    s.save()
    auth.logout(request)
    sta = StatCounter.objects.all().order_by('created_on')
    if sta:
        st = sta[0]
        u = st.registered_users
        s = st.translated_sentences
        a = st.published_articles
    else:
        u = 0
        a = 0
        s = 0
    data = {
        'form': LoginForm(),
        'registered_users':u,
        'translated_sentences':s,
        'published_articles':a
        } 
    messages.success(request,"You're logged out successfully!!!")
    return render_to_response('login/home.html',data,context_instance=RequestContext(request))   

def account(request):
    user = request.user
    uid = user.pk

    if user.is_authenticated():
        sta = StatCounter.objects.all().order_by('created_on')
        if sta:
            st = sta[0]
            u = st.registered_users
            s = st.translated_sentences
            a = st.published_articles
        else:
            u = 0
            a = 0
            s = 0
          
        user_pro = UserProfile.objects.filter(user = uid)
        user_profile = user_pro[0]
        total_translated_sentences = user_profile.total_translated_sentences 
        no_of_perfect_translations = user_profile.no_of_perfect_translations 
        total_uploaded_tasks = user_profile.total_uploaded_tasks 
        total_evaluated_sentences = user_profile.total_evaluated_sentences
        data = {
                'uid':uid,
                'total_translated_sentences':total_translated_sentences,
                'no_of_perfect_translations': no_of_perfect_translations,
                'total_uploaded_tasks':total_uploaded_tasks,
                'total_evaluated_sentences':total_evaluated_sentences,
                'registered_users':u,
                'translated_sentences':s,
                'published_articles':a,
                'username':user
        } 
        return render_to_response('translation/account.html',data,context_instance=RequestContext(request))
    else:
        data = {
        'form': LoginForm(),
        'uid':uid
        } 
    messages.error(request,"You're not logged in!!!")
    return render_to_response('login/home.html',data,context_instance=RequestContext(request)) 

def upload(request):   
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
        return render_to_response('translation/upload.html',data,context_instance=RequestContext(request))
    else:
        data = {
        'form': LoginForm(),
        'username':user,
        } 
    messages.error(request,"You're not logged in!!!")
    return render_to_response('login/home.html',data,context_instance=RequestContext(request)) 

def process_upload(request):
    user = request.user
    uid = user.pk
    try:
        if request.method == 'POST':
            if request.POST.getlist('target_language'):     
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
                    'username':user,
                   }
            ta = TransactionAction.objects.filter(session = Session.objects.filter(user=user,logout_timestamp=None))[0]
            ta.task = Task.objects.get(pk=newtask.id)
            ta.action_timestamp = datetime.datetime.now()
            ta.save()
            messages.success(request,"File uploaded sucessfully!!!")
            return render_to_response('translation/account.html',data,context_instance=RequestContext(request))
    except:
        log.exception("Upload Failed!!!")
        traceback.print_exc() 
        messages.error(request, "Upload Failed")
   
def translate(request,uid):
    user = request.user
    if user.is_authenticated():
        try:
            logged_in_user_id = uid
            i = 0
            c = 0
            available_sentences_done_by_user = UserHistory.objects.filter(user=logged_in_user_id)
            available_microtasks = Microtask.objects.filter(assigned = 0)    
                                   
            for j in available_sentences_done_by_user:
                available_microtasks = available_microtasks.exclude(original_sentence = available_sentences_done_by_user[i]).order_by('id')
                i +=1
            
            for j in available_microtasks:
                c += 1
                
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
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
            else:
                available_microtask = available_microtasks[0]
                s = StaticMicrotask.objects.filter(id=available_microtask.static_microtask_id)
                parent_static_microtask = StaticMicrotask.objects.get(id=s)
                microtask_translation = parent_static_microtask.translated_sentence
                machine_translation = parent_static_microtask.machine_translation
                other = UserHistory.objects.filter(original_sentence=available_microtask.original_sentence)
                other_translations = ""

                for i in other:
                    text = i.translated_sentence
                    if text:
                        other_translations = other_translations + "-> " + text + '\n'
                                  
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
                }
                                
                available_microtask.assigned=True
                available_microtask.save()
                ta = TransactionAction()
                ta.session = Session.objects.filter(user=user,logout_timestamp=None)[0]
                ta.user = user
                ta.action = Master_Action.objects.filter(action="Translate")[0]
                ta.action_timestamp = datetime.datetime.now()
                ta.save()
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
        except:
            log.exception("Load microtask for translation Failed!!!")
            traceback.print_exc() 
            messages.error(request, "Load microtask for translation Failed!!!")
    else:
        data = {
        'form': LoginForm(),
        } 
        messages.error(request,"Please login.You're not logged in!!!")
        return render_to_response('login/home.html',data,context_instance=RequestContext(request))
    return HttpResponse("Error!!!")

def process_translate(request,id,uid):
    user = request.user    
    if user.is_authenticated():
        if request.method == 'POST':
            try:
                correction_episode = request.POST['cmd']
                epi = correction_episode.split(' ')
                i = 0
                list = []
                for j in epi:
                    if epi[i]=='' or epi[i]=='\n' or epi[i]=='\t' or epi[i]=='\t\t\t':
                        pass
                    else:
                        list.append(epi[i])
                    i += 1                
                
                engl = Microtask.objects.filter(pk=id)
                eng = engl[0]
                hist = UserHistory.objects.filter(microtask=eng)
                h = hist[0]
                h.translated_sentence = request.POST['translated_sentence']
                h.submission_timestamp = datetime.datetime.now()
                h.stability = 0.0
                h.current_active_tag = 1
                h.change_flag = 1
                h.status_flag = 'Reviewed'
                h.correction_episode = list 
                h.save()
                data = serializers.serialize('json', UserHistory.objects.filter(pk=h.id), fields=('correction_episode'), ensure_ascii=False)
                h.correction_episode = data
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
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))
            except:
                log.exception("Save translated microtask Failed!!!")
                traceback.print_exc() 
                messages.error(request, "Save translated microtask Failed!!!")
    else:
        return HttpResponse("Please login.You're not logged in!!!")

def load_context(request,id,uid):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            try:
                count = request.POST['context_size']
                english = Microtask.objects.get(id=id)
                rec = Microtask.objects.get(id = english.id)
                prev_translation = request.POST['translated_sentence']
                hist = UserHistory.objects.filter(user = uid, original_sentence = rec.original_sentence)
                h = hist[0]
               
                static = StaticMicrotask.objects.filter(original_sentence = rec.original_sentence)
               
                s = static[0]
                a = s.pk - int(count)
                b = s.pk + int(count)
                prev_context = ""
                next_context = ""

                while a < s.pk:
                    st = StaticMicrotask.objects.filter(id=a)
                    if st:
                        t = StaticMicrotask.objects.get(id=st)
                        prev_context = prev_context + t.original_sentence + ". "
                    a += 1

                c = s.pk + 1
                while c <= b:
                    st = StaticMicrotask.objects.filter(id=c)
                    if st:
                        t = StaticMicrotask.objects.get(id=st)
                        next_context = next_context + t.original_sentence + ". "
                    c += 1
                    
                sentence =  rec.original_sentence + prev_context + next_context
                dict = sentence.split(' ')
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
                
                data = {
                    'form': TranslateForm(instance=h),
                    'curr_id':id,
                    'uid': uid,
                    'english': rec.original_sentence,
                    'prev_context':prev_context,
                    'next_context':next_context,
                    'hindi': prev_translation,
                    'dictionary': hindi_dictionary,
                    'word':word,
                    'username':user,
                    }        
                return render_to_response('translation/translate.html',data,context_instance=RequestContext(request))     
            except:
                log.exception("Context loading Failed!!!")
                traceback.print_exc() 
                messages.error(request, "Context loading Failed!!!")
    else:
        return HttpResponse("Please login.You're not logged in!!!")

def account_settings(request,uid):
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
    return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))    

def process_account_settings(request,uid):
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
            if f_password == f_confirm_password:
                if f_email and f_first_name and f_last_name:
                    count = User.objects.exclude(username=request.user).filter(email=f_email).count() 
                                            
                    if count !=0:
                        data = {
                            'form': SignUpForm(request.POST), 
                        }
                        messages.error(request,"EmailID already in use.Try another one!!!")
                        return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
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
                        
                    data = {
                        'form': SignUpForm(), 
                        }
                    messages.success(request,"Record saved successfully!!.")
                    return render_to_response('translation/account.html',data,context_instance=RequestContext(request))                              
                else:
                    data = {
                        'form': SignUpForm(request.POST),
                        }
                    messages.error(request,"Please fill in all fields!!!")
                    return render_to_response('translation/account_settings.html',data,context_instance=RequestContext(request))
    
            else:
                data = {
                    'form': SignUpForm(request.POST),
                } 
                messages.error(request,"Confirm password correctly!!!")
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