import tkinter
from tkinter import ttk
import tkinter.messagebox
import sqlite3

class MyGUI:

    def __init__(self):

        #выбор строки
        def select_row(e):

            self.student_name.delete(0,'end')
            selected = self.tree.focus()
            values = self.tree.item(selected,'values')
            self.student_name.insert(0,values[1])

        #получить наименование всех факультетов

        def get_departments():

            self.departments = []

            conn = None

            try:

                conn = sqlite3.connect('student_info.db')
                cur = conn.cursor()

                cur.execute('''SELECT Departments.Name FROM Departments''')

                self.departments = [n[0] for n in cur.fetchall()]

            except sqlite3.Error as err:

                tkinter.messagebox.showinfo('Ошибка базы данных', err)

            finally:

                if conn != None:
                    conn.close()

            return self.departments

        #получить наименование всех специальностей

        def get_majors():
                       

            self.majors = []

            conn = None

            try:

                conn = sqlite3.connect('student_info.db')
                cur = conn.cursor()

                cur.execute('''SELECT Majors.Name FROM Majors''')

                self.majors = [n[0] for n in cur.fetchall()]

            except sqlite3.Error as err:

                tkinter.messagebox.showinfo('Ошибка базы данных', err)

            finally:

                if conn != None:
                    conn.close()

            return self.majors

                   
        self.main_window=tkinter.Tk()
        self.main_window.title('База данных студентов')

        self.departments = get_departments()# добавляем список факультетов
        self.majors = get_majors() # добавляем список специальностей

        self.frame1 = tkinter.Frame(pady=10, highlightbackground="black", highlightthickness=1)
        self.frame2 = tkinter.Frame()

    #нижняя часть

        conn = sqlite3.connect('student_info.db')
        cur = conn.cursor()
        cur.execute('''SELECT Students.StudentID, Students.Name, Departments.Name, Majors.Name FROM Students, Departments, Majors WHERE Students.DeptID == Departments.DeptID AND Students.MajorID == Majors.MajorID''')
        results = cur.fetchall()

        columns = ('StudentID','Name','Department','Major')

        #таблица
        self.tree=ttk.Treeview(self.frame2, columns=columns, show='headings', height=500)

        self.tree.grid(row=0, column=0,sticky='nsew')

        self.tree.heading('StudentID', text='ID студента', anchor='w')
        self.tree.heading('Name', text='Ф.И.О. студента', anchor='w')
        self.tree.heading('Department', text='Факультет', anchor='w')
        self.tree.heading('Major', text='Специальность', anchor='w')

        self.tree.column('#1', stretch='NO', width=80)
        self.tree.column('#2', stretch='NO', width=400)
        self.tree.column('#3', stretch='NO', width=400)
        self.tree.column('#4', stretch='NO', width=400)

        for student in results:
            self.tree.insert('','end',value=student)


        self.tree.bind('<ButtonRelease>',select_row)

        conn.commit()
        conn.close()

    #верхняя часть

        self.title1 = tkinter.Label(self.frame1, text='Ф.И.О. студента для поиска: ')
        self.title1.grid(column=0,row=1,sticky='w')

        self.student_name = tkinter.StringVar()
        self.student_name.trace('w', self.find_row)
        self.student_name = tkinter.Entry(self.frame1, width=50, textvariable=self.student_name)
        self.student_name.bind('<Return>', (lambda event: self.find_row()))
        self.student_name.grid(column=1,row=1,sticky='w')

        self.search_button = tkinter.Button(self.frame1, text='Найти')
        self.search_button.bind('<Button-1>', (lambda event: self.find_row()))
        self.search_button.grid(column=2,row=1,sticky='w', padx=[10,0])

        self.edit_button = tkinter.Button(self.frame1, text='Редактировать',
                                            command=self.edit_gui)
        self.edit_button.grid(column=3,row=1,sticky='w', padx=5)

        self.add_button = tkinter.Button(self.frame1, text='Добавить',
                                            command=self.add_gui)
        self.add_button.grid(column=4,row=1,sticky='w', padx=5)

        self.delete_button = tkinter.Button(self.frame1, text='Удалить',
                                            command=self.delete_gui)
        self.delete_button.grid(column=5,row=1,sticky='w',padx=5)

        self.exit_button = tkinter.Button(self.frame1, text='Выйти',
                                            command=self.main_window.destroy)
        self.exit_button.grid(column=6,row=1,sticky='w',padx=5)
        
        self.frame1.pack(anchor='nw', side='top', fill='x')
        self.frame2.pack()

        

        tkinter.mainloop()

        #функция поиска  

    def find_row(self):  

        lookup_record = self.student_name.get()

        conn = sqlite3.connect('student_info.db')
        cur = conn.cursor()

        cur.execute('''SELECT Students.StudentID, Students.Name, Departments.Name, Majors.Name FROM Students, Departments, Majors WHERE Students.DeptID == Departments.DeptID AND Students.MajorID == Majors.MajorID AND Students.Name LIKE ?''',('%'+lookup_record+'%',))
        results = cur.fetchall()

        columns = ('StudentID','Name','Department','Major')

        #таблица

        self.tree=ttk.Treeview(self.frame2, columns=columns, show='headings', height=500)

        self.tree.grid(row=0, column=0,sticky='nsew')

        self.tree.heading('StudentID', text='ID студента', anchor='w')
        self.tree.heading('Name', text='Ф.И.О. студента', anchor='w')
        self.tree.heading('Department', text='Факультет', anchor='w')
        self.tree.heading('Major', text='Специальность', anchor='w')

        self.tree.column('#1', stretch='NO', width=80)
        self.tree.column('#2', stretch='NO', width=400)
        self.tree.column('#3', stretch='NO', width=400)
        self.tree.column('#4', stretch='NO', width=400)

        for student in results:

            self.tree.insert('','end',value=student)       

        conn.commit()
        conn.close()

    def edit_gui(self):

        selected = self.tree.focus() # заполнить существующие значения строки
        values = self.tree.item(selected,'values')
        student_id = values[0]

        self.edit_window = tkinter.Tk()
        self.edit_window.title('Редактировать информацию по студенту')

        self.edit_student_name_label = tkinter.Label(self.edit_window, text='Ф.И.О. студента: ', width=20, anchor='w')
        self.edit_student_name_label.grid(column=0,row=0, sticky='w')

        self.edit_student_name_entry = tkinter.Entry(self.edit_window, width=70)
        self.edit_student_name_entry.insert(0,values[1])
        self.edit_student_name_entry.grid(column=1,row=0,sticky='w')
        
        self.edit_student_department_label = tkinter.Label(self.edit_window, text='Факультет: ', width=20, anchor='w')
        self.edit_student_department_label.grid(column=0,row=1, sticky='w')

        
        choose_dept = tkinter.StringVar()
        choose_dept = self.departments.index(values[2])
        self.edit_student_department_combobox = ttk.Combobox(self.edit_window, width=50, textvariable = choose_dept)
        self.edit_student_department_combobox['values']=self.departments
        self.edit_student_department_combobox.current(choose_dept)
        self.edit_student_department_combobox.grid(column=1,row=1,sticky='nesw')

        self.edit_student_major_label = tkinter.Label(self.edit_window, text='Специальность: ', width=20, anchor='w')
        self.edit_student_major_label.grid(column=0,row=2, sticky='w')

        choose_major = tkinter.StringVar()
        choose_major = self.majors.index(values[3])
        self.edit_student_major_combobox = ttk.Combobox(self.edit_window, width=50, textvariable = choose_major)
        self.edit_student_major_combobox['values']=self.majors
        self.edit_student_major_combobox.current(choose_major)
        self.edit_student_major_combobox.grid(column=1,row=2,sticky='nesw')

        self.edit_student_add_button = tkinter.Button(self.edit_window, text='Обновить', command= lambda: self.edit(student_id,selected))
        self.edit_student_add_button.grid(column=0, row=3, sticky='nesw')

        self.edit_student_add_button = tkinter.Button(self.edit_window, text='Выйти', command=self.edit_window.destroy)
        self.edit_student_add_button.grid(column=1, row=3, sticky='nesw')


    def edit(self,student_id,selected):

        conn = None

        try:

            conn = sqlite3.connect('student_info.db')
            cur = conn.cursor()

            cur.execute('PRAGMA foreign_keys=ON')

            name = self.edit_student_name_entry.get()
            dept_name = self.edit_student_department_combobox.get()
            major_name = self.edit_student_major_combobox.get()

            cur.execute('''SELECT Departments.DeptID FROM Departments WHERE Departments.Name = ?''',(dept_name,))
            results1=cur.fetchone()[0]

            cur.execute('''SELECT Majors.MajorID FROM Majors WHERE Majors.Name = ?''',(major_name,))
            results2=cur.fetchone()[0]

        except sqlite3.Error as err:

            tkinter.messagebox.showinfo('Ошибка ввода данных', err)

        finally:

            cur.execute('''UPDATE Students SET Name = ?, DeptID = ?, MajorID = ? WHERE Students.StudentID = ?''',(name,results1,results2,student_id))
            tkinter.messagebox.showinfo('Информационное окно','Изменения успешно внесены.')
            self.edit_window.destroy()
            self.tree.item(selected, text='', values=(student_id,name,dept_name,major_name))
            
            conn.commit()
            conn.close()
        

    def add_gui(self):
                        
            self.add_window = tkinter.Tk()
            self.add_window.title('Добавить информацию по студенту')

            self.new_student_name_label = tkinter.Label(self.add_window, text='Введите Ф.И.О. студента: ', width=20, anchor='w')
            self.new_student_name_label.grid(column=0,row=0, sticky='w')

            self.new_student_name_entry = tkinter.Entry(self.add_window, width=60)
            self.new_student_name_entry.grid(column=1,row=0,sticky='w')

            self.new_student_department_label = tkinter.Label(self.add_window, text='Факультет: ', width=20, anchor='w') 
            self.new_student_department_label.grid(column=0,row=1, sticky='w')

            choose_dept = tkinter.StringVar()
            self.new_student_department_combobox = ttk.Combobox(self.add_window, textvariable = choose_dept)
            self.new_student_department_combobox['values']=self.departments
            self.new_student_department_combobox.current(0)
            self.new_student_department_combobox.grid(column=1,row=1,sticky='nesw')

            self.new_student_major_label = tkinter.Label(self.add_window, text='Специальность: ', width=20, anchor='w')
            self.new_student_major_label.grid(column=0,row=2, sticky='w')

            choose_major = tkinter.StringVar()
            self.new_student_major_combobox = ttk.Combobox(self.add_window, textvariable = choose_major)
            self.new_student_major_combobox['values']=self.majors
            self.new_student_major_combobox.current(0)
            self.new_student_major_combobox.grid(column=1,row=2,sticky='nesw')

            self.new_student_add_button = tkinter.Button(self.add_window, text='Добавить данные', command = self.add)
            self.new_student_add_button.grid(column=0, row=3, sticky='nesw')

            self.new_student_add_button = tkinter.Button(self.add_window, text='Выйти', command=self.add_window.destroy)
            self.new_student_add_button.grid(column=1, row=3, sticky='nesw')

            self.add_window.mainloop()


    def add(self):
            
        conn = sqlite3.connect('student_info.db')
        cur = conn.cursor()

        cur.execute('PRAGMA foreign_keys=ON')

        name = self.new_student_name_entry.get()
        dept_name = self.new_student_department_combobox.get()
        major_name = self.new_student_major_combobox.get()

        try:

            cur.execute('''SELECT Departments.DeptID FROM Departments WHERE Departments.Name = ?''',(dept_name,))
            results1=cur.fetchone()[0]

            cur.execute('''SELECT Majors.MajorID FROM Majors WHERE Majors.Name = ?''',(major_name,))
            results2=cur.fetchone()[0]

        except sqlite3.Error as err:

            tkinter.messagebox.showinfo('Ошибка ввода данных', err)

        finally:

            cur.execute('''INSERT INTO Students (Name, DeptID, MajorID) VALUES (?,?,?)''',(name,results1,results2))
            conn.commit()
            cur.execute('''SELECT Students.StudentID FROM Students WHERE Students.Name =?''',(name,))
            student_id = cur.fetchone()[0]
            conn.close()

            tkinter.messagebox.showinfo('Информационное окно','Данные успешно добавлены.')
            self.add_window.destroy()
            self.tree.insert(parent='', index='end', text='', values=(student_id,name,dept_name,major_name))


    #интерфейс удаления

    def delete_gui(self):

        selected = self.tree.focus()
        values = self.tree.item(selected,'values')

        self.delete_window = tkinter.Tk()
        self.delete_window.title('Удаление информации по студенту')

        self.delete_student_label = tkinter.Label(self.delete_window, text=f'Вы уверены что хотите удалить \n информацию о "{values[1]}"?', anchor='w')
        self.delete_student_label.grid(column=0,row=0, sticky='w', columnspan=2)

        self.delete_student_info_yes = tkinter.Button(self.delete_window, text='Да', command = lambda: self.delete(values,selected))
        self.delete_student_info_yes.grid(column=0,row=1,sticky='nesw')

        self.delete_student_info_no = tkinter.Button(self.delete_window, text='Нет', command = self.delete_window.destroy)
        self.delete_student_info_no.grid(column=1,row=1,sticky='nesw')

    def delete(self, values, selected):

        conn = None

        try:

            conn = sqlite3.connect('student_info.db')
            cur = conn.cursor()
            cur.execute('''DELETE FROM Students WHERE StudentID == ?''',(values[0],))
            conn.commit()

            tkinter.messagebox.showinfo('Информационное окно','Данные удалены.')
            self.delete_window.destroy()
            self.tree.delete(selected)

        except sqlite3.Error as err:
            print('Ошибка базы данных', err)

        finally:

            if conn != None:
                conn.close()
                

    

        

        

        

      

        

        

        

    
    
   

      

        
       

    
            

        


        



if __name__=='__main__':
    my_gui = MyGUI()













  
        

