import time
import requests,subprocess,platform
#import dns.resolver
import socket
import platform
from selenium import webdriver
from Mi_Functions import *
#from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
#from selenium import webdriver
#from Params import *





def OPEN_WEB_SITE_SELENIUM(url,proxy=None,timeout=5*60,SAVE_SCREENSHOT=False,return_source=False, load_delay=0):
    try:
        print '... Starting Firefox browser: '+url
        if proxy!=None:
            PROXY = proxy
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                "httpProxy":PROXY,
                "ftpProxy":PROXY,
                "sslProxy":PROXY,
                "noProxy":None,
                "proxyType":"MANUAL",
                "class":"org.openqa.selenium.Proxy",
                "autodetect":False
            }

        if 'linux' in platform.system().lower():
            display = Display(visible=0, size=(800, 600))
            display.start()

        driver = webdriver.Firefox()
        driver.delete_all_cookies()
        driver.set_page_load_timeout(timeout)
        start_time=time.time()
        driver.get(url)
        time.sleep(load_delay)
        current_url=driver.current_url


        page_source=driver.page_source

        stop_time=time.time()
        if SAVE_SCREENSHOT==True:
            screenshoot_name=str(time.time()).split('.')[0]+'_'+url.split('//')[-1].replace('.','_').replace('/','_')+'.jpg'
            driver.get_screenshot_as_file(screenshoot_name)
        if SAVE_SCREENSHOT==False:
            screenshoot_name=None
        driver.close()
        if 'linux' in platform.system().lower():
            display.stop()
            os.system('sudo killall -9 firefox')
        if return_source==True:
            return {'Page_Load_Time[sec]':stop_time-start_time,'Final_URL':current_url,'ScreenshootName':screenshoot_name,'Page_Source':page_source}
        if return_source==False:
            return {'Page_Load_Time[sec]':stop_time-start_time,'Final_URL':current_url,'ScreenshootName':screenshoot_name}
    except Exception,e:
        print 'Exception: '+str(e)
        driver.close()
        #FIX_SELENIUM_LINUX()
        return{'Exception_in_OPEN_WEB_SITE_SELENIUM':str(e)}


#HTTP get to some domain and calculate its size basing on Content-Length response header
def HTTP_GET_SITE(site_url,loops_number,proxies=None,request_headers=None,delay=0):
    #user_agent={'User-agent':'''Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'''}
    try:
        start_total_time=time.time()
        times=[]
        sizes=[]
        for x in range(0,loops_number):
            test_site=site_url
            start_time=time.time()
            if proxies==None:
                r = requests.get(test_site,headers=request_headers,verify=False)
            else:
                r = requests.get(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False)
            if 'content-length' in str(r.headers).lower():
                content_length_found=True
                size=int(eval(str(r.headers).lower())['content-length'])
                sizes.append(size)
            else:
                content_length_found=False
                size=len(r.content)
                sizes.append(size)

            stop_time=time.time()
            dif=stop_time-start_time

            times.append(dif)
            if content_length_found==True:
                print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Download_Time:'+str(dif)+'[sec] Download_Size_(Based on: Content-Length):'+str(size/1024.0)+'[kb]'
            if content_length_found==False:
                print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Download_Time:'+str(dif)+'[sec] Download_Size_(Based on: Received data):'+str(size/1024.0)+'[kb]  '
            time.sleep(delay)
        stop_total_time=time.time()
        return {'Average_Download_Time_[msec]':sum(times)/len(times)*1000,'Total_Download_Size_[kb]':sum(sizes)/1024.0,'Traffic_Execution_Time_[sec]':stop_total_time-start_total_time,'Is_Content_Length_Size':str(content_length_found)}
    except Exception,e:
        return {'HTTP_GET_SITE_Exception':str(e)}

def DNS_QUERY(site,loop_number):
    try:
        myResolver = dns.resolver.Resolver()
        response=[]
        start_time=time.time()
        for x in range(0,loop_number):
            #time.sleep(2)
            try:
                myAnswers = myResolver.query(site, "A")
                response_to_print=''
                for rdata in myAnswers:
                    response.append(rdata)
                    response_to_print+=' '+str(rdata)
                print 'No:'+str(x+1)+' '+'DNS_Response:'+response_to_print
            except Exception, e:
                print str(e)
                response.append(None)
                print 'No:'+str(x+1)+' '+'DNS_Response:'+str(None)
        stop_time=time.time()
        return {'Failures':response.count('None'),'Sucess':loop_number-response.count('None'),'Average_Response_Time':(stop_time-start_time)/loop_number}
    except Exception, e:
        return {'Exception':str(e)}

def HTTP_GET_SOCKET(host,port,loop_number):
    try:
        send_data=''
        send_data+='GET / HTTP/1.1\r\n'
        send_data+='Host: www.'+host+'\r\n'
        send_data+='Connection: close\r\n'
        send_data+='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
        send_data+='Upgrade-Insecure-Requests: 1\r\n'
        send_data+='User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\r\n'
        #send_data+='Accept-Encoding: gzip, deflate, sdch\r\n'
        send_data+='Accept-Language: en-US,en;q=0.8\r\n'
        send_data+='\r\n'
        send_data+='\r\n'
        #print send_data

        total_size=0
        for x in range(0,loop_number):
            s = socket.socket()
            s.connect((host,port))
            s.send(send_data)
            #response=s.recv(10000)
            response=''
            while True:
                data = s.recv(1)
                #print data
                if not data: break
                response+=data

            #print response
            s.close()
            total_size+=len(send_data)+len(response)
            print 'No:'+str(x+1)+' Host:'+host+' Request_size:'+str(len(send_data)/1024.0)+'[kb] Response_size:'+str(len(response)/1024.0)+'[kb]'
        return {'Total_TCP_size_[kb]':total_size/1024.0}
    except Exception, e:
        return {'Exception':str(e)}

def SSH_QUERY_SOCKET(ip,port,msg,loop_number):
    total_sent_size=0
    for x in range(0,loop_number):
        time.sleep(1)
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip,port)
        total_sent_size+=len(msg)
        try:
            # Send data
            #print >>sys.stderr, 'sending "%s"' % msg
            sent = sock.sendto(msg, server_address)
            # Receive response
            #print >>sys.stderr, 'waiting to receive'
            data, server = sock.recvfrom(4096)
            #print >>sys.stderr, 'received "%s"' % data
        except Exception,e:
            print str(e)
            sock.close()
    return {"Total_Sent_Data[kb]":total_sent_size/1024.0}

#### PING based on CLI ###




def PING_HOST(host,loop_number):
    try:
        start_time=time.time()
        times=[]
        for x in range(0,loop_number):
            if 'windows' in platform.system().lower():
                ping = subprocess.Popen(["ping", "-n", "1",host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
            if 'linux' in platform.system().lower():
                ping = subprocess.Popen(["ping", "-c", "1",host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
            out, error = ping.communicate()
            out = out.strip()
            error = error.strip()
            print '-'*100
            print '\r\nNo:'+str(x+1)+' '+'PING_Response:\r\n'+str(out)#[0:20])+'...'+str(out[-20:-1])
            #print error
            Time=None
            if "timed out" in out.lower(): #Windows:
                times.append('timeout')
            if "100% packet loss" in out.lower(): #Linux
                times.append('timeout')
            else:
                for l in out.rsplit(','):
                    if 'Average' in l:#Windows
                        Time=l.split(' ')[-1].split('ms')[0]
                        print '-->',Time
                    if 'time=' in l.lower():
                        Time=l.split('=')[-1].split(' ms')[0]
                        print '-->',Time
            if Time!=None:
                times.append(float(Time))

        #Statistics
        total_time=0.0
        total_timeouts=0
        total_pass=0
        for item in times:
            if str(type(item))=="<type 'float'>":
                total_time+=item
                total_pass+=1
            else:
                total_timeouts+=1
        if list(set(times))!=['timeout']:
            average_time=total_time/total_pass
        else:
            average_time=None
        packets_lost=total_timeouts
        stop_time=time.time()
        return {'Average_Response_Time_[msec]':average_time,'Packet_Lost':packets_lost,'Execution_Time':stop_time-start_time}
    except Exception, e:
        return {'Exception':str(e)}

def HTTP_GET_SOCKET_TEST_RULES(host,port,accept_encoding,loop_number):
    try:
        send_data=''
        send_data+='GET / HTTP/1.1\r\n'
        send_data+='Host: www.'+host+'\r\n'
        send_data+='Connection: close\r\n'
        send_data+='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
        send_data+='Upgrade-Insecure-Requests: 1\r\n'
        send_data+='User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\r\n'
        send_data+='Accept-Encoding:'+accept_encoding+'\r\n'# gzip, deflate, sdch\r\n'
        send_data+='Accept-Language: en-US,en;q=0.8\r\n'
        send_data+='\r\n'
        send_data+='\r\n'
        #print send_data

        total_size=0
        for x in range(0,loop_number):
            s = socket.socket()
            s.connect((host,port))
            s.send(send_data)
            #response=s.recv(10000)
            response=''
            while True:
                data = s.recv(1)
                #print data
                if not data: break
                response+=data

            #print response
            s.close()
            total_size+=len(send_data)+len(response)
            print 'No:'+str(x+1)+' Host:'+host+' Request_size:'+str(len(send_data)/1024.0)+'[kb] Response_size:'+str(len(response)/1024.0)+'[kb]'
        return {'Total_TCP_size_[kb]':total_size/1024.0}
    except Exception, e:
        return {'Exception':str(e)}


#print HTTP_GET_SOCKET_TEST_RULES('nana.co.il',80,'zababun',100)

#print HTTP_GET_SITE('https://google.co.il',10,proxies=None,request_headers={'h1':'h1','h2':'h2'})

#print OPEN_WEB_SITE_SELENIUM('http://ynet.co.il',"149.215.113.110:70")
