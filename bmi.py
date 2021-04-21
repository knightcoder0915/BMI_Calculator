from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import mysql.connector as mysql
import sys
import time
import calendar
import datetime as dt
import csv
import os.path


main_window = Tk()
main_window.withdraw()
splash_main=Tk()

def splash():	
	splash_main.deiconify()
	
	#SPLASH SCREEN
	splash_main.title("Welcome")
	splash_main.geometry("2500x2500")
	#Hide title Bar
	#splash_main.overrideredirect(True)
	splash_label=Label(splash_main, text="\n BMI Calculator \n By Tanvi", font=('Arial',100,'bold'),foreground="red")
	splash_label.config(anchor=CENTER)
	splash_label.pack()

	#SPLASH SCREEN TIMER
	splash_main.after(3000,main)
	

def main():
	splash_main.destroy()
	main_window.deiconify()

def greet():
	x=dt.datetime.now()
	w=x.strftime("%H")
	if w <= "12":
		a="Good Morning"
	elif w> "12" and w<= "16":
		a="Good Afternoon"
	else:
		a="Good Evening"
	return a

def count():
	con = mysql.connect(host="localhost", user="root", password="abc456",database="bmidb")
	cursor =  con.cursor()
	cursor.execute("select count(*) from bmi")
	(no_of_rows,)=cursor.fetchone()
	con.close();
	count = no_of_rows
	return count
	



	
def convert():
	try:
		feet=int(convert_window_ent_feet.get())
		if feet<0:
			raise Exception("Invalid Feet")
		inch=int(convert_window_ent_inches.get())
		if inch>12 or inch<0:
			raise Exception("Invalid Inches")
		ans = (feet*0.3048)+(inch*0.0254)
		showinfo("Meters",ans)
		calc_window.deiconify()
		convert_window.withdraw()
	except ValueError:
		showerror('Failure',"Only numeric value accepted")

	except NameError:
		showerror('Failure',"Only numeric value accepted")
	except Exception as e:
		showerror('Failure',e)

def calc():
	try:
		name = calc_window_ent_name.get()
		if (len(name)<2 or any(map(str.isdigit,name))==True):
			raise Exception("Incorrect Name")
		age = calc_window_ent_age.get()
		if int(age)<0 or int(age)>100:
			raise Exception("Incorrect Age")
		phone = calc_window_ent_no.get()
		if int(phone)<1000000:
			raise Exception("Incorrect Phone No.")
		gender = gen.get()
		height = calc_window_ent_ht.get()
		if float(height)<0 or float(height)>3:
			raise Exception("Incorrect Height")
		weight = calc_window_ent_wt.get()
		if float(weight)<0 or float(weight)>500:
			raise Exception("Incorrect Weight")
		date = None
		
		if(name=="" or age =="" or phone =="" or gender =="" or height =="" or weight==""):
			showinfo("Insert Status","All fields are required")
		else:
			con = mysql.connect(host="localhost", user="root", password="abc456",database="bmidb")
			cursor =  con.cursor()
			result = float(weight)/(float(height)*float(height))
			cursor.execute("insert into bmi values(default,'"+ name +"','"+ age +"','"+ phone +"','"+ gender +"','"+ height +"','"+ weight +"','"+ str(result) +"',default)")
			cursor.execute("commit");
			d = [name,age,phone,gender,height,weight,result]
			info =" Name: "+str(d[0])+" \n Age: "+str(d[1])+" \n Phone: "+str(d[2])+"\n Gender: "+str(d[3])+" \n Height: "+str(d[4])+" \n Weight: "+str(d[5])+"\n BMI: "+str(d[6])+" \n"
			if (float(result) > 25.0):
				showinfo('BMI',info + "\n You are overweight")
			elif (float(result) > 18.0):
				showinfo('BMI',info + "\n You are normal weight")
			else:
				showinfo('BMI',info + "\n You are underweight")


			calc_window_ent_name.delete(0,END)                        
			calc_window_ent_name.focus()
			calc_window_ent_age.delete(0,END)                        
			calc_window_ent_age.focus()
			calc_window_ent_no.delete(0,END)                        
			calc_window_ent_no.focus()
			calc_window_ent_ht.delete(0,END)                        
			calc_window_ent_ht.focus()
			calc_window_ent_wt.delete(0,END)                        
			calc_window_ent_wt.focus()
			
			con.close();
	except ValueError:
		showerror('Failure',"Incorrect Details entered")

	except NameError:
		showerror('Failure',"Incorrect Details entered")
                       
	except Exception as e:
		showerror('Failure',e)

			
def view():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0,END)
	info = ""
	con = None
	try:
		con = mysql.connect(host="localhost", user="root", password="abc456",database="bmidb")
		cursor =  con.cursor()
		sql="select * from bmi"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " Name: "+str(d[1])+" \n Age: "+str(d[2])+" \n Phone: "+str(d[3])+"\n Gender: "+str(d[4])+"\n BMI: "+str(d[7])+" \n ************************\n"
		print(info)
		view_window_st_data.insert(INSERT,info)
	except Exception as e:
		showerror('Failure',e)
	finally:

		if con is not None:
			con.close()



def fetch_table_data():
    # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
	con = mysql.connect(host="localhost", user="root", password="abc456",database="bmidb")
	cursor =  con.cursor()
	cursor.execute("select pid,name,age,phone,gender,result as bmi,currentDate as date from bmi")
	header = [row[0] for row in cursor.description]
	rows = cursor.fetchall()

    # Closing connection
	con.close()
	return header, rows


	

def export():
	header, rows = fetch_table_data()

    # Create csv file
	filename = 'D:/bmidata/patient_{0}.csv'.format(dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
	
	f = open(filename, 'w')

    # Write header
	f.write(','.join(header) + '\n')

	for row in rows:
		f.write(','.join(str(r) for r in row) + '\n')

	f.close()
	print(str(len(rows)) + ' rows written successfully to ' + f.name)

def on_closing():
	if askokcancel("Quit", "Do you want to quit?"):
		main_window.destroy()	
	

def f1():
	calc_window.deiconify()
	main_window.withdraw()
def f2():
	main_window.deiconify()
	calc_window.withdraw()
	con = mysql.connect(host="localhost", user="root", password="abc456",database="bmidb")
	cursor =  con.cursor()
	cursor.execute("select count(*) from bmi")
	(no_of_rows,)=cursor.fetchone()
	con.close();	
	count.config(text=("Count:",no_of_rows))



def f3():
	convert_window.deiconify()
	calc_window.withdraw()
def f4():
	main_window.deiconify()
	view_window.withdraw()

#MAIN WINDOW

splash()

main_window.configure(background='light blue')
main_window.title("BMI Calculator")
main_window.geometry("800x500+300+50")

datetime = Label(main_window, text=f"{dt.datetime.now()}\n{greet()} ", font=('Arial',20,'bold'))

main_window_btn_calc = Button(main_window, text="Calculate BMI", font=('Arial',20,'bold'),width=20,command=f1)
main_window_btn_view = Button(main_window, text="View History", font=('Arial',20,'bold'),width=20,command=view)
main_window_btn_export = Button(main_window, text="Export Data", font=('Arial',20,'bold'),width=20,command=export)



count = Label(main_window,text=f"Count:{count()}", font=('Arial',20,'bold'))







datetime.pack(pady=10)
main_window_btn_calc.pack(pady=10)
main_window_btn_view.pack(pady=10)
main_window_btn_export.pack(pady=10)
count.pack(pady=10)



#CALCULATE WINDOW
calc_window = Toplevel(main_window)
calc_window.title("Calculate")
calc_window.geometry("800x500+300+50")
calc_window.configure(background='light blue')

calc_window_lbl_name = Label(calc_window, text="Enter name", font=('Arial',20,'bold'))
calc_window_ent_name = Entry(calc_window,bd=5, font=('Arial',20,'bold'))
calc_window_lbl_age = Label(calc_window, text="Enter age", font=('Arial',20,'bold'))
calc_window_ent_age = Entry(calc_window,bd=5, font=('Arial',20,'bold'))
calc_window_lbl_no = Label(calc_window, text="Enter phone", font=('Arial',20,'bold'))
calc_window_ent_no = Entry(calc_window,bd=5, font=('Arial',20,'bold'))
calc_window_lbl_gender=Label(calc_window, text="Gender", font=('Arial',20,'bold'))

gen = StringVar()

radiobutton_1 = Radiobutton(calc_window, text='Male', variable=gen, value="Male", font=('Arial',20,'bold'))
radiobutton_2 = Radiobutton(calc_window, text='Female', variable=gen, value="Female", font=('Arial',20,'bold'))
gen.set(None)

calc_window_lbl_ht = Label(calc_window, text="Enter Ht in mtr", font=('Arial',20,'bold'))
calc_window_ent_ht = Entry(calc_window,bd=5, font=('Arial',20,'bold'))
calc_window_lbl_wt = Label(calc_window, text="Enter Wt in kg", font=('Arial',20,'bold'))
calc_window_ent_wt = Entry(calc_window,bd=5, font=('Arial',20,'bold'))

calc_window_btn_convert = Button(calc_window, text="Convert", font=('Arial',20,'bold'),command=f3)
calc_window_btn_calculate = Button(calc_window, text="Calculate", font=('Arial',20,'bold'),command=calc)
calc_window_btn_back = Button(calc_window, text="Back", font=('Arial',20,'bold'),command=f2)



calc_window_lbl_name.grid(row=0,padx=5,pady=10)
calc_window_ent_name.grid(row=0, column=1, padx=5,pady=10)
calc_window_lbl_age.grid(row=1,padx=5,pady=10)
calc_window_ent_age.grid(row=1, column=1,padx=5,pady=10)
calc_window_lbl_no.grid(row=2,padx=5,pady=10)
calc_window_ent_no.grid(row=2, column=1,padx=5,pady=10)
calc_window_lbl_gender.grid(row=3, padx=5,pady=10)
radiobutton_1.grid(row=3,column=1,padx=5,pady=10)
radiobutton_2.grid(row=3,column=2,padx=5,pady=10)
calc_window_lbl_ht.grid(row=4,padx=5,pady=10)
calc_window_ent_ht.grid(row=4, column=1,padx=5,pady=10)

calc_window_btn_convert.grid(row=4,column=2,padx=5,pady=10)

calc_window_lbl_wt.grid(row=5,padx=5,pady=10)
calc_window_ent_wt.grid(row=5, column=1,padx=5,pady=10)

calc_window_btn_calculate.grid(row=6,padx=5,pady=10)
calc_window_btn_back.grid(row=6, column=1, padx=5,pady=10)
calc_window.withdraw()


#CONVERT WINDOW
convert_window = Toplevel(calc_window)
convert_window.title("Height Converter")
convert_window.geometry("800x500+300+50")
convert_window.configure(background='light green')

convert_window_lbl_ht = Label(convert_window, text="Enter your Height", font=('Arial',20,'bold'))
convert_window_lbl_feet = Label(convert_window, text="Feet", font=('Arial',20,'bold'))
convert_window_ent_feet = Entry(convert_window,bd=5, font=('Arial',20,'bold'))
convert_window_lbl_inches = Label(convert_window, text="Inches", font=('Arial',20,'bold'))
convert_window_ent_inches = Entry(convert_window,bd=5, font=('Arial',20,'bold'))

convert_btn = Button(convert_window, text="Convert", font=('Arial',20,'bold'),command=convert)

convert_window_lbl_ht.pack(pady=10)
convert_window_lbl_feet.pack(pady=10)
convert_window_ent_feet.pack(pady=10)
convert_window_lbl_inches.pack(pady=10)
convert_window_ent_inches.pack(pady=10)
convert_btn.pack(pady=10)
convert_window.withdraw()


#VIEW WINDOW
view_window = Toplevel(main_window)
view_window.title("View")
view_window.geometry("800x500+300+50")
view_window.configure(background='light blue')

view_window_st_data = ScrolledText(view_window,width=30,height=10,font=('Arial',20,'bold'))
view_window_btn_back = Button(view_window, text="Back", font=('Arial',20,'bold'),command=f4)

view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()





main_window.protocol("WM_DELETE_WINDOW", on_closing)
main_window.mainloop()
