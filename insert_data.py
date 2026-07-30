import mysql.connector

db = mysql.connector.connect(

host="localhost",

user="root",

password="Adetoks@1971",

database="knowireland_ai"

)

cursor = db.cursor()

sql = """

INSERT INTO companies(

company_name,

industry,

country,

employees,

annual_revenue,

energy_consumption,

water_consumption,

waste_generated,

recycling_rate,

renewable_energy,

transport_emissions,

carbon_emissions)

VALUES

(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

"""

values=(

"Green Manufacturing Ltd",

"Manufacturing",

"Ireland",

250,

5000000,

420000,

21000,

150,

62,

45,

320,

210

)

cursor.execute(sql,values)

db.commit()

print("Record Inserted Successfully")