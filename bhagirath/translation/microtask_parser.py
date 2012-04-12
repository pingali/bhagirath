# coding: utf-8
from bhagirath.translation.models import Task,Subtask,StaticMicrotask,Master_Experiment, Master_English2Hindi
from stemming.porter2 import stem
from django.core import serializers
import re

splitlist = []
RE = re.compile('\bSgt|p|v|pp|cf|Retd|Ltd|Inc|Mrs|Mr|Ms|Prof|Dr|Gen|Rep|Sen|C.O|U.S|U.K|i.e|ex|rep|prof|dr|Co|co|ltd|mr|ms|mrs|\
                Sgt|sgt|Maj|maj|Col|col|etc|e.g|Ing|Asso|asso\b')

def microtaskParser():
        data = ''
        results = Subtask.objects.filter(assigned = 0)
        if results:
            subtask = results[0]#subtask id
            subtask_id = subtask.id
            sub = Subtask.objects.get(id = subtask_id)
        
            task_id = sub.task_id
            task = Task.objects.get(id = task_id)
            sub.assigned = 1 
             
            data = str(sub.original_data)
          
            data = re.sub('[\t\n]+','\n',data)
            data = re.sub('(\[see\])',r'', data)
            data = re.sub('(\[citation needed\])',r'', data)
            data = re.sub('(\[cite.*\])',r'', data)
            data = re.sub('(\[deadlink\])',r'', data)
            data = re.sub('(\[disambi*\])',r'', data)
            data = re.sub('(\[note*\])',r'', data)
            data = re.sub('(\[[0-9]+\])', r'',data)
            
            lst = data.split("\n")
        
            string = ''
            for each1 in lst:
                sent = each1.split(". ")
                for each in sent:
                        string = string + '. SEN_END ' + (''.join(str(each))).lstrip()
               
            string = re.sub('([\?\.\!]+\s*)(\[\d+\]\s*)(\w+)', r'\1 SEN_END \2\3', string)
            string = re.sub('(\.\"[\t\n\s]+)([A-Z]+)', r'\1SEN_END \2', string)
            match_list = RE.findall(string)
            for abr in match_list:
                string = re.sub(r'\b[ \s\W]+' + abr + r'. SEN_END\b', " "+abr+".", string)
            string = re.sub('(SEN_END)\s*([a-z]+)',r'\s\2', string)
            string = re.sub('([\s\W]+)([A-Z0-9][\.\?\!]\s+)(SEN_END)', r'\1\2',string)
            string = re.sub('\.+','.',string)
            string = re.sub('[\t\s]+',' ',string)
            #print string
            i = 0
            splitlist = string.split("SEN_END")
            
            b = Master_Experiment.objects.all()
            
            td = str(sub.translated_data)
            itd = td.split("\n\n")
            k = 0
             
            for each in splitlist:
                each1= each
                if not(each == '. ' or each == '' or each == ' '):        
                                #if single word translate and replace...google api??
                                if (len(each.split(' '))<=4):
                                    flag = 1
                                    #code yet to be written
                                    #translate that word as it is and store, code to be writen, google api??
                                else:
                                    if int(i) == 10:
                                        i = 0
                                    a = b[i]
                                    micro = StaticMicrotask()  
                                    micro.subtask = subtask
                                    micro.task = task
                                    micro.original_sentence = each
                                    micro.bit_array = a
				    micro.meaning = dictionary(each)
                                    micro.save()
                                    micro.machine_translation = itd[k]
				    dat = serializers.serialize('json', StaticMicrotask.objects.filter(pk=micro.id), fields=('meaning'), ensure_ascii=False)
                                    micro.meaning = dat
                                    micro.save()
                                    i += 1
                                    k += 1
                                 
            sub.save()
            msg = ""
        else:
            msg = "No subtask available for parsing"
            
        return msg 


def dictionary(sentence):
    words = sentence.split(' ')
    cnt = len(words)
    x = 0
    
    dict = []
    o = [".",",",";","?","!",":","'",")","]","}",'"']
    r = ["'","(","[","{",'"']
    
    while x < cnt:
        s = words[x]
        if s:
            while s[-1] in o or s[0] in r:
                if s[-1] in o:
                    s = s[:-1]
                if s:
                    if s[0] in r:
                        s = s[1:]
                if s:
                    pass    
                else:
                    break
        
        y = s.lower()
        
        mean = Master_English2Hindi.objects.filter(english_word = y)
        if not mean:
            z = stem(y)
            mean = Master_English2Hindi.objects.filter(english_word = z)
        
        for p in mean:
            w =  Master_English2Hindi.objects.get(pk=p.pk)
            mean_dict = {}
            mean_dict['word'] = y
            mean_dict['pos'] = w.pos
            mean_dict['mean'] = w.hindi_word.split("--") 
            dict.append(mean_dict)
        x += 1
    return dict   

def tempMicrotaskParser():
        data = ''
        results = Subtask.objects.filter(assigned = 0)
        print results
        if results:
            subtask = results[0]#subtask id
            subtask_id = subtask.id
            sub = Subtask.objects.get(id = subtask_id)
        
            task_id = sub.task_id
            task = Task.objects.get(id = task_id)
            sub.assigned = 1 
            
            k = 0
            b = Master_Experiment.objects.get(pk=4)
             
            data = str(sub.original_data)
            lst = data.split("\r\n\r\n")
            
            td = str(sub.translated_data)
            itd = td.split("\n\n")
 
            for each in lst:
                micro = StaticMicrotask()  
                micro.subtask = subtask
                micro.task = task
                micro.original_sentence = each
                micro.bit_array = b
		micro.meaning = dictionary(each)
                micro.save()
                micro.machine_translation = itd[k]
		dat = serializers.serialize('json', StaticMicrotask.objects.filter(pk=micro.id), fields=('meaning'), ensure_ascii=False)
                micro.meaning = dat                
		micro.save()
                k += 1
                                 
            sub.save()
            msg = ""
        else:
            msg = "No subtask available for parsing"
            
        return msg 
