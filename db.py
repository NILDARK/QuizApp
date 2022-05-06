import mysql.connector
from mysql.connector import errorcode
from tkinter import messagebox
class Database:
    def __init__(self,root):
        try:
            self.db = mysql.connector.connect(user='',password='',host="",database="") # enter database details here    
            self.cur = self.db.cursor()
        except:
            messagebox.showerror("Error","Server Not Reachable. Please Try Again Later.")
            root.exit()
            pass

    def disconnectDB(self):
        self.db.close()
    
    def insertToRegisteredClients(self,values):   
        try:     
            self.cur.execute(f"""INSERT INTO registeredClients VALUES('{values[0]}','{values[1]}','{values[2]}','{values[3]}','{values[4]}',curdate())""")
            self.db.commit()
            messagebox.showinfo("Success","Registered Successfully.")
        except Exception as e:
            messagebox.showerror("Error","Something Went Wrong.")
            print(e)
    
    def getPassword(self,username):
        try:
            self.cur.execute(f"""SELECT client_password from registeredClients WHERE username = '{username}'""")
            res = self.cur.fetchone()
            res = res[0]
            return str(res)
        except:
            return "-1"
    
    def getEmail(self,email):
        try:
            self.cur.execute(f"""SELECT client_email from registeredClients WHERE client_email = '{email}'""")
            res = self.cur.fetchone()
            res = res[0]
            return str(res)
        except:
            return "-1"

    def getUsername(self,username):
        try:
            self.cur.execute(f"""SELECT username from registeredClients WHERE username = '{username}'""")
            res = self.cur.fetchone()
            res = res[0]
            return str(res)
        except:
            return "-1"

    def logEntry(self,username):
        try:
            self.cur.execute(f"""INSERT INTO logtable(username,datetimeOfLogin,datetimeOfSigningOut) VALUES('{username}',current_timestamp(),NULL)""")
            self.db.commit()
        except Exception as e:
            print(e)
    
    def logExit(self,username):
        try:
            self.cur.execute(f"""UPDATE logtable SET datetimeOfSigningOut = current_timestamp() WHERE username = '{username}' and ISNULL(datetimeOfSigningOut)""")
            self.db.commit()
        except Exception as e:
            print(e)
            
    def getQIds(self):
        self.cur.execute(f"""SELECT COUNT(qId) FROM Questions""")
        cnts = self.cur.fetchone()
        return [i for i in range(1,cnts[0]+1)]

if __name__=="__main__":        
    values = ("test12345","Nilay","test@12345","nilu.patel2002@gmail.com",20)
    newdb = Database(root="hi")
    # newdb.insertToRegisteredClients(values)
    print(newdb.getPassword("test12345"))
    print(newdb.getUsername("test12345"))
    print(newdb.getQIds())
    newdb.disconnectDB()