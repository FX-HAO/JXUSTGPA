#!/usr/bin/env python



from tkinter import *
from py.custom.crawlerJXUST import GPA
from tkinter import ttk

class GUIGPA(object):
    def __init__(self,initdir=None):
        self.root=Tk()
        self.root.title('Student GPA')
        tip=Label(self.root,text='Please enter ur student number and password!')
        tip.pack()

        self.snofm=Frame(self.root)
        self.snolabel=Label(self.snofm,text='Sno: ')
        self.sno=StringVar(self.snofm)
        self.snolabel.pack(side=LEFT)
        self.snoarea = Entry(self.snofm, width=20,textvariable=self.sno)
        self.snoarea.pack(side=RIGHT)
        self.snofm.pack()

        self.pwdfm=Frame(self.root)
        self.pwdlabel=Label(self.pwdfm,text='Pwd: ')
        self.pwdlabel.pack(side=LEFT)
        self.pwd=StringVar(self.pwdfm)
        self.pwdarea=Entry(self.pwdfm,width=20,textvariable=self.pwd)
        self.pwdarea.pack(side=RIGHT)
        self.pwdarea.bind("<Return>",self.enter)
        self.pwdfm.pack()
        
        self.submit=Button(self.root,text='submit',command=self.getGPA,bg='black',fg='red')
        self.submit.bind("<Return>", self.enter)
        self.submit.pack(expand=1)
        
        self.root.mainloop()
    
    def enter(self,event):
        #self.getGPA()
        self.submit.invoke()

    def getGPA(self):
        if hasattr(self,'info'):
            self.info.destroy()
        student=GPA(self.sno.get(),self.pwd.get())
        student.getGPA()
        self.result=student.result
        self.GPA=student.GPA
        if self.result == 'Incorrect username or password.':
            self.info=Frame(self.root)
            label=Label(self.info,text=self.result)
            label.pack()
            self.info.pack()
        else:
            self.treeview=ttk.Treeview(self.root)
            self.treeview['columns']=('second','third','fourth')
            self.treeview.column('second',width=100,anchor="center")
            self.treeview.column('third',width=100,anchor="center")
            self.treeview.column('fourth',width=100,anchor="center")
            self.treeview.heading("second",text="学分")
            self.treeview.heading("third",text="绩点")
            self.treeview.heading("fourth",text="成绩")
            scrollbar=ttk.Scrollbar(self.treeview,orient='vertical',command=self.treeview.yview)
            self.treeview.configure(yscroll=scrollbar)
            self.treeview.pack()
            self.treeview.insert('',"end",text='平均学分绩点',values=('',self.GPA,''))
            for eachLine in self.result:
                if eachLine == self.result[0]:
                    continue
                self.treeview.insert('',"end",text=eachLine[3],values=(eachLine[6],eachLine[7],eachLine[8]))

if __name__ == '__main__':
    GUIGPA()
