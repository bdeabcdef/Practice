import os,importlib
import operator
import Pmw
import tkinter as tk
from tkinter import Menu,ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mbox
from configurations import *
from add_data import AddData
import file as wicon
import algos
from model import FileHandle 
from tkinter import font



global alloperatorobjects
alloperatorobjects = dict()


class View(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.parent.geometry("{0}x{1}+0+0"
                        .format(parent.winfo_screenwidth()-2,
                                parent.winfo_screenheight()-2))
#        self.parent.grid_rowconfigure(0, weight=1)
        self.helv36 = font.Font(family='Helvetica', size=12, weight='bold')
        self.init_gui()
        global controller
        controller = Controller()
        
        
    def init_gui(self):
        self.create_menubar()
        self.create_topframe()
        self.allocate_frames()
        
    def allocate_frames(self):
        self.mainframe = tk.Frame(self.parent)
        self.mainframe.grid(row=1,padx=4)
        self.rf1=RightFrame(self.mainframe)
        self.mf1=MiddleFrame(self.mainframe,self.rf1)
        self.lf1=LeftFrame(self.mainframe,self.mf1)
#        self.mainpane.grid()
#        self.mainpane.add(self.mainframe)
        
    def create_menubar(self):
        self.menuBar = Menu()                      
        self.parent.config(menu=self.menuBar)
        
        self.fileMenu = Menu(self.menuBar,tearoff=0)                 
        self.editMenu = Menu(self.menuBar,tearoff=0)
        self.settingMenu = Menu(self.menuBar,tearoff=0)
        self.viewmenu = Menu(self.menuBar,tearoff=0)
        self.helpMenu = Menu(self.menuBar,tearoff=0)
        
        self.fileMenu.add_command(label="Open file",command=lambda: self.lf1.add_data())
        self.fileMenu.add_command(label="Reset",command=self.__reset)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save process",command=lambda: self.mf1.name_to_save())
        self.fileMenu.add_command(label="Execute process",command=lambda: self.mf1.execute_process())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit",command = self.__quit)
        
        self.editMenu.add_command(label="Copy", accelerator='ctrl + c',
                                  compound='left',command=self.copy)
        self.editMenu.add_command(label="Cut", accelerator='ctrl + x',
                                  compound='left',command=self.cut)
        self.editMenu.add_command(label="Paste", accelerator='ctrl + v')
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Delete",state='disabled')
        
        self.settingMenu.add_command(label="Add Repository",command=lambda: self.lf1.add_repo())        
        self.settingMenu.add_command(label="preferences",command=lambda:controller.pops('Feature not available'))
#        self.settingMenu.add_command(label="Arima_demo")        
        
        self.helpMenu.add_command(label="about Dsf",command=lambda:controller.pops('You are running the application \nDecision Sciences Factory v1.5'))
        
        self.viewmenu.add_command(label="Design Tab",command=self.design)
        self.viewmenu.add_command(label="Result Tab",command=self.result)
        
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)
        self.menuBar.add_cascade(label="View", menu=self.viewmenu)
        self.menuBar.add_cascade(label="Settings", menu=self.settingMenu)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        
    def create_topframe(self):
        self.topframe = tk.LabelFrame(self.parent)
        self.topframe.grid(row=0,column=0,pady=6,sticky='WE')        
        self.create_topleftframe()
        self.create_topcenterframe()
        
    def create_topleftframe(self):
        top_llframe = tk.Frame(self.topframe)
        top_llframe.grid(row=0,column=0,sticky='NW')

        def ci(name):
            pic = tk.PhotoImage(file=top_images_dir+name+'.PNG')
            return pic
            
        oicon = ci('1_open')            
        sicon = ci('2_save')
        picon = ci('3_play')
        dicon = ci('4_download')
        vicon = ci('6_vis')

        obtn = tk.Button(top_llframe,image=oicon,relief='groove',command=lambda: self.lf1.add_data())
        sbtn = tk.Button(top_llframe,image=sicon,relief='groove',command=lambda: self.mf1.name_to_save())        
        pbtn = tk.Button(top_llframe,image=picon,relief='groove',command=lambda: controller.on_run(self.mf1,alloperatorobjects))        
        dbtn = tk.Button(top_llframe,image=dicon,relief='groove',command=lambda: self.lf1.add_repo())        
        vbtn = tk.Button(top_llframe,image=vicon,relief='groove',command=lambda: controller.visualize()) 

        obtn.image = oicon
        sbtn.image = sicon
        pbtn.image = picon
        dbtn.image = dicon
        vbtn.image = vicon        
        
        
        obtn.grid(row=0,column=1,padx=2)        
        sbtn.grid(row=0,column=2,padx=2)
        pbtn.grid(row=0,column=3,padx=2)
        dbtn.grid(row=0,column=4,padx=2)
        vbtn.grid(row=0,column=5,padx=2)
                
    def design(self):
        self.design_btn.config(state='disabled')
        self.result_btn.config(state='normal')
        self.mf1.design_tab()
    def result(self):
        self.result_btn.config(state='disabled')
        self.design_btn.config(state='normal')
        self.mf1.result_tab()

    def create_topcenterframe(self):
        top_cframe = tk.Frame(self.topframe)
        top_cframe.grid(row=0,column=1,padx=220,sticky='WE')
        self.design_btn = tk.Button(top_cframe,text='Design',state='disabled',relief='raised',width=7,height=1,font=cambriabig,command=self.design)
        self.design_btn.grid(row=0,column=0,pady=5,padx=5,ipadx=50,ipady=2,sticky='w')
        self.result_btn = tk.Button(top_cframe,text='Result',state='normal',relief='raised',width=7,height=1,font=cambriabig,command=self.result)
        self.result_btn.grid(row=0,column=1,pady=5,padx=5,ipadx=50,ipady=2,sticky='w')

    def cut(self):
        self.mf1.resultnb.event_generate("<<Cut>>")
        
    def copy(self):
        self.mf1.resultnb.event_generate("<<Copy>>")

    def __reset(self):
        self.__quit()
        main()
        
    def __quit(self):
        self.parent.destroy()
#==============================================================================
#                               Right Frame
#==============================================================================

class RightFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.mainframe = parent
        self.rightframe = tk.LabelFrame(self.mainframe,highlightthickness=4,bd=1,height=550,width=50,relief='solid')
        self.rightframe.grid(row=1,column=2,sticky='NES',padx=5)
        self.param_frame = tk.Frame(self.rightframe)
        self.balloon = Pmw.Balloon(self.mainframe)
        plabel = tk.Label(self.rightframe,text='Parameters',font=cambriabig,bg='#e0e0e0')
        plabel.grid(ipadx=80)
        self.columns = []

    def create_wspace(self):
        try:
            self.param_frame.destroy()
            
        except:
            pass
        finally:
            self.param_frame = tk.Frame(self.rightframe)
            self.param_frame.grid(row=2,column=0,sticky='W')
                    
            
    def label_name(self,name,row=2,col=0):
        label = tk.Label(self.param_frame,text=name,font=cambriamedium)
        label.grid(row=row,column=col,sticky='SW')
    
    def header(self,name,row=1,col=0):
        self.param_frame = tk.Frame(self.rightframe)
        self.param_frame.grid(row=2,column=0,sticky='W')
        self.p_label = tk.Label(self.param_frame,text=name,font=bigbutton)
        self.p_label.grid(row=row,column=col,sticky='w',pady=4)
    
    def widget_entry(self,name,row=2,balloon='',show=None):
        self.label_name(name,row=row)
        w_entry = tk.Entry(self.param_frame,show=show,width=17)
        w_entry.grid(row=row,column=1,ipady=6,sticky='EW')
        self.balloon.bind(w_entry,balloon)
        return w_entry

    def widget_listbox(self,name,lbox=[],c=1,row=2,col=1,balloon=''):
        self.label_name(name,row=row)
        lval = tk.StringVar()
        w_lbox = ttk.Combobox(self.param_frame,width=15,textvariable=lval)
        w_lbox['values'] = lbox       
        w_lbox.current(c)
        w_lbox.grid(row=row,column=col,ipady=2,pady=2,sticky='w')
        self.balloon.bind(w_lbox,balloon)
        return lval
    
    def widget_spinbox(self,name,start=-5,end=5,row=2,balloon=''):
        self.label_name(name,row=row)
        spinval = tk.StringVar()
        w_sbox = tk.Spinbox(self.param_frame,width=15,from_=start,to=end,textvariable=spinval)
        w_sbox.grid(row=row,column=1,ipady=2,pady=2,sticky='w')
        self.balloon.bind(w_sbox,balloon)
        return spinval        

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func  
  
    def get_path(self,obj_id,ext1,ext2):
        path = fd.askopenfilename(filetypes=[(ext1,ext2)])
        if path:
            alloperatorobjects[obj_id]['function'].filepath = path 
            self.columns = alloperatorobjects[obj_id]['function'].get_columns()
   
    def populate_manualReplaceObjects(self,uid,replace_value) :
        print(replace_value)
        alloperatorobjects[uid]['function'].replace_value = replace_value
    
    def populate_csvobjects(self,uid,sepp):
        sep = sepp[sepp.find('(')+1:sepp.find(')')]
        alloperatorobjects[uid]['function'].sep = sep
        
    def populate_uidobjects(self,uid,sep,ucols):
        alloperatorobjects[uid]['function'].seperator = sep
        alloperatorobjects[uid]['function'].uid_cols = ucols
        
    def populate_normalizeObjects(self,uid,unique_column_id) :
        alloperatorobjects[uid]['function'].unique_column_id = unique_column_id
        
    def populate_standardizeObjects(self,uid,unique_column_id,target) :
        alloperatorobjects[uid]['function'].unique_column_id = unique_column_id
        alloperatorobjects[uid]['function'].target = target
        
    def populate_SuperhackObjects(self,uid,unique_column_id,target) :
        alloperatorobjects[uid]['function'].unique_column_id = unique_column_id
        alloperatorobjects[uid]['function'].target = target

    def populate_textProcess(self,uid,feature,sw,al,norm) :
        alloperatorobjects[uid]['function'].feature = feature
        alloperatorobjects[uid]['function'].stop_words = sw
        alloperatorobjects[uid]['function'].analyzer = al
        alloperatorobjects[uid]['function'].norm = norm

    def populate_excelObjects(self,uid,sheetval) :
        print('excelobject',sheetval)
        alloperatorobjects[uid]['function'].sheetname = sheetval

    def populate_joinObjects(self,uid,join_type,keys) :
        alloperatorobjects[uid]['function'].keys = keys
        alloperatorobjects[uid]['function'].join_type = join_type
#        self.columns = alloperatorobjects[uid]['function'].get_columns()

    def populate_visualizeobjects(self,uid,user,passwd):
        vis = alloperatorobjects[uid]['function']
        vis.user = user
        vis.passwd = passwd
        vis.init_engine()
        db_list = vis.db_list()
        
        self.dbwin = tk.Toplevel()
        self.db_frame = tk.LabelFrame(self.dbwin, text = 'Choose a Database')
        self.db_frame.grid()
        self.db_lbox = tk.Listbox(self.db_frame, width=50)        
        for r in db_list:
            self.db_lbox.insert(tk.END , r)
        self.db_lbox.grid()
        self.db_lbox.bind("<Double-Button-1>",lambda e: self.chooseDb(e,vis))
    
    def populate_filterObjects(self, uid, column, symbol, filter_typeValue):
        print(column,symbol,filter_typeValue)
        alloperatorobjects[uid]['function'].column = column
        alloperatorobjects[uid]['function'].type = symbol
        alloperatorobjects[uid]['function'].value = filter_typeValue

    def populate_aggregateObjects(self, uid, column, aggregator_typeValue):
        alloperatorobjects[uid]['function'].column = column
        alloperatorobjects[uid]['function'].aggregator = aggregator_typeValue

    def populate_sortObjects(self, uid, column, sort_type):
        print(column,sort_type)
        alloperatorobjects[uid]['function'].column = column
        alloperatorobjects[uid]['function'].sort_type = sort_type

    def populate_pivotObjects(self, uid, column, index_col, pivot_type):
        alloperatorobjects[uid]['function'].column = column
        alloperatorobjects[uid]['function'].index_column = index_col
        alloperatorobjects[uid]['function'].pivot_agg = pivot_type        

        
    def populate_col_ops(self,uid,f_column,ops_value,s_column,col_name):
        print(f_column,ops_value,s_column,col_name)
        alloperatorobjects[uid]['function'].f_col = f_column
        alloperatorobjects[uid]['function'].ops_val = ops_value
        alloperatorobjects[uid]['function'].s_col = s_column
        alloperatorobjects[uid]['function'].col_name = col_name
        print(f_column,ops_value,s_column,col_name)

    def populate_rawscriptobjects(self,uid,user_code):
        alloperatorobjects[uid]['function'].code = [user_code]
        controller.script_feed(uid)
        print(user_code)
        
    def chooseDb(self,event,vis):
            name = self.db_lbox.get(self.db_lbox.nearest(event.y))
            vis.dbname = name
            engine = vis.activate_db()
            self.dbwin.destroy()
            controller.visualize(engine,name)
            
    def readcsv_param(self,event,obj_id):
        self.header('Read Csv')
        
        self.folder_icon = tk.PhotoImage(file=frame_images+'folder.png')
        
        csv_entry = self.widget_entry('Csv file',row=3)
        button = tk.Button(self.param_frame,image=self.folder_icon,command=lambda arg1=obj_id,arg2="Csv Files(*.csv)",arg3=".csv": self.get_path(arg1,arg2,arg3))
        button.image = self.folder_icon            
        button.grid(row=3,column=2,sticky='E',padx=5)
        
        separators = ['comma (,)','semicolon (;)','Pipe (|)','tab','whitespace']        
        entry = self.widget_listbox('Column Seperator',lbox=separators,row=5,c=0)
        ebtn = tk.Button(self.param_frame,text='ok',command=lambda:self.populate_csvobjects(obj_id,entry.get()))
        ebtn.grid(row=5,column=2)
  
    
    def readjson_param(self,event,obj_id):
        self.header('Read Json')
        folder_icon = tk.PhotoImage(file=frame_images+'folder.png')
        
        entry = self.widget_entry('Json file',row=3)
        
        button = tk.Button(self.param_frame,image=folder_icon,command=lambda arg1=obj_id,arg2="Json Files(*.json)",arg3=".json": self.get_path(arg1,arg2,arg3))
        button.image = folder_icon            
        button.grid(row=3,column=2,sticky='E',padx=5)
            
        
    def readexcel_param(self, event, obj_id):
        self.header('Read Excel')
        
        folder_icon = tk.PhotoImage(file=frame_images+'folder.png')
        self.widget_entry('Excel file',row=3)
        button = tk.Button(self.param_frame,image=folder_icon,command=lambda arg1=obj_id,arg2="Excel Files(*.xlsx)",arg3=".xlsx": self.get_path(arg1,arg2,arg3))
        button.image = folder_icon            
        button.grid(row=3,column=2,sticky='E',padx=5)
        
        sheet_num = self.widget_spinbox('Sheet Number',start=0,row=5)
        sheet_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda:self.populate_excelObjects(obj_id,sheet_num.get()))
        sheet_submit.grid(row=6,column=0,ipadx=3,ipady=2,sticky='W')
    
    def predict_param(self, event, obj_id):
        self.header('Test File')
        radvar = tk.IntVar()
        
        r1button = tk.Radiobutton(self.param_frame,text='Predict Existing Data',font=cambriamedium,variable=radvar,value=0)
        r1button.grid(row=3,column=0,sticky='SW')
        r2button = tk.Radiobutton(self.param_frame,text='Predict Test Data',font=cambriamedium,variable=radvar,value=1)
        r2button.grid(row=5,column=0,sticky='SW')
        folder_icon = tk.PhotoImage(file=frame_images+'folder.png')
        entry = self.widget_entry('Test data',row=6)
        button = tk.Button(self.param_frame,image=folder_icon,command=lambda arg1=obj_id,arg2="Csv Files(*.csv)",arg3=".csv": self.get_path(arg1,arg2,arg3))
        button.image = folder_icon            
        button.grid(row=6,column=2,sticky='E',padx=5)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:controller.predict(obj_id,radvar.get()))
        w_submit.grid(row=8,column=1,ipadx=3,ipady=2)
            
    def readzip_param(self):
        self.header('Read Zip')
        folder_icon = tk.PhotoImage(file=frame_images+'folder.png')
        label = tk.Label(self.param_frame,text='Zip file',font=cambriamedium)
        label.grid(row=3,column=0,sticky='SW')
        entry = tk.Entry(self.param_frame,width=17)
        entry.grid(row=3,column=1,ipady=6,sticky='EW')
        button = tk.Button(self.param_frame,image=folder_icon,command=lambda arg1=obj_id,arg2="Excel Files(*.xlsx)",arg3=".xlsx": self.get_path(arg1,arg2,arg3))
        button.image = folder_icon            
        button.grid(row=3,column=2,sticky='EW',padx=5)
            
    def manualreplace_param(self, event, uid):
        self.header('Manual Replace')
        mval = self.widget_spinbox('Value',row=4)                
        self.manualReplace_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda arg1=uid :self.populate_manualReplaceObjects(arg1,mval.get()))
        self.manualReplace_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
    
            
    def autoreplace_param(self, event, uid):
        self.header('Auto Replace')
        autoReplace_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium)
        autoReplace_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
    
    
    def extend_col_param(self,event, uid):
        self.header('Extend Columns')
        f_box = self.widget_listbox('Column 1',row=2,lbox=self.columns)            
        olist = ['Concatenate', 'Soon to Come']
        ops_box = self.widget_listbox('Operator',row=3,lbox=olist,c=0)
        s_box = self.widget_listbox('Column 2',row=4,lbox=self.columns)            
        n_col = self.widget_entry('New Column',row=5)            
        
        s_button = tk.Button(self.param_frame, text = 'Submit',font=cambriamedium, command=lambda arg1=uid: self.populate_col_ops(arg1,f_box.get(),ops_box.get(),s_box.get(),n_col.get()) )
        s_button.grid(row=6, column=1, sticky='w')
            
            
    def uidgen_param(self,event,uid):
        self.col_count = 1
        cols_dict = {}
        def create_column(colno):
            try:
                atype_colno = tk.Label(self.param_frame,text='Column %d'%colno)
                atype_colno.grid(row=colno+4,column=0,sticky='w',padx=2,pady=3)
                atypebox_colno = ttk.Combobox(self.param_frame,state='readonly')
                atypebox_colno['values'] = self.columns
                atypebox_colno.current(0)            
                atypebox_colno.grid(row=colno+4,column=1,ipady=2,pady=2,sticky='w')
                cols_dict[colno] = (atype_colno,atypebox_colno)
                self.col_count += 1
            except:
                return 'Columns not found'
        def remove_column(colno):
            try:
                colno_temp = cols_dict.pop(colno)
                self.col_count-=1
                colno_temp[0].grid_forget()
                colno_temp[1].grid_forget()
            except KeyError:
                return 'key not found'
                
        self.header('Unique ID')
        
        create_column(self.col_count)
        addbtn = tk.Button(self.param_frame,text='Add column',command=lambda:create_column(self.col_count+1))
        addbtn.grid(row=2,column=0,sticky='w',padx=2)

        delbtn = tk.Button(self.param_frame,text='Remove column',command=lambda:remove_column(self.col_count))
        delbtn.grid(row=2,column=1,sticky='w',padx=2)
        seplist = ['|','','_','-']       
        sepval = self.widget_listbox('Seperator',row=4,c=0,lbox=seplist)

        submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                           command=lambda:self.populate_uidobjects(uid,sepval.get(),[v[1].get() for k,v in cols_dict.items()]))
        submit.grid(row=3,column=1,ipadx=3,ipady=2,sticky='W')
            
            
    def rawscript_param(self, event, uid):
        self.header('Raw Script')
        text = tk.Text(self.param_frame,width=32,height=25,bd=1,relief='solid')
        text.configure(state='normal',wrap="none")
        text.grid(row=2,column=0,padx=3,sticky="NEWS")
        submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                           command=lambda:self.populate_rawscriptobjects(uid,text.get('1.0','end-1c')))
        submit.grid(row=3,column=0,ipadx=3,ipady=2,sticky='W')
    
    
    def join_param(self, event, uid):
        self.c_count = 1
        cols_dict = {}
        def create_column(colno):
            try:
                atype_colno = tk.Label(self.param_frame,text='Column %d'%colno)
                atype_colno.grid(row=colno+4,column=0,sticky='w',padx=2,pady=3)
                atypebox_colno = ttk.Combobox(self.param_frame,state='readonly')
                atypebox_colno['values'] = self.columns
                atypebox_colno.current(0)            
                atypebox_colno.grid(row=colno+4,column=1,ipady=2,pady=2,sticky='w')
                cols_dict[colno] = (atype_colno,atypebox_colno)
                self.c_count += 1
            except:
                return 'Columns not found'
        def remove_column(colno):
            try:
                colno_temp = cols_dict.pop(colno)
                self.c_count-=1
                colno_temp[0].grid_forget()
                colno_temp[1].grid_forget()
            except KeyError:
                return 'key not found'
        self.header('Join')
        create_column(self.c_count)
        addbtn = tk.Button(self.param_frame,text='Add column',command=lambda:create_column(self.c_count+1))
        addbtn.grid(row=2,column=0,sticky='w',padx=2)

        delbtn = tk.Button(self.param_frame,text='Remove column',command=lambda:remove_column(self.c_count))
        delbtn.grid(row=2,column=1,sticky='w',padx=2)
        types = ['left','right','outer','inner']        
        join_type = self.widget_listbox('Type of Join',row=4,lbox=types,c=3)
            
        submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                           command=lambda:self.populate_joinObjects(uid,join_type.get(),[v[1].get() for k,v in cols_dict.items()]))
        submit.grid(row=3,column=1,ipadx=3,ipady=2,sticky='W')
            
################# Append parameter screen #######################

    def append_param(self, event, uid):
        self.header('Append Data')
												
##################End of Append Parameter screen ######################

########### Drop Duplicates Parameter Screen #######################            
            
    def drop_duplicate_param(self,event,uid):
        self.header('Drop Duplicates')
            
################## End of Drop Duplicates Parameter Screen #########
            
################ Start of Remove Nulls #######################   
            
    def drop_null_param(self,event,uid):
        self.header('Remove Null values')

################ End of Remove nulls########################## 

######################## To DB param #################################

    def todb_param(self,event,uid):
        self.header('Write Database')
        vals = getattr(alloperatorobjects[uid]['function'],'init_engine')()
        db_label = tk.Label(self.param_frame,text='Select Connection',font=cambriamedium)
        db_label.grid(row=3,column=0,sticky='NSW')
        db_box = self.widget_listbox('Select connection',row=3,c=0,lbox=vals)
        db_entry = self.widget_entry('Table Name',row=4)        
        
        db_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda:controller.database(uid,db_box.get(),db_entry.get()))
        db_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='NSW')
                        
########################### End of To DB param ########################           
            
    
    def tofile_param(self,event,uid):
        self.header('Write File')
            
        write_entry = self.widget_entry('FileName',row=3)            
            
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:controller.to_file(write_entry.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2)
    
    def normalize_param(self,event,uid):
        self.header('Normalize Data')
        n_entry = self.widget_listbox('Unique ID',row=3,lbox=self.columns)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid :self.populate_normalizeObjects(arg1,n_entry.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2)
       
    def standardize_param(self,event,uid):
        self.header('Standardize Data')
        n_entry = self.widget_listbox('Unique ID',row=3,lbox=self.columns)
        n_target = self.widget_listbox('Target',row=4,lbox=self.columns)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid :self.populate_standardizeObjects(arg1,n_entry.get(),n_target.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2)
       
#==============================================================================
# Super Hack       
#==============================================================================
       
    def superhack_param(self,event,uid):
        self.header('Super Hack')
        n_entry = self.widget_listbox('Unique ID',row=3,lbox=self.columns)
        n_target = self.widget_listbox('Target',row=4,lbox=self.columns)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid :self.populate_SuperhackObjects(arg1,n_entry.get(),n_target.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2)

    def sh_report(self):
        c_len,m_type,m_acc = controller.super_hack_report()
        self.label_name('New Column Length',row=3)
        self.label_name(c_len,row=3,col=2)
        self.label_name('Model Type',row=4)
        self.label_name(m_type,row=5,col=2)
        self.label_name('Model Accuracy',row=4)
        self.label_name(m_acc.values(),row=7,col=2)
        
        
    def sh_report_param(self,event,uid):
        self.header('SH Report')
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = self.sh_report)
        a_submit.grid(row=2,column=0,ipadx=3,ipady=2)
    
#==============================================================================
# Super hack end    
#==============================================================================
    
    def textpreprocess_param(self,event,uid):
        self.header('Preprocess Data')
        n_feature = self.widget_listbox('Feature',row=3,lbox=self.columns)
        n_stpwrd = self.widget_listbox('Stop Words',row=4,lbox=['english','None'],c=0)
        n_analyzer = self.widget_listbox('Analyzer',row=5,lbox=['word','char'],c=0)
        n_norm = self.widget_listbox('Normalization',row=6,lbox=['None','l1','l2'],c=0)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid :self.populate_textProcess(arg1,n_feature.get(),n_stpwrd.get(),n_analyzer.get(),n_norm.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2)
         
    def recommend_param(self,event,uid):
        self.header('Recommend')
            
        uentry = self.widget_listbox('Uid',row=3,lbox=self.columns)  
        tentry = self.widget_listbox('Target',row=5,lbox=self.columns)
        alist = ['RandomForest','GradientBoost']
        rentry = self.widget_listbox('Algorithm',row=6,lbox=alist,c=0)
        
        r_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda :controller.recommend(uentry.get(),tentry.get(),rentry.get()))
        r_submit.grid(row=7,column=1,ipadx=3,ipady=2)

    def manual_param(self,event,uid):
        self.header('Feature Engineering')
            
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:self.features_window(uid))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='NSW')
        
    def runmodel_param(self,event,uid):
        self.header('Run Model')
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:self.model_window())
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='NSW')
   
    def crossvalidation_param(self,event,uid):
        self.header('Model Accuracy')
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = self.cv_score)
        a_submit.grid(row=2,column=0,ipadx=3,ipady=2)
    
    def mse_param(self,event,uid):
        self.header('Mean Squared Error')
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = self.mse_score)
        a_submit.grid(row=7,column=1,ipadx=3,ipady=2)
            
    def loadrepo_param(self,event,uid):
        self.header('Repository File')
        def ucols():
            self.columns = alloperatorobjects[uid]['function'].get_columns()
        a_submit = tk.Button(self.param_frame,text='Load',font=cambriamedium,command = lambda: ucols())
        a_submit.grid(row=2,column=1,ipadx=3,ipady=2)
        
    def visualize_param(self,event,uid):
        self.header('Visualize')
        user = self.widget_entry('Username',row=3)
        passwd = self.widget_entry('password',show='*',row=4)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:self.populate_visualizeobjects(uid,user.get(),passwd.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='NSW')
    
    def imgprocess_param(self,event,uid):
        self.header('Image Process')
        user = self.widget_entry('Username',row=3)
        passwd = self.widget_entry('password',show='*',row=4)
        w_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:controller.imgprocess(uid,user.get(),passwd.get()))
        w_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='NSW')
    
    def filter_param(self,event,uid):
        self.header('Filter')

        fname = self.widget_listbox('Column',lbox=self.columns,row=3)

        tlist = ['<','>','==','!=']
        sname = self.widget_listbox('Type',lbox=tlist,row=4)        

        ventry = self.widget_entry('Value',row=5)
        f_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid: self.populate_filterObjects(arg1,fname.get(),sname.get(),ventry.get()))
        f_submit.grid(row=8,column=1,pady=4)

    def aggregate_param(self,event,uid):
        self.header('Aggregate')
        
        gname = self.widget_listbox('Column',row=3,lbox=self.columns)
        agg_list = ['sum','mean','count','max']
        aname = self.widget_listbox('Type',row=4,lbox=agg_list)
        
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid: self.populate_aggregateObjects(arg1,gname.get(),aname.get()))
        a_submit.grid(row=14,column=1,pady=4)

####################################
    def sort_param(self,event,uid):
        self.header('Sort Data')

        sname = self.widget_listbox('Column',lbox=self.columns,row=3)        
        
        slist = ['ascending','descending']
        stname = self.widget_listbox('Type',lbox=slist,row=4,c=0)
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid: self.populate_sortObjects(arg1,sname.get(),stname.get()))
        a_submit.grid(row=14,column=1,pady=4)
#######################
    def transpose_param(self,event,uid):
        self.header('Transpose')
 
#########################
    def pivot_param(self,event,uid):
        self.header('Pivot table')
        pname = self.widget_listbox('Column',row=3,lbox=self.columns)        
        piname = self.widget_listbox('Index',row=4,lbox=self.columns)        
        plist = ['sum','mean','count','max']
        ptname = self.widget_listbox('Type',row=5,lbox=plist,c=0)

        p_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda arg1=uid: self.populate_pivotObjects(arg1,pname.get(),piname.get(),ptname.get()))
        p_submit.grid(row=14,column=1,pady=4)

    def splitdata_param(self, event, uid):	
        self.header('Train-Test split')
        split_size = self.widget_entry('Split-size',row=3)
        split_size.insert(tk.END,0.7)
       		
        s_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda:controller.split_data(uid,split_size.get()))		
        s_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')

    def lda_param(self,event,uid):
        self.header('LDA')
        ndime = self.widget_spinbox('N-Dimensions',row=3,start=1,end=9)        
        u_keys = self.widget_listbox('UID',row=4,lbox=self.columns)        
        t_keys = self.widget_listbox('Target',row=5,lbox=self.columns)
        
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:controller.lda_dim(uid,ndime.get(),u_keys.get(),t_keys.get()))
        a_submit.grid(row=6,column=1,ipadx=3,ipady=2)

    def pca_param(self,event,uid):
        self.header('PCA')
        ndime = self.widget_spinbox('N-Dimensions',row=3,start=1,end=9)        
        u_keys = self.widget_listbox('UID',row=4,lbox=self.columns)        
        t_keys = self.widget_listbox('Target',row=5,lbox=self.columns)
        
        a_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command = lambda:controller.pca_dim(uid,ndime.get(),u_keys.get(),t_keys.get()))
        a_submit.grid(row=6,column=1,ipadx=3,ipady=2)
#==============================================================================
# Algorithm parameters
#==============================================================================
            
    def knn_param(self,event,uid):
        self.header('KNN')
        vlist = ['Classifier','Regressor']
        atypebox = self.widget_listbox('Type',row=2,lbox=vlist,c=0)        
        nnbe = self.widget_entry('Neighbours',row=3,balloon='Number of Neighbors')        
        leafn = self.widget_entry('Leaf size',row=4,balloon='leaf size between')
        njobe = self.widget_entry('N_Jobs',row=5,balloon='Number of Jobs')        
        
        submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda: controller.run_algos(uid,alg_type=atypebox.get(),n_neighbors=nnbe.get(),leaf_size=leafn.get(),n_jobs=njobe.get()))
        submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
            
        
    def svm_param(self,event,uid):
        self.header('SVM')
        vlist = ['Classifier','Regressor']
        atypebox = self.widget_listbox('Type',row=2,lbox=vlist,c=0) 
        nlist = ['True','False']              
        nnbe = self.widget_listbox('Shrinking',row=3,lbox=nlist,c=0,balloon='shrinking,Default=True')        
        leafn = self.widget_entry('Penalty parameter',row=4,balloon='C value to apply penalty')
        leafn.insert(0,1.0)            
        
        submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda: controller.run_algos(uid,alg_type=atypebox.get(),shrinking=bool(nnbe.get()),C=float(leafn.get())))
        submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
    

    def linear_param(self,event,uid):
        self.header('Linear Regression')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=vlist,c=1,balloon='Default is False')        
        hparam_n_box = self.widget_listbox('normalize',row=3,lbox=vlist,c=1,balloon='Parameter can be ignored when fit_intercept is set to False')        
        hparam_j_entry = self.widget_spinbox('n_jobs',row=4,start=-1,end=1,balloon='Number of jobs to use for computation\nDefault is 1')       
        
        linear_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,fit_intercept=hparam_f_box.get(),normalize=hparam_n_box.get(),n_jobs=int(hparam_j_entry.get())))
        linear_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)
            
            
    def ridge_param(self,event,uid):
        self.header('Ridge')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=vlist,c=1,balloon='Default is False')        
        hparam_n_box = self.widget_listbox('normalize',row=3,lbox=vlist,c=1,balloon='Parameter can be ignored when fit_intercept is set to False')        
        hparam_a_entry = self.widget_entry('alpha',row=4,balloon='Regularization strength, Must be a positive float \nDefault is 1.0')       

        ridge_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,fit_intercept=hparam_f_box.get(),normalize=hparam_n_box.get(),alpha=hparam_a_entry.get()))
        ridge_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)
            
    
    def lasso_param(self,event,uid):
        self.header('Lasso')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=vlist,c=1,balloon='Default is False')        
        hparam_n_box = self.widget_listbox('normalize',row=3,lbox=vlist,c=1,balloon='Parameter can be ignored when fit_intercept is set to False')                       
        hparam_a_entry = self.widget_entry('alpha',row=4,balloon='Regularization strength, Must be a positive float \n0 Is not advised')       

        lasso_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,fit_intercept=hparam_f_box.get(),normalize=hparam_n_box.get(),alpha=hparam_a_entry.get()))
        lasso_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
            
    def lars_param(self,event,uid):
        self.header('LARS')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=vlist,c=1,balloon='Default is False')        
        hparam_n_box = self.widget_listbox('normalize',row=3,lbox=vlist,c=1,balloon='Parameter can be ignored when fit_intercept is set to False')                       
        
        lars_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,fit_intercept=hparam_f_box.get(),normalize=hparam_n_box.get()))
        lars_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
            
            
    def elastic_param(self,event,uid):
        self.header('Elastic Net')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=vlist,c=1,balloon='Default is False')        
        hparam_n_box = self.widget_listbox('normalize',row=3,lbox=vlist,c=1,balloon='Parameter can be ignored when fit_intercept is set to False')                       
        hparam_a_entry = self.widget_entry('alpha',row=4,balloon='Measure of Regularization strength \n 0 is not advised')       
        hparam_l_entry = self.widget_entry('l1_ratio',row=5,balloon='0 <= l1_ratio <= 1')       

        enet_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,fit_intercept=hparam_f_box.get(),normalize=hparam_n_box.get(),alpha=hparam_a_entry.get(),l1_ratio=hparam_l_entry.get()))
        enet_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')

    def bayes_param_mlti(self,event,uid):
        self.header('Multinomial\nNaive Bayes')
        hparam_f_entry = self.widget_entry('alpha',row=2,balloon='Additive(Laplace/Lidstone)Smoothing parameter(0 for no smoothing)')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_prior',row=3,lbox=vlist,c=0,balloon='Default is True')        

        bayes_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,alpha=hparam_f_entry.get(),fit_prior=hparam_f_box.get()))
        bayes_submit.grid(row=4,column=1,ipadx=3,ipady=2,sticky='w')
            
    def bayes_param_gaussian(self,event,uid):
        self.header('Gaussian Naive Bayes')
        bayes_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium, command=lambda :controller.run_algos(uid))
        bayes_submit.grid(row=2,column=1,ipadx=3,ipady=2,sticky='w')

    def logistic_param(self,event,uid):
        self.header('Logistic Regression')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=vlist,c=1,balloon='Default is False')        
        nlist = ['l1','l2']
        hparam_n_box = self.widget_listbox('penalty',row=3,lbox=nlist,c=1,balloon='Specify the norm used in the penalization')                       
        hparam_c_entry = self.widget_entry('C',row=4,balloon='Inverse of regularization strength\nmust be a positive float')       
        hparam_c_entry.insert(tk.END,1.0)
        
        logistic_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda: controller.run_algos(uid,fit_intercept=hparam_f_box.get(),penalty=hparam_n_box.get(),C=hparam_c_entry.get()))
        logistic_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)

            
    def theilsen_param(self,event,uid):
        self.header('TheilSen')
        tlist = ['True', 'False']      
        tparam_f_box = self.widget_listbox('fit_intercept',row=2,lbox=tlist,c=0,balloon='Default is True')            
        
        tparam_m_box = self.widget_entry('max_subpopulation',row = 3,balloon='Instead of computing with a set of cardinality \n \'n choose k’, where n is the number of samples  \n and k is the number of subsamples \n (at least number of features), consider only a stochastic \n subpopulation of a given maximal size if \n ‘n choose k’ is larger than max_subpopulation.')
        tparam_m_box.insert(tk.END,10000.0)
        
        tparam_i_entry = self.widget_entry('max_iter',row=5,balloon='Maximum number of iterations for the calculation \n of spatial median.')        
        tparam_i_entry.insert(tk.END,300)
        
        tparam_t_entry = self.widget_entry('tol',row=6,balloon='Tolerance when calculating spatial median.')
        tparam_t_entry.insert(tk.END,0.001)
        theilsen_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                                    command=lambda :controller.run_algos(uid,fit_intercept=tparam_f_box.get(),max_subpopulation=tparam_m_box.get(),
                                                                         max_iter=tparam_i_entry.get(),tol=tparam_t_entry.get()))
        theilsen_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)
    


    def passagg_param(self,event,uid):
        def on_class_reg(index,value,op):
            try:
                pf_label.grid_forget()
                pf_box.grid_forget()
            except:
                pass
            finally:
                if ptypebox.get() == 'Regressor':
                    pe_label = tk.Label(self.param_frame,text='epsilon')
                    pe_label.grid(row=5,column=0,sticky='w',padx=2)
                    pe_entry = tk.Entry(self.param_frame,width=21)
                    pe_entry.grid(row=5,column=1,ipady=2,pady=2,sticky='w')
                    self.balloon.bind(pe_entry,'If the difference between the current prediction and \n the correct label is below this threshold,\n the model is not updated')
                    pe_entry.insert(tk.END,0.1)
                    
                    pl_label = tk.Label(self.param_frame,text='loss')
                    pl_label.grid(row=6,column=0,sticky='w',padx=2)
                    pl_box = ttk.Combobox(self.param_frame,width=21)
                    pl_box.grid(row=6,column=1,ipady=2,pady=2,sticky='w')
                    pl_box['values'] = ['epsilon_insensitive','squared_epsilon_insensitive']
                    self.balloon.bind(pl_box,'The loss function to be used: \n epsilon_insensitive: equivalent to PA-I in the reference paper.\n squared_epsilon_insensitive: equivalent to PA-II in the reference paper.')
                    p_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda: controller.run_algos(uid,alg_type=ptypebox.get(),C=pc_entry.get(),n_iter=pi_entry.get(),epsilon=pe_entry.get(),loss=pl_box.get()))
                    
                    p_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
                
                else:
                    pf_label = tk.Label(self.param_frame,text='fit_intercept',font=cambriamedium)
                    pf_label.grid(row=5,column=0,sticky='w',padx=2)
                    pf_box = ttk.Combobox(self.param_frame, state='readonly')
                    pf_box['values'] = ['True', 'False']
                    pf_box.current(1)
                    pf_box.grid(row=5,column=1,sticky='w',ipady=2,pady=2)
                    self.balloon.bind(pf_box, 'Default is False')
        
                    pcl_label = tk.Label(self.param_frame,text='loss')
                    pcl_label.grid(row=6,column=0,sticky='w',padx=2)
                    pcl_box = ttk.Combobox(self.param_frame,width=21)
                    pcl_box.grid(row=6,column=1,ipady=2,pady=2,sticky='w')
                    pcl_box['values'] = ['hinge','squared_hinge']
                    self.balloon.bind(pcl_box,'The loss function to be used: \n hinge: equivalent to PA-I in the reference paper.\n squared_hinge: equivalent to PA-II in the reference paper.')
                    p_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,command=lambda: controller.run_algos(uid,alg_type=ptypebox.get(),C=pc_entry.get(),n_iter=pi_entry.get(),fit_intercept=pf_box.get(),loss=pcl_box.get()))
                    p_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W')
                
        try:
            self.param_frame.destroy()
        except:
            pass
        finally:
            self.param_frame = tk.Frame(self.rightframe)
            self.param_frame.grid(row=2,column=0,sticky='W')
            r_label = tk.Label(self.param_frame,text='Passive Aggressive',font=bigbutton)
            r_label.grid(column=0,row=1,sticky='W',pady=5)
            
            ptype = tk.Label(self.param_frame,text='Type')
            ptype.grid(row=2,column=0,sticky='w',padx=2,pady=3)
            ptypevar = tk.StringVar()
            ptypevar.trace('w',on_class_reg)
            ptypebox = ttk.Combobox(self.param_frame,state='readonly',textvar=ptypevar)
            ptypebox['values'] = ('Regressor','Classifier')
#            ptypebox.current(0)            
            ptypebox.grid(row=2,column=1,ipady=2,pady=2,sticky='w')
            
            pc_label = tk.Label(self.param_frame,text='C')
            pc_label.grid(row=3,column=0,sticky='w',padx=2)
            pc_entry = tk.Entry(self.param_frame,width=21)
            pc_entry.grid(row=3,column=1,ipady=2,pady=2,sticky='w')
            self.balloon.bind(pc_entry,'Maximum step size (regularization). Defaults to 1.0.')
            pc_entry.insert(tk.END,1.0)
            
            pi_label = tk.Label(self.param_frame,text='n_iter')
            pi_label.grid(row=4,column=0,sticky='w',padx=2)
            pi_entry = tk.Entry(self.param_frame,width=21)
            pi_entry.grid(row=4,column=1,ipady=2,pady=2,sticky='w')
            self.balloon.bind(pi_entry,'The number of passes over the training data (aka epochs)')
            pi_entry.insert(tk.END,5)

    def gbm_param(self,event,uid):
        self.header('Gradient Boosting')
        vlist = ['Classifier','Regressor']
        gtypebox = self.widget_listbox('Type',row=2,lbox=vlist,c=0)        
        learn_entry = self.widget_entry('learning_rate',row=3,balloon='learning rate shrinks the contribution of each tree by learning_rate.')            
        learn_entry.insert(tk.END,0.1)
        est_entry = self.widget_entry('n_estimators',row=4,balloon='The number of boosting stages to perform')
        est_entry.insert(tk.END,100)
        
        mdepth_entry = self.widget_entry('max_depth',row=5,balloon='maximum depth of the individual regression estimators.\n The maximum depth limits the number of nodes in the tree.')        
        mdepth_entry.insert(tk.END,3)
        msample_entry = self.widget_entry('min_samples_split',row=6,balloon='The minimum number of samples required to split an internal node.')
        msample_entry.insert(tk.END,2)
        mleaf_entry = self.widget_entry('min_samples_leaf',row=7,balloon='The minimum number of samples required to be at a leaf node.')
        mleaf_entry.insert(tk.END,1)
      
        gbm_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                                    command=lambda :controller.run_algos(uid,alg_type=gtypebox.get(),learning_rate=learn_entry.get(),n_estimators=est_entry.get(),
                                                                         max_depth=mdepth_entry.get(),min_samples_split=msample_entry.get(),min_samples_leaf=mleaf_entry.get()))
        gbm_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)

    def ada_param(self,event,uid):
        self.header('AdaBoost')
        vlist = ['Classifier','Regressor']
        atypebox = self.widget_listbox('Type',row=2,lbox=vlist,c=0)        
        learn_entry = self.widget_entry('learning_rate',row=3,balloon='learning rate shrinks the contribution of each tree by learning_rate.')            
        learn_entry.insert(tk.END,1.0)
        est_entry = self.widget_entry('n_estimators',row=4,balloon='The number of boosting stages to perform')
        est_entry.insert(tk.END,50)
        
      
        ada_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                                    command=lambda :controller.run_algos(uid,alg_type=atypebox.get(),learning_rate=learn_entry.get(),n_estimators=est_entry.get()))
        ada_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)

    def extree_param(self,event,uid):
        self.header('Extra-Tree')
        vlist = ['Classifier','Regressor']
        gtypebox = self.widget_listbox('Type',row=2,lbox=vlist,c=0)        
        est_entry = self.widget_entry('n_estimators',row=3,balloon='The number of boosting stages to perform')
        est_entry.insert(tk.END,100)
        
        mdepth_entry = self.widget_entry('max_depth',row=4,balloon='maximum depth of the individual regression estimators.\n The maximum depth limits the number of nodes in the tree.')        
        mdepth_entry.insert(tk.END,3)
        msample_entry = self.widget_entry('min_samples_split',row=5,balloon='The minimum number of samples required to split an internal node.')
        msample_entry.insert(tk.END,2)
        mleaf_entry = self.widget_entry('min_samples_leaf',row=6,balloon='The minimum number of samples required to be at a leaf node.')
        mleaf_entry.insert(tk.END,1)
      
        extree_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                                    command=lambda :controller.run_algos(uid,alg_type=gtypebox.get(),n_estimators=est_entry.get(),
                                                                         max_depth=mdepth_entry.get(),min_samples_split=msample_entry.get(),min_samples_leaf=mleaf_entry.get()))
        extree_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)

    def decision_param(self,event,uid):
        self.header('Decision Trees')
        vlist = ['Classifier','Regressor']
        gtypebox = self.widget_listbox('Type',row=2,lbox=vlist,c=0)        
#        est_entry = self.widget_entry('n_estimators',row=3,balloon='The number of boosting stages to perform')
#        est_entry.insert(tk.END,100)
        
        mdepth_entry = self.widget_entry('max_depth',row=4,balloon='maximum depth of the individual regression estimators.\n The maximum depth limits the number of nodes in the tree.')        
        mdepth_entry.insert(tk.END,3)
        msample_entry = self.widget_entry('min_samples_split',row=5,balloon='The minimum number of samples required to split an internal node.')
        msample_entry.insert(tk.END,2)
        mleaf_entry = self.widget_entry('min_samples_leaf',row=6,balloon='The minimum number of samples required to be at a leaf node.')
        mleaf_entry.insert(tk.END,1)
      
        dec_submit = tk.Button(self.param_frame,text='Submit',font=cambriamedium,
                                    command=lambda :controller.run_algos(uid,alg_type=gtypebox.get(),max_depth=mdepth_entry.get(),
                                                                         min_samples_split=msample_entry.get(),min_samples_leaf=mleaf_entry.get()))
        dec_submit.grid(row=9,column=1,ipadx=3,ipady=2,sticky='W',pady=6)

    def bnaive_param(self,event,uid):
        self.header('Bernoulli Naive Bayes')
        alpha_val = self.widget_entry('alpha',row=2,balloon='Additive(Laplace/Lidstone)Smoothing parameter(0 for no smoothing)')
        vlist = ['True','False']
        hparam_f_box = self.widget_listbox('Fit priority',row=3,lbox=vlist,c=0,balloon='True to learn class prior probabilities')        

        bayes_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,alpha=alpha_val.get(),fit_prior=bool(hparam_f_box.get())))
        bayes_submit.grid(row=4,column=1,ipadx=3,ipady=2,sticky='w')
        
    def rforest_param(self,event,uid):
        self.header('Random Forest')
        atype = self.widget_listbox('Type',row=3,lbox=['Classifier','Regressor'])
        n_est = self.widget_entry('N-Estimators',row=4,balloon='no of trees in forest')
        m_depth = self.widget_entry('Max Depth',row=5,balloon='Depth of Tree')
        n_jobs = self.widget_spinbox('No of Jobs',row=6,start=-1,end=1)
        rf_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,alg_type=atype.get(),n_estimators=n_est.get(),max_depth=m_depth.get(),n_jobs=n_jobs.get()))
        rf_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='w')

    def sgd_param(self,event,uid):
        self.header('Gradient Descent')
        atype = self.widget_listbox('Type',row=3,lbox=['Classifier','Regressor'])
        plist = ['l1','l2','elasticnet']        
        penalty = self.widget_listbox('Penalty',row=4,lbox=plist)
        alpha = self.widget_entry('Alpha',row=5,balloon='Smoothing parameter')
        fit_icpt = self.widget_listbox('Fit Intercept',row=6,lbox=['True','False'])
        n_iter = self.widget_entry('N Iterations',row=7,balloon='no of iterations in training sample')
        rf_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,alg_type=atype.get(),penalty=penalty.get(),alpha=alpha.get(),fit_intercept=bool(fit_icpt.get()),n_iter=n_iter.get()))
        rf_submit.grid(row=8,column=1,ipadx=3,ipady=2,sticky='w')

    def perceptron_param(self,event,uid):
        self.header('Perceptron')
        plist = ['l2','l1','elasticnet']
        penalty_box = self.widget_listbox('penalty',row=3,lbox=plist,c=None)
        alpha_entry = self.widget_entry('alpha',row=4,balloon='Constant that multiplies the regularization term if\n regularization is used. Defaults to 0.0001')
        vlist = ['True','False']
        fit_box = self.widget_listbox('fit_intercept',row=5,lbox=vlist,c=0,balloon='If False, the data is assumed to be already centered.\n Defaults to True.')        
        iter_entry = self.widget_entry('n_iter',row=6,balloon='The number of passes over the training data')
        
        perceptron_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,penalty=penalty_box.get(),alpha=alpha_entry.get(),fit_intercept=bool(fit_box.get()),n_iter=iter_entry.get()))
        perceptron_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='w')

    def bayesridge_param(self,event,uid):
        self.header('Bayesian Ridge')
        iter_entry = self.widget_entry('n_iter',row=3,balloon='Maximum number of iterations')
        tol_entry = self.widget_entry('tol',row=4,balloon='Stop the algorithm if w has converged.\n Default is 1.e-3')
        vlist = ['True','False']
        compute_box = self.widget_listbox('compute_score',row=5,lbox=vlist,c=1,balloon='If True, compute the objective function at \n each step of the model. Default is False')
        fit_box = self.widget_listbox('fit_intercept',row=6,lbox=vlist,c=0,balloon='If set to false, no intercept will be used in calculations. \n Default is True.')        
        
        bayesridge_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,n_iter=iter_entry.get(),tol=tol_entry.get(),compute_score=bool(compute_box.get()),fit_intercept=bool(fit_box.get())))
        bayesridge_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='w')

    def omp_param(self,event,uid):
        self.header('OMP')
        nonzero_entry = self.widget_entry('n_nonzero_coefs',row=3,balloon='Desired number of non-zero entries in the solution.\n If None (by default) this value is set to 10% of n_features.')
        tol_entry = self.widget_entry('tol',row=4,balloon='Maximum norm of the residual.\n If not None, overrides n_nonzero_coefs.')
        vlist = ['True','False']
        fit_box = self.widget_listbox('fit_intercept',row=5,lbox=vlist,c=0,balloon='If set to false, no intercept will be used in calculations.')        
        
        omp_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.run_algos(uid,n_nonzero_coefs=nonzero_entry.get(),tol=tol_entry.get(),fit_intercept=bool(fit_box.get())))
        omp_submit.grid(row=7,column=1,ipadx=3,ipady=2,sticky='w')

    def importmodel_param(self,event,uid):
        self.header('Export Model')
        mlist = controller.fetch_models(uid,mtype='import')
    
        model_cur = self.widget_entry('Selected',row=4)
        mdl_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.model_imp(uid,model_cur.get()))
        mdl_submit.grid(row=5,column=1,ipadx=3,ipady=2,sticky='w')
        
        db_lbox = tk.Listbox(self.param_frame, width=20)  
        for r in mlist:
            db_lbox.insert(tk.END , r)
        db_lbox.grid(row=6,column=0,ipadx=3,ipady=3)
        def get_mname(e,wid):
            widget = e.widget
            selection=widget.curselection()
            value = widget.get(selection[0])
            wid.config(state='normal')
            wid.delete(0, 'end')
            wid.insert(tk.END,value)
            wid.config(state='disabled')
            print('current sel =',value)
#            return value
        
        db_lbox.bind("<<ListboxSelect>>",lambda e: get_mname(e,model_cur))
        
    def exportmodel_param(self,event,uid):
        self.header('Export Model')
        mlist = controller.fetch_models(uid,mtype='export')
        
        model_entry = self.widget_entry('Name',row=3)
        model_cur = self.widget_entry('Selected',row=4)
        mdl_submit = tk.Button(self.param_frame, text='Submit',font=cambriamedium,command=lambda :controller.model_exp(uid,model_entry.get(),model_cur.get()))
        mdl_submit.grid(row=5,column=1,ipadx=3,ipady=2,sticky='w')
        
        db_lbox = tk.Listbox(self.param_frame, width=20)  
        for r in mlist:
            db_lbox.insert(tk.END , r)
        db_lbox.grid(row=6,column=0,ipadx=3,ipady=3)
        
        def get_mname(e,wid):
            widget = e.widget
            selection=widget.curselection()
            value = widget.get(selection[0])
            wid.config(state='normal')
            wid.delete(0, 'end')
            wid.insert(tk.END,value)
            wid.config(state='disabled')
            print('current sel =',value)
#            return value
        
        db_lbox.bind("<<ListboxSelect>>",lambda e: get_mname(e,model_cur))
#        val = db_lbox.bind('<Button-1>',lambda e: e.widget.get(e.widget.curselection()[0]))
    
#==============================================================================
#     def chooseDb(self,event,vis):
#                 name = self.db_lbox.get(self.db_lbox.nearest(event.y))
#                 vis.dbname = name
#                 engine = vis.activate_db()
#                 self.dbwin.destroy()
#                 controller.visualize(engine,name)
#             
#==============================================================================
#==============================================================================
#     end of algm parameters    
#==============================================================================
    def empty_frame(self,uid):		
            print('Empty parameter caught with id',uid)		
            pass
        
    def parameter_frame(self,event,obj_id,name):
        print(name)
        try:		   
            self.create_wspace()
            getattr(self,operator_parameters[name])(event,obj_id)		
        except Exception as e:		
            print(str(e))		
            import traceback		
            print(traceback.format_exc())		
            		
            getattr(self,'empty_frame')(obj_id)		
            return 'Frame not found'

    def features_chk(self,feats,fuid,response):
        print(feats)
        if feats == []:
            controller.pops('Select Features')
        elif fuid == '':
            controller.pops('Select a Unique ID')
        elif response == '':
            controller.pops('Select a response')
        elif response in feats:
            controller.pops('Features and Target are same')
        else:
            self.coltab.destroy()
            controller.choices(feats,fuid,response)
                
    def model_chk(self,rad):
        try:
            rad = int(rad)
            self.modeltab.destroy()
            controller.run_alg(rad)
        except:
            controller.pops('Please select a proper model')
            
    def cv_score(self):
        from tabulate import tabulate
        acc_score = controller.model_accuracy()
        acc_score = tabulate(acc_score.items(),headers=['Algorithm','Score'],tablefmt="fancy_grid")
        text = tk.Text(self.param_frame,width=28,height=18,bd=1,relief='solid')
        text.insert(tk.INSERT,acc_score)        
        text.configure(state='disabled',wrap="none")
        text.grid(row=4,column=0,padx=3,sticky="NEWS")
#        self.score_lab = tk.Label(self.param_frame,text=acc_score)
#        self.score_lab.grid(column=0,row=8,sticky='W')
    
    def mse_score(self):
        acc_score = controller.mean_squared_error()
        self.score_lab = tk.Label(self.param_frame,text=acc_score)
        self.score_lab.grid(column=0,row=8,sticky='W')
                
    def features_window(self,uid):
        self.coltab = tk.Toplevel(self.rightframe,highlightthickness=0)
        self.coltab.iconbitmap(bitimage)
        self.coltab.geometry('800x650')
        columns = self.columns
#        self.feteng_frame = tk.Frame(self.coltab,highlightthickness=0,height=600,width=500)
#        self.feteng_frame.grid(row=1,column=0,sticky='NW')
        self.features_frame = tk.Frame(self.coltab,bd=1,height=600,width=500)
#        self.features_frame.grid_columnconfigure(0,weight=1)
        self.features_frame.grid(column=0,row=0,sticky='WE')    
        #self.unique_frame = tk.Frame(self.feteng_frame,bd=1,height=500,width=150)
        #self.target_frame = tk.Frame(self.feteng_frame,bd=1,height=500,width=150)
        #self.unique_frame.grid(column=1,row=1)
        #self.target_frame.grid(column=2,row=1)
        flabel = tk.Label(self.features_frame,text="Features",font=('Goudy old style',16,'bold'))
        flabel.grid(row=0,column=0,sticky='NW')
        ulabel = tk.Label(self.features_frame,text="Unique ID",font=('Goudy old style',16,'bold'))
        ulabel.grid(row=0,column=1,sticky='NW')
        tlabel = tk.Label(self.features_frame,text="Target",font=('Goudy old style',16,'bold'))
        tlabel.grid(row=0,column=2,sticky='NW')
            
        for win in self.features_frame.winfo_children():
            win.grid(padx=30,pady=10)
            
        self.fcanvas=tk.Canvas(self.features_frame,height=500,width=280)
        self.fcanvas.grid(row=1,column=0)
        self.column_frame = tk.Frame(self.fcanvas,highlightthickness=0)
        self.column_frame.grid(row=0,column=0,sticky='WE')

        featscroll = ScrollBar()
#        horz = featscroll.add_hbar(self.features_frame,self.fcanvas,3,0)
        vert = featscroll.add_vbar(self.features_frame,self.fcanvas,1,0)
        featscroll.activate_scrollbar(self.fcanvas,vbar=vert)

        def checkbox_chk():
            for i,item in enumerate(check_box):
                if feat[i].get():
                    if item['text'] not in self.checked_item:
#                        print(item['text'],'\n==========')
                       self.checked_item.append(item['text'])
                elif feat[i].get() ==0:
                    if item['text'] in self.checked_item:
                        self.checked_item.remove(item['text'])
        def select_all(status):
            for ix in range(len(check_box)):
                if status==1:
                    check_box[ix].select()
                elif status == 0:
                    check_box[ix].deselect()
            print('status=',status)
#==============================================================================
# Features
#==============================================================================
#        self.checked_item = tk.StringVar()
        self.checked_item = []
        check_box=[]
        feat = []
        selectall = tk.IntVar()
        for ix,item in enumerate(columns):
            feat.append(tk.IntVar())
            check_box.append(tk.Checkbutton(self.column_frame, text=item, variable=feat[ix],state='normal',command=checkbox_chk))
            check_box[ix].grid(row=ix+2,column=0,sticky='W')
            check_box[ix].deselect()
        
        all_cb = tk.Checkbutton(self.column_frame, text='Select-all', variable=selectall,state='normal',command=lambda :select_all(selectall.get()))
        all_cb.grid(row=ix+4,column=0,sticky='W')
        all_cb.deselect()
#        if self.feat.get():
#            if self.feat.get() not in self.checked_item:
#                self.checked_item.append(self.feat.get())            
    
#==============================================================================
# Unique ID    
#==============================================================================
        self.fuid = tk.Variable()
        unikey = ttk.Combobox(self.features_frame, width=20, textvariable=self.fuid, state='normal')
        unikey['values'] = columns 
        unikey.grid(column=1, row=1, sticky='NW',padx=8,pady=2)              
        unikey.current()

#==============================================================================
# Target Variable
#==============================================================================
        self.response = tk.Variable()
        Chosen = ttk.Combobox(self.features_frame, width=20, textvariable=self.response, state='normal')
        Chosen['values'] = columns 
        Chosen.grid(column=2,row=1,sticky='NW',padx=8,pady=2)              
        Chosen.current()
        
        self.choicebutton = tk.Button(self.features_frame, text="Submit",font=cambriabig, command = lambda: self.features_chk(self.checked_item,self.fuid.get(),self.response.get()))
        self.choicebutton.grid(column=1,row=4,sticky='NW')
        
        self.fcanvas.create_window((4,4),window=self.column_frame)
        self.column_frame.bind("<Configure>",self.scrollevent)
    
    def scrollevent(self,e):
        self.fcanvas.configure(scrollregion=self.fcanvas.bbox("all"))
    
    def model_window(self):
        try:
            self.modeltab = tk.Toplevel(self.rightframe,bd=0,highlightthickness=0)
            self.modeltab.iconbitmap(bitimage)
            self.modeltab.geometry('800x650')
            self.model_frame = tk.LabelFrame(self.modeltab,bd=0,highlightthickness=0)
            self.model_frame.grid(column=0,row=1,sticky='WE')
            
            self.coltab.destroy()
            tk.Label(self.model_frame,text='Select a model',font=('Goudy old style',18,'bold')).grid(row=1,column=0)
            self.radvar = tk.StringVar()
            self.radvar.set(None)
            for i in range(len(leftcol)):
                lcol = tk.Radiobutton(self.model_frame, text="{}".format(leftcol[i]),font=("Times",12),variable=self.radvar, value=i)
                lcol.grid(column=0, row=i+3,sticky='W')
            
            for j in range(len(rightcol)):
                rcol = tk.Radiobutton(self.model_frame, text="{}".format(rightcol[j]),font=("Times",12),variable=self.radvar, value=j+50)
                rcol.grid(column=1, row=j+3, sticky='W')

#            allcol = tk.Radiobutton(self.model_frame,text='All models',variable=self.radvar,value=100)
#            allcol.grid(column=1,row=len(rightcol)+3,sticky='W')            
#==============================================================================
#             def confirm(self):
#                 from tkinter import messagebox as mbox
#                 answer = mbox.askyesno("confirm","Are you sure to save the session?")
#                 if answer == True:
#                     self.session_save.config(state=tk.DISABLED,command=Controller.save(self))
#                 else:
#                     self.session_save.deselect()
#                 
#             self.session_save = tk.Checkbutton(self.model_frame,text = "Save my session",command =lambda: confirm(self))
#             self.session_save.grid(column=2,row=5)
#==============================================================================
            self.runbutton = tk.Button(self.model_frame, text="Run",font=cambriamedium, command = lambda: self.model_chk(self.radvar.get()))
            self.runbutton.grid(column=2,row=7)

        except Exception as e:
            print(str(e))
            controller.pops('Select Features to\n run model')
            pass
            
#==============================================================================
#                               Middle Frame
#==============================================================================
      
class MiddleFrame(tk.Frame):
    def __init__(self,parent,rf1):
        tk.Frame.__init__(self,parent)
        self.mainframe = parent
        self.rf = rf1
        self.imageslist = []
        self.lineobjects = dict()
        self.imagecoordinates = dict()
        
        self.mid_frame = tk.Frame(self.mainframe,height=600)
        self.mid_frame.grid(row=1,column=1,sticky='N')
        self.design_frame = tk.Frame(self.mid_frame,relief='solid',bd=1,height=600)
        self.design_frame.grid(row=1,column=1,sticky='N')
        self.result_frame = tk.Frame(self.mid_frame,relief='solid',bd=1,height=600)
        self.designcanvas = tk.Canvas(self.design_frame,width=800,height=580,bg='white')
        self.designcanvas.grid(sticky='N')
        self.output_obj()
        self.resultnb = tk.Frame(self.result_frame,width=800,height=580,bg='white')
#        self.resultcanvas.create_text(50,50,text='This is result tab',tag='empty')
        self.resultnb.grid(sticky='N')        
        self.result_frame.bind("<Button-3>",self.right_click)
        
    def design_tab(self):
        self.result_frame.grid_forget()
        self.design_frame.grid(row=1,column=1)
            
    def result_tab(self,result=None):
        self.design_frame.grid_forget()
        self.result_frame.grid(row=1,column=1)
    
    def output_obj(self):
#        obj_id = self.designcanvas.create_oval(750, 220, 780,250, fill="black", outline="#DDD", width=4)
        operator_icon = self.create_image('output')
        self.imageslist.append(operator_icon)
        obj_id = self.designcanvas.create_image(750,250,image=operator_icon) 
#        self.imagecoordinates[obj_id] = (x,y)        
        alloperatorobjects[obj_id] = {'function':wicon.Output(obj_id)} 
        self.designcanvas.tag_bind(obj_id,'<Button-3>',lambda e:self.draw_line(e,obj_id))

    def create_image(self,name):
        icon = tk.PhotoImage(file=workflow_images+"{}.png".format(name))
        return icon            
            
    def update_coords(self,obj_id,x,y):
        alloperatorobjects[obj_id]['function'].xcoord = x
        alloperatorobjects[obj_id]['function'].ycoord = y
        
    def display_result(self,df,stats):
        from tabulate import tabulate
        tabulated_data = tabulate(df,headers=[col for col in df.columns],tablefmt="fancy_grid")
        stats_data = tabulate(stats,headers=[col for col in stats.columns],tablefmt="fancy_grid")
        resultic = tk.Frame(self.resultnb)
        resultds = tk.Frame(self.resultnb,width=720,height=600)
        resultic.grid(row=0,column=0)
        resultds.grid(row=0,column=1)
        def preview():
            data_button.config(state='disabled')
            stats_button.config(state='active')
            text = tk.Text(resultds,width=85,height=35)
            text.insert(tk.INSERT,tabulated_data)
            text.configure(state='disabled',wrap="none")
            text.grid(row=1,column=1,sticky="NEWS")
            resultscroll = ScrollBar()
            horz = resultscroll.add_hbar(resultds,text,3,1)
            vert = resultscroll.add_vbar(resultds,text,1,2)
            resultscroll.activate_scrollbar(text,horz,vert)

        def describe():
            stats_button.config(state='disabled')
            data_button.config(state='active')
            text = tk.Text(resultds,width=85,height=35)
            text.insert(tk.INSERT,stats_data)
            text.configure(state='disabled',wrap="none")
            text.grid(row=1,column=1,sticky="NEWS")
            resultscroll = ScrollBar()
            horz = resultscroll.add_hbar(resultds,text,3,1)
            vert = resultscroll.add_vbar(resultds,text,1,2)
            resultscroll.activate_scrollbar(text,horz,vert)
        
        data_icon = tk.PhotoImage(file = frame_images+"data-icon.png")
        stats_icon = tk.PhotoImage(file = frame_images+"stats-icon.png")
        data_button = tk.Button(resultic,text='Data',image=data_icon,compound='top',command=preview)
        data_button.image = data_icon
        data_button.grid(column=0,row=1,pady=2)
        stats_button = tk.Button(resultic,text='Stats',image=stats_icon,compound='top',command=lambda: describe())
        stats_button.image = stats_icon
        stats_button.grid(column=0,row=2,pady=2)        
        
        
            
    def rank_extraction(self,rank,cols):
        self.rank_frame = tk.Toplevel()
        tv = ttk.Treeview(self.rank_frame)
        tv['columns'] = ('column','rank')
        tv.heading('#0',text='',anchor='w')
        tv.column('#0',anchor='w',width=0)
        tv.heading('column',text='Attribute Name')
        tv.column('column',anchor='center',width=170)
        tv.heading('rank',text='Ranking')
        tv.column('rank',anchor='center',width=70)
        tv.grid(sticky=('N,S,W,E'))
        for r,c in sorted(zip(rank,cols),key=operator.itemgetter(0)):
            tv.insert('','end',values=(c,r))
            
    def right_click(self,event):
        print('this is right click')
#        View.editMenu.post(e.x,e.y)
        
            
    def genRandomCoordinates(self):
        import random
        def duplicateExists(d,v):
            for k in d:
                if d[k] == v:
                    return True
            return False
        x = random.randint(50,680)
        y = random.randint(50,450)
        
        while duplicateExists(self.imagecoordinates,(x,y)):
            x = random.randint(50,680)
            y = random.randint(50,450)
            
        return x,y
        
    def drag_n_drop(self,e,obj_id):
        self.designcanvas.coords(obj_id,e.x,e.y)
        self.update_coords(obj_id,e.x,e.y)
        self.imagecoordinates[obj_id]=(e.x,e.y)

    def draw_line(self,event,object_id):
        def on_motion(event,lineid):
            x2 = event.x
            y2 = event.y
            self.designcanvas.coords(lineid,x1,y1,x2,y2)
            self.designcanvas.bind('<Button-3>',lambda e: self.on_drop_line(e,lineid,object_id,x1,y1))
        x1 = event.x
        y1 = event.y
        lineid = self.designcanvas.create_line(x1,y1,x1+1,y1+1,arrow='last',tag=object_id)
        print('lineid=',lineid)
        self.designcanvas.bind('<Motion>',lambda e:on_motion(e,lineid))
        

    def on_drop_line(self,event,lineid,object_id,x1,y1):
        drop_id=self.designcanvas.find_closest(event.x,event.y, halo=3, start=lineid)
        if drop_id[0]==lineid:
            self.designcanvas.delete(lineid)
        else:
            self.lineobjects[lineid] = [x1,y1,event.x,event.y]
            alloperatorobjects[drop_id[0]]['function'].inputList.append(object_id)
            print(str(object_id)+"->"+str(drop_id[0]))
        self.designcanvas.unbind('<Motion>')
        self.designcanvas.unbind('<Button-3>')       
        self.designcanvas.tag_bind(lineid,'<Button-2>',lambda e:self.delete_line(e,lineid,drop_id[0],object_id))
        
    def create_display_object(self,name,tag_name=None):
        if tag_name is not None:
            if tag_name == 'algos':
                operator_icon = self.create_image('algorithm')
            else:
                operator_icon = self.create_image(name)
            self.imageslist.append(operator_icon)
            x,y = self.genRandomCoordinates()
            obj_id = self.designcanvas.create_image(x,y,image=operator_icon,tag=name) 
            self.imagecoordinates[obj_id] = (x,y)
            alloperatorobjects[obj_id]={'function':getattr(globals()[tag_name],operator_fns[name])(obj_id)}        
            self.update_coords(obj_id,x,y)        
            self.activate_features(self.designcanvas,obj_id,name)
            self.rf.balloon.tagbind(self.designcanvas,obj_id,name)
            return obj_id
        else:
            raise 'TagError'
    
    def delete_line(self,e,line_id,dropid,objectid):
        try:
            print('in line delete',line_id)
            self.designcanvas.delete(line_id)
            self.lineobjects.pop(line_id,None)
            alloperatorobjects[dropid]['function'].inputList.remove(objectid)
        except:
            pass
        
        
    def delete_image(self,e,obj_id):
        self.designcanvas.delete(obj_id)
        alloperatorobjects.pop(obj_id,None)
        self.imagecoordinates.pop(obj_id,None)
        

    def name_to_save(self,ext='dsf'):
        ptypes = [('Process', '*.{}'.format(ext))] 
        odir = processes_dir
        sname = fd.asksaveasfilename(initialdir=odir,filetypes = ptypes)
        if sname:
            self.save_process(sname)
        
    def activate_features(self,canvas,tag,name):
        canvas.tag_bind(tag,'<B1-Motion>',lambda e:self.drag_n_drop(e,tag))
        canvas.tag_bind(tag,'<Button-2>',lambda e:self.delete_image(e,tag))
        canvas.tag_bind(tag,'<Double-Button-1>',lambda e:self.rf.parameter_frame(e,tag,name))        
        canvas.tag_bind(tag,'<Button-3>',lambda e:self.draw_line(e,tag))
        
        
    def save_process(self,name):
        from klepto.archives import file_archive as klp
        obj_items = {}
        klw = klp('{0}.dsf'.format(name))
        for objs,val in alloperatorobjects.items():
            obj_items[objs] = val['function']
        klw['line'] = self.lineobjects
        klw['objs'] = obj_items
        klw.dump()
        del klw
        
    def execute_process(self):
        from klepto.archives import file_archive as klp   
        ptypes = [('Process', '*.dsf')] 
        edir = processes_dir
        name = fd.askopenfilename(initialdir=edir,filetypes=ptypes)
        klr = klp(name)
        klr.load()
        self.draw_workflow(klr)
        
    def draw_workflow(self,wf_dict):
        wobject = wf_dict.get('objs')
        lobject = wf_dict.get('line')
        for k,v in wobject.items():
            if k ==1:
                alloperatorobjects[k]= {'function': v}
            else:
                img_name = vars(v).get('image')
                x = vars(v).get('xcoord')
                y = vars(v).get('ycoord')
                imgs = self.create_image(img_name)
                self.imageslist.append(imgs)
                obj_id = self.designcanvas.create_image(x,y,image=imgs)
                self.imagecoordinates[obj_id] = (x,y)
#        #            self.create_line_bindings(img_id)
                self.activate_features(self.designcanvas,obj_id,img_name)
                alloperatorobjects[obj_id] = {'function': v}
        for k,v in lobject.items():
            self.designcanvas.create_line(v[0],v[1],v[2],v[3],arrow='last')
            
#==============================================================================
#                              left frame
#==============================================================================
class LeftFrame(tk.Frame):
    def __init__(self,parent,mf1):
        tk.Frame.__init__(self,parent)
        self.mainframe = parent
        self.mf = mf1
        self.left_frame = tk.LabelFrame(self.mainframe,height=40)
        self.left_frame.grid(row=1,column=0,sticky='NW')
        self.create_repository_tree()
        self.create_operator_tree()
    
    def create_repository_tree(self):
        add_icon = tk.PhotoImage(file=frame_images+"add-data.png")
        add_btn = tk.Button(self.left_frame,image=add_icon,text='Add Data',font=cambriabig,width=190,height=30,compound='left',relief='groove',command=self.add_data)
        add_btn.image = add_icon        
        add_btn.grid(row=0,column=0,ipadx=3,ipady=2,sticky='NW')
        self.style = ttk.Style()
        self.style = self.style.configure("Treeview", font=cambriamedium)
        self.localrepo = ttk.Treeview(self.left_frame,show='tree')
        self.localrepo.grid(row=1,column=0)
        self.localrepo.tag_configure('local')
        counter=0
        self.localrepo.insert("",index=0,iid="local", text="Local Repository")
        for root,dirs,files in os.walk(localrepository):
            counter = counter+1
            subdir = os.path.basename(root)
            self.localrepo.insert("local",iid=subdir,text=subdir,index=counter)
                        
            for f in files:
                docs = os.path.abspath(os.path.join(root,f))
                self.localrepo.insert(subdir,text=f,index=files.index(f),tags=['licon',docs])
        self.localrepo.tag_bind('licon',"<Double-Button-1>",lambda e:self.get_repo_path(e))

    def add_repo(self):
        self.repoframe = tk.Toplevel()
        name_label = tk.Label(self.repoframe, text = 'Repository Name',font=('Arial', 13))
        name_label.grid(row = 0, column = 0, sticky = 'w')
        name_entry = tk.Entry(self.repoframe, width = 20)
        name_entry.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = 'w')
        btn = tk.Button(self.repoframe,text='Ok',command=lambda:self.repo(name_entry.get()))
        btn.grid(row=2,column=0,ipadx=3)
#        nametosave = mbox.askquestion('create','Repository Name')
#        nametosave = tk.simpledialog.askstring('Repository Name')

    def repo(self,name):
        self.repoframe.destroy()
        os.chdir(localrepository)
        if name:
            if not os.path.exists(name):
                os.makedirs(name)
            else:
                controller.pops('Name already exists')
        else:
            controller.pops('Select a name')
        importlib.reload(self.create_repository_tree())
        
    def add_data(self):
        self.choose_top = tk.Tk()
        self.choose_top.iconbitmap(bitimage)
        self.choose_top.title('DSF')
#        self.choose_top.geometry('780x600')
        self.choose_top.resizable(height=False,width=False)
        self.choose_top.focus()        
        self.choose_top.grab_set()
        self.choose_frame = tk.Frame(self.choose_top)
#        self.choose_frame.pack(side='top',fill='both',expand=True)
        self.choose_frame.grid()
        choose_frame = tk.Frame(self.choose_frame,bg='white')
        choose_frame.grid(row=1,column=2,columnspan=4)
        label = tk.Label(choose_frame,text='Choose the data from',bg='white',font=('cambria',24))
        label.grid(row=0,column=0,padx=250,pady=20,sticky='w')
        mid_frame = tk.Frame(self.choose_frame,background='orange')
        mid_frame.grid(row=2,column=1,columnspan=6,sticky="WE",pady=100)
        computer = tk.Button(mid_frame,text='My Computer',width=20,height=1,font=('cambria',20),command=lambda:self.store_local('computer'))
        computer.grid(row=5,column=2,ipady=2,sticky='W',padx=30,pady=100)
        db = tk.Button(mid_frame,text='Database',width=20,height=1,font=('cambria',20),command=lambda:self.store_local('database'))
        db.grid(row=5,column=5,ipady=2,pady=150,sticky='W',padx=30)

    def store_local(self,datasrc):
        rd = AddData(self.choose_top)
        if datasrc =='computer':
            rd.create_pcgui()
        elif datasrc == 'database':
            rd.create_dbgui()
        self.choose_frame.destroy()

#==============================================================================
# Operator- TreeView        
#==============================================================================
    def create_operator_tree(self):
        self.operator = ttk.Treeview(self.left_frame,show='tree',height=16)
#        self.operator.config(font=cambriamedium)
        self.operator.grid(row=2,column=0,pady=10)
#==============================================================================
#       Data Access Tree        
#==============================================================================
        self.operator.insert("",index=0,iid="da", text="Read")
        self.operator.insert("da",index=1,text="CSV",tag='wicon')
        self.operator.insert("da",index=2,text="Json",tag='wicon')
        self.operator.insert("da",index=3,text="Excel",tag='wicon')
        self.operator.insert("da",4,text="Database")
#==============================================================================
#       Cleansing
#==============================================================================
        self.operator.insert("",index=1,iid="cleansing", text="Cleanse")

#        self.operator.insert("cleansing",0,"duplicate",  text="Duplicates")
#        self.operator.insert("duplicate",index="end",text="Remove Duplicates")

        self.operator.insert("cleansing",1,"restrict",  text="Restrict")
        self.operator.insert("restrict",0,"filter",  text="Filter",tag='wicon')

        self.operator.insert("cleansing",2,"missing",  text="Missing")
        self.operator.insert("missing",0,"end",text="Auto Replace",tag='wicon')
        self.operator.insert("missing",1,text="Manual Replace",tag='wicon')

        self.operator.insert("cleansing",3,"normalize",  text="Scaler")   
        self.operator.insert("normalize",0, text="Normalize",tag='wicon')
        self.operator.insert("normalize",1, text="Standardize",tag='wicon')
        self.operator.insert('cleansing',4,text='Duplicate',tag='wicon')
        self.operator.insert('cleansing',5,text='Remove Nulls',tag='wicon')
        self.operator.insert('cleansing',5,text='Text Preprocess',tag='wicon')

        
#==============================================================================
#       Blending
#==============================================================================
        self.operator.insert("",index=2,iid="blending", text="Blend")
#        self.operator.insert("blending",0,"conversion", text="Conversions")
#        self.operator.insert("conversion",index="end",text="Number to date")
#        self.operator.insert("conversion",index="end",text="Date to number")
#        
#        self.operator.insert("blending",4,"group", text="Group")
        self.operator.insert('blending',index=1,text="Uid Generator",tag='wicon')
        self.operator.insert("blending", index=2, text="Raw Script",tag='wicon')
        self.operator.insert("blending",index=5, text="Aggregate",tag='wicon')

        self.operator.insert("blending",3,"join", text="Joins")
#        join = ["Append","Intersect","Join","Union"]
        self.operator.insert("blending",0,'append', text="Append", tag='wicon')
        join = ["Join"]
        for i in join:
            self.operator.insert("join",index="end",text=i,tag='wicon')
#==============================================================================
#       Wrangling 
#==============================================================================
        self.operator.insert("",index=3,iid='wrangling',text='Wrangle')
        self.operator.insert('wrangling',0,text='Extend Columns',tag='wicon')

#==============================================================================
#       Reshaping
#==============================================================================
#>>>>>>>>>>>>>>>>>>>>>
        self.operator.insert("", index=4, iid="reshaping", text="Reshape")
        
        self.operator.insert("reshaping",1,"sort",text="Sort",tag='wicon')
        
        self.operator.insert("reshaping",2,"transpose",text="Transpose",tag='wicon')
        
        self.operator.insert("reshaping",3,"pivot",text="Pivot",tag='wicon')
            
#==============================================================================
#           Dimensionality Reduction
#==============================================================================
        self.operator.insert("reshaping",index=4,iid="dimred", text="Dimensionality Reduction")
        self.operator.insert("dimred",0,text="PCA",tag='wicon')
        self.operator.insert("dimred",1,text="LDA",tag='wicon')
        

#==============================================================================
#       Feature Engineering
#==============================================================================
        self.operator.insert("",index=5,iid="feature", text="Feature Engineering")
        self.operator.insert("feature",0,"feature_selection",text="Feature Selection")
        self.operator.insert("feature_selection",index="end",text='Recommend',tag='wicon')

        self.operator.insert("feature",1,"weights", text="Weight")
        self.operator.insert("weights",index="end",text='Manual',tag='wicon')
        self.operator.insert("feature",2, text="Split",tag='wicon')
#        feature_selection=["Forward Selection","Backward Elimination","Optimize Selection","Optimize Selection (Brute Force)",
#                           "Optimize Selection (Wieght Guided)","Optimize Selection (Evolutionary)"]
#        for i in feature_selection:
#            self.operator.insert("feature_selection",index="end",text=i)
                           
#==============================================================================
#       Modelling        
#==============================================================================
        self.operator.insert("",index=6,iid="modelling", text="Models")
        self.operator.insert("modelling",1,"ib",text='InstanceBased')
        self.operator.insert('modelling',2,'ik',text='Regression')
        self.operator.insert('modelling',3,'reg',text='Regularization')
        self.operator.insert('modelling',4,'nb',text='Bayesian')
        self.operator.insert('modelling',5,'enb',text='Ensemble')
        self.operator.insert("modelling",6,"importmodel",text='Import Model',tag='wicon')
        self.operator.insert("modelling",7,"exportmodel",text='Export Model',tag='wicon')
        self.operator.insert("modelling",8,"Predictive",text='Predictive',tag='wicon')
            
        for c in instance_based.keys():
            self.operator.insert("ib",index="end",text=c,tags=['algos','wicon'])
        
        for r in regressors.keys():
            self.operator.insert('ik',index='end',text=r,tags=['algos','wicon'])
        
        for reg in regularizer.keys():
            self.operator.insert('reg',index='end',text=reg,tags=['algos','wicon'])
            
        for nb in bayesian.keys():
            self.operator.insert('nb',index='end',text=nb,tags=['algos','wicon'])
        
        for enb in ensemble.keys():
            self.operator.insert('enb',index='end',text=enb,tags=['algos','wicon'])
#==============================================================================
#       Confidences                
#==============================================================================
#        self.operator.insert("",index=5,iid="confidence", text="Confidences")
#        confidence = ["Rescale Confidences","Drop Predictions","Generate Prediction","Generate Prediction Ranking"]
#        for i in confidence:
#            self.operator.insert("confidence",index="end",text=i)


#==============================================================================
#       Validation Performance         
#==============================================================================
        self.operator.insert("",index=7,iid="validation", text="Validate")
        self.operator.insert("validation",0,text='Cross Validate',tag='wicon')
        self.operator.insert("validation",1,text='MSE',tag='wicon')
        

#        wbutton = tk.Button(self.left_frame, text="Create \nworkflow")
#        wbutton.grid(pady=2,ipadx=10,ipady=1)
        
#==============================================================================
#        write CSV
#==============================================================================
        self.operator.insert("",index=8,iid="write", text="Write")
        self.operator.insert("write",1,text="To File",tag='wicon')
        self.operator.insert("write",2,text="To Database",tag='wicon')
        self.operator.insert("write",3,text="Visualize",tag='wicon')

        oscroll = ScrollBar()
#        horz = oscroll.add_hbar(self.left_frame,self.operator,3,0)
        vert = oscroll.add_vbar(self.left_frame,self.operator,2,1)
        oscroll.activate_scrollbar(self.operator,vbar=vert)

        self.operator.insert("",index=9,iid="cv", text="Computer Vision")
        self.operator.insert("cv",1,text="Image Process",tag='wicon')
        self.operator.insert("cv",2,text="LSTM",tag='wicon')
        self.operator.tag_bind('wicon',"<Double-Button-1>",lambda e:self.get_op_name(e))
        
        self.operator.insert("",index=10,iid="sh", text="Automation")
        self.operator.insert("sh",1,text="Super Hack",tag='wicon')

    def get_op_name(self,event):
        op_id = self.operator.focus()
        op_name = self.operator.item(op_id,'text')
        tag_name = self.operator.item(op_id,'tags')[0]
        self.mf.create_display_object(op_name,tag_name)
    
    def get_repo_path(self,event):
        op_id = self.localrepo.focus()
        op_name = self.localrepo.item(op_id,'tags')[1]
        obj_id = self.mf.create_display_object('loadrepo','wicon')
        alloperatorobjects[obj_id]['function'].filepath = op_name
        
        
        
class ScrollBar:
    @staticmethod
    def add_hbar(frame,item_name,row=1,col=0):
        xsb = ttk.Scrollbar(frame,orient=tk.HORIZONTAL,command=getattr(item_name,'xview'))
        xsb.grid(row=row,column=col,sticky='EW')
        return xsb
        
    @staticmethod
    def add_vbar(frame,item_name,row=2,col=1):
        ysb = ttk.Scrollbar(frame,orient=tk.VERTICAL,command=getattr(item_name,'yview'))
        ysb.grid(row=row,column=col,sticky='NS')
        return ysb
        
    @staticmethod    
    def activate_scrollbar(item_name,hbar=None,vbar=None):
        if hbar is not None:
            arg1 = getattr(hbar,'set')
        else:
            arg1 = None
            
        if vbar is not None:
            arg2 = getattr(vbar,'set')
        else:
            arg2 = None
        
        getattr(item_name,'configure')(xscrollcommand=arg1,yscrollcommand=arg2)
        
class Controller:
    def __init__(self):
        self.fh = FileHandle()
        self.models_name = {}
#==============================================================================
# play button
#==============================================================================

    def pops(self,message):
        mbox.showinfo(title="Dsf",message="{}".format(message))

    def update_dataframe(self,df):
        stats = df.describe()            
        self.rframe.rf.columns = [col for col in df.columns]
        self.rframe.display_result(df[:100],stats)
        self.fh.raw_data = df

        
    def on_run(self,rframe,alloperatorobjects):
        self.rframe = rframe
        try:
            self.recursive_algo(1)
            df = alloperatorobjects[1]['function'].dfs[alloperatorobjects[1]['function'].inputList[0]]
            self.update_dataframe(df)
        except Exception as e:
            print(str(e))
            self.pops('please select valid Data')
        
        
    def recursive_algo(self, uid):
        try:
            if not alloperatorobjects[uid]['function'].is_list_empty():
                for i in range(len(alloperatorobjects[uid]['function'].inputList)):
                    alloperatorobjects[uid]['function'].dfs[alloperatorobjects[uid]['function'].inputList[i]] = self.recursive_algo(alloperatorobjects[uid]['function'].inputList[i])
            return alloperatorobjects[uid]['function'].get_dataframe()
        except:
            pass
#            self.pops('Data not valid!!')
            
    def choices(self,feats,uid,response):
        self.fh.features=feats
        self.fh.uid = uid
        self.fh.response = response  
        df = self.fh.categorize(uid,self.fh.raw_data)
        self.update_dataframe(df)
                    
    def split_data(self,uid,size):
        try:
            print(self.fh.raw_data.head(20))
            X_train,y_train,self.X_test,self.y_test,self.z_test = self.fh.train_test_split(size)  
            algos.X_train = X_train
            algos.y_train = y_train
            algos.X_test = self.X_test
            
        except Exception as e:
            print(str(e))
            self.pops('data contains missing values')
    
    def lda_dim(self, obj_id,ncomp,uid,target):
        try:
            print(ncomp,uid,target)
            alloperatorobjects[obj_id]['function'].dimension=ncomp
            self.fh.uid = uid   
            self.fh.response = target
            self.fh.features = ['Lda']            
            X = self.fh.categorize(uid,self.fh.raw_data[self.fh.raw_data.columns.difference([uid,target])])           
            y = self.fh.raw_data[target]
            df =  alloperatorobjects[obj_id]['function'].get_dataframe(X,y,self.fh.raw_data[uid])
            self.update_dataframe(df)
        except Exception as e:
            print(str(e))   
            
    def pca_dim(self, obj_id,ncomp,uid,target):
        try:
            print(ncomp,uid,target)
            alloperatorobjects[obj_id]['function'].dimension=ncomp
            self.fh.uid = uid   
            self.fh.response = target
            self.fh.features = ['Pca']            
            X = self.fh.categorize(uid,self.fh.raw_data[self.fh.raw_data.columns.difference([uid,target])])           
            y = self.fh.raw_data[target]
            df =  alloperatorobjects[obj_id]['function'].get_dataframe(X,y,self.fh.raw_data[uid])
            self.update_dataframe(df)
        except Exception as e:
            print(str(e))    
    
    def script_feed(self,obj_id):
        if not self.fh.raw_data.empty:
            df = alloperatorobjects[obj_id]['function'].get_dataframe(self.fh.raw_data)
            self.update_dataframe(df)
        
    def run_algos(self,obj_id,**kwargs):
        msg = alloperatorobjects[obj_id]['function'].set_parameters(**kwargs)
        if msg:
            self.pops(msg)
#        model = alloperatorobjects[obj_id]['function'].run_model()
        alloperatorobjects[obj_id]['fit_model'] = \
                        alloperatorobjects[obj_id]['function'].run_model()
        self.models_name[obj_id] = alloperatorobjects[obj_id]['function'].__class__.__name__
        print('model built',alloperatorobjects[obj_id]['fit_model'])
               
    def predict(self,obj_id,state):
        try:
            self.pred_id = obj_id
            models_list = alloperatorobjects[obj_id]['function'].inputList
                  
            if state == 1:
                df = alloperatorobjects[obj_id]['function'].get_dataframe()
            else:
                df = alloperatorobjects[obj_id]['function'].merge_dataframe(self.X_test,self.z_test)
                print(df.shape)
            if models_list:
                alloperatorobjects[obj_id]['result'] = dict()
                for model_id in models_list:
                    alloperatorobjects[obj_id]['result'][alloperatorobjects[model_id]['function'].__class__.__name__] = \
                        self.fh.predict(alloperatorobjects[model_id]['fit_model'],df)
            else:
                self.pops('connect model to predictive operator')
        except:
            self.pops('Split the data')
            
              
    def recommend(self,uid,target,algo):
        if algo =='RandomForest':
            val = 1
        elif algo == 'GradientBoost':
            val = 2

        try:
            rank,cols=self.fh.feature_ranking(uid,target,val)
            self.rframe.rank_extraction(rank,cols)
        except Exception as e:
            print(str(e))
            self.pops('please check the values')                      
              
    def model_accuracy(self):
        accuracy_list = {}
        try:
            for model_id,predicted in alloperatorobjects[self.pred_id]['result'].items():
                accuracy_list[model_id] = self.fh.model_accuracy(predicted)
            
            return accuracy_list
        except:
            self.pops('Is Predictive operator imported?')
    
    def mean_squared_error(self):
        try:
            return self.fh.mse()
        except:
            self.pops('Is Predictive operator imported?')
        
    def to_file(self,name):
        result_df = self.fh.create_df()
        try:
            for rname,pred_values in alloperatorobjects[self.pred_id]['result'].items():
                result_df = self.fh.add_result(result_df,rname,pred_values)
                
            self.fh.download_result(result_df,name)
        except:
            self.pops('Is Predictive operator imported?')

################ Write to Database #######################
																
    def database(self,obj_id,connection_name,table_name):
        try:
            alloperatorobjects[obj_id]['function'].write_db(connection_name,table_name,self.result)
        except Exception as e:
            print(str(e))
            
############### End of Write to Database ##################            
            
    def visualize(self,engine,name):
        try:
            self.fh.visualize(engine,self.result,name)
        except:
            self.pops('No data to visualize\n Please check the Server')
            
    def imgprocess(self,uid,user_name,pwd):
        if user_name == 'yottaasys' and pwd == 'password':
            try:
                import webbrowser
                webbrowser.open('http://localhost:8888/notebooks/Customer-wise/Toshiba_HDD/1_image_process.ipynb')
            except:
                self.pops('Server not active')
        else:
            self.pops("UserName and password doesn't match")
    
############## Model import and Export ###################
    
    def fetch_models(self,obj_id,mtype='export'):
        if mtype == 'export':
            return list(self.models_name.values())
        elif mtype == 'import':
            return alloperatorobjects[obj_id]['function'].models_list()
   
    def model_exp(self,obj_id,name,value):
        for k,v in self.models_name.items():
            if v == value:
                index = k
         
        state = alloperatorobjects[obj_id]['function'].save_model(name,alloperatorobjects[index]['fit_model'])
        if state:
            self.pops('Success')
        else:
            self.pops('Failed')
            
    def model_imp(self,obj_id,name):
        alloperatorobjects[obj_id]['fit_model'] = alloperatorobjects[obj_id]['function'].retrieve_model(name)
        self.pops('success')
        
#==============================================================================
# Super hack controller        
#==============================================================================
        def super_hack_report(self):
            c_len,m_type,m_acc = ()
        
#==============================================================================
# end of play button
#==============================================================================        


def main():
    root = tk.Tk()
    try:
        root.wm_iconbitmap(bitimage)
    except:
        pass
    root.title('DSF')
    View(root)
    root.mainloop()        
        
        
if __name__ =='__main__':
    main()