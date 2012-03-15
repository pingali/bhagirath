# coding: utf-8
from bhagirath.translation.models import Task,Subtask,StaticMicrotask,Master_Experiment
import re

splitlist = []
RE = re.compile('\bSgt|p|v|pp|cf|Retd|Ltd|Inc|Mrs|Mr|Ms|Prof|Dr|Gen|Rep|Sen|C.O|U.S|U.K|i.e|ex|rep|prof|dr|Co|co|ltd|mr|ms|mrs|\
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
  
    data = re.sub('[\t\n]+','\n',data)
    
    data = re.sub('(\[see\])',r'', data)
    data = re.sub('(\[citation needed\])',r'', data)
    data = re.sub('(\[cite.*\])',r'', data)
    data = re.sub('(\[deadlink\])',r'', data)
    data = re.sub('(\[disambi*\])',r'', data)
    data = re.sub('(\[note*\])',r'', data)
    data = re.sub('([\s\W]*)(\[[0-9]+\])', r'',data)

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
                            
                            join_before = sent.pop(each_index)
                            try:
                                join_after = sent.pop(each_index + 1)
                            except:
                                join_after = ''
                            each = join_before + '. ' + join_after
                            sent.insert(each_index,each)
                            
                            break
                string = string + '. SEN_END ' + (''.join(str(each))).lstrip()
        else:
                string = string + '. SEN_END ' + (''.join(str(each1))).lstrip()
    
    string = re.sub('([\?\.\!]+\s*)(\[\d+\]\s*)(\w+)', r'\1 SEN_END\2\3', string)
    string = re.sub('(SEN_END)\s*([a-z]+)',r'\2', string)
    string = re.sub('([\s\W]+)([A-Z0-9][\.\?\!]\s+)(SEN_END)', r'\1\2',string)
    
    
    flag = 0
    i = 0
    splitlist = string.split("SEN_END")
    b = Master_Experiment.objects.all()
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
                            micro.save()
                            i += 1
                             
    sub.save()
    
