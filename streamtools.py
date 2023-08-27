import os
import subprocess
import sys
import json
import tkinter as tk
from tkinter import messagebox

class ST_Process:
    def __init__(self, pid, status, command, process):
        self.pid = pid
        self.status = status
        self.command = command
        self.process = process

class StreamTools:
    controlcenter_process = ""
    def check_if_process_running(self, process):
        result = ""
        if process.pid is not None:
            result = "Control Center is running with PID ".format(process.pid)
        else:
            result = "Control Center is not running"
        process.status = result
    
    def start_controlcenter(self):
        global controlcenter_process
        #Start StreamTools Control Center
        controlcenter = subprocess.Popen(["py", "api/controlcenter/streamtools_controlcenter.py"])
        controlcenter_process = ST_Process(controlcenter.pid, "Control Center is running with PID {pid}".format(controlcenter.pid), "api/controlcenter/streamtools_controlcenter.py", controlcenter)
        self.cc_status_label.configure(text = "StreamTools Control Center Status: {status}".format(status = str(controlcenter_process.status)))
        self.start_cc_button.configure(text = "Stop StreamTools Control Center", command=self.stop_controlcenter)
        self.cc_url_label.configure(text = self.server_address)
    def stop_controlcenter(self):
        global controlcenter_process
        controlcenter_process.process.terminate()
        self.start_cc_button.configure(text = "Start StreamTools Control Center", command=self.start_controlcenter)
        controlcenter_process.status = "Control Center is not running"
        self.cc_status_label.configure(text = "StreamTools Control Center Status: {status}".format(status = str(controlcenter_process.status)))

    def __init__(self, master):
        global controlcenter_process
        self.master = master
        master.geometry("640x480+0+0")
        master.title("Stream Tools")

        # Load or create config
        self.config = self.load_config()
        self.content = self.load_content()
        self.server_address = "{addr}:{port}".format(addr = self.config.get("server_bind_address"), port = self.config.get("server_port"))
        init_status = "Control Center is not running"

        self.start_cc_button = tk.Button(master, text="Start StreamTools Control Center", command=self.start_controlcenter)
        self.start_cc_button.place(relx=0.5, rely=0.6, anchor="center")
        self.cc_url_label = tk.Label(master, text="Stream Control Center URL:")
        self.cc_url_label.place(relx=0.5, rely=0.8, anchor="center")
        try:
            self.cc_status_label = tk.Label(master, text="StreamTools Control Center Status: " + controlcenter_process.status)
            self.cc_status_label.place(relx=0.5, rely=0.7, anchor="center")
            self.cc_status_button = tk.Button(master, text="Check Control Center Status", command=self.update_status_label(controlcenter_process))
        except:
            self.cc_status_label = tk.Label(master, text="StreamTools Control Center Status: " + init_status)
            self.cc_status_label.place(relx=0.5, rely=0.7, anchor="center")
            
        #self.create_overlay_button = tk.Button(master, text="Create Overlay", command=self.create_overlay)
        #self.create_overlay_button.place(relx=0.5, rely=0.8, anchor="center")
        #self.validate_streamtools_button = tk.Button(master, text="Validate StreamTools", command=self.validate_streamtools)
        #self.validate_streamtools_button.place(relx=0.5, rely=0.9, anchor="center")

        # Deactivate virtual environment when window is closed
        master.protocol("WM_DELETE_WINDOW", self.close)

    def load_config(self):
        # Check for config file
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_file):
            # Load config from file
            with open(config_file) as f:
                config = json.load(f)
        else:
            # Create default config
            config = {"pip_path": "pip", "requirements_file": "requirements.txt", "server_bind_address": "0.0.0.0", "server_port": "1420", "content_library":"content_directory"}

            # Write config to file
            with open(config_file, "w") as f:
                json.dump(config, f)

            # Create requirements file
            with open(config["requirements_file"], "w") as f:
                f.write("")
        return config
    def load_content(self):
        #Check for content file
        content_config = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(content_config):
            # Load content paths from file
            with open(content_config) as f:
                content = json.load(f)
        else:
            # Create default content_config
            content = {"ContentFolder1Name": "ContentFolder1Path", "ContentFolder2Name": "ContentFolder2Path"}

            # Write config to file
            with open(content_config, "w") as f:
                json.dump(content, f)
        return content

    def close(self):
        # Close application window
        self.master.destroy()

    #def create_overlay(self):
    #    # Call create_overlay.py
    #    os.system(" ".join(["py", "create_overlay.py"]))
        
    #def validate_streamtools(self):
    #    # Call validate_streamtools.py
    #    os.system(" ".join(["py", "validate_streamtools.py"]))

    def update_status_label(self,process):
        process.status = self.check_if_process_running(process)
        self.cc_status_label = tk.Label(text="StreamTools Control Center Status: {status}".format(process.status))

root = tk.Tk()
stream_tools = StreamTools(root)
root.mainloop()
