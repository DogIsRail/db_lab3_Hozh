import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

username = 'tim'
password = 'tim'
database = 'tim'
host = 'localhost'
port = '5432'


query_1 = '''
CREATE view VictimsIncAmount as
    SELECT incidentid, COUNT(incidentid) as amount_victim
    FROM victim
    GROUP BY incidentid
    ORDER BY amount_victim DESC;
'''
query_2 = '''
CREATE view ShooterOutcomes as
    SELECT shooteroutcome, COUNT(incidentid) as amount_outcomes
    FROM shooter
    GROUP BY shooteroutcome
    ORDER BY amount_outcomes DESC;
'''
query_3 = '''
CREATE view IncPerYear as
    SELECT yr, COUNT(inc) as amount_outcomes
    FROM victim join (SELECT incident_id as inc, EXTRACT(YEAR FROM date) as yr
                              FROM incident) as t
    ON inc = victim.incidentid
    GROUP BY yr
    ORDER BY yr DESC;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
print(type(conn))

with conn:
    cur = conn.cursor()
    cur.execute('DROP VIEW IF EXISTS VictimsIncAmount')
    cur.execute(query_1)
    cur.execute('SELECT * FROM VictimsIncAmount')
    incident = []
    amount_per_inc = []
    for row in cur:
        incident.append(row[0])
        amount_per_inc.append(row[1])

    cur.execute('DROP VIEW IF EXISTS ShooterOutcomes')
    cur.execute(query_2)
    cur.execute('SELECT * FROM ShooterOutcomes')
    outcomes = []
    amount_of_outcomes = []
    for row in cur:
        outcomes.append(row[0])
        amount_of_outcomes.append(row[1])

    cur.execute('DROP VIEW IF EXISTS IncPerYear')
    cur.execute(query_3)
    cur.execute('SELECT * FROM IncPerYear')
    inc_per_year = []
    year = []
    for row in cur:
        if row[1]:
            inc_per_year.append(row[0])
            year.append(row[1])

fig, (bar_ax, pie_ax, dot_ax) = plt.subplots(1, 3)

bar_ax.set_title('Кількість жертв кожного інциденту')
bar_ax.set_xlabel('Інцидент')
bar_ax.set_ylabel('Кількість')
bar_ax.bar(incident, amount_per_inc)
fig.autofmt_xdate(rotation=90)

pie_ax.pie(amount_of_outcomes, labeldistance=0.02, autopct='%1.1f%%')
pie_ax.legend(outcomes, loc="lower center", bbox_to_anchor=(0.5, -0.2, 0.1, 0.5))
pie_ax.set_title('Долі стрільців')



data_query_3 = pd.DataFrame({'year': inc_per_year, 'number_of_incidents': year})
dot_ax.set_title('Інциденти на рік')
sns.scatterplot(data=data_query_3, x='year', y='number_of_incidents', ax=dot_ax)
fig.autofmt_xdate(rotation=90)


plt.get_current_fig_manager().resize(1900, 900)
plt.subplots_adjust(left=0.1,
                    bottom=0.321,
                    right=0.9,
                    top=0.967,
                    wspace=0.5,
                    hspace=0.195)
plt.show()