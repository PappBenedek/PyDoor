import mysql.connector
import datetime
#Convert the day infromation wich is pulled from the database
def ConvertIntervals(it):
   def day(i):
    switcher={
        'H':'Monday',
        'K':'Tuesday',
        'SZ':'Wednesday',
        'CS':'Thursday',
        'P':'Friday',
        'SZOM':'Saturday',
        'V':'Sunday'
        }
    return switcher.get(i)
   returndict = {}
#Build up the dictionary formated like : {Day:[time intervall1, time intervall2]}   
   for x in it:
    d = day(x.split('>')[0])
    ido1, ido2 = x.split('>')[1].split('-')
    returndict[d] = [ido1, ido2]
   return returndict

class Database():
    def __init__(self):
#Set up the database connection    
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="benedek",
            password="MysecretPassw0rd:)",
            database="pydoor"
           )
#Init my cursor wich is handeling the sql commands
        self.mycursor = self.mydb.cursor()
    
    def login(self, username, password):
        self.mycursor.execute(f"SELECT * FROM users WHERE name = '{username}';")
        result = self.mycursor.fetchall()
#Check for the user is in the database
        if len(result) == 0:
            return False 
        else:
#If there, validate the password
            self.mycursor.execute(f"SELECT * FROM users WHERE name = '{username}';")
            result = self.mycursor.fetchall()
            self.mycursor.execute(f"SELECT PASSWORD('{password}')")
            qpassw = self.mycursor.fetchall()
            if result[0][2]  ==  qpassw[0][0]:
                return True
            else:
                return False

#Pull the time intervalls from database and converts for processing
#Return a simple true or false 
    def DoorCanBeOpened(self, username):
       self.mycursor.execute(f"SELECT * FROM users WHERE name = '{username}';")
       result = self.mycursor.fetchall()
       intervall = result[0][3].split('|')
       intervalls = ConvertIntervals(intervall)
       times = intervalls[datetime.datetime.now().strftime("%A")]
       time1hour = int(times[0].split(':')[0])
       time1second = int(times[0].split(':')[1])
       totaltime1 = int(time1hour) * 60 + int(time1second)
       time2hour = int(times[1].split(':')[0])
       time2second = int(times[1].split(':')[1])
       totaltime2 = int(time2hour) * 60 + int(time2second)
       currenthour = int(datetime.datetime.now().strftime("%H"))
       currentsecond = int(datetime.datetime.now().strftime("%M"))
       currenttotal = int(currenthour) * 60 + int(currentsecond)
       if totaltime1 <= currenttotal  and  totaltime2 >= currenttotal:
          return True
       else:
          return False

db = Database()
