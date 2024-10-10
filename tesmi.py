
from geopy import distance
from operator import itemgetter
import random
import mysql.connector


connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='aroundtheworld',
    user='ympari',
    password='1234',
    collation = 'utf8mb4_general_ci',
    autocommit=True
)


def create_game(start_money, cur_airport, tired):
    sql = "INSERT INTO game (money, location, tired) VALUES (%s, %s, %s);"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (start_money, cur_airport, tired))
    g_id = cursor.lastrowid
    return g_id

#haetaan nykyisen kentän pituuspiiri
def get_current_longitude():
    sql = f"SELECT longitude_deg FROM airport WHERE ident = %s;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (current_ap,))
    result = cursor.fetchone()
    return result['longitude_deg']

#kopioitiin esimerkistä lentokentän tarvittavan tiedon haku sekä etäisyyksien lasku
def get_airport_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km

#haetaan lähimmät 9 kenttää 300 ja 1500 km sisällä, itään päin

def get_easterner_ap(c_ap):
    nineclosest = {}
    listnine = []
    sql = f"SELECT name, longitude_deg, latitude_deg, ident FROM airport WHERE longitude_deg > '{get_current_longitude()}' ORDER BY longitude_deg;"
    cursor = connection.cursor(dictionary=True, buffered=True)
    cursor.execute(sql)
    ran = len(cursor.fetchall())
    cursor.execute(sql)
    serial = 0
    for i in range(ran):
        result = cursor.fetchone()
        if 300 < calculate_distance(c_ap, result['ident']) < 1500:
            tuple = calculate_distance(c_ap, result['ident']), result['name']
            listnine.append(tuple)
    sortedlist9 = sorted(listnine)
    for i in range(9):
        i+=1
        nineclosest.update({i:sortedlist9[i]})
    #sorted_nineclosest = dict(sorted(nineclosest.items(), key=itemgetter(1)))
    return nineclosest

def update_location(icao, p_tired, u_money, g_id):
    sql = f'''UPDATE game SET location = %s, tired = %s, money = %s WHERE id = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_tired, u_money, g_id))

#asetetaan perusarvoja
total_travel_dist = 0
total_co2_spent = 0
money = 1000
tired = 0
score = 0
win = False
current_ap = 'EGGW'
price0 = 0
price1 = 100
price2 = 200
price3 = 300
game_id = create_game(money, current_ap, tired)
#pelilooppi
airports = get_easterner_ap(current_ap)

print(airports[1])
