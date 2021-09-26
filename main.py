from tkinter import *
from tkinter import messagebox
import random,string
import re
import json

FONT_NAME = "Courier"
WHITE = '#ffffff'
BLACK = '#000000'

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
	generated = ''.join(random.choices(
		string.ascii_uppercase + string.digits + string.ascii_lowercase, k=12))
	pword_entry.delete(0, END)
	pword_entry.insert(0, generated)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
	try:
		with open('data.json') as data_file:
			data = json.load(data_file)
	except FileNotFoundError:
		messagebox.showinfo(title='Error', message=f'No file found')
	else:
		site = site_entry.get()
		if site in data:
			email = data[site]['username']
			password = data[site]['password']
			messagebox.showinfo(title=site, message=f'Email: {email}\nPassword: {password}')
		else:
			messagebox.showinfo(title=site, message=f'No credentials found for {site}')

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
	website = site_entry.get()
	email = uname_entry.get()
	password = pword_entry.get()

	if(passes_validations(website, email, password)):
		new_data = {
			website:{
				'username': email,
				'password': password,
				}
			}

		try:
			with open('data.json', 'r') as data_file:
				data = json.load(data_file)
		except FileNotFoundError:
			with open('data.json', 'w') as data_file:
				json.dump(new_data, data_file, indent=4)
		else:
			data.update(new_data)
		
			with open('data.json', 'w') as data_file:
				json.dump(new_data, data_file, indent=4)
				messagebox.showinfo(title=website, message=f'Successfully saved {website} credentials')
		finally:
			site_entry.delete(0, END)
			uname_entry.delete(0, END)
			pword_entry.delete(0, END)

def passes_validations(website, email, password):
	if(website==''):
		messagebox.showerror(title='Error', message='You must provide a website')
		return False
	elif(email==''):
		messagebox.showerror(title='Error', message='You must provide a username')
		return False
	elif not re.match('[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+', email):
		messagebox.showerror(title='Error', message='You must provide a valid email')
		return False
	elif(password==''):
		messagebox.showerror(title='Error', message='You must provide a password')
		return False
	return True

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("PwdMgr")
window.config(padx=40, pady=40, bg=WHITE)

canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=1)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

site_label = Label(text="Site", fg=BLACK, bg=WHITE, font=(FONT_NAME))
site_label.grid(row=1, column=0)
site_entry = Entry(width=25)
site_entry.grid(row=1, column=1)

search_btn = Button(text='Find Credentials', width=14, command=find_password)
search_btn.grid(row=1, column=2)

uname_label = Label(text="Username", fg=BLACK, bg=WHITE, font=(FONT_NAME))
uname_label.grid(row=2, column=0)
uname_entry = Entry(width=25)
uname_entry.grid(row=2, column=1)

pword_label = Label(text="Password", fg=BLACK, bg=WHITE, font=(FONT_NAME))
pword_label.grid(row=3, column=0)
pword_entry = Entry(width=25)
pword_entry.grid(row=3, column=1)

gen_btn = Button(text='Generate Password', command=gen_password)
gen_btn.grid(row=3, column=2)

add_btn = Button(text='Add', width=25, command=save)
add_btn.grid(row=4, column=1, columnspan=2)

window.mainloop()