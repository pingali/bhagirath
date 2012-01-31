import sqlite3
import re

splitlist = []
RE = re.compile('Ltd|Inc|Mrs|Mr|Ms|Prof|Gen|Rep|Sen|Retd|Ltd|Inc|Mrs|Mr|Ms|Prof|Dr|Gen|Rep|Sen|C.O|U.S')

def microtaskParser():
    data = ''
    conn = sqlite3.connect("/home/ankita/git/bhagirath/src/bhagirath/bhagirath.db")
    
    with conn:
        c = conn.cursor()
        sql_data = 'SELECT * FROM translation_subtask WHERE assigned=0'     
        try:
            c.execute(sql_data)
            results = c.fetchall()
            for row in results:
                subtask_id = row[0]
                task_id = row[1]
                data = row[2]
                break;
            sql_flag = "UPDATE translation_subtask SET assigned = 1 WHERE task_id = '?'",(task_id)
            try:
                c.execute(sql_flag)
                c.commit()
            except:
                c.rollback()        
        except:
            print "Error: unable to fetch data"
  
        data = data.replace('\'','\\\'')
        #entire data content is in 'data','dump data' contains whole data before the last See also link(to exclude refrences..etc)
        #find all occurencs of see also,mark index to discrd contnt after the last see also
        for_discard = data.rsplit('See also',1)
        dump_data = for_discard[0]

        splitlist = dump_data.split(". ") 
        
        for each in splitlist:
            each_index = splitlist.index(each)
            match_list = RE.findall(each)
            for i in match_list:
                if each.endswith(i):
                    #join this and next sentence and relace the two sentences in the list
                    join_after = splitlist.pop(each_index + 1)
                    join_before = splitlist.pop(each_index)
                    each = join_before + '. ' + join_after
                    splitlist.insert(each_index,each)
                    break        
            
         
        final = []
        for i in splitlist:
            final = i.split(' ')
            index = 0
            spacecount =0
            for each in final:
                if each == '':
                    index = index + 1                   
                else:
                    dump = ''
                    group = final[index:]
                    for next in group:
                        if next == '':
                            spacecount = spacecount + 1
                            if spacecount > 1:
                                break
                            else:
                                continue
                        dump = dump + ' '+ (''.join(str(next)))
                        index = index + 1
                        
                    if not(dump == ''):        
                        #if single word translate and replace...google api??
                        if (len(dump.split(' '))<=6):
                            dump_list = dump.split(' ')
                            #translate that word as it is and store, code to be writen, google api??
                        else:    
                            #print (dump)    
                            c = conn.cursor()
                            t = (task_id,subtask_id,dump,False,False,0)
                            c.execute("INSERT INTO translation_staticmicrotask (task_id,subtask_id,original_sentence,assigned,scoring_done,hop_count) VALUES (?,?,?,?,?,?)",t)
                            c.close()
    
    conn.close()