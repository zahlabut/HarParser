import json
from MintigoFunctions import *




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

### Print encodeing in request but missing in response ###
cached_urls=open('nana.har','r').readlines()
cached_urls=[item.split(' ')[0] for item in cached_urls]
result=CHECK_COMPRESS_RULE('nana.har', cached_urls)
counter=0
for item in result:
    #print item.keys()
    if 'RESPONSE_HEADER' not in item.keys():
        counter+=1
        print counter,item
    #print item

WRITE_DICTS_TO_CSV('nana.csv',result)


#
# print ('\r\n')*10



# counter=0
# for item in result:
#     #print item.keys()
#     if 'RESPONSE_HEADER' not in item.keys():
#         counter+=1
#         print counter,item['URL']

