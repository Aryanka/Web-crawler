import threading
from queue import Queue
from Spider import Spider
from domain import *
from general import *
        
PROJECT_NAME = 'Web crawler'
HOMEPAGE = 'https://www.eckovation.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


#Each queue link is a new job...
def create_jobs():
        for link in file_to_set(QUEUE_FILE):
                queue.put(link)
        queue.join()
        crawl()

#check if the items iin queue...
def crawl():
        queued_links = file_to_set(QUEUE_FILE)
        if len(queued_links)>0:
                print(str(len(queued_links) )+ 'links in the queue')
                create_jobs()


create_workers()
crawl()
