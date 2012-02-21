# coding: utf-8
from bhagirath.translation.models import Task,Subtask,StaticMicrotask,Master_Experiment
import re

splitlist = []
RE = re.compile('\bRetd|Ltd|Inc|Mrs|Mr|Ms|Prof|Dr|Gen|Rep|Sen|C.O|U.S|U.K|i.e|ex|rep|prof|dr|Co|co|ltd|mr|ms|mrs|\
                Sgt|sgt|Maj|maj|Col|col|etc|e.g|Ing|Asso|asso\b')

def microtaskParser():
    data = ''
    results = Subtask.objects.filter(assigned = 0)
    subtask = results[0]#subtask id
    subtask_id = subtask.id
    sub = Subtask.objects.get(id = subtask_id )

    task_id = sub.task_id
    task = Task.objects.get(id = task_id)
    sub.assigned = 1 
     
    data = str(sub.original_data)
     
    #data = data.encode('utf-8')   
    data = re.sub('[\t\n]+','\n',data)
    lst = data.split("\n")
    string = ''
    for each1 in lst:
        sent = each1.split(". ")
        if len(sent) > 1:
            #for hamdling acronyms LIST TO BE UPDATED
            for each in sent:
                each_index = sent.index(each)
                match_list = RE.findall(each)
                for i in match_list:
                        if each.endswith(i):
                            #join this and next sentence and relace the two sentences in the list
                            join_after = sent.pop(each_index + 1)
                            join_before = sent.pop(each_index)
                            each = join_before + '. ' + join_after
                            sent.insert(each_index,each)
                            #print each + "\n" #dump 
                            break
                string = string + '. SEN_END ' + (''.join(str(each))).lstrip()
        else:
                string = string + '. SEN_END ' + (''.join(str(each1))).lstrip()
    
    string = re.sub('([\?\.\!]+\s*)(\[\d+\]\s*)(\w+)', r'\1 SEN_END\2\3', string)
    string = re.sub('(SEN_END)\s*([a-z]+)',r'\2', string)
    string = re.sub('([\s\W]+)([A-Z0-9][\.\?\!]\s+)(SEN_END)', r'\1\2',string)
    string = re.sub('(\.)+','.', string)
    
    flag = 0
    i = 0
    splitlist = string.split("SEN_END")
    b = Master_Experiment.objects.all()
    for each in splitlist:
        each1= unicode(each)
        
        if not(each == '. ' or each == '' or each == ' '):        
                        #if single word translate and replace...google api??
                        if (len(each.split(' '))<=1):
                            flag = 1
                            #code yet to be written
                            #translate that word as it is and store, code to be writen, google api??
                        else:
                            a = b[i]
                            micro = StaticMicrotask()  
                            micro.subtask = subtask
                            micro.task = task
                            micro.original_sentence = each
                            micro.bit_array = a.id
                            micro.save()
                            if i == 10:
                                i = 0
                            else:
                                i += 1
                             
    sub.save()
   
    
