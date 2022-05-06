from tkinter import *
from tkinter import messagebox
from functools import partial
import smtplib
import random
import string
import creds
import mysql.connector
import time
import threading


class Database:
    def __init__(self, root):
        try:
            self.db = mysql.connector.connect(
                user='', password='', host="", database="") # enter database details here
            self.cur = self.db.cursor()
        except:
            messagebox.showerror(
                "Error", "Server Not Reachable. Please Try Again Later.")
            root.quit()

    def disconnectDB(self):
        self.db.close()

    def insertToRegisteredClients(self, values):
        try:
            self.cur.execute(
                f"""INSERT INTO registeredClients VALUES('{values[0]}','{values[1]}','{values[2]}','{values[3]}','{values[4]}',curdate())""")
            self.db.commit()
            messagebox.showinfo("Success", "Registered Successfully.")
        except Exception as e:
            messagebox.showerror("Error", "Something Went Wrong.")
            print(e)

    def getPassword(self, username):
        try:
            self.cur.execute(
                f"""SELECT client_password from registeredClients WHERE username = '{username}'""")
            res = self.cur.fetchone()
            res = res[0]
            return str(res)
        except:
            return "-1"

    def getEmail(self, email):
        try:
            self.cur.execute(
                f"""SELECT client_email from registeredClients WHERE client_email = '{email}'""")
            res = self.cur.fetchone()
            res = res[0]
            return str(res)
        except:
            return "-1"

    def getUsername(self, username):
        try:
            self.cur.execute(
                f"""SELECT username from registeredClients WHERE username = '{username}'""")
            res = self.cur.fetchone()
            res = res[0]
            return str(res)
        except:
            return "-1"

    def logEntry(self, username):
        try:
            self.cur.execute(
                f"""INSERT INTO logtable(username,datetimeOfLogin,datetimeOfSigningOut) VALUES('{username}',current_timestamp(),NULL)""")
            self.db.commit()
        except Exception as e:
            print(e)

    def logExit(self, username):
        try:
            self.cur.execute(
                f"""UPDATE logtable SET datetimeOfSigningOut = current_timestamp() WHERE username = '{username}' and ISNULL(datetimeOfSigningOut)""")
            self.db.commit()
        except Exception as e:
            print(e)

    def getQIds(self):
        self.cur.execute(f"""SELECT COUNT(qId) FROM Questions""")
        cnts = self.cur.fetchone()
        cnts = cnts[0]
        return [i for i in range(1, cnts+1)]

    def getQuestion(self, qId):
        self.cur.execute(f"""SELECT que FROM Questions WHERE qId={qId}""")
        que = self.cur.fetchone()
        return que[0]

    def getOpts(self, qId):
        opts = []
        for i in range(1, 5):
            self.cur.execute(
                f"""SELECT opt_id{i},opt{i} FROM Questions WHERE qId={qId}""")
            opts.append(self.cur.fetchone())
        return opts

    def getAnsId(self, qId):
        self.cur.execute(f"""SELECT ans_id FROM Questions WHERE qId={qId}""")
        ansId = self.cur.fetchone()
        return ansId[0]

    def pushScoreDetails(self, username, score):
        self.cur.execute(
            f"""INSERT INTO Student_Scores(username,score,timeStampOfAttempt) VALUES('{username}',{score},current_timestamp())""")
        self.db.commit()


username = ''
root = Tk()
root.title("Quiz")
db = Database(root)
quizInstFrame = Frame(root)
instructLabel = Label(quizInstFrame, text="""**Instructions For Quiz: \n
        \t~1. There will be total of 10 questions.\n
        \t~2. All questions are mandatory to attempt.\n
        \t~3. You can view one question at a time.\n
        \t~4. You will be given 4 choices. Select appropriate.\n
        \t~5. You can toggle questions to and fro from below toggle palete.Moreover you can direct\n
        \t\ttoggle to any question\n
        \t~6. After selecting every option you have to confirm your selection by clicking "Confirm".\n
        \t~7. To qualify quiz you have to attempt 7 questions correctly.\n
        """)
        
class Quiz:
    qIds = db.getQIds()
    response = {}
    random.shuffle(qIds)
    timerStat = None
    actQue = 1
    timeFrame = Frame(root)
    hrs, mins, secs = StringVar(), StringVar(), StringVar()
    timerHrs = Label(timeFrame, textvariable=hrs)
    timerMins = Label(timeFrame, textvariable=mins)
    timerSecs = Label(timeFrame, textvariable=secs)
    questionFrame = Frame(root)
    curr_time = Label(timeFrame, font='arial 15 bold',
                      text='', fg='gray25', bg='papaya whip')
    

    def __init__(self, username):
        self.client = username    

    def drawQuestion(self, qId):
        queSet = []
        queText = db.getQuestion(qId)
        queOpts = db.getOpts(qId)
        queSet.append(queText)
        queSet.append(queOpts)
        return queSet

    def checkAnswers(self):
        score = 0
        for id, resp in Quiz.response.items():
            if(resp == db.getAnsId(id)):
                score += 1
        return score

    def submitquiz(self):
        res = messagebox.askyesno("Confirmation", "Confirm to submit quiz.")
        if(res == 1):
            Quiz.questionFrame.destroy()
            Quiz.timerStat = False
            score = self.checkAnswers()
            db.pushScoreDetails(self.client, score)
            resultLabel = Label(root, text=f"Your Score is {score}.")
            resultLabel.grid()
            root.after(5000, root.quit)
        else:
            return

    def submitForce(self):
        for qId in Quiz.qIds:
            if(qId not in Quiz.response):
                Quiz.response[qId] = -1
        score = self.checkAnswers()
        db.pushScoreDetails(self.client,score)
        resultLabel = Label(root, text=f"Your Score is {score}.")
        resultLabel.grid()
        root.after(5000, root.quit)

    def confirm(self, resp, qId, qframe):
        if(resp.get() == 0):
            messagebox.showwarning("Warning!", "Select One Option.")
            return
        Quiz.response[qId] = resp.get()
        if(len(Quiz.response) == len(Quiz.qIds)):
            submitQuiz = Button(
                Quiz.questionFrame, text="Submit Quiz", command=partial(self.submitquiz))
            submitQuiz.grid(row=1,column=0)
        self.nextQue(qframe)
        return None

    def showQuestion(self, qId):
        qframe = Frame(Quiz.questionFrame)
        qframe.grid(row=0,column=0)
        queSet = self.drawQuestion(qId)
        random.shuffle(queSet[1])
        opts = queSet[1]
        resp = IntVar()
        queTextLabel = Label(qframe, text=queSet[0])
        queTextLabel.config(width=50)
        queTextLabel.grid(row=0,column=0)
        opt1 = Radiobutton(
            qframe, text=opts[0][1], variable=resp, value=opts[0][0],width=40)
        opt2 = Radiobutton(
            qframe, text=opts[1][1], variable=resp, value=opts[1][0],width=40)
        opt3 = Radiobutton(
            qframe, text=opts[2][1], variable=resp, value=opts[2][0],width=40)
        opt4 = Radiobutton(
            qframe, text=opts[3][1], variable=resp, value=opts[3][0],width=40)
        opt1.grid(row=1,column=0)
        opt2.grid(row=1,column=1)
        opt3.grid(row=2,column=0)
        opt4.grid(row=2,column=1)
        nextButton = Button(qframe, text="Next Question",width=20,
                            command=partial(self.nextQue, qframe))
        nextButton.grid(row=3,column=1)
        prevButton = Button(qframe, text="Previous Question",width=20,
                            command=partial(self.prevQue, qframe))
        prevButton.grid(row=3,column=0)
        confrm = Button(qframe, text="Confirm",width=20, command=partial(
            self.confirm, resp, qId, qframe))
        confrm.grid(row=3,column=2)

    def nextQue(self, qframe):
        if(Quiz.actQue < len(Quiz.qIds)):
            qframe.destroy()
            Quiz.actQue += 1
            self.showQuestion(Quiz.qIds[Quiz.actQue-1])
        else:
            return
        return Quiz.actQue

    def prevQue(self, qframe):
        if(Quiz.actQue > 1):
            qframe.destroy()
            Quiz.actQue -= 1
            self.showQuestion(Quiz.qIds[Quiz.actQue-1])
        else:
            return

    def startQuiz(self):
        quizInstFrame.destroy()
        Quiz.questionFrame.grid(row=2,column=0,columnspan=3)
        Quiz.hrs.set('00')
        Quiz.mins.set('00')
        Quiz.secs.set('00')
        Quiz.timeFrame.grid(row=1,column=2)
        Quiz.curr_time.grid(row=0,column=1)
        self.clock()
        Quiz.timerStat = True
        self.timerHrs.config(width=6)
        self.timerMins.config(width=6)
        self.timerSecs.config(width=6)
        self.timerHrs.grid(row=0,column=2)
        self.timerMins.grid(row=0,column=3)
        self.timerSecs.grid(row=0,column=4)
        t1 = threading.Thread(target=self.countdown)
        t2 = threading.Thread(target=self.showQuestion,
                              args=(Quiz.qIds[Quiz.actQue-1],))
        t1.start()
        t2.start()

    def clock(self):
        clock_time = time.strftime('%H:%M:%S %p')
        Quiz.curr_time.config(text=clock_time)
        Quiz.curr_time.after(1000, self.clock)

    def countdown(self):
        times = 300
        while times > -1 and Quiz.timerStat == True:
            minute, second = (times // 60, times % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)
            second = f"{second:02d} sec"
            minute = f"{minute:02d} min"
            hour = f"{hour:02d} hr"
            Quiz.secs.set(second)
            Quiz.mins.set(minute)
            Quiz.hrs.set(hour)
            try:
                Quiz.timeFrame.update()
            except:
                pass
            time.sleep(1)
            if(times == 0):
                messagebox.showwarning("Timer Warning", "Time Up.")
                self.submitForce()
                Quiz.secs.set('00')
                Quiz.mins.set('00')
                Quiz.hrs.set('00')

            times -= 1


class Login:
    login = False
    usrname = ''
    name = ''
    age = ''
    email = ''

    def __init__(self, usrName, usrPass):
        if(True):
            self.usrname = usrName
            self.pswd = usrPass
            self.check()
        else:
            Login.login = False

    def check(self):
        if(db.getUsername(self.usrname) == self.usrname and self.pswd == db.getPassword(self.usrname)):
            Login.login = True
            ch = 0
            return
        else:
            Login.login = False


def loginProcess():
    loginFrame = Frame(root)
    signUpFrame = Frame(root)
    loginFrame.grid()
    loginStatus = Login.login
    usrNameLabel = Label(
        loginFrame, text="Enter User Name:").grid(row=0, column=0)
    eUsrName = Entry(loginFrame)
    eUsrName.grid(row=0, column=1)
    usrPassLabel = Label(
        loginFrame, text="Enter Password:").grid(row=1, column=0)
    eUsrPass = Entry(loginFrame, show="*")
    eUsrPass.grid(row=1, column=1)
    usrName, usrPass = '', ''

    class SignUp():
        sent = 1
        OTP = ''
        emailVerified = 0

        @staticmethod
        def pswdIns():
            pswdIns = Label(signUpFrame, text='''**Password Should Contain Following: \n
            ~ Length should be 8 characters to 16 characters.
            ~ Should not blank or space.
            ~ Should Contain atleast one Symbols (@,#,$).
            ~ Should conatin at least one Alphabet and Digit.''').grid()

        @staticmethod
        def usrnameIns():
            usrNameIns = Label(signUpFrame, text='''**User Name Should Contain Following: \n
            ~ Should not blank or space.
            ~ Length should be 8 characters to 12 characters.
            ~ Should not Contain any Symbols.
            ~ Should conatin at least one Alphabet and Digit.''').grid()

        def __init__(self):
            nameLabel = Label(signUpFrame, text="Enter Your Good Name:").grid(
                row=0, column=0)
            self.nameEntry = Entry(signUpFrame)
            self.nameEntry.grid()
            self.name = self.nameEntry.get()
            SignUp.usrnameIns()
            usrnameLabel = Label(
                signUpFrame, text="Enter Your User Name:")
            self.usrnameEntry = Entry(signUpFrame)
            self.usrnameEntry.grid()

            emailEntryLabel = Label(
                signUpFrame, text="Enter Your Email:").grid()
            self.emailEntry = Entry(signUpFrame)
            self.emailEntry.grid()
            SignUp.pswdIns()
            pswdEntryLabel = Label(
                signUpFrame, text="Enter New Password:").grid()
            self.pswdEntry = Entry(signUpFrame, show="*")
            self.pswdEntry.grid()
            ageEntryLabel = Label(
                signUpFrame, text="Enter your Age:").grid()
            self.ageEntry = Entry(signUpFrame)
            self.ageEntry.grid()
            submitButton = Button(
                signUpFrame, text="Sign Up", command=self.submit)
            submitButton.grid()

        def submit(self):
            self.checkUsrNameAvb()
            self.checkPSWDAvb()
            self.checkEmailAvb()
            self.checkAge()
            if(self.checkedAge and self.checkedEmailId and self.checkedPswd and self.checkedUsrName):
                SignUp.OTP = SignUp.generateOTP()
                self.sendOTP()
                self.emailVerification()
            elif(self.checkedAge == '-1' or self.checkedEmailId == '-1' or self.checkedUsrName == "-1"):
                messagebox.showinfo("Error", "All Fields are Mandatory.")
                return
            else:
                return

        def checkUsrNameAvb(self):
            self.checkedUsrName = 0
            uname = self.usrnameEntry.get()
            self.newUsrName = uname
            if(uname == '' or uname.isspace() == True):
                self.usrnameEntry.delete(0, END)
                self.checkedUsrName = 0
                return '-1'
            if(uname == db.getUsername(uname)):
                messagebox.showerror("Error", "User Name already exist.")
                self.usrnameEntry.delete(0, END)
                self.checkedUsrName = 0
                return
            if len(uname) <= 12 and len(uname) >= 8:
                pass
            else:
                messagebox.showerror(
                    "Error", "Length of User Name should be 8-12.")
                self.usrnameEntry.delete(0, END)
                self.checkedUsrName = 0
                return
            if uname.isalnum() == True and uname.isprintable() == True and uname.isalpha() == False and uname.isnumeric() == False:
                pass
            else:
                messagebox.showerror(
                    "Error", "User Name should contain both Alphabets and digits.")
                return
            self.checkedUsrName = 1

        def checkEmailAvb(self):
            eid = self.emailEntry.get()
            self.email = eid
            self.checkedEmailId = 0
            if(eid == '' or eid.isspace() == True):
                self.emailEntry.delete(0, END)
                return '-1'
            if('@' and '.' not in eid):
                messagebox.showerror("Error", "Email Id is Invalid.")
                self.emailEntry.delete(0, END)
                return
            if(eid == db.getEmail(self.usrnameEntry.get())):
                messagebox.showerror(
                    "Error", "Email Id already in use. Try using different Id.")
                self.emailEntry.delete(0, END)
                return
            self.checkedEmailId = 1

        def checkPSWDAvb(self):
            self.checkedPswd = 0
            psd = self.pswdEntry.get()
            self.pswd = psd
            if (('@' or '#' or '$' in psd == True) and len(psd) >= 8 and len(psd) <= 16 and psd.isspace() == False and psd != '' and psd.isprintable() == True and psd.isalpha() == False and psd.isnumeric() == False):
                pass
            else:
                messagebox.showerror("Error", "Invalid Password String.")
                self.pswdEntry.delete(0, END)
                return
            self.checkedPswd = 1

        def checkAge(self):
            self.checkedAge = 0
            ag = self.ageEntry.get()
            self.age = ag
            if(ag == ''):
                self.ageEntry.delete(0, END)
                return '-1'
            if((int(ag) < 18) or (int(ag) >= 80)):
                messagebox.showerror("Error", "Age Limit does not Match.")
                self.ageEntry.delete(0, END)
                return
            self.checkedAge = 1

        @staticmethod
        def generateOTP():
            otp = ''
            for i in range(6):
                otp = otp + random.choice(random.choice(string.digits))
            return otp

        def emailVerification(self):
            self.emailVerificationFrame = Frame(signUpFrame)
            self.emailVerificationFrame.grid()
            OTPLabel = Label(self.emailVerificationFrame,
                             text="Enter OTP: ").grid()
            self.OTPEntry = Entry(self.emailVerificationFrame, show="*")
            self.OTPEntry.grid()
            uOTP = self.OTPEntry.get()
            OTPCheckButton = Button(
                self.emailVerificationFrame, text="Submit OTP", command=self.OTPcheck)
            OTPCheckButton.grid()

        def OTPcheck(self):
            if(SignUp.OTP != self.OTPEntry.get()):
                res = messagebox.showerror(
                    "Error", "Incorrect OTP. Try Again.")
                SignUp.emailVerified = 0
                self.emailVerificationFrame.destroy()
                return
            res = messagebox.showinfo("Success", "Email Verified.")
            self.appendDetails()
            SignUp.emailVerified = 1
            self.emailVerificationFrame.destroy()

        def sendOTP(self):
            try:
                srv = smtplib.SMTP('smtp.gmail.com', 587)
                srv.starttls()
                srv.login(creds.myid, creds.mypass)
                srv.sendmail(
                    creds.myid, self.email, f"Subject: One Time Password\n\nHi {self.nameEntry.get()},\n\tYour One Time Password for User Name: {self.newUsrName} is: {SignUp.OTP}.\nThanks,\nFrom Team Dark.")
                srv.quit()
                messagebox.showinfo(
                    "Success", f"OTP sent Succesfully on Email ID {self.email}. Please Verify Your Email ID to Proceed.")
                self.sentOTP = 1
            except Exception as e:
                print(e)
                self.sentOTP = 0
                messagebox.showerror(
                    "Error", f"Unexpected Error Occured, try again later.")
                return

        def appendDetails(self):
            details = []
            name = self.nameEntry.get()
            details.append(self.newUsrName)
            details.append(str(name))
            details.append(self.pswd)
            details.append(self.email)
            details.append(self.age)
            db.insertToRegisteredClients(details)
            signUpFrame.destroy()
            loginProcess()

    def loginCred(signup=False):
        if not signup:
            global username
            usrName = eUsrName.get()
            usrPass = eUsrPass.get()
            eUsrName.delete(0, END)
            eUsrPass.delete(0, END)
            l = Login(usrName, usrPass)
            loginStatus = Login.login
            if(Login.login is True):
                messagebox.showinfo("Login Status", "Login Successful!")
                db.logEntry(usrName)
                loginFrame.destroy()
                quizInstFrame.grid(row=0,column=0)
                q = Quiz(usrName)
                instructLabel.grid(column=0, row=0)
                startButton = Button(
                    quizInstFrame, text="Start Quiz", command=q.startQuiz)
                startButton.grid(column=0,row=1)
                username = usrName
            else:
                res = messagebox.askyesno(
                    "Login Status", "Login Unsuccessful!\n Do you want to Sign Up?")
                if(res == 0):
                    root.quit()
                else:
                    loginFrame.destroy()
                    signUpFrame.grid()
                    newEntry = SignUp()
        else:
            loginFrame.destroy()
            signUpFrame.grid()
            new = SignUp()
    loginCred_button = Button(loginFrame, text="Login", command=partial(
        loginCred, False)).grid(row=2, column=0)
    signUpButton = Button(loginFrame, text="Sign Up", command=partial(
        loginCred, True)).grid(row=2, column=1)


loginProcess()
root.mainloop(n=0)
Login.login = False
db.logExit(username)
