class Login:     
    import pandas as pd
    import os
    os.chdir(r"C:\Users\KIIT\Desktop\python programming\python projects\Quiz")  
    df = pd.read_excel("data.xlsx")
    srno = 0
    login = False
    usrname = ''
    name = ''
    age = ''
    email = ''
    for data in df.iterrows():
        srno +=1
    
    def __init__(self,usrName,usrPass):
        # print(f"Total entries = {Login.srno}")
        if(Login.srno>0):
            self.usrname = usrName
            self.pswd = usrPass
            self.check()
        else:
            Login.login=False

    
    def check(self):
        for index,item in Login.df.iterrows():
            if(self.usrname==item['UserName']):
                self.id = index                
                usrPswd = item['Password']
                Login.usrname = self.usrname        
                self.checkPSWD(usrPswd)
                ch = 0
                break
        else:
            Login.login=False
    
    def checkPSWD(self,usrPswd):
        if(self.pswd==usrPswd):            
            Login.login = True  
            ch=0                
        else:
            Login.login=False
if __name__=="__main__":
    l = Login()