# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:24:33 2016

@author: Anurag
"""

import tkinter as tk
from tkinter import ttk
import sqlite3 as sl
import pymysql
#import pymongo
import pandas as pd
#import pymssql
import os
from tkinter import filedialog as fd
from configurations import *

class RetrieveData:
	def __init__(self, master):
    		self.master = master
    		self.masterdb = '../secured/connections.db'
    		self.tables = []
    		self.create_dbGui()
#    		self.create_pcGui()
    		
	def create_pcGui(self):
         path = fd.askopenfilename(filetypes=[("Csv files","*.csv")])
         if path:
             self.results = pd.read_csv(path)
             self.display_table(self.results)
             
	def create_dbGui(self):
		self.conn_frame = tk.LabelFrame(self.master, text = 'Available Connections', font =cambriabig)
		self.conn_frame.grid(row = 0, column = 0, padx = 5, pady =5)
		self.style = ttk.Style()
		self.style = self.style.configure("Treeview", font=cambriamedium)
#		self.style = self.style.configure("Heading", foreground='green')
		self.conn_display = ttk.Treeview(self.conn_frame, columns = ('a','b','c','d','e','f','g'))
		self.conn_display.column('a', width = 100, stretch = tk.YES)
		self.conn_display.column('b', width = 100, stretch = tk.NO)
		self.conn_display.column('c', width = 100, stretch = tk.NO)
		self.conn_display.column('d', width = 100, stretch = tk.NO)
		self.conn_display.column('e', width = 100, stretch = tk.NO)
		self.conn_display.column('f', width = 100, stretch = tk.NO)
		self.conn_display.column('g', width = 100, stretch = tk.NO)
		self.conn_display.column('#0', width = 0)
		self.conn_display.heading('a', text = 'Name')
		self.conn_display.heading('b', text = 'Database System')
		self.conn_display.heading('c', text = 'Host')
		self.conn_display.heading('d', text = 'Port')
		self.conn_display.heading('e', text = 'Database Scheme')
		self.conn_display.heading('f', text = 'User')
		self.conn_display.heading('g', text = 'Password')
		self.conn_display.grid(row = 1, columnspan = 3, sticky = 'w', padx = 15, pady = 10)
		self.button_frame = tk.Frame(self.master)
		self.button_frame.grid(row = 2, column =0)
		self.new_button = tk.Button(self.button_frame, text = 'New', width = 12, height = 1, font = (8), command = self.newConnection)
		self.new_button.grid(row = 7, column = 3, sticky = 'w', padx = 15, pady = 15, ipadx = 3, ipady = 3 )
		self.del_button = tk.Button(self.button_frame, text = 'Delete', width = 12, height = 1, font = (8), command = self.deleteConnection)
		self.del_button.grid(row = 7, column = 4, sticky = 'w', padx = 15, pady = 15, ipadx = 3, ipady = 3 )
		self.connect_button = tk.Button(self.button_frame, text = 'Connect',width = 12, height = 1, font = (8), command = self.onConnectClickedGui)
		self.connect_button.grid(row = 7, column = 5, sticky = 'e', ipadx = 3, ipady = 3)
		self.test_button = tk.Button(self.button_frame, text = 'Test Connection',
				 command = lambda:self.assign(), width = 15, height = 1, font = (8))
		self.test_button.grid(row = 7, column =2, ipadx = 3, ipady = 3 )
		self.test_frame = tk.LabelFrame(self.master, text = 'Connection status')
		self.test_frame.grid(row = 7, column = 0, sticky = 'w')
		self.get_conn_details()
#################### For Adding a New Connection ############################

	def newConnection(self):
		new_conn_tplvl = tk.Toplevel()
		connection_frame = tk.LabelFrame(new_conn_tplvl, text = 'Connection Details')
		connection_frame.config(font=('Arial', 16))
		connection_frame.grid(row = 0, column = 0, padx = 6)
		self.user_var = tk.StringVar()
		self.pass_var = tk.StringVar()
		self.host_var = tk.StringVar()
		self.schema_var = tk.StringVar()
		self.url_var = tk.StringVar()
		self.name_label = tk.Label(connection_frame, text = 'Name')
		self.name_label.config(font=('Arial', 13))
		self.name_label.grid(row = 0, column = 0, sticky = 'w')
		self.name_entry = tk.Entry(connection_frame, width = 100)
		self.name_entry.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.connection_label = tk.Label(connection_frame, text = 'Database System')
		self.connection_label.grid(row = 2, column = 0, sticky = 'w')
		self.connection_drpdwn = ttk.Combobox(connection_frame, width = 27, state = 'readonly')
		self.connection_drpdwn['values'] = ['MySQL','Oracle', 'MSSQL', 'ODBC', 'HSQLDB', 'MongoDB', 'PostgreeSQL']
		self.connection_drpdwn.set('Oracle')
		self.connection_drpdwn.grid(row = 3, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.host_label = tk.Label(connection_frame, text = 'Host')
		self.host_label.grid(row = 4, column = 0, sticky = 'w')
		self.host_entry = tk.Entry(connection_frame, width = 30, textvariable = self.host_var)
		self.host_entry.grid(row = 5, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.port_label = tk.Label(connection_frame, text = 'Port')
		self.port_label.grid(row = 6, column =0, sticky = 'nw')
		self.port_entry = tk.Entry(connection_frame, width = 30)
		self.port_entry.grid(row = 7, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.db_scheme_label = tk.Label(connection_frame, text = 'Database Schema')
		self.db_scheme_label.grid(row = 8, column = 0, sticky = 'w')
		self.db_scheme_entry = tk.Entry(connection_frame, width = 30, textvariable = self.schema_var)
		self.db_scheme_entry.grid(row = 9, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.user_label = tk.Label(connection_frame, text = 'User')
		self.user_label.grid(row = 10, column = 0, sticky = 'w')
		self.user_entry = tk.Entry(connection_frame, width = 30, textvariable = self.user_var)
		self.user_entry.grid(row = 11, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.passwrd_label = tk.Label(connection_frame, text = 'Password')
		self.passwrd_label.grid(row = 12, column = 0, sticky = 'w')
		self.pass_entry = tk.Entry(connection_frame, width = 30,show='*', textvariable = self.pass_var)
		self.pass_entry.grid(row = 13, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.url_label = tk.Label(connection_frame, text = 'URL')
		self.url_label.grid(row = 14, column = 0, sticky = 'w')
		self.url_entry = tk.Entry(connection_frame, width = 30, textvariable = self.url_var)
		self.url_entry.config(state = 'disabled')
		self.url_entry.grid(row = 15, column = 0, padx = 5, pady = 2, sticky = 'w')
		self.details_button = tk.Button(connection_frame, text = 'Save & Continue',
                        command = self.do_all, width = 25, height = 1, font = ('Cambria', 13))
		self.details_button.grid(row = 16, column = 1, padx = 4, pady = 7, sticky = 'e')

		# Tree should show all the values entered by the user.
		self.db_tree = ttk.Treeview(connection_frame, columns = ('one','two','three','four','five','six','seven','eight'), height = 6)
		self.db_tree.heading('#01', text = 'Name')
		self.db_tree.heading('#02', text = 'Database System')
		self.db_tree.heading('#03', text = 'Host')
		self.db_tree.heading('#04', text = 'Port')
		self.db_tree.heading('#05', text = 'Database Scheme')
		self.db_tree.heading('#06', text = 'User')
		self.db_tree.heading('#07', text = 'Password')
		self.db_tree.heading('#08', text = 'url')
		self.db_tree.column('#08', width = 100, stretch = tk.NO)
		self.db_tree.column('#07', width = 100, stretch = tk.NO)
		self.db_tree.column('#06', width = 100, stretch = tk.NO)
		self.db_tree.column('#05', width = 100, stretch = tk.NO)
		self.db_tree.column('#04', width = 100, stretch = tk.NO)
		self.db_tree.column('#03', width = 100, stretch = tk.NO)
		self.db_tree.column('#02', width = 100, stretch = tk.NO)
		self.db_tree.column('#01', width = 100, stretch = tk.NO)
		self.db_tree.column('#0', width = 0)
		self.db_tree.grid(row = 18, columnspan = 3)
		self.user_var.trace('w', self.update_url)
		self.pass_var.trace('w', self.update_url)
		self.host_var.trace('w', self.update_url)
		self.schema_var.trace('w', self.update_url)

##### Function to update the url #######

	def update_url(self,*args):
		uname = self.user_var.get()
		passwd = self.pass_var.get()
		host = self.host_var.get()
		schema = self.schema_var.get()
		url = '{0}/{1}@{2}/{3}'.format(uname,passwd,host,schema)
		self.url_var.set(url)
	
	
	def get_name_and_value(self):
	    self.db_tree.insert('', 'end', text = 'Connection_1', 
                   values = (self.name_entry.get(), self.connection_drpdwn.get(), self.host_entry.get(), 
                             self.port_entry.get(), self.db_scheme_entry.get(), self.user_entry.get(), self.pass_entry.get()))
    
	def insert_all(self):
		# Get all the values from all the widgets and insert them all into MySQL db.
	      atr1 = self.name_entry.get()
	      atr2 = self.connection_drpdwn.get()
	      atr3 = self.host_entry.get() 
	      atr4 = self.port_entry.get()
	      atr5 = self.db_scheme_entry.get()
	      atr6 = self.user_entry.get()
	      atr7 = self.pass_entry.get()
	      db = sl.connect(self.masterdb)
	      query = ("INSERT INTO conn_table(name,database_system,host,port,database_scheme,user,pwd) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\")".format(atr1,atr2,atr3,atr4,atr5,atr6,atr7))
#	      print('writing')
	      c = db.cursor()
	      c.execute(query)
	      db.commit()
	      db.close()					
#	      print('wrote')
	
	def do_all(self):
         self.get_name_and_value()
         self.insert_all()
         self.get_conn_details()


##########################End of New Connection Code ######################################
		
	def get_conn_details(self):
		self.db = sl.connect(self.masterdb)
		self.cur = self.db.cursor()
		self.query = 'SELECT * FROM conn_table;'
#		print('!!!!!!')
		self.res = self.cur.execute(self.query)
		self.result = self.res.fetchall()
		
		for row in self.result:
#		     print('#####rows of table#####')
#		     print(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
		     self.conn_display.insert('', 0, text = '' ,values = (row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
		self.db.commit()
		return self.result
	
	def get_current(self):
		self.curr = self.conn_display.focus()
		self.val = self.conn_display.item(self.curr)
		self.det = self.val.get('values')
#		print(self.det)
		return self.det
		
	def deleteConnection(self):
		self.get_current()
		delQuery = 'Delete from conn_table where Name = \'{}\''.format(self.det[0])
		self.cur.execute(delQuery)
		self.conn_display.delete(self.conn_display.selection())
		self.db.commit()

	def test_mongoDbConnection(self,host,port):
		self.client = pymongo.MongoClient(host=host,port=port)
		self.db = self.client.test
		self.table_name = self.db.name
#		print(self.db.my_collection)
		self.test_label = tk.Label(self.button_frame, text = 'Connection Ok')
		self.test_label.grid(row=7, column = 0, sticky = 'w')
		return self.table_name
		
	def test_sqlServer(self,host,user,passwd,dbname):
#		print('host={0}\n user={1} \n passwd={2} \n dbname={3}'.format(host,user,passwd,dbname))
		self.db = pymssql.connect(host=host,user=user,password=passwd,database=dbname)
		self.c = self.db.cursor()
		self.query ='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\';'
		self.c.execute(self.query)
		self.res = self.c.fetchall()
		self.tables[:] = []
		for r in self.res:
			self.tables.append(r[0])
		self.test_label = tk.Label(self.button_frame, text = 'Connection Ok')
		self.test_label.grid(row=7, column = 0, sticky = 'w')
#		print('connected')
#		print('Table Names:', self.tables)
		return self.tables
	
	
	def test_mysqlconnection(self,host,user,passwd,dbname):
		print('host={0}\n user={1} \n passwd={2} \n dbname={3}'.format(host,user,passwd,dbname))
		self.db = pymysql.connect(host=host,user=user,passwd=passwd,db=dbname)
		self.c = self.db.cursor()
#		self.query ='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\' AND TABLE_SCHEMA=\'connection_details\';'
		self.query ='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\' AND TABLE_SCHEMA=\'{}\';'.format(dbname)
		self.c.execute(self.query)
		self.res = self.c.fetchall()
		self.tables[:] = []
		for r in self.res:
			self.tables.append(r[0])
		self.test_label = tk.Label(self.button_frame, text = 'Connection Ok')
		self.test_label.grid(row=7, column = 0, sticky = 'w')
#		print('connected')
#		print('Table Names:', self.tables)
		return self.tables
	
	def assign(self):
		self.val = self.get_current()
		if self.val[1] == 'MySQL':
			self.host = self.val[2]
			self.user = self.val[5]
			self.passwd = str(self.val[6])
			self.dbname = self.val[4]
			return self.test_mysqlconnection(self.host,self.user,self.passwd,self.dbname)
		elif self.val[1] == 'MongoDB':
			self.host = self.val[2]
			self.port = self.val[3]
			return self.test_mongoDbConnection(self.host,self.port)
		elif self.val[1] == 'MSSQL':
			self.host = self.val[2]
			self.user = self.val[5]
			self.passwd = self.val[6]
			self.dbname = self.val[4]
			return self.test_sqlServer(self.host,self.user,self.passwd,self.dbname)

########################### Loading Top Level Connect Window ##################################
		
	def onConnectClickedGui(self):
		self.connectwindow = tk.Toplevel()
		self.table_frame = tk.LabelFrame(self.connectwindow, text = 'Tables')
		self.attr_frame = tk.LabelFrame(self.connectwindow, text = 'Attributes')
		self.query_frame = tk.LabelFrame(self.connectwindow, text = 'SQL Query')

############## Creating Listboxes, scrollbar and Text-pad ##############
		self.table_list = tk.Listbox(self.table_frame, width = 32)
		self.table_list.bind('<ButtonPress-1>', self.fillAttrList)
#		self.table_list.bind('<ButtonRelease-1>', self.executeSqlQuery)
		self.attr_list = tk.Listbox(self.attr_frame, width = 32)
		self.text_pad = tk.Text(self.query_frame, fg = 'blue')
		self.nxt_button = tk.Button(self.query_frame, text = 'Submit', command = self.onSubmitQuery)
		
		
################### Closing the Widgets #########################
		self.table_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
		self.attr_frame.grid(row = 0, column = 0, padx = 5, pady = 5)
		self.query_frame.grid(row = 4,padx = 5, pady = 5)
		self.table_list.grid(row = 0, padx = 5, pady = 5)
		self.attr_list.grid(row = 0, padx = 5, pady = 5)
		self.text_pad.grid(row = 0, padx = 5, pady = 5)
		self.nxt_button.grid(row = 1, column = 0)
		self.fillTableList()

####### Creating binding for tables list-box to attr-listbox for showing the attributes #####
		
	def fillTableList(self):
		self.result = self.assign()
#		print(self.result)
		for r in self.result:
			self.table_list.insert(tk.END , r)
#		print(self.result)
#		print(type(self.result))
		return self.result
	
	def fillAttrList(self,event):
#		table = self.table_list.get(self.table_list.curselection())
		table = self.table_list.get(self.table_list.nearest(event.y))
#		print(table)
		self.attr_list.delete(0, tk.END)
		if self.det[1] == 'MySQL':
			self.table_query = 'Show columns from {}'.format(table)
		elif self.det[1] == 'MSSQL':
			self.table_query = 'SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(\'{}\')'.format(table)
		self.c.execute(self.table_query)
		self.tab = self.c.fetchall()
		for t in self.tab:
			self.attr_list.insert(1, t[0])
		self.executeSqlQuery(event)
		
################### SQL Query Fom Textpad #######################
	def executeSqlQuery(self,event):
#		widget = self.table_list.get(self.table_list.curselection())
		widget = self.table_list.get(self.table_list.nearest(event.y))
		query_table = 'select * from {}'.format(widget)
		self.text_pad.delete('1.0', tk.END)
		self.text_pad.insert(tk.INSERT,query_table)
		
	def onSubmitQuery(self):
		sub_query = self.text_pad.get('1.0',tk.END)
		self.c.execute(sub_query)
		self.df = pd.read_sql_query(sub_query,self.db)
#		print(self.df)
		self.display_table(self.df)

	def display_table(self,df):
		from tabulate import tabulate
		from v5_view import ScrollBar
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
		repo_label = tk.Label(repository_frame,text='Where to store the Data')
		repo_label.grid(row=0,column=1)
		file_label = tk.Label(repository_frame, text = 'File Name')
		file_label.grid(row = 8, column =0)
		self.file_entry = tk.Entry(repository_frame, width = 80)
		self.file_entry.grid(row = 8, column =1)
		finish_button = tk.Button(repository_frame, text = 'Finish', command =lambda: self.saveToPickle(df))
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



def main():
	root = tk.Tk()
	NewConnection(root)
#	RetrieveData(root)
	root.mainloop()

if __name__ == "__main__":
	main()
