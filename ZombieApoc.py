from tkinter import *
from main import *
from game import launch_game, QuickRoll
import random
import time
import sqlite3

screen = Tk()
screen.title("Player Login")
conn = sqlite3.connect('game_data.db')
c = conn.cursor()

# new account making function
def submit(name, pw):
    try:
        p = player(name, pw, 'None')
        c.execute(
            "INSERT INTO PLAYER_DATA (username, password, food, ammo, survivors, core, dog) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, pw, p.stats['Food'], p.stats['Ammo'], p.stats['Survivors'], p.stats['Gang'], p.stats['Dog'])
        )
        conn.commit()
        screen.withdraw()
        return f"Account created successfully! Welcome, {name}!"
    except sqlite3.IntegrityError:
        return f"Username '{name}' already exists."


# not new account function
def login(name, pw):
    c.execute("SELECT password FROM PLAYER_DATA WHERE username = ?", (name,))
    row = c.fetchone()
    if row and row[0] == pw:
        screen.withdraw()
        return f"Login successful! Welcome back, {name}!"
    else:
        return "Login failed! Incorrect username or password."

def change_password(name, p, window, button):
    cp_frame = Frame(window)
    cp_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky='w')

    Label(cp_frame, text="Enter new password:").grid(row=0, column=0, sticky='w')
    new_pw_entry = Entry(cp_frame, show="*")
    new_pw_entry.grid(row=1, column=0, sticky='w')

    message_label = Label(cp_frame, text="")
    message_label.grid(row=2, column=0, sticky='w')

    def save_pw():
        new_pw = new_pw_entry.get().strip()
        
        if not new_pw:
            message_label.config(text="Password cannot be empty.", fg="red")
            return
        c.execute("UPDATE PLAYER_DATA SET password = ? WHERE username = ?", (new_pw, name))
        conn.commit()
        try:
            p.password = new_pw
        except Exception:
            pass
        message_label.config(text="Password changed.", fg="green")

    Button(cp_frame, text="Save", command=save_pw).grid(row=3, column=0, sticky='w', pady=5, padx=(0,10))
    Button(cp_frame, text="Back", command=lambda: [cp_frame.destroy(), button.grid(row=0,column=0)]).grid(row=3, column=1, sticky='e', pady=5)


def settings(name, p, window, lbutton=None, mbutton=None):
    if lbutton:
        try:
            lbutton.grid_forget()
        except Exception:
            pass
    if mbutton:
        try:
            mbutton.grid_forget()
        except Exception:
            pass
    settings_frame = Frame(window)
    settings_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

    quick_roll_var = BooleanVar(value=p.stats.get('QuickRoll', False))

    Label(settings_frame, text="Settings", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    Checkbutton(settings_frame, text="Quick Roll", variable=quick_roll_var,
                command=lambda: p.stats.update({'QuickRoll': quick_roll_var.get()})).grid(row=1, column=0, sticky='w', padx=10)

    Button(settings_frame, text="Change password", command=lambda: [change_password(name, p, window,settings_frame),settings_frame.forget()]).grid(row=2, column=0, sticky='w', padx=10, pady=5)
    if lbutton and mbutton:
        Button(settings_frame, text="Back", command=lambda:[settings_frame.destroy(), lbutton.grid(row=0,column=0),mbutton.grid(row=1,column=0)]).grid(row=3, column=0, sticky='w', padx=10, pady=5)
    elif lbutton:
        Button(settings_frame, text="Back", command=lambda:[settings_frame.destroy(), lbutton.grid(row=0,column=0)]).grid(row=3, column=0, sticky='w', padx=10, pady=5)
    elif mbutton:
        Button(settings_frame, text="Back", command=lambda:[settings_frame.destroy(), mbutton.grid(row=0,column=0)]).grid(row=3, column=0, sticky='w', padx=10, pady=5)
    else:
        Button(settings_frame, text="Back", command=lambda: settings_frame.destroy()).grid(row=3, column=0, sticky='w', padx=10, pady=5)
def logout(name, p, window):
    c.execute("UPDATE PLAYER_DATA SET food = ?, ammo = ?, survivors = ?, core = ?, dog = ? WHERE username = ?",
              (p.stats['Food'], p.stats['Ammo'], p.stats['Survivors'], p.stats['Gang'], p.stats['Dog'], name))
    window.destroy()
    

# prints all existing account details
def admincheck():
    c.execute("SELECT username, password FROM PLAYER_DATA")
    rows = c.fetchall()
    print("Current PLAYER_DATA:")
    for row in rows:
        print(f"Username: {row[0]}, Password: {row[1]}")

# removes an account
def adminremove(username):
    c.execute("DELETE FROM PLAYER_DATA WHERE username = ?", (username,))
    conn.commit()
    print(f"Account '{username}' has been removed.")

Title = Label(
    screen,
    text="Enter your username and password below",
    font=("Segoe UI", 9, "bold"),
    fg="black",
)
Title.grid(row=0, column=0, columnspan=2)
TextName = Label(screen, text="Username: ")
TextName.grid(row=1, column=0)
TextPW = Label(screen, text="Password: ")
TextPW.grid(row=2, column=0)
InputName = Entry(screen)
InputName.grid(row=1, column=1)
InputPW = Entry(screen, show="*")
InputPW.grid(row=2, column=1)

def start():
    name = InputName.get().strip()
    pw = InputPW.get()
    if not name:
        Title.config(text="Please enter a username.", fg="red")
        return

    window = Toplevel(screen)

    c.execute("SELECT 1 FROM PLAYER_DATA WHERE username = ? LIMIT 1", (name,))
    exists = c.fetchone() is not None

    if exists:
        msg = login(name, pw)
        if "failed" in msg:
            Title.config(text=msg, fg="red")
            return
        else:
            screen.withdraw()
    else:
        msg = submit(name, pw)
    
    
    Message = Label(window, text=msg)
    Message.grid(row=0, column=0, padx=10, pady=10)
    
    # Load data
    c.execute("SELECT food, ammo, survivors, core, dog FROM PLAYER_DATA WHERE username = ?", (name,))
    row = c.fetchone()
    if row:
        food, ammo, survivors, core, dog = row
        p = player(name, pw, core if core is not None else 'None')
        p.stats['Food'] = food if food is not None else p.stats.get('Food', 0)
        p.stats['Ammo'] = ammo if ammo is not None else p.stats.get('Ammo', 0)
        p.stats['Survivors'] = survivors if survivors is not None else p.stats.get('Survivors', 0)
        p.stats['Gang'] = core if core is not None else p.stats.get('Gang', 'None')
        p.stats['Dog'] = dog if dog is not None else p.stats.get('Dog', 1)
    else:
        p = player(name, pw, 'None')
    set_tings = Button(window, text="Settings", command=lambda: settings(name, p, window, set_tings, log))
    set_tings.grid(row=1, column=0)

    log = Button(window, text="Log out", command=lambda: logout(name, p, window))
    log.grid(row=2, column=0)

    window.after(2000, lambda: Message.destroy())
    window.after(2000, lambda: set_tings.grid(row=0, column=0))
    window.after(2000, lambda: log.grid(row=1, column=0))
    launch_game(p, master=window)

click = Button(screen, text="Submit", command=start)
click.grid(row=3, column=0, columnspan=2)
screen.mainloop()
conn.close()