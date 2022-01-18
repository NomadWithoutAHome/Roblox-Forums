from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from helpers.latestthreads import ThreadScraper


app = Flask(__name__)


@app.route("/api/robloxscriptsforums/userlookup")
def user_api():
    user = request.args.get('name')
    url = requests.get('https://forum.robloxscripts.com/User-{usr}'.format(usr=user))
    soup = BeautifulSoup(url.content, 'html5lib')

    purl = url.url

    if not 'The member you specified is either invalid' in soup.text:
        name = soup.select_one(
            '#content > div.wrapperforum > div.container.bootstrap.snippet > div > div > div.profile-cover-statss3.mobile-hide > span.largetext > strong').text.strip()
        pfp = soup.select_one('div.author-info-img img.profileavatarst')['src']
        try:
            rep = soup.select_one('.reputation_positive').text.strip()
        except AttributeError:
            try:
                rep = soup.select_one('.reputation_negative').text.strip()
            except AttributeError:
                rep = 'no/neutral'
        threads = soup.select_one(':nth-child(1) > .stats-num-cover > a').text.strip()
        posts = soup.select_one(':nth-child(2) > .stats-num-cover > a').text.strip()
        uid = soup.select_one('#content > div.wrapperforum > div:nth-child(10) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > span.useruid125ff').text
        replink = soup.select_one(
            '#content > div.wrapperforum > div:nth-child(10) > div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(1) > div.profile-top > span > strong > center > strong > a')[
            'href']
        timeonline = soup.select_one(
            '#content > div.wrapperforum > div:nth-child(10) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(8)').text.strip().lower()
        threadlink = soup.select_one(
            '#content > div.wrapperforum > div.container.bootstrap.snippet > div > div > div.profile-cover-statss1 > div > div:nth-child(1) > div > a')[
            'href']
        postlink = soup.select_one(
            '#content > div.wrapperforum > div.container.bootstrap.snippet > div > div > div.profile-cover-statss1 > div > div:nth-child(2) > div > a')[
            'href']
        try:
            joindate = soup.select_one(
            'div.mobilevrs1:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > span:nth-child(2)').text.replace(
            'Joined:', '')
        except AttributeError:
            joindate= 'broken'

        try:
            active = soup.select_one(
                '#content > div.wrapperforum > div.container.bootstrap.snippet > div > div > div.profile-cover-statss3.mobile-hide > span.onmobile').text.strip(
                '()')
        except AttributeError:
            active = "no recent activity"

        try:
            status = soup.select_one(
                '#content > div.wrapperforum > div.container.bootstrap.snippet > div > div > div.profile-cover-statss3.mobile-hide > a > span').text.strip()
        except AttributeError:
            try:
                status = soup.select_one(
                    '#content > div.wrapperforum > div.container.bootstrap.snippet > div > div > div.profile-cover-statss3.mobile-hide > span.offline').text.strip()
            except AttributeError:
                print('need to fix api')


        return jsonify(Username=name,pfp=pfp,rep=rep,threads=threads,posts=posts,postlink=postlink,replink=replink,timeonline=timeonline,threadlink=threadlink,active=active,status=status,joindate=joindate,proflink=purl), 200
    else:
        return '1911'

@app.route("/api/robloxscriptsforums/latest-threads")
def threadapi():
    scrape = ThreadScraper()
    return jsonify(scrape.build())




if __name__ == "__main__":
    app.run()