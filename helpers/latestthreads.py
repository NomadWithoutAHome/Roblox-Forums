from bs4 import BeautifulSoup
import requests


class ThreadScraper(object):
    def __init__(self):
        self.r = requests.get('https://forum.robloxscripts.com/xmlhttp.php?action=recent_threads')
        self.data = self.r.text
        self.soup = BeautifulSoup(self.data, 'lxml')

    def get_thread_text(self):
        print('[debug]: Starting [get_thread_text] function')
        u = self.soup.select("span.subject_new")
        threads = [threads.get_text() for threads in u]
        return threads

    def get_thread_link(self):
        print('[debug]: Starting [get_thread_link] function')
        u = self.soup.select("span.subject_new a")
        threads = [threads['href'] for threads in u]
        return threads

    def get_thread_author(self):
        print('[debug]: Starting [get_thread_author] function')
        u = self.soup.select("span+ a")
        threads = [threads.get_text() for threads in u]
        return threads

    def get_thread_time(self):
        print('[debug]: Starting [get_thread_time] function')
        u = self.soup.select("br+ span")
        threads = [threads.get_text() for threads in u]
        return threads

    def build(self):
        print('[debug]: Starting [building] function')
        # database = zip(self.get_data()[0], self.get_video(), self.get_data()[1], self.get_desc(),self.get_mobile())
        database = {"Latest": [{"title": a, "url": b, "author": c, "time": d} for a, b, c, d in
                               zip(self.get_thread_text(), self.get_thread_link(), self.get_thread_author(),
                                   self.get_thread_time())]}
        return database
