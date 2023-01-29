import csv
import decimal
import psycopg2
from datetime import date

username = 'tim'
password = 'tim'
database = 'tim'
host = 'localhost'
port = '5432'


INPUT_INCIDENT = 'import_csv/INCIDENT.csv'
INPUT_SHOOTER = 'import_csv/SHOOTER.csv'
INPUT_VICTIM = 'import_csv/VICTIM.csv'
INPUT_WEAPON = 'import_csv/WEAPON.csv'

query_1 = '''
DELETE FROM incident;
'''
query_2 = '''
DELETE FROM shooter;
'''
query_3 = '''
DELETE FROM victim;
'''
query_4 = '''
DELETE FROM weapon;
'''

query_7 = '''
INSERT INTO INCIDENT(incident_id, date, quarter, school, city, state, school_level) VALUES (%s, %s, %s, %s, %s, %s, %s)
'''
query_8 = '''
select * from incident
'''

query_9 = '''
INSERT INTO shooter(shooterid, incidentid, age, gender, race, schoolaffilation, shooteroutcome, shooterdied, injury, chargesfield, verdict) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
query_10 = '''
select * from shooter limit 10;
'''

query_11 = '''
INSERT INTO victim(victimid, incidentid, race, injury, gender, schoolaffilation, age) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
query_12 = '''
select * from victim limit 10;
'''

query_13 = '''
INSERT INTO weapon(weaponid, incidentid, weaponcaliber, weapondetails, weapontype) VALUES (%s, %s, %s, %s, %s)'''
query_14 = '''
select * from weapon limit 10;
'''



conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()
    cur.execute(query_4)
    cur.execute(query_2)
    cur.execute(query_3)
    cur.execute(query_1)

    input_file = csv.DictReader(open(INPUT_INCIDENT))
    for idx, row in enumerate(input_file):
        values = (row['\ufeffIncident_ID'], row['Date'], row['Quarter'], row['School'], row['City'], row['State'], row['School_Level'])
        cur.execute(query_7, values)
    cur.execute(query_8)
    #for row in cur:
    #    print(row)

    input_shooter = csv.DictReader(open(INPUT_SHOOTER, encoding='utf-8'))
    for idx, row in enumerate(input_shooter):
        values = (idx, row['\ufeffincidentid'], row['age'], row['gender'], row['race'], row['schoolaffiliation'], row['shooteroutcome'], row['shooterdied'], row['injury'], row['chargesfiled'], row['verdict'])
        cur.execute(query_9, values)
    cur.execute(query_10)
    #for row in cur:
    #    print(row)

    input_victim = csv.DictReader(open(INPUT_VICTIM, encoding='utf-8'))
    for idx, row in enumerate(input_victim):
        values = (idx, row['\ufeffincidentid'], row['race'], row['injury'], row['gender'], row['schoolaffiliation'], row['age'])
        cur.execute(query_11, values)
    cur.execute(query_12)
    #for row in cur:
    #    print(row)

    input_weapon = csv.DictReader(open(INPUT_WEAPON, encoding='utf-8'))
    for idx, row in enumerate(input_weapon):
        values = (idx, row['incidentid'], row['weaponcaliber'], row['weapondetails'], row['weapontype'])
        cur.execute(query_13, values)
    cur.execute(query_14)
    #for row in cur:
    #    print(row)

    conn.commit()
