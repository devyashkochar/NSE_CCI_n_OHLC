import sqlite3

conn = sqlite3.connect('bhavcopy/nsedb.db')
curr = conn.cursor()

refTab = "cm16FEB2021bhav"
chkTab = "cm11JAN2021bhav"
date = "11"
month = "JAN"

marketDays=[]
toAdd=" "

stopcode = 0

curr.execute("SELECT * FROM "+refTab)
refs = curr.fetchall()

while True:
    curr.execute("SELECT * FROM "+chkTab)
    chks = curr.fetchall()
    sql = """DELETE FROM """+chkTab+""" WHERE SERIES != 'EQ';"""
    curr.execute(sql)
    #print(sql)
    if len(chks)<len(refs):
        print("NewRef - ",chkTab)
    for chk in chks:
        flag = 0
        for ref in refs:
            if chk[0] == ref[0]:
                flag = 1
                break
        if flag==0:
            sql = """DELETE FROM """+chkTab+""" WHERE SYMBOL = '""" + chk[0] +"""';"""
            curr.execute(sql)
            #print(sql)
    date = str(int(date)+1)
    #print(date)
    while month == "JAN" and (date == "16" or date == "17"or date == "23" or date == "24" or date == "26") :
        date = str(int(date)+1)
    if int(date) > 29 and month == "JAN":
        month = "FEB"
        date = "01"
    while month == "FEB" and (date == "6" or date == "7"or date == "13" or date == "14" or date == "20" or date == "21" or date == "27" or date == "28") :
        date = str(int(date)+1)
    if int(date) >= 29 and month == "FEB":
        month = "MAR"
        date = "01"
    while month == "MAR" and (date == "6" or date == "7") :
        date = str(int(date)+1)
    if month=="MAR" and int(date) > 10:
        stopcode = 1
    if stopcode == 1:
        conn.commit()
        print(marketDays)
        break

    if len(date) == 1:
        date = "0"+date
    chkTab = "cm"+date+month+"2021bhav"
    toAdd = date+month+"2021"
    marketDays.append(toAdd)
    #print(chkTab)


     




    