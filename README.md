# 🔐 WebCam Spyware Security

### A cybersecurity tool to protect users from unauthorized webcam access using password authentication, face recognition, and system-level registry control.

---

## 📌 Project Overview

Hackers often gain access to webcams without user knowledge, exploiting backdoors in software or network vulnerabilities. This Python-based GUI tool implements a **physical security policy** that prevents such spyware activities by:

- Controlling access to the webcam using Windows Registry
- Using password-based and face-based authentication
- Recording intruders if access fails
- Logging every critical action
- Sending OTP to a verified email address
- GUI built using **Tkinter**
- Registry-level webcam toggle using `reg.exe`
- Image-based face recognition using `face_recognition`

---

## 🧰 Technologies Used

- `Python 3.10+`
- `Tkinter` for GUI
- `OpenCV` for video capture
- `face_recognition` for face-based validation
- `SQLite` for local logging
- `smtplib` and `email.mime` for OTP email
- `winreg` and `subprocess` for Registry editing
- `Pillow` for image preview in UI

---

## ⚙️ Features

| Feature | Description |
|--------|-------------|
| 🔒 Password-based Access | Unique session password sent via email. |
| 🧠 Face Recognition | Authorizes camera access only if user face matches uploaded image. |
| 🎥 Intruder Capture | Captures a short video of unauthorized access attempts. |
| 🧾 Logs Viewer | Logs all access attempts and registry actions. |
| 🧑‍💻 Webcam Enable/Disable | Uses Windows Registry to completely disable/enable webcam hardware. |
| 📄 Project Info Page | Shows a beautiful HTML summary with dev and project details. |

---

## 🧪 How It Works

1. **App Launch**:
    - Generates a random password.
    - Sends password to developer's email via SMTP.
    - Initializes SQLite DB for logging actions.

2. **Enable/Disable Webcam**:
    - Requires password entry.
    - Face recognition required to enable camera.
    - If password fails, a 5-second video is recorded using webcam.

3. **Upload Face Image**:
    - Used as the authorized reference during face recognition.

4. **Status Check**:
    - Checks and displays current registry value for webcam access.

5. **Logs Viewer**:
    - Retrieves and displays the latest 50 actions performed in the app.

6. **Project Info**:
    - Opens a well-designed HTML page with team and project details.

---

## 🖥️ How to Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/WebCam-Spyware-Security.git
cd WebCam-Spyware-Security
