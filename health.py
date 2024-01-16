# Import necessary libraries
import os
from tkinter import *
from twilio.rest import Client
from PIL import Image, ImageTk
from tkinter import messagebox
from playsound import playsound
import datetime
from plyer import notification
import pygame

# Create the main application window
pro = Tk()
pro.title("MedKit Reminder")
pro.geometry("500x400")

# Load and display the welcome image
img = Image.open("welcome.png")
img = img.resize((500, 65))
tkimage = ImageTk.PhotoImage(img)

img_label = Label(pro, image=tkimage).grid()

# Set window icon
pro.iconbitmap('icon.ico')


# Function to set and handle notifications
def set_notification():
    # Get user inputs
    get_title = title.get()
    get_msg = msg.get()
    phone_number = num1.get()
    hour = time1.get()
    minute = time2.get()
    second = time3.get()

    # Validate time inputs
    if hour.isdigit() and minute.isdigit() and second.isdigit():
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        # phoneNumber = int(phoneNumber)

        if len(phone_number) != 11:
            messagebox.showwarning("Invalid Phone Number", "Please enter a phone number with only 11 digits.")
            return
        if 0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60:
            time_now = f"{hour:02d}:{minute:02d}:{second:02d}"

            # Play sound for setting the alarm using pygame
            pygame.mixer.init()
            pygame.mixer.music.load('set_alarm.mp3')
            pygame.mixer.music.play()

            while True:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")

                # Check if it's time to trigger the notification
                if current_time == time_now:
                    # Play sound to remind user to take medicine
                    playsound('take.mp3')

                    # Display notification
                    notification.notify(
                        title=get_title,
                        message=get_msg,
                        app_name="Medkit_reminder",
                        app_icon="icon.ico",
                        timeout=10
                    )

                    # Send SMS using Twilio
                    account_sid = 'ACd1a376a9580a6e3a28c2ebc2e3076508'
                    auth_token = '24f6dd653a845a9770f12ff551d92957'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        from_='+12058101221',
                        body='Please take the medicine , Do not forget that !',
                        to='+201156901098'
                    )
                    print(message.sid)

                    # Clear input fields after successful notification
                    title.delete(0, END)
                    msg.delete(0, END)
                    num1.delete(0, END)
                    time1.delete(0, END)
                    time2.delete(0, END)
                    time3.delete(0, END)

                    # Stop the pygame mixer
                    pygame.mixer.music.stop()

                    break  # Exit the loop after sending notification
                elif current_time > time_now:
                    break  # Exit the loop if current time exceeds set time
        else:
            messagebox.showwarning("Invalid Time", "Please enter a valid time.")
    else:
        messagebox.showwarning("Invalid Time", "Please enter a valid time.")


# GUI elements for user input
t_label = Label(pro, text="Title to notify", font=("popins", 10))
t_label.place(x=12, y=75)
title = Entry(pro, width="25", font=("poppins", 13))
title.place(x=123, y=78)

m_label = Label(pro, text="Display Message", font=("poppins", 10))
m_label.place(x=12, y=120)
msg = Entry(pro, width="40", font=("poppins", 13))
msg.place(x=123, y=120, height=30)

num_label = Label(pro, text="Phone Number", font=("poppins", 10))
num_label.place(x=12, y=175)
num1 = Entry(pro, width="30", font=("poppins", 15))
num1.place(x=123, y=175)

time_label = Label(pro, text="Set Time", font=("poppins", 10))
time_label.place(x=12, y=230)
time1 = Entry(pro, width="5", font=("poppins", 10))
time1.place(x=123, y=230)
time_hou_label = Label(pro, text="H", font=("poppins", 10))
time_hou_label.place(x=175, y=230)
time2 = Entry(pro, width="5", font=("poppins", 10))
time2.place(x=227, y=230)
time_min_label = Label(pro, text="M", font=("poppins", 10))
time_min_label.place(x=279, y=230)
time3 = Entry(pro, width="5", font=("poppins", 10))
time3.place(x=331, y=230)
time_sec_label = Label(pro, text="S", font=("poppins", 10))
time_sec_label.place(x=383, y=230)


# Function to restart notification setting
def restart_notification():
    set_notification()
    
# Button to set notification
but = Button(pro, text="SET NOTIFICATION", font=("poppins", 10, "bold"), fg="#ffffff", bg="#528DFF", width=20,
             command=restart_notification)
but.place(x=170, y=300)

# Set icon and disable resizing
pro.iconbitmap('icon.ico')
pro.resizable(0, 0)

# Start the main event loop
pro.mainloop()
