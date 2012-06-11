# coding: utf-8
import lxml.html
from lxml.html.clean import Cleaner
from bhagirath.translation.models import Task,Subtask
import re

exclude = ['Bibliography', 'See also', 'Notes', 'References', 'Sources', 'Further reading', 'External links']

def subtaskParser(filename):
    import sys
    if filename is None:
        filename = sys.argv[1:]

    if filename:
        file = filename
    else:
        pass
    

    if file == '-':
        f = sys.stdin
    else:
        try:
            f = open(file, 'r')
           
        except IOError, msg:
            print file, ":", msg
            sys.exit(1)

    html_source = f.read()
    cleaner = Cleaner(scripts = True, style = True,links = False)
    data =  cleaner.clean_html(html_source)
    obj = lxml.html.fromstring(data)
    cleaned_data = obj.text_content()
    record = cleaned_data
    #print record
    
    #subtask processing
    index = 0
    content = []
    linesplit = record.split("\n")
    #print linesplit
    re1 = re.compile('([\s\W]*)([0-9]+(\.*[0-9]*)*\s+)')
    for each in linesplit:
        index = index + 1
        if each =='':
            continue
        if each == "Contents":
            index = index+1
            check = re.match(re1,linesplit[index])
            while linesplit[index].startswith(check.group(1)):
                for item in exclude:
                    #print linesplit[index]
                    if linesplit[index].endswith(item):
                        add = re.sub(re1,r'',linesplit[index])
                        content.append(add)
                linesplit.remove(linesplit[index]) 
                if linesplit[index] == '' :
                    while linesplit[index] == '':
                        index = index + 1 
                check = re.match(re1,linesplit[index]) 
                if check == None:
                    break        
    content.reverse() 
   
    rev = linesplit
    rev.reverse()
        #if each starts wid number, it is an item in the contents..so see if it matches with one of the exclude.....mke a list and copy dat..after words delete frm end the part after each exlcude eg,. first delete everythng after extrnal links if it was there in ontents..
    index2 = 0
    final = []
    #print content
    for i in rev:
        for item in content:
           
            if i.endswith(item):
                print i
                #remove the content upto this item from start since it is reversed list                                
                ind = rev.index(i)
                final = rev[(ind+1):]
                if content.index(item) == 0:
                    content.remove(item) 
                print content
                break
         
    
    final.reverse()
    data =''
    for each in final:
        data = data + '\n' + (''.join(str(each)))
        
    #print data
            
    sub = Subtask() 
    sub.task = Task.objects.get(pk = id)
    sub.original_data = data
    sub.save()
    

    print "subtask_done"
   
  
#subtaskParser('/home/bhagyashree/Desktop/all content desktop/BtechProject/150_articles/sports -oylmpics (4)/Paralympic Games - Wikipedia, the free encyclopedia.html') 