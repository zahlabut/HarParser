__author__ = 'Arkady'
from BeautifulSoup import BeautifulSoup
from fuzzywuzzy import fuzz
from time import gmtime, strftime
import json,shutil,os,time,csv
import csv,codecs,cStringIO,os,psycopg2,urllib2,sys,shutil,xlsxwriter,time,ConfigParser,string
from collections import Counter
from string import Template
import re,random
from fuzzywuzzy import fuzz
#from BeautifulSoup import BeautifulSoup
import BeautifulSoup
from time import gmtime, strftime
csv.field_size_limit(999999999)
import pyscreenshot as ImageGrab


def WRITE_DICTS_TO_CSV(csv_name,Dict_List):
    ### Get all unique keys ###
    DELETE_LOG_CONTENT(csv_name)
    all_keys=[]
    for item in Dict_List:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)
    csv_headers=all_keys
    ADD_LIST_AS_LINE_TO_CSV_FILE(csv_name,csv_headers)
    for item in Dict_List:
        list_to_write=['' for k in csv_headers]
        for key in item.keys():
            if key in csv_headers:
                list_to_write[csv_headers.index(key)]=item[key]
        ADD_LIST_AS_LINE_TO_CSV_FILE(csv_name,list_to_write)


def SPEC_PRINT(string_list):
    len_list=[]
    for item in string_list:
        len_list.append(len('### '+item.strip()+' ###'))
    max_len=max(len_list)
    print ''
    print"#"*max_len
    for item in string_list:
        print "### "+item.strip()+" "*(max_len-len("### "+item.strip())-4)+" ###"
    print"#"*max_len+'\n'


def PIL_SAVE_SCREENSHOT(dst_path,file_name):
    time.sleep(2)
    ImageGrab.grab_to_file(os.path.join(dst_path,file_name+'.png'))
    time.sleep(2)
def GET_LINKS_FROM_HTML(html):
    links=[]
    soup = BeautifulSoup.BeautifulSoup(html)
    for line in soup.findAll('a'):
        links.append(line.get('href'))
    return links
def EXIT(string):
    stam=raw_input(string)
    sys.exit(1)
def CONTINUE (message=''):
    print message
    cont=raw_input('Continue? y/n  ')
    if (cont=='y'):
        print "Your choose is: '"+cont+"' continue execution!"
        print ''
    elif (cont=='n'):
        print "Your choose is: '"+cont+"' execution will be stopped!"
        sys.exit(1)
    else:
        print "No such option: '"+cont+"'"
        CONTINUE ()
def CHOOSE_OPTION_FROM_LIST_1(lis, msg):
    print ''
    list_object=[item for item in lis]
    list_object.sort(key=str.lower)
    if 'Exit' in list_object:
        list_object.remove('Exit')
        list_object.sort(key=str.lower)
        list_object.append('Exit')
    try:
        if (len(list_object)<1):
            print lis,msg
            print "Nothing to choose :( "
            print "Execution will stop!"
            time.sleep(5)
            EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
            sys.exit(1)

        print msg
        counter=1
        for item in list_object:
            print str(counter)+') - '+item
            counter=counter+1

        choosed_option=raw_input("Choose option by entering the suitable number! ")
        while (int(choosed_option)<0 or int(choosed_option)> len(list_object)):
            print "No such option - ", choosed_option
            choosed_option=raw_input("Choose option by entering the suitable number! ")

        print "Chosen option is : '"+list_object[int(choosed_option)-1]+"'\r\n"
        return list_object[int(choosed_option)-1]

    except Exception, e:
        print '*** No such option!!!***', e
        #print 'Execution will stop! '
        #time.sleep(5)
        #EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
        #sys.exit(1)
        CHOOSE_OPTION_FROM_LIST_1(list_object, msg)
def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')
    f.close()
def DELETE_LOG_CONTENT_PATH(path):
    f = open(os.path.join(path), 'w')
    f.write('')
    f.close()
def ADD_LIST_AS_LINE_TO_CSV_FILE(csv_file_name,lis):
    try:
        f = open(csv_file_name, 'ab')
        writer = csv.writer(f)
        writer.writerow(lis)
        f.close()
    except Exception, e:
        print '*** ADD_LIST_AS_LINE_TO_CSV_FILE!!! ***', e
def ADD_LIST_AS_LINE_TO_CSV_FILE_PATH(csv_file_path,file_name,lis):
    try:
        f = open(os.path.join(csv_file_path,file_name), 'ab')
        writer = csv.writer(f)
        writer.writerow(lis)
        f.close()
    except Exception, e:
        print '*** ADD_LIST_AS_LINE_TO_CSV_FILE!!! ***', e
def READ_CSV_AS_NESTED_LIST(file_name):
    try:
        nested=[]
        with open(file_name, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                nested.append(row)
        return nested

    except Exception, e:
        print '*** READ_CSV_AS_NESTED_LIST!!! ***', e
def CREATE_TEST_DIRECTORY(DIR_NAME):
    TEST_RESULT_DIR_PATH=os.path.join(os.path.abspath('.'),DIR_NAME)
    if os.path.exists(TEST_RESULT_DIR_PATH):
        try:
            shutil.rmtree(TEST_RESULT_DIR_PATH)
        except:
            pass
        time.sleep(1)
        os.mkdir(TEST_RESULT_DIR_PATH)
    else:
        os.mkdir(TEST_RESULT_DIR_PATH)
def RUN_SQL_TO_FILE(dbname,user,host,password,sql,result_file,db_port,single_sql=True):
    try:
        DELETE_LOG_CONTENT(result_file)
        conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password+" port="+db_port
        cursor = psycopg2.connect(conn_string).cursor()

        if single_sql==True:
            cursor.execute(sql)
            data = cursor.fetchall()
            a = cursor.description
            headers=[a[0] for a in cursor.description]
            data=[list(item) for item in data]
            data.insert(0, headers)
            for lis in data:
                print lis
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,lis)

        if single_sql==False:
            count=0
            total_sqls=len(sql)
            all_data=[]
            for item in sql:
                count+=1
                cursor.execute(item)
                data = cursor.fetchall()
                a = cursor.description
                headers=[a[0] for a in cursor.description]
                if len(data)!=0:
                    data=[list(item) for item in data][0]
                    all_data.append(data)
                    percentage_done=count*100.0/total_sqls
                    sys.stdout.write('Completed SQL quaries:'+str(round(percentage_done,2))+'%\r\n')
                    #sys.stdout.flush()
                    #print round(percentage_done,2)
            all_data.insert(0, headers)

            for lis in all_data:
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,lis)
        return True
    except Exception, e:
        print str(e)
        return False
def RUN_SQL(dbname,user,host,password,db_port,sql):
    try:
        conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password+" port="+db_port
        cursor = psycopg2.connect(conn_string).cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        a = cursor.description
        headers=[a[0] for a in cursor.description]
        data=[list(item) for item in data]
        all_dic=[]
        for d in data:
            keys=headers
            values=d
            dictionary=dict(zip(keys, values))
            all_dic.append(dictionary)
        return [True,all_dic]
    except Exception, e:
        return [False,str(e)]
def RUN_SQL_SAMPLE_DB(dbname,user,host,password,db_port,sql,timeout=100):
    start_time=time.time()
    end_time=start_time+timeout
    sample_time=time.time()
    all_dic=[]
    while all_dic==[] and sample_time<end_time:
        time.sleep(30)
        sample_time=time.time()
        print 'Sampling Condition is True!','Time rest:' +str(end_time-sample_time),'SQL result: '+str(all_dic)
        try:
            conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password+" port="+db_port
            cursor = psycopg2.connect(conn_string).cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            a=cursor.description
            headers=[a[0] for a in cursor.description]
            data=[list(item) for item in data]
            for d in data:
                keys=headers
                values=d
                dictionary=dict(zip(keys, values))
                all_dic.append(dictionary)
        except Exception, e:
            print str(e)
            all_dic=[]
            #pass
            continue
    return all_dic
def SQL_QUERY_GET_KEYS(sql_string):
    keys=re.findall('\{(.*?)\}', sql_string)
    keys=[item.lower() for item in keys]
    return keys
def SQL_QUERY_SET_VALUES_BY_KEYS(sql_query, dic):
    for k in dic:
        sql_query=sql_query.replace('{'+k+'}',dic[k])
    return sql_query
def CREATE_EXCEL_SHEETS(file_name,sheet_dict):
    #Create an new Excel file and add a worksheet.
    try:
        workbook = xlsxwriter.Workbook(file_name)
        for d in sheet_dict.keys():
            worksheet = workbook.add_worksheet(d[0:30])#Sheet name should be less 31
            bold = workbook.add_format({'bold': 1})
            nes_lis_data=sheet_dict[d]
            row=0
            for lis in nes_lis_data:
                col=0
                for item in lis:
                    #item=item.decode("utf8")
                    #print item
                    worksheet.write(row, col, str(item).decode('utf8', 'ignore'))
                    col+=1
                row+=1
        workbook.close()
        return True
    except Exception, e:
        print '*** CREATE_EXCEL_SHEETS!!! ***', e

def GET_LIST_STAT(lst):
    len_lis=len(lst)
    data = Counter(lst)
    out=data.most_common()
    display_data=[['Value','Appearance','Percentage']]
    for item in out:
        line=[]
        line.append(item[0])
        line.append(item[1])
        percentage=item[1]*100.0/len_lis
        line.append(str(round(percentage,3))+'%')
        display_data.append(line)
    return display_data
