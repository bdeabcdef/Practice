'''
Add Data Code development for Data Insertion
'''
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
import pymssql
#import pymongo
#import sqlite3 as sl
#import pymongo
import pandas as pd
#import pymssql
import os
import pyodbc
from tkinter import filedialog as fd
#from sqlalchemy import create_engine 
from configurations import *


class AddData:

    

    def __init__(self, root):
        self.root = root
        
        self._geom='600x400+0+0'
        self.root.geometry("{0}x{1}+0+0"
                        .format(root.winfo_screenwidth()-20,
                                root.winfo_screenheight()))        
#        self.create_dbgui()
        self.db_filename = '../secured/connections1.db'
        self.tables = []
        
    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            self.query_result = cursor.execute(query, parameters)
            conn.commit()
        return self.query_result

    def create_pcgui(self):
         path = fd.askopenfilename(filetypes=[("Csv files","*.csv")])
         if path:
             self.results = pd.read_csv(path,encoding="ISO-8859-1")
             self.display_table(self.results)

    def create_dbgui(self):
#        self.create_left_icon()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_bottom_buttons()
        self.view_records()
        

    def create_left_icon(self):
        self.labelframe0 = LabelFrame(self.root)
        self.labelframe0.grid(row=0, column=0, padx=5, pady=5,sticky='W')        
        self.photo = PhotoImage(file=frame_images+'database.gif')
        self.photo_label = Label(self.root,image=self.photo)
        self.photo_label.image = self.photo
        self.photo_label.grid(row=0, column=0,sticky='NW')  
	
    def get_data(self,event):
        self.var = self.connections_display.focus()
        self.name = [self.connections_display.item(self.var).get('values')]
        #print(self.name)
#        self.connection_name_var=self.name.get('values')[1]
#        print(self.connection_name_var)
        '''self.database_type_var=self.name.get('values')[1]
        self.host_var=self.name.get('values')[2]
        self.port_var=self.name.get('values')[3]
        self.schema_var=self.name.get('values')[4]
        self.user_var=self.name.get('values')[5]
        self.pwd_var=self.name.get('values')[6]
        self.url_var=self.name.get('values')[7]
        self.database_name_var=self.name.get('values')[8]
 '''   
    
    def get_current(self):
        self.curr = self.connections_display.focus()
        self.val = self.connections_display.item(self.curr)
        self.det = self.val.get('values')
        #print(self.det)
        return self.det
	
    
    def connect_in(self):
        self.val = self.get_current()
        if self.val[1] == 'MySQL':
            self.host = self.val[2]
            self.user = self.val[5]
            self.passwd = str(self.val[6])
            self.dbname = self.val[4]
            print('host={0}\n user={1} \n passwd={2} \n dbname={3}'.format(host,user,passwd,dbname))
            self.db = pymysql.connect(host=host,user=user,passwd=passwd,db=dbname)
            self.c = self.db.cursor()            
            self.query ='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\' AND TABLE_SCHEMA=\'{}\';'.format(dbname)
            print(self.host,self.user,self.passwd,self.dbname)            
            print('connected')
            
        elif self.val[1] == 'SqlServer':
            self.host = self.val[2]
            self.user = self.val[5]
            self.passwd = self.val[6]
            self.dbname = self.val[4]
            #self.db = create_engine('mssql+pyodbc://'+self.user+':'+self.passwd+'@'+self.host+'/'+self.dbname+'?driver=SQL+Server+Native+Client+11.0?trusted_connection=yes')                        
            #print(self.db)            
            self.query ='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\';'
            self.res = self.db.execute(self.query)
            print(self.host,self.user,self.passwd,self.dbname)            
            print('connected')
        else:
            self.query ='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\';'            
            
           # if self.val[1] == 'SqlServer':
            self.DSN = self.val[2]
            self.temp='DSN='+self.DSN
            self.dsn_connection = pyodbc.connect(self.temp)
            self.cursor = self.dsn_connection.cursor()
            self.message['text'] ='Connected to the '+self.temp                        
            #cursor.tables()
            self.cursor.execute(self.query)
            self.results = self.cursor.fetchall()
            
            self.tables[:] = []
            for r in self.results:
                self.tables.append(r[0])
        self.afterconnectGui()    
    
    def afterconnectGui(self):
        self.connectwindow = tk.Toplevel()
        
        self.table_frame = tk.LabelFrame(self.connectwindow, text = 'Tables',font=('cambria',14))
        self.attr_frame = tk.LabelFrame(self.connectwindow, text = 'Attributes',font=('cambria',14))
        self.query_frame = tk.LabelFrame(self.connectwindow, text = 'SQL Query',font=('cambria',14),height=10)
        self.submit_frame = tk.LabelFrame(self.connectwindow, text = 'Take Actions',font=('cambria',14))
############## Creating Listboxes, scrollbar and Text-pad ##############
        self.table_list = tk.Listbox(self.table_frame, width = 50,font=('cambria',12))
        self.fillTableList() 
        self.table_list.bind('<ButtonPress-1>', self.fillAttrList)
        self.attr_list = tk.Listbox(self.attr_frame, width = 50,font=('cambria',12))
        self.text_pad = tk.Text(self.query_frame,fg = 'blue',font=('cambria',12),height=10,width=100)
        self.next_button = tk.Button(self.submit_frame, text = 'Run Query',width=20,font=('cambria',14), command = self.onSubmitQuery)
        self.save_button = tk.Button(self.submit_frame, text = 'Save Object',width=20,font=('cambria',14))
################### Closing the Widgets #########################
        self.table_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
        self.attr_frame.grid(row = 0, column = 1, padx = 5, pady = 5,sticky = 'E')
        self.query_frame.grid(row = 1,column=0,columnspan=2,padx = 5, pady = 5)
        self.submit_frame.grid(row = 2,column=0,columnspan=2,padx = 5, pady = 5)        
        self.table_list.grid(row = 0, pady = 5)
        self.attr_list.grid(row = 0,column=0, pady = 5)
        self.text_pad.grid(row = 0, column=0,columnspan=2,padx = 5)
        self.next_button.grid(row = 2, column = 0,pady=5,padx=10)
        #self.save_button.grid(row = 2, column = 1,pady=5,padx=10)   
    
    def fillTableList(self):
        self.result = self.tables
        for r in self.result:
            self.table_list.insert(tk.END , r)
            return self.result
    def fillAttrList(self,event):
#		table = self.table_list.get(self.table_list.curselection())
        table = self.table_list.get(self.table_list.nearest(event.y))
        print(table)
        self.attr_list.delete(0, tk.END)
        if self.val[1] == 'MySQL':
            self.table_query = 'Show columns from {}'.format(table)
        elif self.val[1] == 'MSSQL':
            self.table_query = 'SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(\'{}\')'.format(table)
        else:     
            self.table_query = 'SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(\'{}\')'.format(table)
        self.cursor.execute(self.table_query)
        self.tab = self.cursor.fetchall()
        for t in self.tab:
            self.attr_list.insert(1, t[0])
    
    def onSubmitQuery(self):
        self.sub_query = self.text_pad.get('1.0',tk.END)
        self.df_query=pd.read_sql(self.sub_query,self.dsn_connection)
#        print(self.df_query)
        self.display_table(self.df_query)
	
    
    def on_connect_button_clicked(self):
        self.message['text'] = ''
        try:
            self.connections_display
        except IndexError as e:
            self.message['text'] = 'No item selected to connect'
            return
        self.connect_in()
        
        #self.connect()
    

    #def connect(self,*args):
     #   pass        
        '''self.database_type  =        
        self.host = self.host_var.get()        
        self.username = self.username_var.get()
        self.password = self.password_var.get()
        self.db_name  = 
        '''
    
    
    
    
    def create_label_frame(self):
        #self.create_left_icon()	
        self.labelframe = LabelFrame(self.root, text='Create New Connection',font=('cambria',14))
        self.labelframe.grid(row=0, padx=2, pady=2,sticky='E')
        
        self.connection_Label=Label(self.labelframe, text='Connection Name',font=('cambria',11))
        self.connection_Label.grid(row=0, column=1, sticky=W, padx=2,pady=2)
        self.connection_entry = Entry(self.labelframe,font=('cambria',11))
        self.connection_entry.grid(row=0, column=2, sticky=W, padx=2, pady=2)
        
        self.database_label=Label(self.labelframe, text='Select Database',font=('cambria',11))
        self.database_label.grid(row=2, column=1, sticky=W,  pady=1)
        self.database_entry=Listbox(self.labelframe,height=6,font=('cambria',11))
        for line in ['MySql','SqlServer','DSN']:
            #'PostgresSql','HSQLDB','ODBC','Sybase','Oracle','Db2'
            self.database_entry.insert(END,line)    
        self.database_entry.grid(row=2,column=2,padx=2,pady=10,sticky='W')
        #self.temp_var=self.database_name.selection_get()
        #print(self.temp_var)

        self.host_label=Label(self.labelframe,text='Host/DSN',font=('cambria',11))
        self.host_label.grid(row=3,column=1,padx=2,pady=2,sticky='W')
        self.host_entry=Entry(self.labelframe,font=('cambria',11))
        self.host_entry.grid(row=3,column=2,padx=2,pady=2,sticky='W')
        
        self.port_label=Label(self.labelframe,text='Port',font=('cambria',11))
        self.port_label.grid(row=4,column=1,padx=2,pady=2,sticky='W')
        self.port_entry=Entry(self.labelframe,font=('cambria',11))
        self.port_entry.grid(row=4,column=2,padx=2,pady=2,sticky='W')

        self.schema_label=Label(self.labelframe,text='schema',font=('cambria',11))
        self.schema_label.grid(row=5,column=1,padx=2,pady=2,sticky='W')
        self.schema_entry=Entry(self.labelframe,font=('cambria',11))
        self.schema_entry.grid(row=5,column=2,padx=2,pady=2,sticky='W')
        
        self.username_label=Label(self.labelframe,text='Username',font=('cambria',11))
        self.username_label.grid(row=6,column=1,padx=2,pady=2,sticky='W')
        self.username_entry=Entry(self.labelframe,font=('cambria',11))
        self.username_entry.grid(row=6,column=2,padx=2,pady=2,sticky='W')
        
        self.password_label=Label(self.labelframe,text='Password',font=('cambria',11))
        self.password_label.grid(row=7,column=1,padx=2,pady=2,sticky='W')
        self.password_entry=Entry(self.labelframe,font=('cambria',11))
        self.password_entry.grid(row=7,column=2,padx=2,pady=2,sticky='W')
        
        #if self.database_entry.get() == 'Oracle':
		#self.temp_variable = self.username_entry.get()||' / '|| self.password_entry.get()||'@'||self.host_entry.get()||'/'||self.self.database_name_entry()
        self.url_label=Message(self.labelframe,text='URL',font=('cambria',11))
        self.url_label.grid(row=8,column=1,padx=2,pady=2,sticky='W')
        self.url_name=Entry(self.labelframe,font=('cambria',11),width=120)
        self.url_name.config(state = 'disabled')
        self.url_name.grid(row=8,column=2,padx=2,pady=2)
        
        self.database_name_label=Label(self.labelframe,text='Database Name',font=('cambria',11))
        self.database_name_label.grid(row=9,column=1,padx=2,pady=2,sticky='W')
        self.database_name_entry=Entry(self.labelframe,font=('cambria',11))
        self.database_name_entry.grid(row=9,column=2,padx=2,pady=2,sticky='W')        
        
        self.add_record=Button(self.labelframe, text='Add Record', command=self.on_add_record_button_clicked,font=('cambria',16),width=15)
        self.add_record.grid(row=10, column=2, sticky='W', padx=5, pady=10)

    def create_message_area(self):
        self.message = Label(self.root,text='', fg='red',font=('cambria',16))
        self.message.grid(row=1,sticky='WE')

    def create_tree_view(self):
        self.Labelframe2=LabelFrame(self.root,text="Available Connections",width=100,font=('cambria',14))
        self.Labelframe2.grid(row=2,column=0,padx=2,pady=2)
        self.connections_display= ttk.Treeview(self.Labelframe2,height=3,selectmode="extended", columns=('one','two','three','four','five','six','seven','eight','nine'))
        
        self.connections_display.heading('#01', text='Name', anchor=W)
        self.connections_display.column('one',minwidth=0,width=120)
        self.connections_display.heading('#02', text='Database System', anchor=W)
        self.connections_display.column('two',minwidth=0,width=120)        
        self.connections_display.heading('#03', text='Host', anchor=W)
        self.connections_display.column('three',minwidth=0,width=120)
        self.connections_display.heading('#04', text='Port', anchor=W)
        self.connections_display.column('four',minwidth=0,width=120)
        self.connections_display.heading('#05', text='Schema', anchor=W)
        self.connections_display.column('five',minwidth=0,width=120)
        self.connections_display.heading('#06', text='User', anchor=W)
        self.connections_display.column('six',minwidth=0,width=120)
        self.connections_display.heading('#07', text='PWD', anchor=W)
        self.connections_display.column('seven',minwidth=0,width=120)
        self.connections_display.heading('#08', text='URL', anchor=W)
        self.connections_display.column('eight',minwidth=0,width=180)
        self.connections_display.heading('#09', text='Db Name', anchor = W)
        self.connections_display.column('nine',minwidth=0,width=120)
        self.connections_display.grid(row = 1, sticky ='E', padx = 2, pady = 2)
        self.connections_display.bind('<Button-1>',lambda e: self.get_data(e))
        
    def create_bottom_buttons(self):
        self.Labelframe3=LabelFrame(self.root,text="Take Actions",height=100,width=320,font=('cambria',14))
        self.Labelframe3.grid(padx=10,row=3,column=0,sticky='W')        
        self.connect=Button(self.Labelframe3,text='Connect',command=self.on_connect_button_clicked,width=20,font=('cambria',14))
        self.connect.grid(row=2,column=1,padx=50,pady=10)
        
        self.delete=Button(self.Labelframe3,text='Delete Selected', command=self.on_delete_selected_button_clicked,width=20,font=('cambria',14))
        self.delete.grid(row=2,column=2,padx=50,pady=10)
        
        self.modify=Button(self.Labelframe3,text='Modify Selected', command=self.on_modify_selected_button_clicked,width=20,font=('cambria',14))
        self.modify.grid(row=2,column=3,padx=50,pady=10)        
        

    def on_add_record_button_clicked(self):
        self.add_new_record()
        self.view_records()

    def on_delete_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.connections_display.item(self.connections_display.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_record()

    def on_modify_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.connections_display.item(self.connections_display.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to modify'
            return
        self.open_modify_window()

    def add_new_record(self):
        if self.new_records_validated():
            query = 'INSERT INTO connections VALUES(?,?,?,?,?,?,?,?,?)'
            parameters = (self.connection_entry.get(),self.database_entry.get(ACTIVE),
                          self.host_entry.get(),self.port_entry.get(),self.schema_entry.get(),
                          self.username_entry.get(),self.password_entry.get(),self.url_name.get(),self.database_name_entry.get())
            self.execute_db_query(query, parameters)
            self.message['text'] = 'Connection record of {} added'.format(
                self.connection_entry.get())
            self.connection_entry.delete(0, END)
            self.database_entry.delete(0, END)
            self.host_entry.delete(0, END)
            self.port_entry.delete(0, END)
            self.schema_entry.delete(0, END)
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.url_name.delete(0, END)
            self.database_name_entry.delete(0,END)
            
        else:
            self.message['text'] = 'Details cannot be blank'
        
        
    def new_records_validated(self):
        return (len(self.connection_entry.get()) != 0 #and len(self.database_entry.get()) != 0 
        and len(self.host_entry.get()) != 0 )
        #and
        #len(self.port_entry.get()) != 0 and 
        #len(self.schema_entry.get()) != 0 and len(self.username_entry.get()) != 0 
        #and len(self.password_entry.get()) != 0)

    def view_records(self):
        items = self.connections_display.get_children()
        for item in items:
            self.connections_display.delete(item)
        query = 'SELECT * FROM connections ORDER BY connection_entry desc'
        self.connection_entries = self.execute_db_query(query)
        for row in self.connection_entries:
            self.connections_display.insert('', 0, values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
    

    def delete_record(self):
        self.message['text'] = ''
        name = self.connections_display.item(self.connections_display.selection())['values'][0]
        print(name)
        query = 'DELETE FROM connections WHERE connection_entry = ?'
        self.execute_db_query(query, (name,))
        self.message['text'] = 'Connection for {} deleted'.format(name)
        self.view_records()

    def open_modify_window(self):
        name = self.connections_display.item(self.connections_display.selection())['text']
        old_connection_name = self.connections_display.item(self.connections_display.selection())['values'][0]
        self.transient = Toplevel()
        Label(self.transient, text='Connection Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Connection Name:').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_connection_name), state='readonly').grid(row=1, column=2)
        Label(self.transient, text='New Connection Name:').grid(
            row=2, column=1)
        new_connection_name_entry = Entry(self.transient)
        new_connection_name_entry.grid(row=2, column=2)
        Button(self.transient, text='Update Record', command=lambda: self.update_record(
            new_connection_name_entry.get(), old_connection_name, name)).grid(row=3, column=2, sticky='EW')
        self.transient.mainloop()

    def update_record(self, newphone, old_connection_name, name):
        query = 'UPDATE connections SET contactnumber=? WHERE contactnumber=? AND name=?'
        parameters = (newphone, old_connection_name, name)
        self.execute_db_query(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Connection of {} modified'.format(name)
        self.view_records()
    
    def display_table(self,df):
        from tabulate import tabulate
        from view import ScrollBar
        self.tab_toplevel = tk.Toplevel()
        self.disp_frame = tk.Frame(self.tab_toplevel)
        self.disp_frame.grid(row =0, column =0)
        tab_text = tk.Text(self.disp_frame, width = 120, height = 15)
        tab_data = tabulate(df[:501],headers=[col for col in df.columns], tablefmt = 'fancy_grid')
        tab_text.insert(tk.INSERT,tab_data)
        tab_text.config(state='disabled',wrap="none")
        tab_text.grid(row=0, column=0)
############## Adding scrollbar to display table window ###################
        dscroll = ScrollBar()
        horz = dscroll.add_hbar(self.disp_frame,tab_text,1,0)
        vert = dscroll.add_vbar(self.disp_frame,tab_text,0,2)
        dscroll.activate_scrollbar(tab_text,horz,vert)
########## Adding Repository and Preview in a same TopLevel####################
        repository_frame = tk.Frame(self.disp_frame)
        repository_frame.grid(row=2,column=0)
        repo_label = tk.Label(repository_frame,text='Where to store the Data',font=cambriamedium)
        repo_label.grid(row=0,column=1)
        file_label = tk.Label(repository_frame, text = 'File Name',font=cambriamedium)
        file_label.grid(row = 8, column =0)
        self.file_entry = tk.Entry(repository_frame, width = 80)
        self.file_entry.grid(row = 8, column =1)
        finish_button = tk.Button(repository_frame, text = 'Finish',font=cambriamedium,command =lambda: self.saveToPickle(df))
        finish_button.grid(row = 8 , column = 2, sticky = 'w', padx = 2, pady=3)
        self.repository_tree = ttk.Treeview(repository_frame, columns = ['A','B'])
        self.repository_tree.grid(row=2,column=1)
        self.path = r'../LocalRepository'
        repo_dir = self.repository_tree.insert('','end','repo',text='Local Repository')
        self.process_directory(repo_dir,self.path)
        
				
				
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.repository_tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)
	
    def saveToPickle(self,df):
        repo_focus = self.repository_tree.focus()
        repo_name = self.repository_tree.item(repo_focus)
        temp_path = r'{0}\{1}'.format(self.path,repo_name['text'])
        os.chdir(temp_path)
        if self.file_entry.get():
            file_name = self.file_entry.get()
            df.to_pickle(file_name)
        os.chdir(os.path.dirname(os.getcwd()))
        self.tab_toplevel.destroy()
          
	    

if __name__ == '__main__':
    root = Tk()
    root.iconbitmap(bitmap='../images/yot.ico')
    application = AddData(root)
    root.mainloop()