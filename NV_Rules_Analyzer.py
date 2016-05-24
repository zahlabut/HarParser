import json
from Mi_Functions import *
import urlparse
from tld import get_tld
import sys
from urlparse import urlparse
from datetime import datetime
import subprocess


def IS_CDN(host):
    try:
        out=subprocess.check_output(["host", "-a",host])
        if 'CNAME' not in out:
            return None
        else:
            out=out.split('\n')
            for o in out:
                if 'CNAME' in o:
                    return o.strip()
    except Exception,e:
        return str(e)

def PRINT_FOLLOW_TCP_STREAM(har_file):
    with open(har_file) as data_file:
        data = json.load(data_file)
    entries=data['log']['entries']
    for item in entries:
        print '_'*150
        print item['request']['url']
        print '### Request ### '
        for req in item['request']['headers']:
            print {req['name']:req['value']}
        print '### Response ###'
        print item['response']['status']
        for resp in item['response']['headers']:
            print {resp['name']:resp['value']}

def GET_ALL_RECEIVED_IMAGES(har_file):
    data_to_return_list=[]
    data=open(har_file,'r').read().decode('utf-8','ignore')
    data = json.loads(data)
    entries=data['log']['entries']
    for item in entries:
        if item['response']['status']==200:
            #print item['response']['headers']
            for header in item['response']['headers']:
                if header['name']=='Content-Type' and 'image' in header['value'].lower():
                    data_to_return_list.append({'URL':item['request']['url'],
                                                'Content-Type':header['value'],
                                                'ImageSize':item['response']['content']['size'],
                                                'Response_Headers':item['response']['headers'],
                                                'Status':item['response']['status']})
    return data_to_return_list

def CHECK_COMPRESS_RULE(har_file):
    data_to_return_list=[]
    data=open(har_file,'r').read().decode('utf-8','ignore')
    data = json.loads(data)
    entries=data['log']['entries']
    for entry in entries:
        data_to_return={}
        accept_encoding_header_value=None
        for req_header in entry['request']['headers']:
            if 'accept-encoding'==req_header['name'].lower():
                accept_encoding_header_value=req_header['value']
        data_to_return['Accept-Encoding']=accept_encoding_header_value
        data_to_return['URL']=entry['request']['url']
        data_to_return['Code']=entry['response']['status']
        data_to_return['Response_Headers']=entry['response']['headers']
        data_to_return['Response_Body_Size']=entry['response']['content']['size']
        content_length_header_value=None
        content_type_header_value=None
        content_encoding_header_value=None
        for resp_header in entry['response']['headers']:
            if 'content-type'==resp_header['name'].lower():
                content_type_header_value=resp_header['value']
            if 'content-encoding'==resp_header['name'].lower():
                content_encoding_header_value=resp_header['value']
            if 'content-length'==resp_header['name'].lower():
                content_length_header_value=resp_header['value']
        data_to_return['Content-Length']=content_length_header_value
        data_to_return['Content-Type']=content_type_header_value
        data_to_return['Content-Encoding']=content_encoding_header_value
        data_to_return_list.append(data_to_return)
    return data_to_return_list

def GET_ALL_COOKIES(har_file):
    all_cookies=[]
    data=open(har_file,'r').read().decode('utf-8','ignore')
    data = json.loads(data)
    data_to_return_list=[]
    entries=data['log']['entries']
    for item in entries:
        host=None
        referer=None
        request_cookie=None
        response_cookie=None
        request_cookie_len=None
        response_cookie_len=None
        for h in item['request']['headers']:
            if 'host' in str(h).lower():
                host=h['value']
        for h in item['request']['headers']:
            if 'referer' in str(h).lower():
                referer=h['value']
        for h in item['request']['headers']:
            if 'cookie' in str(h).lower():
                request_cookie=h['value']
                request_cookie_len=len(request_cookie)

        response_cookie=[]
        response_cookie_len=[]
        for h in item['response']['headers']:
            if 'cookie' in str(h['name']).lower():
                response_cookie.append({h['name']:h['value'],'Length':len(h['value'])})
                response_cookie_len.append(len(h['value']))
        response_cookie_len=sum(response_cookie_len)

        all_cookies.append(
                        {'URL':item['request']['url'],
                         'Request_Cookie':request_cookie,
                         'Request_Cookie_Length':request_cookie_len,
                         'Response_Cookie':response_cookie,
                         'Response_Cookie_Length':response_cookie_len,
                         'Host':host,
                         'Referer':referer,
                         'ParsedDomain':get_tld(item['request']['url'])})
    return all_cookies

def GET_ALL_DOMAINS(har_file):
    all_domains=[]
    data=open(har_file,'r').read().decode('utf-8','ignore')
    data = json.loads(data)
    entries=data['log']['entries']
    for item in entries:
        for h in item['request']['headers']:
            host=None
            if 'host' in str(h).lower():
                host=h['value']
                break
        for h in item['request']['headers']:
            referer=None
            if 'referer' in str(h).lower():
                #print item['request']['headers']
                referer=h['value']
                break
        parsed_domain=None
        try:
            parsed_domain=get_tld(item['request']['url'])
        except Exception,e:
            parsed_domain=str(e)
        all_domains.append(
            {'URL':item['request']['url'],
             'Host':host,
             'Referer':referer,
             'ParsedDomain':parsed_domain,
             'Status':item['response']['status'],
             'Size':item['response']['content']['size']})
    return all_domains

def GET_ALL_RESPONSE_HEADERS(har_file):
    all_urls=[]
    data=open(har_file,'r').read().decode('utf-8','ignore')
    data = json.loads(data)
    entries=data['log']['entries']

    for entry in entries:
        cache_headers=['Cache-Control','Expires','Date','Pragma','Etag','Last-Modified','Age']
        cache_headers=[item.lower() for item in cache_headers]
        response_headers=''
        cache_headers_dic={}
        for nv in entry['response']['headers']:
            response_headers+=str(nv)+'\r\n'
            if nv['name'].lower() in cache_headers:
                cache_headers_dic.update({nv['name']:nv['value']})
        dic={'URL':entry['request']['url'],'Response_Headers':response_headers,'Status':entry['response']['status'],'Cache_Headers':cache_headers_dic}
        all_urls.append(dic)
    return all_urls



TOOL_DESCRIPTION=['NV_Rules_Analyser_Tool','V 1.0','Designed by: Arkady','Goodbye world']
SPEC_PRINT(TOOL_DESCRIPTION)
RULES=['Reduce the size of your images','Compress Components']
rule=CHOOSE_OPTION_FROM_LIST_1(RULES,'Choose Rule you would like to test:')


if rule=='Reduce the size of your images':
    usage='''### USAGE ###
    1)	Use Chrome
    2)	Close all tabs except NV
    3)	Open a new TAB with "Developers Tools" opened
    4)	Start Emulation on NV tab
    5)	Browse to some site on second TAB
    6)	Stop NV once site is loaded
    7)	On second TAB use "Copy all as HAR" on "Network" and save all the content into *.har file
    8)	Run NV analyzing and save PL file as *csv (Open *.pcap file with Wireshark go to : File - Export Packet Dissections - As CSV)
    9)	Save NV rule's as *.csv in report.txt file
    10)	Open created result file with Excel and analyze the result according rul'e defenition, result file contains the following columns:
    ['Status', 'ImageSize', 'Response_Headers', 'Is_in_3d_Party', 'URL', 'Content-Type', 'Is_In_PL', 'Parsed_URL_Path', 'Is_In_Rule']'''
    print usage
    CONTINUE('Are you ready to start analyzing process?')
    dir_files=[fil for fil in os.listdir('.') if fil.endswith('.py')==False and fil.startswith('.')==False]
    har_file=CHOOSE_OPTION_FROM_LIST_1([f for f in dir_files if f.endswith('.har')==True],'Choose *har file:')
    report_file=CHOOSE_OPTION_FROM_LIST_1([f for f in dir_files if f.endswith('.txt')==True],'Choose rule result file:')
    pl_file=CHOOSE_OPTION_FROM_LIST_1([f for f in dir_files if f.endswith('.csv')==True],'Choose PL file:')
    third_parties_file=CHOOSE_OPTION_FROM_LIST_1([f for f in dir_files if f.endswith('.txt')==True],'Choose 3rd parties file:')
    td_parties=open(third_parties_file,'r').read().lower()
    result=GET_ALL_RECEIVED_IMAGES(har_file)
    rules_result=open(report_file,'r').read()
    packet_list=open(pl_file,'r').read().lower()
    result_list=[]
    for r in result:
        in_rule=False
        if r['URL'].lower() in rules_result:
            in_rule=True
        r.update({'Is_In_Rule':in_rule})
        in_td_parties=False
        try:
            if get_tld(r['URL']).lower() in td_parties:
                in_td_parties=True
        except Exception, e:
            in_td_parties=str(e)
        r.update({'Is_in_3d_Party':in_td_parties})
        in_pl=False
        parsed = urlparse(r['URL'])
        url_path=parsed.path.lower()
        if url_path in packet_list:
            in_pl=True
        r.update({'Parsed_URL_Path':url_path})
        r.update({'Is_In_PL':in_pl})
        print r
        result_list.append(r)
    result_file=har_file.replace('.har','.csv')
    WRITE_DICTS_TO_CSV(result_file,result_list)
    SPEC_PRINT(['Your result file is ready!!!','File name: '+result_file])










# ### "Compress Components" rule ###
# # 1)	Use Chrome
# # 2)	Close all tabs except NV
# # 3)	Open a new TAB with "Developers Tools" opened
# # 4)	Start Emulation on NV tab
# # 5)	Browse to some site on second TAB
# # 6)	Stop NV once site is loaded
# # 7)	On second TAB use "Copy all as HAR" on "Network" and save all the content into *.har file
# # 8)	Run NV analyzing and save PL file as *csv (Open *.pcap file with Wireshark go to : File - Export Packet Dissections - As CSV)
# # 9)	Save NV rule's as *.csv in report.txt file
# # 10)	Open created result file with Excel and analyze the result according rule's defenition, result file contains the following columns:
# # ['Content-Length', 'Code', 'Accept-Encoding', 'Response_Headers', 'Content-Encoding', 'URL', 'Response_Body_Size', 'Is_In_PL', 'Is_in_3d_Party', 'Content-Type', 'Parsed_URL_Path', 'Is_In_Rule']
# # Note: see Issue 20340, you can see current implementation there
# har_file='ynet.har'
# pl_file='ynetCap.csv'
# report_file='report.txt'
# td_parties=open('3rdPartyList.txt','r').read().lower()
# rules_result=open(report_file,'r').read().lower()
# packet_list=open(pl_file,'r').read().lower()
# result_list=[]
# result=CHECK_COMPRESS_RULE(har_file)
# for d in result:
#     in_rule=False
#     if d['URL'].lower() in rules_result:
#         in_rule=True
#     d.update({'Is_In_Rule':in_rule})
#     in_td_parties=False
#     try:
#         if get_tld(d['URL']).lower() in td_parties:
#             in_td_parties=True
#     except Exception, e:
#         in_td_parties=str(e)
#     d.update({'Is_in_3d_Party':in_td_parties})
#     in_pl=False
#     parsed = urlparse(d['URL'])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     d.update({'Parsed_URL_Path':url_path})
#     d.update({'Is_In_PL':in_pl})
#     print d.keys()
#     result_list.append(d)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result_list)
#
#
#










# # ### "Fewer domains" rule ###
# # 1)	Use Chrome
# # 2)	Close all tabs except NV
# # 3)	Open a new TAB with "Developers Tools" opened
# # 4)	Start Emulation on NV tab
# # 5)	Browse to some site on second TAB
# # 6)	Stop NV once site is loaded
# # 7)	On second TAB use "Copy all as HAR" on "Network" and save all the content into *.har file
# # 8)	Run NV analyzing and save PL file as *csv (Open *.pcap file with Wireshark go to : File - Export Packet Dissections - As CSV)
# # 9)	Save NV rule's as *.csv in following format
# # 1,www.ok.ru
# # 1,static3.smi2.net
# # 2,static7.smi2.net
# # 3,clickiocdn.com
# # 10)	Open created result file with Excel and analyze the result according rul'e defenition, result file contains the following columns:
# # ['Status', 'ParsedDomain', 'URL', 'Is_In_PL', 'Is_3d_Party', 'Host', 'InReport', 'Referer', 'ReportedValue', 'CountedHost', 'ReportedHost', 'Parsed_URL_Path', 'Size']
# har_file='Fishki.har'
# third_parties_file='3rdPartyList.txt'
# report_file='report.txt'
# pl_file='ynetCap.csv'
# td_parties=open(third_parties_file,'r').read().lower()
# result=GET_ALL_DOMAINS(har_file)
# hosts=[i['Host'] for i in result]
# referers=[i['Referer'] for i in result]
# parsed_domains=[i['ParsedDomain'] for i in result]
# data=open(report_file,'r').read()
# data_lines=open(report_file,'r').readlines()
# data_lines=[d.split(',') for d in data_lines]
# domains=[item['ParsedDomain'] for item in result]
# stat=GET_LIST_STAT(domains)
# packet_list=open(pl_file,'r').read().lower()
# updated_result=[]
# for r in result:
#     #if r['Host']!=None:
#     reported_value=None
#     reported_host=None
#     in_report=False
#     for d in data_lines:
#         if r['Host'] == d[1].strip():
#             reported_value=d[0]
#             reported_host=d[1].strip()
#             in_report=True
#             break
#     in_pl=False
#     parsed = urlparse(r['URL'])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     r.update({'Parsed_URL_Path':url_path})
#     r.update({'Is_In_PL':in_pl})
#     r.update({'ReportedValue':reported_value})
#     r.update({'ReportedHost':reported_host})
#     r.update({'InReport':in_report})
#     r.update({'CountedHost':hosts.count(r['Host'])})
#     if str(r['Host']).lower() in td_parties:
#         r.update({'Is_3d_Party':True})
#     if str(r['Host']).lower() not in td_parties:
#         r.update({'Is_3d_Party':False})
#     updated_result.append(r)
#     print r.keys()
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),updated_result)












# # ### "Try to reduce the size of the cookies" rule ###
# # # Rule defenition by Shlomo
# # # In case when cookie is in request and not 3d party, violation is true
# # # In case when cookie is in Response and its size is bigger than 100 violation is true
# # 1)	Use Chrome
# # 2)	Close all tabs except NV
# # 3)	Open a new TAB with "Developers Tools" opened
# # 4)	Start Emulation on NV tab
# # 5)	Browse to some site on second TAB
# # 6)	Stop NV once site is loaded
# # 7)	On second TAB use "Copy all as HAR" on "Network" and save all the content into *.har file
# # 8)	Run NV analyzing and save PL file as *csv (Open *.pcap file with Wireshark go to : File - Export Packet Dissections - As CSV)
# # 9)	Save NV rule's as *.csv in report.txt file
# # 10)	Open created result file with Excel and analyze the result according rul'e defenition, result file contains the following columns:
# # ['Request_Cookie_Length', 'ParsedDomain', 'Is_In_Rule', 'Request_Cookie', 'Response_Cookie_Length', 'URL', 'Is_In_PL', 'Host', 'Referer', 'Is_in_3d_Party', 'Response_Cookie', 'Parsed_URL_Path']
# har_file='rambler.har'
# td_parties=open('3rdPartyList.txt','r').read().lower()
# rules_result=open('report.txt','r').read().lower()
# packet_list=open('RamblerCap.csv','r').read().lower()
# packet_list_lines=open('RamblerCap.csv','r').readlines()
# updated_result=[]
# result=GET_ALL_COOKIES(har_file)
# for r in result:
#     in_rule=False
#     if str(r['URL']).lower() in rules_result:
#         in_rule=True
#     r.update({'Is_In_Rule':in_rule})
#     in_td_parties=False
#     if str(r['ParsedDomain'].split('.')[0]).lower() in td_parties:
#         in_td_parties=True
#     r.update({'Is_in_3d_Party':in_td_parties})
#     in_pl=False
#     parsed = urlparse(r['URL'])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     r.update({'Parsed_URL_Path':url_path})
#     r.update({'Is_In_PL':in_pl})
#     print r.keys()
#     updated_result.append(r)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),updated_result)















# ### Test "Minimize number of third-party resources"
# #1)Copy rule's reult into report as isYou need to copy the urls into report.txt and to number it, like that:
# #2) Take PL and export all to csv
# # 1,static3.smi2.net
# # 2,static7.smi2.net
#
# har_file='fishki.har'
# td_parties=open('3rdPartyList.txt','r').read().lower()
# rules_result=open('report.txt','r').read().lower()
# result=GET_ALL_DOMAINS(har_file)
# packet_list=open('FishkCap.csv','r').read().lower()
# packet_list_lines=open('FishkCap.csv','r').readlines()
# updated_result=[]
#
#
# for r in result:
#     in_rule=False
#     if str(r['URL']).lower() in rules_result:
#         in_rule=True
#     r.update({'Is_In_Rule':in_rule})
#
#
#     in_td_parties=False
#     if str(r['ParsedDomain'].split('.')[0]).lower() in td_parties:
#         in_td_parties=True
#     r.update({'Is_in_3d_Party':in_td_parties})
#
#
#     in_pl=False
#     parsed = urlparse(r['URL'])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     r.update({'Parsed_URL_Path':url_path})
#     r.update({'Is_In_PL':in_pl})
#
#     print r.keys()
#     print r['Is_in_3d_Party']
#     updated_result.append(r)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),updated_result)



#
# ### Test cache rule ###
# # Test steps
# #1) Usee Firefox only
# #2) Clean Firefox Cache
# #3) Browse to some site while emulation
# #4) Save HAR content to *.har file
# #5) Save Firefox about:cache content to cache_from_firefox.txt
# #6) Save cache rule result into report.txt
# #7) Save PL as CSV into *CAP.csv
#
# # Read cache from CAHCE file as dictionaries into list
# firefox_cache_file='FishkiFirefoxCache.txt'
# firefox_cache=open(firefox_cache_file,'r').readlines()
# firefox_cache=[line.strip() for line in firefox_cache if line.count('\t')>3]
# headers=firefox_cache[0].split('\t')
# dict_list=[]
# for line in firefox_cache[1:]:
#     dic={}
#     line=line.split('\t')
#     for item in line:
#         dic[headers[line.index(item)]]=item
#     dict_list.append(dic)
# # Update all dicts with expiration in days from now
# now=time.strftime("%Y-%m-%d %H:%M:%S")
# now=datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
# updated_dict_list=[]
# for d in dict_list:
#     if 'No expiration time' not in d['Expires ']:
#         line_date=datetime.strptime(d['Expires '],"%Y-%m-%d %H:%M:%S")
#         d['ExpiresInDays']=str(line_date-now)
#     else:
#         d['ExpiresInDays']=None
#     updated_dict_list.append(d)
# # Pass over all cached files in loop nd add all relevan data from PL, Report and HAR file
# har_file='Fishki.har'
# pl_file='FishkiCap.csv'
# firefox_cache_file='FishkiFirefoxCache.txt'
# report_file='report.txt'
# td_parties=open('3rdPartyList.txt','r').read().lower()
# rules_result=open(report_file,'r').read().lower()
# packet_list=open(pl_file,'r').read().lower()
# result_list=[]
# har_file_result=GET_ALL_RESPONSE_HEADERS(har_file)
#
#
# for d in updated_dict_list:
#     print d['Key ']
#     in_rule=False
#     if d['Key '].lower() in rules_result:
#         in_rule=True
#     d.update({'Is_In_Rule':in_rule})
#
#     in_td_parties=False
#     try:
#         if get_tld(d['Key ']).lower() in td_parties:
#             in_td_parties=True
#     except:
#         pass
#     d.update({'Is_in_3d_Party':in_td_parties})
#
#     in_pl=False
#     parsed = urlparse(d['Key '])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     d.update({'Parsed_URL_Path':url_path})
#     d.update({'Is_In_PL':in_pl})
#
#     for item in har_file_result:
#         #print '*'*100
#         #print d['Key ']
#         #print item['URL']
#         cache_headers_string= ''
#         if d['Key '].lower().strip()==item['URL'].lower().strip():
#             print d['Key ']
#             print item['URL']
#             d.update({'ResponseHeaders':item['Response_Headers']})
#             d.update({'Status_Code':item['Status']})
#             for k in item['Cache_Headers'].keys():
#                 cache_headers_string+= k + ':' + item['Cache_Headers'][k] + '\r\n'
#             d.update({'Cache_Headers_Values':cache_headers_string})
#             d.update({'Cache_Headers_Keys':item['Cache_Headers'].keys()})
#             print d.keys()
#     result_list.append(d)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result_list)





# ### Test CDN rule ###
# # Test steps
# # Run on LINUX as script is using "host" tool
# #1) Browse to some site while emulation
# #2) Save HAR content to *.har file
# #3) Save PL as CSV into *CAP.csv
# #4) Use http://www.cdnplanet.com/tools/cdnfinder/ and type your tested site in "Full site lookup"
# #5) Save result table from previous step in cdnplanet.csv (File. verify that you can open it with Excel)
#
# har_file='Fishki.har'
# pl_file='FishkiCap.csv'
# report_file='report.txt'
# cdn_planet_file='cdnplanet.csv'
# cdn_planet_content=open(cdn_planet_file,'r').read().lower()
# cdn_planet_content_lines=open(cdn_planet_file,'r').readlines()
# td_parties=open('3rdPartyList.txt','r').read().lower()
# known_cdn_file='KnownCdnResources.java'
# known_cdns=open(known_cdn_file,'r').read().lower()
# rules_result=open(report_file,'r').read().lower()
# packet_list=open(pl_file,'r').read().lower()
# result_list=[]
# har_file_result=GET_ALL_DOMAINS(har_file)
#
#
# for d in har_file_result:
#
#     in_cdnplanet=None
#     if d['Host'].lower() in cdn_planet_content:
#         for line in cdn_planet_content_lines:
#             if d['Host'].lower() in str(line).lower():
#                 in_cdnplanet=line.split('\t')[-1].strip()
#                 break
#     d.update({'Host_In_CdnPlanet':in_cdnplanet})
#
#     d.update({'LinuxHostOutput':IS_CDN(d['Host'])})
#
#     in_cdns=False
#     if d['Host'].lower() in known_cdns:
#         in_cdns=True
#     d.update({'Host_In_Known_CDNs':in_cdns})
#
#
#     in_rule=False
#     if d['URL'].lower() in rules_result:
#         in_rule=True
#     d.update({'Is_In_Rule':in_rule})
#
#     in_td_parties=False
#     try:
#         if get_tld(d['URL']).lower() in td_parties:
#             in_td_parties=True
#     except Exception, e:
#         in_td_parties=str(e)
#     d.update({'Is_in_3d_Party':in_td_parties})
#
#     in_pl=False
#     parsed = urlparse(d['URL'])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     d.update({'Parsed_URL_Path':url_path})
#     d.update({'Is_In_PL':in_pl})
#
#     print d
#     result_list.append(d)
#
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result_list)



### Test "Minimize number of third-party resources" rule
# Test steps
#1) Browse to some site while emulation
#2) Save HAR content to *.har file
#3) Save PL as CSV into *CAP.csv


# har_file='ynet.har'
# pl_file='ynetCap.csv'
# report_file='report.txt'
# td_parties=open('3rdPartyList.txt','r').read().lower()
# rules_result=[line for line in open(report_file,'r').readlines() if 'http' in line]
# print 'Objects in report: ',len(rules_result)
# print 'Iniqueue objects: ',len(set(rules_result))
# rules_result=str(set(rules_result)).lower()
# packet_list=open(pl_file,'r').read().lower()
# result_list=[]
# har_file_result=GET_ALL_DOMAINS(har_file)
#
#
# for d in har_file_result:
#
#     in_rule=False
#     if d['URL'].lower() in rules_result:
#         in_rule=True
#     d.update({'Is_In_Rule':in_rule})
#
#     in_td_parties=False
#     try:
#         if get_tld(d['URL']).lower() in td_parties:
#             in_td_parties=True
#     except Exception, e:
#         in_td_parties=str(e)
#     d.update({'Is_in_3d_Party':in_td_parties})
#
#     in_pl=False
#     parsed = urlparse(d['URL'])
#     url_path=parsed.path.lower()
#     if url_path in packet_list:
#         in_pl=True
#     d.update({'Parsed_URL_Path':url_path})
#     d.update({'Is_In_PL':in_pl})
#     print d.keys()
#     result_list.append(d)
#
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result_list)













