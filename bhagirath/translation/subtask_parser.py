# coding: utf-8
import lxml.html
from lxml.html.clean import Cleaner
from bhagirath.translation.models import Task,Subtask

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
   # print html_source.encode('utf-8')
    cleaner = Cleaner(scripts = True, style = True,links = False)
    data =  cleaner.clean_html(html_source)
    obj = lxml.html.fromstring(data)
    cleaned_data = obj.text_content()
    record = cleaned_data
    
    sub = Subtask() 
    sub.task = Task.objects.get(html_doc_name = file)
    sub.original_data = record
    sub.save()
    
    print "subtask_done"
   
  
 

