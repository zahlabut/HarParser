#!/usr/bin/python
import csv,codecs,cStringIO,os,psycopg2,urllib2,os,sys,shutil,xlsxwriter,time,ConfigParser,string
from collections import Counter
from string import Template
import re,random
from fuzzywuzzy import fuzz
from BeautifulSoup import BeautifulSoup
csv.field_size_limit(999999999)

class MyOutput():
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.log = open(logfile, 'w')
    def write(self, text):
        self.stdout.write(text)
        self.log.write(text)
        self.log.flush()
    def close(self):
        self.stdout.close()
        self.log.close()
	    
def PRINT_DUP_LINES(lis):
    ret_lis=[]
    for line in lis:
        line_counter=lis.count(line)
        if line_counter>1:
            #ret_lis.append('Counter:'+str(line_counter)+' Line:'+str(line))
            ret_lis.append(str(line_counter)+' '+str(line))
    for item in list(set(ret_lis)):
        print item
def CONTINUE (message=''):
    print message 
    cont=raw_input('Continue? y/n  ')
    if (cont=='y'):
        print "Your choose is: '"+cont+"' continue execution!"
        print ''
    elif (cont=='n'):
        print "Your choose is: '"+cont+"' execution will be stopped!" 
        EXIT("**************** TYPE ENTER TO EXIT!!!   ******************")
        sys.exit(1)
    else:
        print "No such option: '"+cont+"'"
        CONTINUE ()
def CONVERT_INI_TO_VARIABLES(ini_file_name):
    try:
        config = ConfigParser.ConfigParser()
        config.read(ini_file_name)

        dictionary = {}
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)

        sections=config.sections()
        for section in sections:
            data=dictionary[section]
            globals().update(data)
    except Exception, e:
        print '*** CONVERT_INI_TO_VARIABLES!!! ***', e
        EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
        sys.exit(1) 
def SORT_LIST(lis):
    return sorted(lis, key=str.lower)
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
def ADD_LIST_AS_LINE_TO_CSV_FILE(csv_file_name,lis,delim=','):
    try:
        f = open(csv_file_name, 'ab')
        writer = csv.writer(f,delimiter=delim)
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
class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")
class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self
class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
def INSERT_TO_LOG_UTF(file_name,string):
    try:
        fil=open(file_name,'a')
        fil.write(string.encode("UTF-8")+'\n')
        fil.close()
    except Exception, e:
        print str(e)
def CONVERT_UTF_FILE_TO_CSV_UNICODE(file_in,file_out):
    with open(file_in,'rb') as fin, open(file_out,'wb') as fout:
        reader = UnicodeReader(fin)
        writer = UnicodeWriter(fout,quoting=csv.QUOTE_ALL)
        for line in reader:
            writer.writerow(line)
def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')	
def CONVERT_UNICODE_FILE_TO_CSV(file_in,file_out):
    DELETE_LOG_CONTENT(file_out)
    with open(file_in,'rb') as fin:
        reader = UnicodeReader(fin)
        for line in reader:
            ADD_LIST_AS_LINE_TO_CSV_FILE(file_out,line)
def EXIT(string):
    stam=raw_input(string)
    sys.exit(1)
def MULTI_CHOOSE_OPTION_FROM_LIST_1(list_object, msg):
    if len(list_object)==0:
        print 'Options list is empty! Nothing to choose! '
        time.sleep(5)
        EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
        sys.exit(1)
    try:
        print '\r\n'+msg
        for item in list_object:
            print '<'+item+'>',
        print '' 
        choosed_options=raw_input("Enter option names separated by space or type '*' for all at once: ")
        result=[]

        opt_list=list(choosed_options.split(' '))
        if (opt_list[0]=='*'):
            for item in list_object:
                result.append(item)

        if (opt_list[0]!='*'):
            for item in opt_list:
                if item in list_object:
                    result.append(item)
                else:
                    print 'Ignore <'+item+'>, such option is not exists!'

        print "Your choice is: ", list(set(result))
        if len(list(set(result)))==0:
            print "OPtions list is empty, cannot continue!!!"
            EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
            sys.exit(1)
        return list(set(result))
    except  Exception, e:
            print '*** MULTI_CHOOSE_OPTION_FROM_LIST FAILED!!! ***', e
            EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
def GET_INTEGER_OR_ENTER(msg):
    if_int=None
    while if_int!=True:
        string=raw_input(msg)
        if string=='':
            if_int=True
            intg=''
            #break
        else:
            try:
                intg=int(string)
                if_int=True
            except:
                print '*** Should be integer value!!! ***'
    return intg
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
def REMOVE_DUP_FROM_NESTED_LIST(nested_list):
    result=[]
    count=0
    for lis in nested_list:
        if lis not in result:
            result.append(lis)
        else:
            count+=1
    return [result,count]
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
def RUN_SQL(dbname,user,host,password,sql,result_file,db_port,single_sql=True):
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
def SQL_QUERY_GET_KEYS(sql_string):
    keys=re.findall('\{(.*?)\}', sql_string)
    keys=[item.lower() for item in keys]
    return keys
def SQL_QUERY_SET_VALUES_BY_KEYS(sql_query, dic):
    for k in dic:
        sql_query=sql_query.replace('{'+k+'}',dic[k])
    return sql_query
def STRIP_NON_ASCII(s):
    s=re.sub(r'[^a-zA-Z0-9]','', s)
    return s
def INSERT_TO_LOG(log_file, msg, time_flag=0):
    log_file = open(log_file, 'a')
    if time_flag==0:
        string=msg
    if time_flag==1:
        string=time.strftime("%Y-%m-%d %H:%M:%S")+' '+msg
    log_file.write(string+'\n')
    log_file.close()
def FUZZY(string1, string2, percentage):
    result=fuzz.ratio(string1.lower(),string2.lower())
    if result<percentage:
        return True
    else:
        return False
def isAscii(s):
    for c in s:
        if c not in string.ascii_letters:
            return False
    return True
def COUNT_NO_BLANKS_IN_LIST(lis):
    lis=[item for item in lis if item!='']
    return len(lis)
def MERGE_ITEMS_IN_LIST(lis):
    res=''
    for item in lis:
        res+=item
    return res
def GET_SUBLIST_BY_INDEXES(lis,indexes_lis):
    res=[]
    for i in indexes_lis:
        res.append(lis[i])
    return res
def IS_FLOAT(str):
    try:
        str=float(str)
        return[True,str]
    except:
        return[False,str]
def MY_LIS_COMPARE(lis1,lis2):
    lis1=[item.lower().strip().replace(' ','') for item in lis1]
    lis2=[item.lower().strip().replace(' ','') for item in lis2]
    ### Change for Storm to LPP result comparison
    #replace_strings=['good','error','warning']
    replace_strings=[]
    for string in replace_strings:
        if string in lis1[-1].lower():
            lis1[-1]=string

    for string in replace_strings:
        if string in lis2[-1].lower():
            lis2[-1]=string

    indexes=[]
    if lis1==lis2:
        res=True

    else:
        res=False
        for x in range(0,len(lis1)):
            if str(lis1[x]).lower()!=str(lis2[x]).lower():
                indexes.append(x)
    return [res,indexes]
def MY_LIS_COMPARE_FLOAT_ROUND(lis1,lis2,round_number=1):
    lis1_converted=[]
    for item in lis1:
        is_float=IS_FLOAT(item)
        if is_float[0]==False:
            lis1_converted.append(item)
        if is_float[0]==True:
            lis1_converted.append(str(round(is_float[1],round_number)))
            #lis1_converted.append(str(is_float[1])[0:2])


    lis2_converted=[]
    for item in lis2:
        is_float=IS_FLOAT(item)
        if is_float[0]==False:
            lis2_converted.append(item)
        if is_float[0]==True:
            lis2_converted.append(str(round(is_float[1],round_number)))
            #lis2_converted.append(str(is_float[1])[0:2])

    lis1=lis1_converted
    lis2=lis2_converted

    lis1=[item.lower().strip().replace(' ','') for item in lis1]
    lis2=[item.lower().strip().replace(' ','') for item in lis2]

    ### Change for Storm to LPP result comparison
    #replace_strings=['good','error','warning']
    replace_strings=[]
    for string in replace_strings:
        if string in lis1[-1].lower():
            lis1[-1]=string

    for string in replace_strings:
        if string in lis2[-1].lower():
            lis2[-1]=string

    indexes=[]
    if lis1==lis2:
        res=True

    else:
        res=False
        for x in range(0,len(lis1)):
            if str(lis1[x]).lower()!=str(lis2[x]).lower():
                indexes.append(x)
    return [res,indexes]
def MY_LIS_COMPARE_FLOAT_DEVIATION(lis1,lis2,deviation=10):
    not_equal_indexes=[]
    for x,y in zip(lis1,lis2):
        x_result=IS_FLOAT(x)
        y_result=IS_FLOAT(y)
        if x_result[0]==True and y_result[0]==True:
            delta=(x_result[1]-y_result[1])
            if delta!=0:
                delta=delta/max(x_result[1],y_result[1])*100
                if delta <(-1)*deviation or delta>deviation:
                    not_equal_indexes.append(lis1.index(x))

        else:
            if x.lower()!=y.lower():
                not_equal_indexes.append(lis1.index(x))
    if len(not_equal_indexes)>0:
        return [False,not_equal_indexes]
    else:
        return [True,[]]


#print MY_LIS_COMPARE_FLOAT_DEVIATION(['a','b','1.33453453452'],['a','b','1.53'])
#print MY_LIS_COMPARE(['a','b','1.33453453452'],['a','b','1.43'])
#print MY_LIS_COMPARE(['a','b','1.43'],['a','b','1.43'])


################################################################# Main ################################################################# 
SPEC_PRINT(['--- ColboTigo - tool for saving your time and nervous :) " ---', 'Version 1.0', 'Created by Arkady'])
DELETE_LOG_CONTENT('RuntimeColbotigo.log')
sys.stdout=MyOutput('RuntimeColbotigo.log')
sys.stderr=MyOutput('RuntimeColbotigo.log')
CONVERT_INI_TO_VARIABLES('conf.ini')
modes=['Remove Column from CSV file',
       'Convert CSV file to Unicode file',
       'Get statistics of specific column in CSV file',
       'Perform statistics for *.csv file',
       'Add empty column(s) to CSV file',
       'Convert Unicode file to CSV file',
       'Export specific column(s) from CSV file',
       'Export lines by searching some string in given CSV file column',
       'Export common lines of 2 CSV files by given column(s)',
       'Delete file','Create EXCEL from several CSV files',
       'Create CSV file with given lines number using template file',
       'Create CSV file from SQL query output',
       'Show CSV file column names',
       'Merge CSV files',
       'Show common columns of several CSV files',
       'Generate ContactEmail basing on ContactFirstName, ContactLastName, CompanyWebsite',
       'Split CSV file to range of lengths',
       'Compare two *.csv files','Compare two *.csv files as floats','GREP lines by string',
       'Calculate average value of specific column',
       'Fix CSV (Remove line if its length is bigger than header line length)',
       'Print single row from file "Column_Name:Value"',
       'Convert *csv file from "comma separated" to "tab separated"',
       'Export values from specific column, that contains space tab',
       'Remove empty lines from csv file',
       'Show duplicated lines',
       'Split Marketo OE enriched Data','Generate Leads (By leads number)','Count unique values in given column',
       'Generate Leads (By file size)','Get missing values of 2 files by given column',
       'Print common unique values of specific field in two *csv files',
       'Create duplicated Leads','Exit']
mode=None
while mode!='Exit':
    #try:
        mode=CHOOSE_OPTION_FROM_LIST_1(modes,"Please choose Operation Mode: ")

        if mode=='Remove Column from CSV file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            result_file=csv_file.replace('.csv','')+'_COLUMNS_REMOVED.csv'
            option=None
            fields_to_remove=[]
            csv_file_fields.append('Exit')
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose fields to remove and then "Done" option to continue: ')
                #option=MULTI_CHOOSE_OPTION_FROM_LIST_1(options, 'Please choose fields to remove and then "Done" option to continue: ')
                if option not in fields_to_remove:
                    fields_to_remove.append(option)
                else:
                    print '*** "'+option+'" is already in your list! ***'
            fields_to_remove.remove('Exit')
            csv_file_fields.remove('Exit')
            fields_to_remove_indexes=[csv_file_fields.index(item) for item in fields_to_remove]
            #print fields_to_remove_indexes
            DELETE_LOG_CONTENT(result_file)
            #csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            for lis in csv_file_data:
                new_lis=[item for item in lis if lis.index(item) not in fields_to_remove_indexes]
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,new_lis)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])		

        if mode=='Convert CSV file to Unicode file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            result_file=csv_file.replace('.csv','.txt')
            CONVERT_UTF_FILE_TO_CSV_UNICODE(csv_file,'temp')
            shutil.move('temp',result_file)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	


        if mode=='Convert Unicode file to CSV file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.txt')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            result_file=csv_file.replace('.txt','.csv')
            CONVERT_UNICODE_FILE_TO_CSV(csv_file,'temp')
            shutil.move('temp',result_file)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	


        if mode=='Add empty column(s) to CSV file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            default=['image_url','linkedin_profile_url']
            for dif in default:
                csv_file_fields.append(dif)
            result_file=csv_file.replace('.csv','')+'_FIELDS_ADDED.csv'
            DELETE_LOG_CONTENT(result_file)
            while 1:
                option=CHOOSE_OPTION_FROM_LIST_1(['Add field','Exit'],'Choose your option: ')
                if option=='Exit':
                    break
                field=raw_input('Please enter field name: ')
                csv_file_fields.append(field)
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,csv_file_fields)
            for lis in csv_file_data[1:]:
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,lis)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	


        if mode=='Get statistics of specific column in CSV file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose fields to calculate statistics: ')
            field_index=csv_file_fields.index(option)
            lis=[item[field_index] for item in csv_file_data[1:]]
            stat_result=GET_LIST_STAT(lis)
            stat_result=[str(item) for item in stat_result]
            SPEC_PRINT(['Mode: '+mode,'Status: Done!']+stat_result)	


        if mode=='Count unique values in given column':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose field: ')
            field_index=csv_file_fields.index(option)
            #lis=[item[field_index] for item in csv_file_data[1:]]
            lis=[]
            for line in csv_file_data[1:]:
                if line[field_index]=='':
                    lis.append('BLANK')
                else:
                    lis.append(line[field_index])
            uniq_lis=set(lis)
            len_unique_lis=str(len(uniq_lis))
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Number of unique values:'+len_unique_lis]+['']+['*** Column Name: '+option+' ***']+list(uniq_lis))



        if mode=='Print common unique values of specific field in two *csv files':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose field: ')
            field_index=csv_file_fields.index(option)
            #lis=[item[field_index] for item in csv_file_data[1:]]
            lis=[]
            for line in csv_file_data[1:]:
                if line[field_index]=='':
                    lis.append('BLANK')
                else:
                    lis.append(line[field_index])
            uniq_lis1=set(lis)


            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose field: ')
            field_index=csv_file_fields.index(option)
            #lis=[item[field_index] for item in csv_file_data[1:]]
            lis=[]
            for line in csv_file_data[1:]:
                if line[field_index]=='':
                    lis.append('BLANK')
                else:
                    lis.append(line[field_index])
            uniq_lis2=set(lis)


            common_lines=[]
            for l in uniq_lis1:
                if l in uniq_lis2:
                    common_lines.append(l)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Number of common values:'+str(len(common_lines))]+['']+['*** Common fields: ***']+list(common_lines)) 



        if mode=='Generate Leads (By leads number)':
            number_of_leads=int(raw_input("Please enter the number of leads to generate:"))
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            columns=["First Name","Last Name","Company Name","Title","Website"]
            col_dict={}
            for col in columns:
                col_name=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose "'+col+'":')
                col_index=csv_file_fields.index(col_name)
                col_data=[item[col_index] for item in csv_file_data[1:]]
                col_dict[col]=col_data
            leads_counter=0
            result_file_name='GENERATED_LEADS_'+str(number_of_leads)+'.csv'
            result_file_columns=columns
            result_file_columns.append('Email')
            print result_file_columns
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,result_file_columns)
            generated_leads=[]
            while leads_counter<=number_of_leads:
                f_n=random.choice(col_dict["First Name"])
                l_n=random.choice(col_dict["Last Name"])
                c_n=random.choice(col_dict["Company Name"])
                c_w=col_dict["Website"][col_dict["Company Name"].index(c_n)]
                c_t=random.choice(col_dict["Title"])
                c_e=f_n+'_'+l_n+'@'+c_w.replace('www.','')
                #print c_n,c_e
                gen_lead=[f_n,l_n,c_n,c_t,c_w,c_e]
                if gen_lead not in generated_leads:
                    generated_leads.append(gen_lead)
                    leads_counter+=1
                    ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,gen_lead)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file_name])



        if mode=='Create duplicated Leads':
            number_of_leads=int(raw_input("Please enter the number of leads to generate:"))
            csv_file_fields=["First Name","Last Name","Company Name","Title","Website","Email"]
            f_n=raw_input('Enter first name: ')
            l_n=raw_input('Enter last name: ')
            c_n=raw_input('Enter company name: ')
            tit=raw_input('Enter title: ')
            url=raw_input('Enter website: ')
            email=raw_input('Enter email: ')
            result_file_name='GENERATED_DUPLICATED_LEADS_'+str(number_of_leads)+'.csv'


            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,csv_file_fields)
            for x in range(0,number_of_leads):
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,[f_n,l_n,c_n,tit,url,email])
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file_name])
                                    	        
                                    	        



        if mode=='Generate Leads (By file size)':
            output_file_size=int(raw_input("Please enter file size in Megabytes:"))
            output_file_size_in_m=output_file_size*1024*1024
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            columns=["First Name","Last Name","Company Name","Title","Website"]
            col_dict={}
            for col in columns:
                col_name=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose "'+col+'":')
                col_index=csv_file_fields.index(col_name)
                col_data=[item[col_index] for item in csv_file_data[1:]]
                col_dict[col]=col_data

            result_file_name='GENERATED_LEADS_'+str(output_file_size)+'M.csv'
            file_size=0
            result_file_columns=columns
            result_file_columns.append('Email')
            print result_file_columns
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,result_file_columns)
            generated_leads=[]
            while output_file_size_in_m>=file_size:
                f_n=random.choice(col_dict["First Name"])
                l_n=random.choice(col_dict["Last Name"])
                c_n=random.choice(col_dict["Company Name"])
                c_w=col_dict["Website"][col_dict["Company Name"].index(c_n)]
                c_t=random.choice(col_dict["Title"])
                c_e=f_n+'_'+l_n+'@'+c_w.replace('www.','')
                #print c_n,c_e
                #gen_lead=[f_n,l_n,c_n,c_t,c_w,c_e]
                #if gen_lead not in generated_leads:
                #    generated_leads.append(gen_lead)
                #    leads_counter+=1
                #    ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,gen_lead)


                gen_lead=[f_n,l_n,c_n,c_t,c_w,c_e]
                generated_leads.append(gen_lead)
                file_size=os.path.getsize(result_file_name)

                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,gen_lead)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file_name])	








        if mode=='Perform statistics for *.csv file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            raw_sheet_data=[]
            for item in csv_file_data:
                raw_sheet_data.append(item)
            sheet_dict={}
            sheet_dict['0___Raw_Data']=raw_sheet_data

            for field in csv_file_fields:
                if len(field)!=0:
                    field_data=[item[csv_file_fields.index(field)] for item in csv_file_data]
                    field_stat_result=GET_LIST_STAT(field_data)
                    print "\r\n### "+field+" ###"
                    #for line in field_stat_result:
                    #    print line
                    sheet_dict[field]=field_stat_result

            result_file=csv_file.replace('.csv','')+'_STATISTICS.xlsx'

            #sheet_dict = sheet_dict.fromkeys(string.ascii_lowercase, 0)


            CREATE_EXCEL_SHEETS(result_file,sheet_dict)    
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	





        if mode=='Export values from specific column, that contains space tab':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose your column: ')
            field_index=csv_file_fields.index(option)
            lis=[item[field_index] for item in csv_file_data[1:]]
            lis=[item for item in lis if ' ' in item]
            uniq=[]
            for item in lis:
                if item not in uniq:
                    uniq.append(item)
            result_file=csv_file.replace('.csv','')+'_SPACE_IN_VALUE.csv'
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,[option])
            for item in lis:
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,[item])
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	



        if mode=='Export lines by searching some string in given CSV file column':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            result_file=csv_file.replace('.csv','')+'_SEARCH_RESULT.csv'
            DELETE_LOG_CONTENT(result_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,csv_file_fields)
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose fields to search string in: ')
            field_index=csv_file_fields.index(option)
            #lis=[item[field_index] for item in csv_file_data[1:]]
            search_string=raw_input('Enter string to search:')
            to_display=[]
            for line in  csv_file_data[1:]:
                if search_string.lower() in line[field_index].lower():
                    to_display.append(line)
            for item in to_display:
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,item)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file,'Exported lines number: '+str(len(to_display))])	


        if mode=='GREP lines by string':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            result_file=csv_file.replace('.csv','')+'_GREP_RESULT.csv'
            DELETE_LOG_CONTENT(result_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,csv_file_fields)
            #=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose fields to search string in: ')
            #field_index=csv_file_fields.index(option)
            #lis=[item[field_index] for item in csv_file_data[1:]]
            option=None
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(['Enter string to search','Exit'],'Please choose your option')
                if option!='Exit':
                    counter=0
                    search_string=raw_input('Enter string to search:')
                    for line in csv_file_data[1:]:
                        if search_string.strip().lower() in str(line).lower():
                            counter+=1
                            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,line)
                    print 'Matched lines:'+str(counter)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	

        if mode=='Export specific column(s) from CSV file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=None
            fields_to_export=[]
            csv_file_fields.append('Exit')
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose fields to export and then "Done" option to continue: ')
                if option not in fields_to_export:
                    fields_to_export.append(option)
                else:
                    print '*** "'+option+'" is already in your list! ***'
            fields_to_export.remove('Exit')
            fields_to_export_indexes=[csv_file_fields.index(item) for item in fields_to_export]
            exported_file=csv_file.replace('.csv','')+'_EXPORTED_FIELDS.csv'
            DELETE_LOG_CONTENT(exported_file)
            for lis in csv_file_data:
                lis=[lis[i] for i in fields_to_export_indexes]
                ADD_LIST_AS_LINE_TO_CSV_FILE(exported_file,lis)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+exported_file])		

        if mode=='Export common lines of 2 CSV files by given column(s)':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file1=CHOOSE_OPTION_FROM_LIST_1(csv_files, "Please choose filter file:")
            csv_file2=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose second file:')
            csv_file1_data=READ_CSV_AS_NESTED_LIST(csv_file1)
            csv_file2_data=READ_CSV_AS_NESTED_LIST(csv_file2)
            remove_dup_from_file1=REMOVE_DUP_FROM_NESTED_LIST(csv_file1_data)
            csv_file1_data=remove_dup_from_file1[0]
            print 'Total removed duplicated lines form: "'+csv_file1+'" is: '+str(remove_dup_from_file1[1])
            remove_dup_from_file2=REMOVE_DUP_FROM_NESTED_LIST(csv_file2_data)
            csv_file2_data=remove_dup_from_file2[0]
            print 'Total removed duplicated lines form: "'+csv_file2+'" is: '+str(remove_dup_from_file2[1])
            csv_file1_headers=csv_file1_data[0]
            csv_file1_headers_orig=csv_file1_headers
            csv_file1_headers=[item.lower() for item in csv_file1_headers]
            csv_file2_headers=csv_file2_data[0]
            csv_file2_headers_orig=csv_file2_headers
            csv_file2_headers=[item.lower() for item in csv_file2_headers]

            common_headers=[]
            for item in csv_file1_headers:
                if item in csv_file2_headers:
                    common_headers.append(item)

            res_file=csv_file2.replace('.csv','')+'_IN_'+csv_file1.replace('.csv','')+'.csv'
            res_file_not_found=csv_file2.replace('.csv','')+'_NOT_FOUND_'+csv_file1.replace('.csv','')+'.csv'
            DELETE_LOG_CONTENT(res_file)
            DELETE_LOG_CONTENT(res_file_not_found)
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,csv_file2_headers_orig)
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file_not_found,csv_file2_headers_orig)
            option=None
            common_headers.append('Exit')
            fields=[]
            while(option!='Exit'):
                option=CHOOSE_OPTION_FROM_LIST_1(common_headers, 'Please select fields to base on for exporting: ')
                if option!='Exit':
                    fields.append(option)
            fields_indexes_file_1=[csv_file1_headers.index(item) for item in fields]
            fields_indexes_file_2=[csv_file2_headers.index(item) for item in fields]
            print fields_indexes_file_1
            print fields_indexes_file_2
            for lis1 in csv_file1_data[1:]:
                flag=False
                for lis2 in csv_file2_data:
                    sub_lis1=[lis1[x].lower() for x in fields_indexes_file_1]
                    sub_lis2=[lis2[x].lower() for x in fields_indexes_file_2]
                    if sub_lis1==sub_lis2:
                        #ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,lis2)
                        flag=True
                        break
                if flag==True:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,lis2)
                if flag==False:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,[' ' for x in range(0,len(csv_file2_headers))])
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file_not_found,lis2)
                    #continue	
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+res_file,'Result file Not Found: '+res_file_not_found])




        if mode=='Delete file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv') or item.endswith('.txt') or item.endswith('.xlsx')]
            csv_files.append('Exit')
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose first to delete:')
            if csv_file=='Exit':
                pass
            else:
                os.remove(csv_file)
                SPEC_PRINT(['Mode: '+mode,'Status: Done!','Deleted file: '+csv_file])


        if mode=='Create CSV file with given lines number using template file':
            temp_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            template_file=CHOOSE_OPTION_FROM_LIST_1(temp_files,'Please choose your Template file: ')
            headers=READ_CSV_AS_NESTED_LIST(template_file)[0]
            lines=GET_INTEGER_OR_ENTER('Please enter number of lines to create:')
            start_number=GET_INTEGER_OR_ENTER('Please the initial number to use:')
            new_file='Result_'+str(start_number)+'_'+str(start_number+lines)+'__'+str(lines)+'.csv'
            DELETE_LOG_CONTENT(new_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(new_file,headers)
            temp_line=READ_CSV_AS_NESTED_LIST(template_file)[1]
            for x in range(int(start_number),int(start_number+lines)):
                new_line=[]
                for item in temp_line:
                    item=item.replace('|*|',str(x))
                    new_line.append(item)
                #print new_line
                ADD_LIST_AS_LINE_TO_CSV_FILE(new_file,new_line)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+new_file])	


        if mode=='Create EXCEL from several CSV files':
            print '*** You have to remove all failed leads!!! ***'
            option=None
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_files.append('Exit')
            files_to_merge=[]
            result_file=''
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose file:')
                if option!='Exit':
                    #csv_files.remove(option)
                    files_to_merge.append(option)
                    result_file+=option.replace('.csv','_')
            result_file+='.xlsx'
            sheet_dict={}
            for fil in files_to_merge:
                fil_data=READ_CSV_AS_NESTED_LIST(fil)
                sheet_dict.update({fil:fil_data})


            done=CREATE_EXCEL_SHEETS(result_file,sheet_dict)
            if done==True:
                SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file])	




        if mode=='Create CSV file from SQL query output':
            print mode
            done_flag=None
            sqls=open('SQLs.sql','r').readlines()
            sqls=[sql.strip() for sql in sqls if sql.startswith('#')==False]
            sql=CHOOSE_OPTION_FROM_LIST_1(sqls, 'Please choose SQL query to run: ')

            #parse_sql=SQL_QUERY_GET_KEYS(sql)
            #if len(parse_sql)>0:
            #    csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            #    csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your *csv file that contains: '+str(parse_sql)+' fields:')
            #    csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            #    csv_file_headers=csv_file_data[0]
            #    csv_file_headers=[item.lower() for item in csv_file_headers]
            #    res_file=csv_file.replace('.csv','')+'_SQL.csv'
            #    for item in parse_sql:
            #        if item not in csv_file_headers:
            #            print '"'+item+'" is not is your *csv file: "'+csv_file+'"'
            #    sqls=[]
            #    dic={}
            #    for line in csv_file_data[1:]:
            #        for item in parse_sql:
            #            dic.update({item:line[csv_file_headers.index(item)].replace("'",",,")})#Replace is to bypass special characters like O'Neil in sql shoild be O''Neil
            #        sql_to_add=SQL_QUERY_SET_VALUES_BY_KEYS(sql, dic)
            #        sqls.append(sql_to_add)
            #    done_flag=RUN_SQL(db_name,db_user,db_host,db_pass,sqls,res_file,False)
            if len(sql)!=0:
                print '--> '+sql.strip()
                res_file='Output_SQL.csv'
                done_flag=RUN_SQL(db_name,db_user,db_host,db_pass,sql.strip(),res_file,db_port,True)



            if done_flag==True:
                SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+res_file])



        if mode=='Merge CSV files':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_files.append('Exit')
            option=None
            files_to_merge=[]
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(csv_files, 'Choose file for merging: ')
                if option!='Exit':
                    files_to_merge.append(option)
            all_files_headers=[]
            res_file=''
            for fil in files_to_merge:
                file_headers=READ_CSV_AS_NESTED_LIST(fil)[0]
                file_headers=[item.lower() for item in file_headers]
                all_files_headers+=file_headers
                res_file+=fil.replace('.csv','')+'_'
            all_files_headers=[item.lower() for item in all_files_headers]
            uniq_files_headers=list(set(all_files_headers))
            res_file+='MERGED.csv'
            DELETE_LOG_CONTENT(res_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,['File_Name']+uniq_files_headers)
            for fil in files_to_merge:
                file_headers=READ_CSV_AS_NESTED_LIST(fil)[0]
                file_headers=[item.lower() for item in file_headers]
                for line in READ_CSV_AS_NESTED_LIST(fil)[1:]:
                    line_to_write=[fil]
                    for header in uniq_files_headers:
                        if header in file_headers:
                            line_to_write.append(line[file_headers.index(header)])
                        else:
                            line_to_write.append('')
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,line_to_write)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+res_file])




        if mode=='Show CSV file column names':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose CSV file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_headers=csv_file_data[0]
            fields_number=len(csv_file_headers)
            csv_file_headers.sort()
            print csv_file_headers
            SPEC_PRINT(['CSV File name: '+csv_file,'Lines number: '+str(len(csv_file_data)),' Total fields:'+str(fields_number),'-'*50]+csv_file_headers)


        if mode=='Split Marketo OE enriched Data':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose CSV file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_headers=csv_file_data[0]
            enriched_data_index=csv_file_headers.index('Enriched_Data_Fields')
            enriched_data_fields=[]
            for line in csv_file_data[1:]:
                if len(line[enriched_data_index])>0:
                    enriched_data_in_line=eval(line[enriched_data_index])[2:]
                    #print enriched_data_in_line
                else:
                    enriched_data_in_line=[]
                    #print enriched_data_in_line

                for item in enriched_data_in_line:
                    if item[0] not in enriched_data_fields:
                        enriched_data_fields.append(item[0])
            result_file_name=csv_file.split('.csv')[0]+'_ENRICHED_VALUES_ADDED.csv'
            result_file_headers=csv_file_headers+enriched_data_fields
            DELETE_LOG_CONTENT(result_file_name)
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,result_file_headers)

            for line in csv_file_data[1:]:
                result_line=line
                for f in enriched_data_fields:
                    result_line.append('')

                if len(line[enriched_data_index])>0:
                    enriched_data_in_line=eval(line[enriched_data_index])[2:]
                else:
                    enriched_data_in_line=[]

                for field in result_file_headers:
                    for item in enriched_data_in_line:
                        if field==item[0]:
                            result_line[result_file_headers.index(field)]=item[1]
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file_name,result_line)



            fields_number=len(csv_file_headers)
            csv_file_headers.sort()
            SPEC_PRINT(['Total fields:'+str(fields_number)]+csv_file_headers)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+result_file_name])


        if mode=='Show common columns of several CSV files':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_files.append('Exit')
            option=None
            files_to_merge=[]
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(csv_files, 'Choose file: ')
                if option!='Exit':
                    files_to_merge.append(option)
            all_files_headers=[]
            for fil in files_to_merge:
                file_headers=READ_CSV_AS_NESTED_LIST(fil)[0]
                file_headers=[item.lower() for item in file_headers]
                all_files_headers+=file_headers
            all_files_headers=[item.lower() for item in all_files_headers]
            common_fields=[item for item in all_files_headers if all_files_headers.count(item)>1]
            common_fields=list(set(common_fields))
            common_fields.sort()
            SPEC_PRINT(common_fields)



        if mode=='Generate ContactEmail basing on ContactFirstName, ContactLastName, CompanyWebsite':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=option=CHOOSE_OPTION_FROM_LIST_1(csv_files, 'Choose file: ')
            file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            file_headers=file_data[0]
            contact_first_name=CHOOSE_OPTION_FROM_LIST_1(file_headers,'Select ContactFirstName column:')
            contact_first_name_index=file_headers.index(contact_first_name)
            contact_last_name=CHOOSE_OPTION_FROM_LIST_1(file_headers,'Select ContactLastName column:')
            contact_last_name_index=file_headers.index(contact_last_name)
            company_website=CHOOSE_OPTION_FROM_LIST_1(file_headers,'Select CompanyWebsite column:')
            company_website_index=file_headers.index(company_website)
            res_file=csv_file.replace('.csv','')+'_ContactEmail_ADDED.csv'
            DELETE_LOG_CONTENT(res_file)
            file_headers.append('ContactEmailAddress')
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,file_headers)
            for item in file_data[1:]:
                new_item=item
                contact_email=STRIP_NON_ASCII(item[contact_first_name_index])+'_'+STRIP_NON_ASCII(item[contact_last_name_index])+'@'+item[company_website_index].replace('www.','').strip()
                new_item.append(contact_email)
                ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,new_item)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+res_file])	
            #	file_headers=[item.lower() for item in file_headers]
            #	all_files_headers+=file_headers
            #all_files_headers=[item.lower() for item in all_files_headers]
            #common_fields=[item for item in all_files_headers if all_files_headers.count(item)>1]
            #common_fields=list(set(common_fields))
            #common_fields.sort()
            #SPEC_PRINT(common_fields)

        if mode=='Fix CSV (Remove line if its length is bigger than header line length)':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=option=CHOOSE_OPTION_FROM_LIST_1(csv_files, 'Choose file: ')
            file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            file_headers=file_data[0]
            res_file=csv_file.replace('.csv','')+'_FIXED.csv'
            DELETE_LOG_CONTENT(res_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,file_headers)
            header_len=len(file_headers)
            print header_len
            for line in file_data[1:]:
                if len(line)==header_len:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,line)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+res_file])


        if mode=='Remove empty lines from csv file':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=option=CHOOSE_OPTION_FROM_LIST_1(csv_files, 'Choose file: ')
            file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            file_headers=file_data[0]
            res_file=csv_file.replace('.csv','')+'_EMPTY_LINES_REMOVED.csv'
            DELETE_LOG_CONTENT(res_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,file_headers)
            for line in file_data[1:]:
                if len(list(set(line)))>1:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,line)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Result file: '+res_file])


        if mode=='Show duplicated lines':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            print 'Counter: '+str(csv_file_fields)
            PRINT_DUP_LINES(csv_file_data)





        if mode=='Split CSV file to range of lengths':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=option=CHOOSE_OPTION_FROM_LIST_1(csv_files, 'Choose file: ')
            file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            file_headers=file_data[0]
            file_data=file_data[1:]
            data_size=len(file_data)
            #SPEC_PRINT(['File contains:',str(data_size)])
            limit_reached=False
            total_size=0
            sizes=[]
            option=None
            while option!='Exit':
                option=CHOOSE_OPTION_FROM_LIST_1(['Enter number of lines to split:','Exit'],'Please choose your option:')
                if option=='Exit':
                    break
                else:
                    size=raw_input('Please enter amount of lines to split:')
                    total_size+=int(size)
                    if total_size<data_size:
                        sizes.append(int(size))
                    else:
                        option='Exit'
                        print "You have reached maximum lines number in total!"
            print sizes
            start=0
            stop=0
            for size in sizes:
                stop+=size
                result_file=csv_file.split('.')[0]+'_'+'SPLIT'+'_'+str(size)+'.'+csv_file.split('.')[1]
                DELETE_LOG_CONTENT(result_file)
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,file_headers)
                print start,stop
                for line in file_data[start:stop]:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,line)
                start=stop

        if mode=='Get missing values of 2 files by given column':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            #Big File
            file1=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose first CSV file (Filter file/Big file):')
            csv_file_data1=READ_CSV_AS_NESTED_LIST(file1)
            csv_file_fields1=csv_file_data1[0]
            option1=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields1, 'Please choose fields field in '+file1+': ')
            index1=csv_file_fields1.index(option1)
            #Small file
            file2=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose second CSV file (Small file):')
            csv_file_data2=READ_CSV_AS_NESTED_LIST(file2)
            csv_file_fields2=csv_file_data2[0]
            option2=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields2, 'Please choose relevant field in '+file2+': ')
            index2=csv_file_fields2.index(option2)

            filter_values=[item[index2].lower() for item in csv_file_data2]
            filter_values=filter_values[1:]

            result_file=file1.split('.')[0]+'_MISSING_VALUES.csv'
            DELETE_LOG_CONTENT(result_file)
            ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,csv_file_fields1)

            result_list=[]
            for item in csv_file_data1[1:]:
                #print item
                #print item[index1]
                if item[index1].lower() not in filter_values and item not in result_list:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,item)
                    result_list.append(item)
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Missing values are in:'+result_file])

        if mode=='Compare two *.csv files':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            file1=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose first CSV file:')
            file2=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose second CSV file:')
            conf_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose configuration CSV file:')
            result_file=file1.split('.')[0]+'_'+file2.split('.')[0]+'_COMPARISON_RESULT.xlsx'
            ## Remove result file ##
            try:
                os.remove(result_file)
            except:
                pass

            # Check if comparison is possible
            file1_data=READ_CSV_AS_NESTED_LIST(file1)
            len_fil1=len(file1_data)
            header_line_1=file1_data[0]
            header_line_1=[h.lower() for h in header_line_1]
            file2_data=READ_CSV_AS_NESTED_LIST(file2)
            len_fil2=len(file2_data)
            header_line_2=file2_data[0]
            header_line_2=[h.lower() for h in header_line_2]
            common_fields=[x for x in header_line_1 if x in header_line_2]
            SPEC_PRINT(['*** Header line: '+file1+'***']+header_line_1)
            SPEC_PRINT(['*** Header line: '+file2+'***']+header_line_2)
            SPEC_PRINT(['*** Common Fileds***']+common_fields)
            if len(common_fields)==0:
                print "Error - no common fields found!"
                EXIT('Type ENTER to Exit!')
            if len_fil1!=len_fil2:
                print "Error - length of two given files is different!"
                EXIT('Type ENTER to Exit!')
            ### Get configuration settings #
            conf_data=READ_CSV_AS_NESTED_LIST(conf_file)
            conf_data=conf_data[1:] #without header line
            conf_data=[item for item in conf_data if item[0].startswith('#')==False]
            print conf_data
            conf_uniq_fields=list(set([item[0] for item in conf_data]))

            ### Start comparison 
            sheet_dict={}
            errors=[]
            for	item in conf_data:
                try:
                    print '-'*80
                    indexes1=[]
                    indexes2=[]
                    sheet_name=item[0]
                    sheet_data=[]
                    fields=item[1].split(',')
                    fields=[f.lower() for f in fields ]
                    #print fields
                    sheet_header_line=['InputFileName']+fields+['Compare Result']
                    #print sheet_header_line
                    sheet_data.append(sheet_header_line)
                    print "Excel Sheet Name: ",sheet_name
                    print "Header Line: ",sheet_header_line
                    for f in fields:
                        indexes1.append(header_line_1.index(f))
                        indexes2.append(header_line_2.index(f))
                    print indexes1
                    print indexes2
                    for x in range(0,len_fil1):
                        sub_lis_1=GET_SUBLIST_BY_INDEXES(file1_data[x],indexes1)
                        sub_lis_2=GET_SUBLIST_BY_INDEXES(file2_data[x],indexes2)
                        #print '1- ',sub_lis_1
                        #print '2- ',sub_lis_2
                        compare_result=MY_LIS_COMPARE(sub_lis_1,sub_lis_2)
                        if compare_result[0]==False:
                            diffs=[fields[x] for x in compare_result[1]]
                            compare_result=diffs
                        else: 
                            compare_result=compare_result[1]
                        #print compare_result
                        sub_lis_1.insert(0,file1)
                        sub_lis_2.insert(0,file2)
                        sub_lis_1.append(compare_result)
                        sub_lis_2.append(compare_result)
                        sheet_data.append(sub_lis_1)
                        sheet_data.append(sub_lis_2)
                        #sheet_data.append(sub_lis_1.append(compare_result))
                    sheet_dict.update({sheet_name:sheet_data})
                    #print sheet_dict
                except Exception, e:
                    print str(e)
                    errors.append(str(e))


            CREATE_EXCEL_SHEETS(result_file,sheet_dict)	

            if len(errors)!=0:
                print "#"*80
                print 'Ahtung Ahtung!!!'
                print 'There were errors during the process:'
                for e in errors:
                    print e

        if mode=='Compare two *.csv files as floats':
            float_option=CHOOSE_OPTION_FROM_LIST_1(['Round by number of digits','Deviation percentage'],'Please choose your option for float values:')
            if float_option=='Round by number of digits':
                round_number=int(raw_input('Please enter round_nymber:'))
            if float_option=='Deviation percentage':
                deviation=int(raw_input('Please enter deviation percentage for float values:'))
            #round_number=1
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            file1=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose first CSV file:')
            file2=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose second CSV file:')
            conf_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Choose configuration CSV file:')
            result_file=file1.split('.')[0]+'_'+file2.split('.')[0]+'_COMPARISON_RESULT.xlsx'
            ## Remove result file ##
            try:
                os.remove(result_file)
            except:
                pass

            # Check if comparison is possible
            file1_data=READ_CSV_AS_NESTED_LIST(file1)
            len_fil1=len(file1_data)
            header_line_1=file1_data[0]
            header_line_1=[h.lower() for h in header_line_1]
            file2_data=READ_CSV_AS_NESTED_LIST(file2)
            len_fil2=len(file2_data)
            header_line_2=file2_data[0]
            header_line_2=[h.lower() for h in header_line_2]
            common_fields=[x for x in header_line_1 if x in header_line_2]
            SPEC_PRINT(['*** Header line: '+file1+'***']+header_line_1)
            SPEC_PRINT(['*** Header line: '+file2+'***']+header_line_2)
            SPEC_PRINT(['*** Common Fileds***']+common_fields)
            if len(common_fields)==0:
                print "Error - no common fields found!"
                EXIT('Type ENTER to Exit!')
            if len_fil1!=len_fil2:
                print "Error - length of two given files is different!"
                EXIT('Type ENTER to Exit!')
            ### Get configuration settings #
            conf_data=READ_CSV_AS_NESTED_LIST(conf_file)
            conf_data=conf_data[1:] #without header line
            conf_data=[item for item in conf_data if item[0].startswith('#')==False]
            print conf_data
            conf_uniq_fields=list(set([item[0] for item in conf_data]))

            ### Start comparison 
            sheet_dict={}
            errors=[]
            for	item in conf_data:
                try:
                    print '-'*80
                    indexes1=[]
                    indexes2=[]
                    sheet_name=item[0]
                    sheet_data=[]
                    fields=item[1].split(',')
                    fields=[f.lower() for f in fields ]
                    #print fields
                    sheet_header_line=['InputFileName']+fields+['Compare Result']
                    #print sheet_header_line
                    sheet_data.append(sheet_header_line)
                    print "Excel Sheet Name: ",sheet_name
                    print "Header Line: ",sheet_header_line
                    for f in fields:
                        indexes1.append(header_line_1.index(f))
                        indexes2.append(header_line_2.index(f))
                    print indexes1
                    print indexes2
                    for x in range(0,len_fil1):
                        sub_lis_1=GET_SUBLIST_BY_INDEXES(file1_data[x],indexes1)
                        sub_lis_2=GET_SUBLIST_BY_INDEXES(file2_data[x],indexes2)
                        #print '1- ',sub_lis_1
                        #print '2- ',sub_lis_2
                        if float_option=='Deviation percentage':
                            compare_result=MY_LIS_COMPARE_FLOAT_DEVIATION(sub_lis_1,sub_lis_2,deviation)
                        if float_option=='Round by number of digits':
                           compare_result=MY_LIS_COMPARE_FLOAT_ROUND(sub_lis_1,sub_lis_2,round_number) 
                        if compare_result[0]==False:
                            diffs=[fields[x] for x in compare_result[1]]
                            compare_result=diffs
                        else: 
                            compare_result=compare_result[1]
                        #print compare_result
                        sub_lis_1.insert(0,file1)
                        sub_lis_2.insert(0,file2)
                        sub_lis_1.append(compare_result)
                        sub_lis_2.append(compare_result)
                        sheet_data.append(sub_lis_1)
                        sheet_data.append(sub_lis_2)
                        #sheet_data.append(sub_lis_1.append(compare_result))
                    sheet_dict.update({sheet_name:sheet_data})
                    #print sheet_dict
                except Exception, e:
                    print str(e)
                    errors.append(str(e))


            CREATE_EXCEL_SHEETS(result_file,sheet_dict)	

            if len(errors)!=0:
                print "#"*80
                print 'Ahtung Ahtung!!!'
                print 'There were errors during the process:'
                for e in errors:
                    print e



        if mode=='Calculate average value of specific column':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            option=CHOOSE_OPTION_FROM_LIST_1(csv_file_fields, 'Please choose fields to calculate average value: ')
            field_index=csv_file_fields.index(option)
            try:
                lis=[float(item[field_index]) for item in csv_file_data[1:] if len(item[field_index])!=0]
                #lis=[float(item) for item in lis]
                total_sum=0
                for item in lis:
                    total_sum+=item
                average=total_sum/len(lis)
                SPEC_PRINT(['Mode: '+mode,'Status: Done!','Column:'+str(option),'Average value is: '+str(average)])

            except Exception,e:
                print str(e)
                SPEC_PRINT(['Mode: '+mode,'Status: Failed!',str(e)])


        if mode=='Print single row from file "Column_Name:Value"':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            csv_file_fields=csv_file_data[0]
            csv_file_fields=[item.lower() for item in csv_file_fields]

            sorted_csv_file_fields=sorted(csv_file_fields)

            raw_number=input('Please enter raw number: ')
            relevant_raw=csv_file_data[raw_number]
            #print relevant_raw

            data=[]
            for csv_field in sorted_csv_file_fields:
                sub=''
                field_index=csv_file_fields.index(csv_field)
                sub+=csv_field
                sub+= " - "
                sub+=relevant_raw[field_index]
                data.append(sub)
            SPEC_PRINT(data)

        if mode=='Convert *csv file from "comma separated" to "tab separated"':
            csv_files=[item for item in os.listdir('.') if item.endswith('.csv')]
            csv_file=CHOOSE_OPTION_FROM_LIST_1(csv_files,'Please choose your file:')
            csv_file_data=READ_CSV_AS_NESTED_LIST(csv_file)
            new_file=csv_file.replace('.csv','')+'_TABBED.txt'
            for lis in csv_file_data:
                ADD_LIST_AS_LINE_TO_CSV_FILE(new_file,lis,'\t')
            SPEC_PRINT(['Mode: '+mode,'Status: Done!','Converted file is:'+new_file])
            EXIT('Type ENTER to Exit!')

    #except Exception, e:
    #    SPEC_PRINT([mode,'ERROR: '+str(e)])



