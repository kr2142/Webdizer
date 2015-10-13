import guess_language
from BeautifulSoup import BeautifulSoup
import os
import collections
import matplotlib.pyplot as plt
import random
from datetime import datetime


start_time = datetime.now()
timestamp = start_time.strftime("%d.%m.%Y-%H.%M.%S")
languages = []
sizes = []
most, biggest, most_words = 0, 0, 0
least, smallest, least_words = 10000000000, 10000000000, 10000000000
most_links, least_links, mwords_file, lwords_file, biggest_file, smallest_file = '', '', '', '', '', ''

settings = open('directory.ini', 'r')
for line in settings:
        if 'read_from::' in line:
            read_from = line[11:]
            
settings.close()
if read_from[-1] !='\\':
        read_from += '\\' 

for name in os.listdir(read_from):
    path = os.path.join(read_from, name)
    if not os.path.isfile(path):
        for webpage in os.listdir(path):
            urls = []
            if webpage[-4:] == '.txt':
                continue
            webpage = os.path.join(path, webpage)
            if os.path.isfile(webpage):
                html = open(webpage).read()
                soup = BeautifulSoup(html)

                links = soup.findAll('a', href=True)
                for tag in links:
                    link = tag.get('href',None)
                    if link != None:
                        urls.append(link)
                
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.getText()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                language = guess_language.guessLanguageName(text.encode('utf8'))
                languages.append(language)
                size = os.path.getsize(webpage)
                words = text.encode('utf8').split()
                
                report = open('%s%s' % (str(timestamp), '-hard_metrics.txt'), 'a')
                report.write(webpage)
                report.write('%s%s' % ('\nLanguage: ', language))
                report.write('%s%s' % ('\nNumber of links: ', str(len(urls))))
                report.write('%s%s' % ('\nSize of file: ', str(size)))
                report.write('%s%s' % ('\nAmount of words: ', str(len(words))))
                report.write('\n==============================================================\n')
                report.close()
                sizes.append(size)
                
                if len(urls)>most:
                    most = len(urls)
                    most_links = webpage
                if len(urls)<least:
                    least = len(urls)
                    least_links = webpage
                if size>biggest:
                    biggest = size
                    biggest_file = webpage
                if size<smallest:
                    smallest = size
                    smallest_file = webpage
                if len(words)>most_words:
                    most_words = len(words)
                    mwords_file = webpage
                if len(words)<least_words:
                    least_words = len(words)
                    lwords_file = webpage
                    

finish_time=datetime.now()
counter=collections.Counter(languages)
counter1=collections.Counter(sizes)
report = open('%s%s' % (str(timestamp), '-hard_metrics.txt'), 'a')
report.write("%-50s"%( "Start time:")+str(start_time)+ "\n")
report.write("%-50s"%( "Finish time:")+str(finish_time)+ "\n")
report.write("%-50s"%( "Time spent on analysis:")+str(finish_time - start_time)+ "\n")
report.write("%-50s"% ('File with highest # of links(' + str(most) + '):') + most_links + '\n')
report.write("%-50s"% ('File with lowest # of links(' + str(least) + '):') + least_links + '\n')
report.write("%-50s"% ('File with highest # of words(' + str(most_words) + '):') + mwords_file + '\n')
report.write("%-50s"% ('File with lowest # of words(' + str(least_words) + '):') + lwords_file + '\n')
report.write("%-50s"% ('Biggest file in the collection(' + str(biggest) + '):') + biggest_file + '\n')
report.write("%-50s"% ('Smallest file in the collection(' + str(smallest) + '):') + smallest_file + '\n')
report.write("%-50s"% ('Languages in the collection with # of files:') + str (counter) + '\n')
report.write("%-50s"% ('Sizes (bytes) in the collection with # of files:') + str (counter1) + '\n')
report.close()

labels = []
colors = []
r = lambda: random.randint(0,255)
for part in counter:
    labels.append(part)
    colors.append('#%02X%02X%02X' % (r(),r(),r()))
sizes = counter.values()


plt.pie(sizes,  labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.title('Languages in collection\n')

plt.show()
