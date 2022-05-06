from login import Login
class SignUp(Login):
    import smtplib
    import random
    import string
    from creds import myid,mypass
    u=-1
    e = -1
    p = -1
    a = -1
    v = -1
    sent =1
    d = 1
    OTP=''
    ndf = Login.pd.DataFrame()

    @staticmethod
    def pswdIns():
        print("\n")
        print("**Password Should Contain Following: ")
        print("~ Should not blank or space.")
        print("~ Length should be 8 characters to 16 characters.")
        print("~ Should Contain atleast one Symbols (@,#,$).")
        print("~ Should conatin at least one Alphabet and Digit.")
        print("\n")   

    @staticmethod
    def usrnameIns():         
        print("**User Name Should Contain Following: ")
        print("~ Should not blank or space.")
        print("~ Length should be 8 characters to 12 characters.")
        print("~ Should not Contain any Symbols.")
        print("~ Should conatin at least one Alphabet and Digit.")
        print("\n")   

    def __init__(self):
        self.name = input("\tEnter Your Good Name: ")
        SignUp.usrnameIns()
        self.usrname = input("\tEnter Your User Name: ")
        self.checkUsrNameAvb()
        if SignUp.u==0:
            self.email= input("\tEnter Your Email: ")
            self.checkEmailAvb()
            
            if SignUp.e==0:
                SignUp.pswdIns()
                self.pswd = input("\tCreate Your Password: ")
                self.checkPSWDAvb()
                
                if (SignUp.p==0):
                    print("\nYou Should Be Older than 18 years.")
                    self.age = input("\tEnter Your Age: ")
                    self.checkAge()
                    if(SignUp.a==0):                        
                        SignUp.OTP= SignUp.generateOTP()
                        self.sendOTP()                        
                        self.emailVerification()
                        if(SignUp.v==0):
                            self.appendDetails()
                            if(SignUp.d==0):
                                print(f"Account Created Successfully...Welcome To The Community {self.name}")
                                 
        
    def checkUsrNameAvb(self):
        uname = self.usrname
        if(uname == '' or uname.isspace()==True):
                print("User Name should not Blank...")
                self.usrin()
        for index,item in Login.df.iterrows():
            if(uname==item['UserName']):
                print("User Name already exist Login or Try another User Name...")
                self.usrin()
                self.checkUsrNameAvb() 
        if len(uname)<=12 and len(uname)>=8:
            SignUp.u=0
        else:
            print("Max Length = 12 characters and Min Length = 8 characters")
            self.usrin()
            self.checkUsrNameAvb()
        
        if uname.isalnum()==True and uname.isprintable()==True and uname.isalpha()==False and uname.isnumeric()==False:
            SignUp.u=0
        else:
            print("Should Contain Alphabets and Numericals Both...")
            self.usrin()
            self.checkUsrNameAvb()
        
    def emailin(self):
        self.email = input("Enter Email Id again: ")

    def checkEmailAvb(self):
        eid = self.email
        if(eid == '' or eid.isspace()==True):
                print("Email Id is Mandatory...")
                self.emailin()
        else:
            SignUp.e = 0
            
        if('@' and '.' not in eid):
            print("Enter Valid Email Id...")
            self.emailin()
        else:
            SignUp.e=0
        for index,item in Login.df.iterrows():
            if(eid==item['Email']):
                print("Email Id already in use. Try using different Id...")
                self.emailin()
                self.checkEmailAvb()
            else:
                SignUp.e=0

    def checkPSWDAvb(self):
        psd = self.pswd
        
        if (('@'or'#'or'$' in psd==True) and len(psd)>=8 and len(psd)<=16 and psd.isspace()==False and psd!='' and psd.isprintable()==True and psd.isalpha()==False and psd.isnumeric()==False):
            SignUp.p=0
        else:
            SignUp.pswdIns()
            self.pswdin()
            self.checkPSWDAvb()
    
    def checkAge(self):
        ag = self.age
        if(ag==''):
            print("Age is Mandatory...")
            self.agein()                
        
        if(int(ag)<18):
            print("You are Too Young...Sorry.")
            print("You should wait for Some Time...Thanks for Playing.")
            exit(0)        

        if(int(ag)>=80):
            print("You are Too Old...Sorry")
            exit(0)
        SignUp.a=0
        
        
    def agein(self):
        self.age = input("\tEnter Valid Age: ")
    
    @staticmethod
    def generateOTP():
        otp = ''          
        for i in range(6):
            otp = otp + SignUp.random.choice(SignUp.random.choice(SignUp.string.digits))    
        return otp

    def emailVerification(self):
        self.usrOTP = input(f"Enter OTP sent on Email ID {self.email}: ")
        uOTP = self.usrOTP
        if(SignUp.OTP==uOTP):
            SignUp.v=0
            print("Email ID Verified...")
        else:
            print("Incorrect OTP...Try Later...")
            exit(0)
        

    def sendOTP(self):        
        try:
            srv = SignUp.smtplib.SMTP('smtp.gmail.com',587)
            srv.starttls()
            srv.login(SignUp.myid,SignUp.mypass)
            print("Sending OTP...Please Wait\n")
            srv.sendmail(SignUp.myid,self.email,f"Subject: One Time Password\n\nHi {self.name},\n\tYour One Time Password for User Name: {self.usrname} is: {SignUp.OTP}.\nThanks,\nFrom Team Dark.")
            srv.quit()
            print(f"OTP sent Succesfully on Email ID {self.email}. Please Verify Your Email ID to Proceed...")
            sent = 0
        except Exception as e:
            sent = -1
            print("An Unexpected Error occured...Please Try Signing Up Later...")
            print("Thank You..")
            exit(0)
        
    def appendDetails(self):
        try:
            Login.srno +=1
            SignUp.ndf = Login.pd.DataFrame({'Srno':[str(SignUp.srno)],
                'UserName':[self.usrname],
                'Name':[self.name],'Email':[self.email],'Age':[str(self.age)],'Password':[self.pswd]})
            frames = [Login.df,SignUp.ndf]
            Login.df = Login.pd.concat(frames)
            Login.df.to_excel('data.xlsx',index=False)
            SignUp.d = 0
        except Exception as e:
            d = -1
            print("Some Unexpected error occured Creating Your Account...\nSorry try again later...")
            # print(e)
    
if __name__=="__main__":
    usr2 = SignUp()
    