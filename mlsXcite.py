"""
Example flask app for Insight program
John Felde
"""

import os
from flask import Flask, render_template, Markup
import pymysql
# from numpy import random
from datetime import datetime, timedelta
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# import pandas as pd

app = Flask(__name__, static_folder=os.path.join(os.getcwd(),'static'))

# os.path.join(os.getcwd(),'web','static')

#user = 'johnfel1_insight' #add your username here (same as previous postgreSQL)
#passwd = 'datascience'
#host = 'localhost'
#dbname = 'johnfel1_mls'
#conn = pymysql.connect(host=host,user=user,passwd=passwd,db=dbname,autocommit=True)

def ticket_url(home):
    """
    Return the link to the ticket page for the home team.
    """
    team_urls = {'ATL':('http://www.ticketmaster.com/Atlanta-United-FC-tickets/artist/2213124',
                        'https://www.stubhub.com/atlanta-united-fc-tickets/performer/1515465/'),
                 'CHI':('http://www.ticketmaster.com/Chicago-Fire-tickets/artist/805916',
                        'https://www.stubhub.com/chicago-fire-tickets/performer/52204/'),
                 'CLB':('http://www.ticketmaster.com/Columbus-Crew-SC-tickets/artist/805928',
                        'https://www.stubhub.com/columbus-crew-tickets/performer/17888/'),
                 'COL':('http://www.ticketmaster.com/Colorado-Rapids-tickets/artist/805925',
                        'https://www.stubhub.com/colorado-rapids-tickets/performer/19789/'),
                 'DAL':('http://www.ticketmaster.com/FC-Dallas-tickets/artist/805930',
                        'https://www.stubhub.com/fc-dallas-tickets/performer/52005/'),
                 'DC':('http://www.ticketmaster.com/D-C-United-tickets/artist/806390',
                       'https://www.stubhub.com/dc-united-tickets/performer/23188/'),
                 'HOU':('http://www.ticketmaster.com/Houston-Dynamo-tickets/artist/1017951',
                        'https://www.stubhub.com/houston-dynamo-tickets/performer/100417/'),
                 'KC':('http://www.ticketmaster.com/Sporting-Kansas-City-tickets/artist/805957',
                       'https://www.stubhub.com/sporting-kansas-city-tickets/performer/52304/'),
                 'LA':('http://www.ticketmaster.com/LA-Galaxy-tickets/artist/805960',
                       'https://www.stubhub.com/los-angeles-galaxy-tickets/performer/12587/'),
                 'MIN':('http://www.ticketmaster.com/Minnesota-United-FC-tickets/artist/1501648',
                        'https://www.stubhub.com/united-fc-de-minnesota-tickets/performer/437944/'),
                 'MTL':('http://www.ticketmaster.com/Montreal-Impact-tickets/artist/806614',
                        'https://www.stubhub.com/montreal-impact-tickets/performer/302489/'),
                 'NE':('http://www.ticketmaster.com/New-England-Revolution-tickets/artist/805981',
                       'https://www.stubhub.com/new-england-revolution-tickets/performer/19689/'),
                 'NY':('http://www.ticketmaster.com/New-York-Red-Bulls-tickets/artist/806601',
                       'https://www.stubhub.com/new-york-red-bulls-tickets/performer/105417/'),
                 'NYC':('http://www.ticketmaster.com/New-York-City-FC-tickets/artist/1991293',
                        'https://www.stubhub.com/new-york-city-fc-tickets/performer/1495038/'),
                 'ORL':('http://www.ticketmaster.com/Orlando-City-SC-tickets/artist/1550331',
                        'https://www.stubhub.com/orlando-city-sc-tickets/performer/723465/'),
                 'PHI':('http://www.ticketmaster.com/Philadelphia-Union-tickets/artist/1418418',
                        'https://www.stubhub.com/philadelphia-union-tickets/performer/425898/'),
                 'POR':('http://www.ticketmaster.com/Portland-Timbers-tickets/artist/806820',
                        'https://www.stubhub.com/portland-timbers-tickets/performer/415899/'),
                 'RSL':('http://www.ticketmaster.com/Real-Salt-Lake-tickets/artist/959263',
                        'https://www.stubhub.com/real-salt-lake-tickets/performer/52006/'),
                 'SEA':('http://www.ticketmaster.com/Seattle-Sounders-FC-tickets/artist/1292961',
                        'https://www.stubhub.com/seattle-sounders-fc-tickets/performer/388488/'),
                 'SJ':('http://www.ticketmaster.com/San-Jose-Earthquakes-tickets/artist/806017',
                       'https://www.stubhub.com/san-jose-earthquakes-tickets/performer/143/'),
                 'TOR':('http://www.ticketmaster.com/Toronto-FC-tickets/artist/1110670',
                        'https://www.stubhub.com/toronto-fc-tickets/performer/137567/'),
                 'VAN':('http://www.ticketmaster.com/Vancouver-Whitecaps-FC-tickets/artist/821721',
                        'https://www.stubhub.com/vancouver-whitecaps-tickets/performer/415898/')}
    return team_urls[home]

# def get_stars_model(date, home, away):
def get_stars_model(num):
    """
    return the number of stars given a particular game
    """
    return Markup(u''.join([u'&#9733;&nbsp;' for i in range(num)]))

def build_url(home, away, year, month, day):
    name_map = {'ATL':'atlanta-united-fc',
                'CHI':'chicago-fire',
                'CHV':'chivas-usa',
                'CLB':'columbus-crew-sc',
                'COL':'colorado-rapids',
                'DAL':'fc-dallas',
                'DC':'dc-united',
                'HOU':'houston-dynamo',
                'KC':'sporting-kansas-city',
                'LA':'la-galaxy',
                'MIN':'minnesota-united-fc',
                'MTL':'montreal-impact',
                'NE':'new-england-revolution',
                'NY':'new-york-red-bulls',
                'NYC':'new-york-city-fc',
                'ORL':'orlando-city-sc',
                'PHI':'philadelphia-union',
                'POR':'portland-timbers',
                'RSL':'real-salt-lake',
                'SEA':'seattle-sounders-fc',
                'SJ':'san-jose-earthquakes',
                'TOR':'toronto-fc',
                'VAN':'vancouver-whitecaps-fc'}
    url = 'https://matchcenter.mlssoccer.com/matchcenter/'
    url += year+'-'+month+'-'+day+'-'
    url += name_map[home]
    url += '-vs-'
    url += name_map[away]+'/'
    return url

@app.route('/')
@app.route('/index')
def index():
    # return "Hello"
    # today = datetime.now().date()
    # last_week = today-timedelta(7)
    # next_week = today+timedelta(7)
    # ATL, CHI, CLB, COL, DAL, DC, HOU, KC, LA, MIN, MTL, NE, NY, NYC, ORL
    # PHI, POR, RSL, SEA, SJ, TOR, VAN
    games = [
            ['Sunday, Oct. 22', 'ATL', 'TOR', build_url('ATL','TOR','2017','10','22'), get_stars_model(3), ticket_url('ATL')],
            ['', 'DC', 'NY', build_url('DC','NY','2017','10','22'), get_stars_model(1), ticket_url('DC')],
            ['', 'MTL', 'NE', build_url('MTL','NE','2017','10','22'), get_stars_model(4), ticket_url('MTL')],
            ['', 'NYC', 'CLB', build_url('NYC','CLB','2017','10','22'), get_stars_model(4), ticket_url('NYC')],
            ['', 'PHI', 'ORL', build_url('PHI','ORL','2017','10','22'), get_stars_model(3), ticket_url('PHI')],
            ['', 'DAL', 'LA', build_url('DAL','LA','2017','10','22'), get_stars_model(4), ticket_url('DAL')],
            ['', 'RSL', 'KC', build_url('RSL','KC','2017','10','22'), get_stars_model(1), ticket_url('RSL')],
            ['', 'POR', 'VAN', build_url('POR','VAN','2017','10','22'), get_stars_model(2), ticket_url('POR')],
            ['', 'SJ', 'MIN', build_url('SJ','MIN','2017','10','22'), get_stars_model(3), ticket_url('SJ')],
            ['', 'SEA', 'COL', build_url('SEA','COL','2017','10','22'), get_stars_model(5), ticket_url('SEA')],
            ['', 'HOU', 'CHI', build_url('HOU','CHI','2017','10','22'), get_stars_model(3), ticket_url('HOU')],
            ['Wednesday, Oct. 25', 'CHI', 'NY', build_url('CHI','NY','2017','10','25'), get_stars_model(3), ticket_url('CHI')],
            ['', 'VAN', 'SJ', build_url('VAN','SJ','2017','10','25'), get_stars_model(4), ticket_url('VAN')],
            ['Thursday, Oct. 26', 'ATL', 'CLB', build_url('ATL','CLB','2017','10','26'), get_stars_model(4), ticket_url('ATL')],
            ['', 'HOU', 'KC', build_url('HOU','KC','2017','10','26'), get_stars_model(3), ticket_url('HOU')]
            ]
    # games = [['a','b','c','d','e','f']]
    return render_template("schedule.html", games=games)
    # return render_template("schedule.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/slides')
def slides():
    return render_template("slides.html")

@app.route('/schedule')
def schedule_page():
    today = datetime.now().date()
    last_week = today-timedelta(7)
    next_week = today+timedelta(7)
    # games = [['Monday, January 1st','SEA','COL','http://google.com',get_stars_model(),('http://test1.com','http://test2.com')]]
    # print games
    # return render_template("schedule.html", games=games)
    cmd = "SELECT date,home,away,url FROM schedule WHERE date>="
    cmd += "'{0}' AND date<='{1}';".format(today,next_week)
    cur = conn.cursor()
    cur.execute(cmd)
    results = cur.fetchall()
    games = []
    for i,(date,home,away,url) in enumerate(results):
        tix_url = ticket_url(home)
        stars = get_stars_model(date,home,away)
        if i == 0:
            last_date = date
            games_up.append([date.strftime('%A, %B %d'),home,away,url,stars,tix_url])
            continue
        if date == last_date:
            games.append(['',home,away,url,stars,tix_url])
        else:
            last_date = date
            games.append([date.strftime('%A, %B %d'),home,away,url,stars,tix_url])
    games = ['Monday, January 1','SEA','DC','test',5,('test1','test2')]
    return render_template("schedule.html",games=games)

if __name__ == '__main__':
    app.run()


    # table = ""
    # hline = False
    # for i,(date,home,away,url) in enumerate(results):
    #     if i==0:
    #         last_date = date
    #         table += date.strftime("%B, %d %Y")+'<br>\n'
    #     if date == last_date:
    #         table += home
    #         table += ' vs. '
    #         table += away
    #         table += '<a href="{0}">MatchCenter</a>'.format(url)
    #         table += '<br>\n'
    #     else:
    #         last_date = date
    #         table += date.strftime("%B, %d %Y")+'<br>\n'
    #         table += home
    #         table += ' vs. '
    #         table += away
    #         table += '<a href="{0}">MatchCenter</a>'.format(url)
    #         table += '<br>\n'
    #     if date > today and not hline:
    #         print "here"
    #         table += '<hr><br>\n'
    #         hline = True
    # return table

# @app.route('/db_fancy')
# def cesareans_page_fancy():
#     sql_query = """
#                SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
#                 """
#     query_results=pd.read_sql_query(sql_query,con)
#     births = []
#     for i in range(0,query_results.shape[0]):
#         births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
#     return render_template('cesareans.html',births=births)
