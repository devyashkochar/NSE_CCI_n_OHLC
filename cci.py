marketDays = ['11JAN2021','12JAN2021', '13JAN2021', '14JAN2021', '15JAN2021', '18JAN2021', '19JAN2021', '20JAN2021', '21JAN2021', '22JAN2021', '25JAN2021', '27JAN2021', '28JAN2021', '29JAN2021', '01FEB2021', '02FEB2021', '03FEB2021', '04FEB2021', '05FEB2021', '08FEB2021', '09FEB2021', '10FEB2021', '11FEB2021', '12FEB2021', '15FEB2021', '16FEB2021', '17FEB2021', '18FEB2021', '19FEB2021', '22FEB2021', '23FEB2021', '24FEB2021', '25FEB2021', '26FEB2021', '01MAR2021', '02MAR2021', '03MAR2021', '04MAR2021', '05MAR2021', '08MAR2021','09MAR2021','10MAR2021'] 

print("Trending CCI on 9th March after closing..")

import sqlite3

conn = sqlite3.connect('bhavcopy/nsedb.db')
curr = conn.cursor()

refTab = "cm11JAN2021bhav"
chkTab = "cm11JAN2021bhav"

stockName = " "
calcTypicalList = []
TypicalPrice = []
SMA = 0.0
MD = 0.0
CCI = 0.0
CCIToday = {}
CCIYesterday = {}

curr.execute("SELECT * FROM "+refTab)
refs = curr.fetchall()

for ref in refs:
    stockName = " "
    calcTypicalList.clear()
    TypicalPrice.clear()
    SMA = 0.0
    MD = 0.0
    CCI = 0.0
    stockName = str(ref[0])
    for marketDay in marketDays[-20:]:
        chkTab = "cm"+str(marketDay)+"bhav"
        #print(marketDay)
        curr.execute("SELECT * FROM "+chkTab+""" WHERE SYMBOL = '"""+stockName+"""';""")
        refs = curr.fetchall()
        #print(refs)
        calcTypicalList = list(refs[0])
        TypicalPrice.append((float(calcTypicalList[3])+float(calcTypicalList[4])+float(calcTypicalList[5]))/3)
    for i in TypicalPrice:
        SMA = SMA+i
    SMA = SMA/20
    for j in TypicalPrice:
        MD = MD + abs(SMA-j)
    MD = MD/20
    CCI = (TypicalPrice[-1]-SMA)/(0.015*MD)
    CCIToday[stockName] = CCI


refTab = "cm11JAN2021bhav"
chkTab = "cm11JAN2021bhav"
curr.execute("SELECT * FROM "+refTab)
refs = curr.fetchall()

for ref in refs:
    stockName = " "
    calcTypicalList.clear()
    TypicalPrice.clear()
    SMA = 0.0
    MD = 0.0
    CCI = 0.0
    stockName = str(ref[0])
    for marketDay in marketDays[-21:-1]:
        chkTab = "cm"+str(marketDay)+"bhav"
        #print(marketDay)
        curr.execute("SELECT * FROM "+chkTab+""" WHERE SYMBOL = '"""+stockName+"""';""")
        refs = curr.fetchall()
        calcTypicalList = list(refs[0])
        TypicalPrice.append((float(calcTypicalList[3])+float(calcTypicalList[4])+float(calcTypicalList[5]))/3)
    for i in TypicalPrice:
        SMA = SMA+i
    SMA = SMA/20
    for j in TypicalPrice:
        MD = MD + abs(SMA-j)
    MD = MD/20
    CCI = (TypicalPrice[-1]-SMA)/(0.015*MD)
    CCIYesterday[stockName] = CCI

sql = """CREATE TABLE CCI"""+marketDays[-1]+""" (
	SYMBOL TEXT,
	CCIToday REAL,
	CCIYesterday REAL,
    IsNifty BINARY
	);"""

curr.execute(sql)

niftyCheck = 0

refTab = "cm11JAN2021bhav"
chkTab = "cm11JAN2021bhav"
curr.execute("SELECT * FROM "+refTab)
refs = curr.fetchall()

chkTab = "nifty20009MAR2021"
curr.execute("SELECT * FROM "+chkTab)
nifty = curr.fetchall()
niftyList = []

for niftyStock in nifty:
    niftyList.append(niftyStock[0])

for ref in refs:
    stockName = " "
    stockName = str(ref[0])
    if CCIToday[stockName]>50 and CCIYesterday[stockName]<50:
        if stockName in niftyList:
            niftyCheck = 1
        else:
            niftyCheck = 0
        sql = "INSERT INTO CCI"+marketDays[-1]+ " (SYMBOL, CCIToday, CCIYesterday, IsNifty) VALUES ('"+ stockName+"',"+str(CCIToday[stockName])+","+str(CCIYesterday[stockName])+","+str(niftyCheck)+");"
        print(sql)
        curr.execute(sql)   

conn.commit()