marketDays = ['11JAN2021','12JAN2021', '13JAN2021', '14JAN2021', '15JAN2021', '18JAN2021', '19JAN2021', '20JAN2021', '21JAN2021', '22JAN2021', '25JAN2021', '27JAN2021', '28JAN2021', '29JAN2021', '01FEB2021', '02FEB2021', '03FEB2021', '04FEB2021', '05FEB2021', '08FEB2021', '09FEB2021', '10FEB2021', '11FEB2021', '12FEB2021', '15FEB2021', '16FEB2021', '17FEB2021', '18FEB2021', '19FEB2021', '22FEB2021', '23FEB2021', '24FEB2021', '25FEB2021', '26FEB2021', '01MAR2021', '02MAR2021', '03MAR2021', '04MAR2021', '05MAR2021', '08MAR2021','09MAR2021','10MAR2021','12MAR2021','15MAR2021'] 

import sqlite3

conn = sqlite3.connect('bhavcopy/nsedb.db')
curr = conn.cursor()

refTab = "cm11JAN2021bhav"
chkTab = "cm11JAN2021bhav"

stockName = " "
HammerT = {}
gap=0
daYN = -1
percUW = 0.0
HammerTchk = 0


stockName = " "

chkTab = "cm"+str(marketDays[dayN])+"bhav"
curr.execute("SELECT * FROM "+chkTab+";")
refs = curr.fetchall()
for ref in refs:
    stockName = str(ref[0])
    HammerTchk = 0
    if float(ref[2])<float(ref[5]):
        gap = float(ref[5])-float(ref[2])
        if ((float(ref[2])-float(ref[4])) >= 2*gap):
            percUW = ((float(ref[3])-float(ref[5]))/(gap))
            if percUW < 1:
                HammerTchk = 1
        
    elif float(ref[2])>float(ref[5]):
        gap = float(ref[2])-float(ref[5])
        if ((float(ref[5])-float(ref[4])) >= 2*gap):
            percUW = ((float(ref[3])-float(ref[2]))/(gap))
            if percUW < 1:
                HammerTchk = 1 
    
    if HammerTchk == 1:
        HammerT[stockName]=[HammerTchk,percUW]
    else:
        HammerT[stockName]=[HammerTchk,0]


chkTab = "nifty20009MAR2021"
curr.execute("SELECT * FROM "+chkTab)
nifty = curr.fetchall()
niftyList = []

for niftyStock in nifty:
    niftyList.append(niftyStock[0])

sql = """CREATE TABLE Hammar"""+marketDays[dayN]+""" (
	SYMBOL TEXT,
    IsHammar BINARY,
    UWPerc REAL,
    IsNIFTY BINARY
	);"""

curr.execute(sql)

refTab = "cm11JAN2021bhav"
chkTab = "cm11JAN2021bhav"
curr.execute("SELECT * FROM "+refTab)
refs = curr.fetchall()

niftyCheck = 0

for ref in refs:
    stockName = " "
    stockName = str(ref[0])
    if stockName in niftyList:
        niftyCheck = 1
    else:
        niftyCheck = 0
    sql = "INSERT INTO Hammar"+marketDays[dayN]+ " (SYMBOL, IsHammar, UWPerc, IsNIFTY) VALUES ('"+ stockName+"',"+str(HammerT[stockName][0])+","+str(HammerT[stockName][1])+","+str(niftyCheck)+");"
    curr.execute(sql)

conn.commit()