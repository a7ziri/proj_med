import mysql.connector
import uuid

con = mysql.connector.connect(
    user='root',
    password='Dend1y13',
    host='localhost',
    database='doctor'
)
print('connect')
cur = con.cursor()





with open('Symptoms.txt', 'r') as f:
    myNames = [line.strip() for line in f]
    print(myNames)

with open('Weight.txt', 'r') as f:
    myNames2 = [line.strip() for line in f]
    print(myNames2)

list = []
for element, element2 in myNames, myNames2:
    list.append(element)
    print(list)

    list.append(element2)
    print(list)
    insert_command_name = """
            REPLACE INTO doctor.syptom_name (symptom, symptom_number)
            VALUES (%s, %s)
        """

    cur.execute(insert_command_name, list)
    con.commit()
    list.clear()
    
