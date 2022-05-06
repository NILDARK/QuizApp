from tkinter import *
from tkinter import messagebox
root = Tk()
e = Entry(root,show='*')
s=''
def click():
    global s
    s=e.get()
e.pack()
# b= Button(text='click',command=click).pack()
# res=messagebox.askyesno("snldf","anfln")
# e.pack()
Label1 = Label(text='''**Password Should Contain Following: \n
        ~ Length should be 8 characters to 16 characters.
        ~ Should not blank or space.
        ~ Should Contain atleast one Symbols (@,#,$).
        ~ Should conatin at least one Alphabet and Digit.''').pack()
res = IntVar()

# newframe = Frame(root)
# newframe.pack()
# l1 = Label(newframe,text="agsf;sj").pack()
root.mainloop()