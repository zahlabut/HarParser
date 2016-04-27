import json
from Mi_Functions import *
import urlparse





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
    with open(har_file) as data_file:
        data = json.load(data_file)
    entries=data['log']['entries']
    for item in entries:
        if item['response']['status']==200:
            #print item['response']['headers']
            for header in item['response']['headers']:
                if header['name']=='Content-Type' and 'image' in header['value'].lower():
                    data_to_return_list.append({'URL':item['request']['url'],
                                                'Content-Type':header['value'],
                                                'ImageSize':item['response']['content']['size'],
                                               'Response_Headers':item['response']['headers']})
    return data_to_return_list
        #if 'Content-Type' in item['response']['headers'].keys():
            #    print item['response']
        # print item['request']['url']
        # print '### Request ### '
        # for req in item['request']['headers']:
        #     print {req['name']:req['value']}
        # print '### Response ###'
        # print item['response']['status']
        # for resp in item['response']['headers']:
        #     print {resp['name']:resp['value']}

def CHECK_COMPRESS_RULE(har_file, cached_urls):
    data_to_return_list=[]
    with open(har_file) as data_file:
        data = json.load(data_file)
    entries=data['log']['entries']
    for entry in entries:
        #print '_'*150
        print entry['request']['url']
        print entry['response']['status']
        #print entry['response']['status']
        #print len(entries)
        data_to_return={}
        for req_header in entry['request']['headers']:
            if 'accept-encoding' in req_header['name'].lower() and\
                            'content-encoding' not in str(entry['response']['headers']).lower() and\
                            entry['response']['status']>0 and\
                            'https' not in entry['request']['url'] and\
                            entry['response']['bodySize']>0 and\
                            entry['request']['url'] not in cached_urls:
                data_to_return['URL']=entry['request']['url']
                data_to_return['Code']=entry['response']['status']
                data_to_return['Accept-Encoding']={req_header['name']:req_header['value']}
                data_to_return['Response_Headers']=entry['response']['headers']
                data_to_return['Response_Body_Size']=entry['response']['content']['size']
                for resp_header in entry['response']['headers']:
                    for resp_header in entry['response']['headers']:
                        if 'content-type' in resp_header['name'].lower():
                            data_to_return['Content-Type']={resp_header['name']:resp_header['value']}
        if data_to_return!={}:
            data_to_return_list.append(data_to_return)

    # for item in entries:
    #     data_to_return={'TYPE':"Encoding in response and no encoding in request"}
    #     for resp in item['response']['headers']:
    #         if 'content-encoding' in resp['name']:
    #             data_to_return['URL']=item['request']['url']
    #             if 'accept-encoding' not in item['request']['headers']:
    #                 data_to_return['REQUEST_HEADER']=item['request']['headers']
    #     if data_to_return!={'TYPE':"Encoding in response and no encoding in request"}:
    #         data_to_return_list.append(data_to_return)

    return data_to_return_list




def GET_ALL_COOKIES(har_file):
    all_requests_cookies=[]
    all_response_cookies=[]
    data_to_return_list=[]
    with open(har_file) as data_file:
        data = json.load(data_file)
    entries=data['log']['entries']
    for item in entries:
        host=None
        referer=None
        for h in item['request']['headers']:
            if 'host' in str(h).lower():
                host=h['value']
        for h in item['request']['headers']:
            if 'referer' in str(h).lower():
                referer=h['value']

        if len(item['request']['cookies'])>0:
            all_requests_cookies.append(
                {'URL':item['request']['url'],
                 'Cookie':item['request']['cookies'],
                 'Cookie_Length':len(str(item['request']['cookies'])),
                 'Type':'Request_Cookie',
                 'Host':host,
                 'Referer':referer})
        if len(item['response']['cookies'])>0:
             all_response_cookies.append(
                {'URL':item['request']['url'],
                 'Cookie':item['response']['cookies'],
                 'Cookie_Length':len(str(item['response']['cookies'])),
                 'Type':'Response_Cookie',
                 'Host':host,
                 'Referer':referer})
    return all_requests_cookies+all_response_cookies


def GET_ALL_DOMAINS(har_file):
    all_domains=[]
    with open(har_file) as data_file:
        data = json.load(data_file)
    entries=data['log']['entries']
    for item in entries:
        host=None
        referer=None
        for h in item['request']['headers']:
            if 'host' in str(h).lower():
                host=h['value']
        for h in item['request']['headers']:
            if 'referer' in str(h).lower():
                referer=h['value']

        all_domains.append(
            {'URL':item['request']['url'],
             'Host':host,
             'Referer':referer,
             'ParsedDomain':urlparse.urljoin(item['request']['url'], '/'),
             'Status':item['response']['status']})
    return all_domains


url = 'http://stackoverflow.com/questions/1234567/blah-blah-blah-blah'
urlparse.urljoin(url, '/')


# Test "fewer domains" export all domains and run statistics
har_file='fishki.har'
result=GET_ALL_DOMAINS(har_file)
WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result)
print 'Now run Colbotigo.py to analyze the results!'









#
# #Test - export all Request and Response cookies into csv file + filter out cookie that aren't in report
# har_file='fishki.har'
# result=GET_ALL_COOKIES(har_file)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result)
#
#
# print '\r\nMissing Cookies in report'
# missing=[]
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] not in data:
#         c+=1
#         print c,item
#         item['Status']='Missing'
#         missing.append(item)
# print '\r\nExisting Cookies in report'
# existing=[]
# c=0
# for item in result:
#     if item['URL'] in data:
#         c+=1
#         print c,item
#         item['Status']='Existing'
#         existing.append(item)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','')+'_missing_existing_Cookies.csv',missing+existing)








# ### Print encodeing in request but missing in response ###
# cached_urls=open('nana.har','r').readlines()
# cached_urls=[item.split(' ')[0] for item in cached_urls]
# result=CHECK_COMPRESS_RULE('nana.har', cached_urls)
# counter=0
# for item in result:
#     #print item.keys()
#     if 'RESPONSE_HEADER' not in item.keys():
#         counter+=1
#         print counter,item
#     #print item
# WRITE_DICTS_TO_CSV('nana.csv',result)



### Get all images from har ###
# har_file='Fishki.har'
# result=GET_ALL_RECEIVED_IMAGES(har_file)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result)


# #Test filter out all missing JPG images in report
# print '\r\nMissing JPG Images in report'
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] not in data and item['Content-Type']=='image/jpeg':
#         c+=1
#         print c,item
# print '\r\nExisting JPG Images in report'
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] in data and item['Content-Type']=='image/jpeg':
#         c+=1
#         print c,item
#
#
#
#
# #Test filter out all missing GIF images in report
# print '\r\nMissing GIF Images in report'
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] not in data and item['Content-Type']=='image/gif':
#         c+=1
#         print c,item
# print '\r\nExisting GIF Images in report'
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] in data and item['Content-Type']=='image/gif':
#         c+=1
#         print c,item
#
#
#
#
# #Test filter out all missing JPG images in report
# print '\r\nMissing PNG Images in report'
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] not in data and item['Content-Type']=='image/png':
#         c+=1
#         print c,item
# print '\r\nExisting PNG Images in report'
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     if item['URL'] in data and item['Content-Type']=='image/png':
#         c+=1
#         print c,item

# #Test if images that have no-transform in cache-control GET header exists in report
# har_file='cnn.har'
# result=GET_ALL_RECEIVED_IMAGES(har_file)
# WRITE_DICTS_TO_CSV(har_file.replace('.har','.csv'),result)
# data=open('report.txt','r').read()
# c=0
# for item in result:
#     #print item
#     if 'no-transform' in str(item):
#         c+=1
#         print c,item
#         for h in item['Response_Headers']:
#             print h
#
#         if item['URL'] in data:
#             print 'yep'
