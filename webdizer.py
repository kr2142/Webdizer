from BeautifulSoup import BeautifulSoup
import os
import re
import urllib2
from hashlib import md5
from datetime import datetime
import collections

def get_site(url):
    result = re.search(r'//[\w+\.]*\.\w{2,6}', url)
    if result:
        return result.group()[2:]
        
def grab_page(url, user_agent, flag, timestamp, save_to):
    headers = { 'User-Agent' : user_agent }
    if 'http' not in url:
        if '//' in url:
            url = 'http:%s' % (url)
        else:
            url = 'http://%s' % (url)

    try:
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        page = response.read()
        directory = '%s%s%s%s' % (save_to,str(timestamp), '_', get_site(url))

        if not os.path.exists(directory):
            os.makedirs(directory)

        urls = []
        soup = BeautifulSoup(page)
        links = soup.findAll('a', href=True)
        for tag in links:
            link = tag.get('href',None)
            if link != None:
                urls.append(link)
                
        if flag:
            grabbed_urls = open ('%s%s' % (directory, '\\grabbed_urls.txt'), 'a+')
            grabbed_urls.write('%s%s' % (url, '\n'))
            grabbed_urls.close()
            size = os.path.getsize('%s%s' % (directory, '\\grabbed_urls.txt'))

        else:
            m = md5()
            m.update(url)
            file_name = '%s%s%s%s' % (directory, '\\', str(m.hexdigest()), '.html')
            grabbed_urls = open ('%s%s' % (directory, '\\url+md5.txt'), 'a+')
            grabbed_urls.write('%s%s%s%s' % (file_name, '    |    ', url, '\n'))
            grabbed_urls.close()                
            result = open(file_name, 'wb')
            result.write(page)
            result.close()
            size = os.path.getsize(file_name)
        return urls, size

    except:
        pass

    
#Main part
if __name__ == "__main__":
    start_time = datetime.now()
    timestamp = start_time.strftime("%d.%m.%Y-%H.%M.%S")
    settings = open('settings.ini', 'r')
    for line in settings:
        if 'user_agent::' in line:
            user_agent = line[12:-1]        
        if 'url_list::' in line:
            path2list = line[10:-1]
        if 'depth::' in line:
            depth = int(line[7:])
        if 'save_method::' in line:
            if line[13:-1] == 'url':
                save_method = True
            else:
                save_method = False
        if 'save_to::' in line:
            save_to = line[9:]
            
    settings.close()
    if save_to[-1] !='\\':
        save_to += '\\'            
    url_list = open (path2list, 'r')
    solution = [line.rstrip('\n') for line in url_list]
    url_list.close()
    short = len(solution[0])
    short_link = solution[0]
    longest = 0
    total_data = 0
    walked_length = 0
    links_number = len(solution)
    big_chunk = []
    for site in solution:
        walked = []
        walked.append(site)
        buff = []
        if 'http' not in site:
            site = 'http://%s' % (site)
        try:
            url_list, data_amount = grab_page(site, user_agent, save_method, timestamp, save_to)
            total_data += data_amount
            start_url = get_site(site)
            links_number += len(url_list)
            print site
        except:
            print "--==##Bad url: ", site
            continue
        if len(site)>longest:
            longest = len(site)
            longest_link = site
        if len(site)<short:
            short = len(site)
            short_link = site

        for i in range (0,depth):
            for url_name in url_list:
                
                if start_url != get_site(url_name):
                    if ('www.%s'%(start_url)) != get_site(url_name):
                        if len(url_name)<2:
                            continue
                        if ('//' != url_name[0:2]) and url_name[0] == '/':
                            url_name = '%s%s'%(start_url, url_name)
                        else:
                            continue
                big_chunk.append(url_name)
                if url_name in walked:
                    continue            
                else:
                    walked.append(url_name)
                    
                    try:
                        urls, data_amount  = grab_page(url_name, user_agent, save_method, timestamp, save_to)
                        total_data += data_amount
                        links_number += len(urls)
                        buff.extend(urls)
                        print url_name
                    except:
                        print "--==##Bad url: ", url_name
                        
                    if len(url_name)>longest:
                        longest = len(url_name)
                        longest_link = url_name
                    if len(url_name)<short:
                        short = len(url_name)
                        short_link = url_name

            url_list = list(set(buff))
            buff = []
            walked_length += len(walked)
            print"=============================================="
    finish_time=datetime.now()
    counter=collections.Counter(big_chunk)

    metrics = open('%s%s' % (str(timestamp), '_metrics.txt'), 'w')
    metrics.write("=============BASIC__CRAWLER__METRICS=============\n")
    metrics.write("%-42s"%( "Start time:")+str(start_time)+ "\n")
    metrics.write("%-42s"%( "Finish time:")+str(finish_time)+ "\n")
    metrics.write("%-42s"%( "Crawled time:")+str(finish_time - start_time)+ "\n")
    metrics.write("%-42s"%( "Number of collected links:")+str(links_number)+ "\n")
    metrics.write("%-42s"%( "Of them unique, related to inputed sites:")+str(walked_length)+ "\n")
    metrics.write("%-42s"%( "Longest link(" + str(longest) + " symbols): ") + longest_link + "\n")
    metrics.write("%-42s"%( "Shortest link(" + str(short) + " symbols): ") + short_link + "\n")
    metrics.write("%-42s"%( "Amount of downloaded data:") +  str(total_data) + " bytes" + "\n")
    metrics.write("\n=====Link, times it is quoted=====\n")
    for item in counter.items():
        metrics.write(str(item)+'\n')
    metrics.close()

    print ("Done!")    
