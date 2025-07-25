import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser
from PIL import Image, ImageTk
import os
import time
import tempfile
import winreg
import ctypes
import secrets
import string
import smtplib
from email.mime.text import MIMEText
import cv2
import time
from tkinter import filedialog
import face_recognition
import sqlite3
import sys

# Global Password Holder
password = ""

authorized_image_path = ""  # Path to the authorized user's face image

def resource_path(relative_path):
    """ Get absolute path to resource, works for .py and .exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def generate_random_password(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def init_db():
    conn = sqlite3.connect("spyware_logs.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT
        )
    ''')
    conn.commit()
    conn.close()

def send_password_email(pwd):
    sender_email = "abhinandsrajesh16@gmail.com"  # Use your Gmail address
    sender_password = "cujswbaakwkxbieb"  # Use App Password from Gmail settings
    receiver_email = "abhinandsrajesh16@gmail.com"  # You can use your own or other email.

# The mail will be recieved in the inbox of the receiver.
    subject = "Your One-Time Access Password for WebCam Spyware Security"
    body = f"Hello,\n\nYour temporary access password is: {pwd}\n\nNote: This password will expire once the application is closed.\n\nRegards,\nWebCam Security System"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        log_action("Password sent to email")
    except Exception as e:
        log_action(f"Email sending failed: {e}")

#the log_action function is used to log the actions performed by the user in a log.txt file.
#It appends the action and the current time to the log file.
def log_action(action):
    timestamp = time.ctime()
    conn = sqlite3.connect("spyware_logs.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, action) VALUES (?, ?)", (timestamp, action))
    conn.commit()
    conn.close()

    # Also write to log.txt (optional)
    with open("log.txt", "a") as f:
        f.write(f"[{timestamp}] {action}\n")

#Details of the project, team details, and company details are displayed in a HTML format.
def project_info():
    html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Project Information</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #2c0000;
            color: #ffffff;
            padding: 40px 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background-color: #3b0000;
            border: 2px solid #ff4c4c;
            border-radius: 8px;
            padding: 30px;
        }

        h1, h2 {
            text-align: center;
            color: #ff4c4c;
            margin-bottom: 20px;
        }

        p {
            text-align: center;
            margin-bottom: 30px;
            color: #ffcccc;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }

        th, td {
            border: 1px solid #ff4c4c;
            padding: 12px 15px;
            text-align: left;
        }

        th {
            background-color: #800000;
            color: #ffffff;
        }

        td {
            background-color: #4d0000;
            color: #ffdddd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Project Information</h1>
        <p>This project was developed by <strong>Team 29</strong> as part of a Cyber Security Internship.</p>

        <h2>Project Details</h2>
        <table>
            <tr><th>Field</th><th>Value</th></tr>
            <tr><td>Project Name</td><td>WebCam Spyware Security</td></tr>
            <tr><td>Description</td><td>Implementing Physical Security Policy on Web Cam in Devices to Prevent Spyware Activities</td></tr>
            <tr><td>Start Date</td><td>28-May-2025</td></tr>
            <tr><td>End Date</td><td>18-July-2025</td></tr>
            <tr><td>Status</td><td>Completed</td></tr>
        </table>

        <h2>Developer Details</h2>
        <table>
         
            
            
            <tr>
                <td>Prathicksha M</td>
                <td>ST#IS#7950</td>
                <td>prathicksha.manimaran@gmail.com</td>
            </tr>
            <tr>
                <td>Praveen R</td>
                <td>ST#IS#7951</td>
                <td>rajupraveen.2005@gmail.com</td>
            </tr>
            <tr>
                <td>S Ajishad Thampi</td>
                <td>ST#IS#7952</td>
                <td>ajishadthampi@gmail.com</td>
            </tr>
           <tr>
                <th>V A Padmesh</th>
                <th>ST#IS#7953</th>
                <th>vapadmesh@gmail.com</th>
            </tr>
            <tr>
                <td>Abhinand S Rajesh</td>
                <td>ST#IS#7954</td>
                <td>abhinandsrajesh16032004@gmail.com</td>
            </tr>
        </table>

        <h2>Company Details</h2>
        <table>
            <tr><td>Name</td><td>Supraja Technologies</td></tr>
            <tr><td>Contact Email</td><td>suprajatasks@gmail.com</td></tr>
        </table>
    </div>
</body>
</html>
"""

    path = os.path.join(tempfile.gettempdir(), "project_info.html")
    with open(path, "w") as f:
        f.write(html_code)
    webbrowser.open(f"file://{path}")
#for disabling the camera, it will ask for a password and then disable the camera by modifying the registry.
#It will also log the action in a log.txt file.
def disable_camera():
    def on_ok():
        if password_entry.get() == password:
            try:
                subprocess.run(r'C:\Windows\System32\reg.exe DELETE "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /f', shell=True)
                subprocess.run(r'C:\Windows\System32\reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /t REG_DWORD /d 0 /f', shell=True)
                messagebox.showinfo("Success", "Camera Disabled Successfully")
                log_action("Camera Disabled (REG_DWORD 0)")
                password_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Disabling failed: {e}")
        else:
            error_label.config(text="Incorrect password. Try again.")
            password_entry.delete(0, tk.END)
            log_action("Wrong password attempt on Disable Camera")
            # Record intruder BEFORE disabling camera
            record_intruder_video()
            try:
                subprocess.run(r'C:\Windows\System32\reg.exe DELETE "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /f', shell=True)
                subprocess.run(r'C:\Windows\System32\reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /t REG_DWORD /d 0 /f', shell=True)
                log_action("Camera Disabled (REG_DWORD 0) after intruder video")
                messagebox.showinfo("Notice", "Camera has now been disabled due to unauthorized access attempt.")
                password_window.destroy()
            except Exception as e:
                log_action(f"Error disabling camera after intruder recording: {e}")

    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")
    tk.Label(password_window, text="Enter Password:").pack()
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()
    tk.Button(password_window, text="OK", command=on_ok).pack()
    error_label = tk.Label(password_window, text="", fg="red")
    error_label.pack()

    
#for enabling the camera, it will ask for a password and then enable the camera by modifying the registry.
#It will also log the action in a log.txt file.
def enable_camera():
    def on_ok():
        if password_entry.get() == password:
            if authorized_image_path == "":
                messagebox.showerror("Error", "No authorized face image uploaded.")
                log_action("Enable camera failed: No authorized image.")
                password_window.destroy()
                return

            try:
                # TEMPORARILY ENABLE CAMERA
                subprocess.run(r'C:\Windows\System32\reg.exe DELETE "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /f', shell=True)
                log_action("Camera temporarily enabled for face verification")
                time.sleep(1)  # Allow camera hardware to power up

                # Capture image from webcam
                cap = cv2.VideoCapture(get_first_working_camera())
                ret, frame = cap.read()
                cap.release()

                if not ret:
                    messagebox.showerror("Error", "Failed to capture image from webcam.")
                    log_action("Webcam capture failed for face recognition")
                    password_window.destroy()
                    return

                authorized_img = face_recognition.load_image_file(authorized_image_path)
                authorized_encodings = face_recognition.face_encodings(authorized_img)

                if not authorized_encodings:
                    messagebox.showerror("Error", "No face found in authorized image.")
                    log_action("No face found in uploaded image")
                    return

                authorized_encoding = authorized_encodings[0]
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(frame_rgb)
                face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

                match_found = False
                for face_encoding in face_encodings:
                    if face_recognition.compare_faces([authorized_encoding], face_encoding)[0]:
                        match_found = True
                        break

                if match_found:
                    messagebox.showinfo("Success", "Camera Enabled Successfully (Face Verified)")
                    log_action("Camera Enabled after face verification")
                    # leave the camera enabled
                else:
                    # DISABLE CAMERA AGAIN
                    subprocess.run(r'C:\Windows\System32\reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /t REG_DWORD /d 0 /f', shell=True)
                    log_action("Camera disabled again due to face mismatch")
                    messagebox.showwarning("Face Mismatch", "Face does not match. Camera access revoked.")

                password_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Face verification failed: {e}")
                log_action(f"Face verification error: {e}")
                password_window.destroy()
        else:
            error_label.config(text="Incorrect password. Try again.")
            password_entry.delete(0, tk.END)
            log_action("Wrong password attempt on Enable Camera")

            # TEMPORARILY ENABLE CAMERA TO RECORD INTRUDER
            subprocess.run(r'C:\Windows\System32\reg.exe DELETE "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v Value /f', shell=True)
            time.sleep(1)

            record_intruder_video()

            messagebox.showwarning("Warning", "Unauthorized attempt to enable camera detected.")
            password_window.destroy()

        # else:
        #     error_label.config(text="Incorrect password. Try again.")
        #     password_entry.delete(0, tk.END)
        #     log_action("Wrong password attempt on Enable Camera")
        #     record_intruder_video()
        #     messagebox.showwarning("Warning", "Unauthorized attempt to enable camera detected.")
        #     password_window.destroy()

    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")
    tk.Label(password_window, text="Enter Password:").pack()
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()
    tk.Button(password_window, text="OK", command=on_ok).pack()
    error_label = tk.Label(password_window, text="", fg="red")
    error_label.pack()

def get_first_working_camera(max_index=5):
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return i
        cap.release()
    return -1

def record_intruder_video():
    log_action("Intruder detected! Recording started.")

    cam_index = get_first_working_camera()
    if cam_index == -1:
        log_action("Failed to open any webcam for intruder recording.")
        return

    cap = cv2.VideoCapture(cam_index)

    # Ensure the folder exists
    save_folder = r"D:\cybersecurity\project\snipptes"
    os.makedirs(save_folder, exist_ok=True)

    # Video codec and output file
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path = os.path.join(save_folder, f"intruder_{int(time.time())}.avi")
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))  # 20 fps, 640x480 resolution

    start_time = time.time()
    while time.time() - start_time < 5:  # record for 5 seconds
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    log_action(f"Intruder video saved: {output_path}")

    
# This function retrieves the registry value for the webcam access status.
# It checks both Local Machine and Current User registry hives.
def get_registry_value(root, subkey, value_name):
    try:
        reg_key = winreg.OpenKey(root, subkey)
        value, _ = winreg.QueryValueEx(reg_key, value_name)
        winreg.CloseKey(reg_key)
        return value
    except FileNotFoundError:
        return None
    except Exception:
        return None

# This function checks the webcam access status for both Local Machine and Current User.
# It retrieves the values from the registry and interprets them.
def status():
    subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
    value_name = "Value"

    value_lm = get_registry_value(winreg.HKEY_LOCAL_MACHINE, subkey, value_name)
    value_cu = get_registry_value(winreg.HKEY_CURRENT_USER, subkey, value_name)

    def interpret_value(val):
        if val is None:
            return "Not Set"
        elif isinstance(val, int):
            return "Disabled" if val == 0 else "Enabled"
        elif isinstance(val, str):
            if val.lower() == "deny":
                return "Disabled"
            elif val.lower() == "allow":
                return "Enabled"
        return f"Unknown ({val})"

    lm_status = interpret_value(value_lm)
    cu_status = interpret_value(value_cu)

    status_msg = f"Local Machine: {lm_status}\nCurrent User: {cu_status}"
    ctypes.windll.user32.MessageBoxW(0, status_msg, "Camera Status", 0)

# This function opens the log file if it exists, otherwise shows a message.
def view_logs():
    conn = sqlite3.connect("spyware_logs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")  # Get latest 50 logs
    records = c.fetchall()
    conn.close()

    log_window = tk.Toplevel(root)
    log_window.title("Logs")
    text = tk.Text(log_window, wrap="word", width=80, height=20)
    text.pack()

    for rec in records:
        text.insert(tk.END, f"[{rec[1]}] {rec[2]}\n")

# This function allows the user to change the password manually.
# It creates a new password and sends it via email.
def change_password():
    def set_password():
        global password
        if new_pass.get() == confirm_pass.get():
            password = new_pass.get()
            send_password_email(password) 
            log_action("Password manually changed and emailed")
            messagebox.showinfo("Success", "Password changed successfully")
            cp_window.destroy()
        else:
            messagebox.showerror("Error", "Passwords do not match")

# Create a new window for changing the password
    cp_window = tk.Toplevel(root)
    cp_window.title("Change Password")
    tk.Label(cp_window, text="New Password").pack()
    new_pass = tk.Entry(cp_window, show="*")
    new_pass.pack()
    tk.Label(cp_window, text="Confirm Password").pack()
    confirm_pass = tk.Entry(cp_window, show="*")
    confirm_pass.pack()
    tk.Button(cp_window, text="Change", command=set_password).pack()

    # Global image label reference
authorized_img_label = None
authorized_img_preview = None  # Keep a reference to prevent garbage collection

def upload_authorized_image():
    global authorized_image_path, authorized_img_label, authorized_img_preview

    path = filedialog.askopenfilename(title="Select Authorized Image",
                                      filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if path:
        authorized_image_path = path
        messagebox.showinfo("Success", "Authorized face image uploaded.")
        log_action(f"Authorized face image set: {path}")

        try:
            # Load and resize the image for preview
            img = Image.open(path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            authorized_img_preview = ImageTk.PhotoImage(img)

            # If label already exists, update it. Otherwise, create one.
            if authorized_img_label is not None:
                authorized_img_label.config(image=authorized_img_preview)
            else:
                authorized_img_label = tk.Label(root, image=authorized_img_preview, bg='black')
                authorized_img_label.place(x=10, y=10)  # Top-left corner

        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            log_action(f"Failed to load preview image: {e}")

# Initialize the database
init_db()

# Generate password when app starts
password = generate_random_password()
send_password_email(password)
log_action(f"New session password: {password}")

# Main GUI
root = tk.Tk()
root.title("Web Cam Security")
root.geometry("600x500")
root.configure(bg='black')

tk.Button(root, text="Project Info", font=("Arial", 14, "bold"), bg='red', command=project_info).pack(pady=10)
tk.Label(root, text="WebCam Spyware Security", font=("Arial", 18, "bold"), fg="white", bg="black").pack(pady=15)

# Image loading
# Image loading from file

try:
    image_path = resource_path("web.png")
    image = Image.open(image_path).convert("RGBA")  
 
    datas = image.getdata()
    newData = []
    for item in datas:
        # If white pixel, make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))  # Transparent
        else:
            newData.append(item)
    image.putdata(newData)

    image = image.resize((200, 150), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    tk.Label(root, image=photo, bg='black').pack(pady=10)

except Exception as e:
    tk.Label(root, text=f"Image load error: {e}").pack(pady=10)

# Button Sections
frame1 = tk.Frame(root, bg="black")
frame1.pack(pady=10)
tk.Button(frame1, text="View Logs", font=("Arial", 14, "bold"), bg="red", command=view_logs).pack(side="left", padx=5)
tk.Button(frame1, text="Check Status", font=("Arial", 14, "bold"), bg="red", command=status).pack(side="left", padx=5)
tk.Button(root, text="Change Password", font=("Arial", 14, "bold"), bg="red", command=change_password).pack(pady=10)
tk.Button(root, text="Upload Authorized Face", font=("Arial", 14, "bold"), bg="red", command=upload_authorized_image).pack(pady=10)


frame2 = tk.Frame(root, bg="black")
frame2.pack(pady=10)
tk.Button(frame2, text="Disable Camera", font=("Arial", 14, "bold"), bg="red", command=disable_camera).pack(side="left", padx=5)
tk.Button(frame2, text="Enable Camera", font=("Arial", 14, "bold"), bg="red", command=enable_camera).pack(side="left", padx=5)

# Clear session password
def on_exit():
    global password
    password = ""  
    log_action("Application closed, password expired")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
