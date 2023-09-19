import os
import subprocess
import tkinter as tk
from api.controlcenter.st_process import ST_Process
import api.controlcenter.st_settings as s

# UI for StreamTools api.
#TODO: implement more than just controlcenter
class StreamTools:
    #TODO: One var for each process? Do we care about scale?
    CONTROLCENTER_PROCESS = None
    
    def check_if_process_running(self, process):
        result = None
        if process.pid() is not None:
            result = f"{process.label} is running with PID {process.pid()}"
        else:
            result = f"{process.label} is not running"
        return result

    def start_st_process(self, command, status = None, label = None):
        return ST_Process(subprocess.Popen(["py", command]), status, label)


    def start_controlcenter(self):
        #Start StreamTools Control Center
        st_command = os.path.join('api', 'controlcenter', 'st_controlcenter.py')
        #TODO: add a way to select which process we're starting
        self.CONTROLCENTER_PROCESS = self.start_st_process(st_command, f"Control Center is starting", "StreamTools ControlCenter")
        self.cc_status_label.configure(text = f"{self.check_if_process_running(self.CONTROLCENTER_PROCESS)}")
        self.start_cc_button.configure(text = "Stop StreamTools Control Center", command=self.stop_controlcenter)
    
    def stop_controlcenter(self):
        self.CONTROLCENTER_PROCESS.terminate()
        self.start_cc_button.configure(text = "Start StreamTools Control Center", command=self.start_controlcenter)
        self.CONTROLCENTER_PROCESS.status = "Control Center is not running"
        self.cc_status_label.configure(text = f"{self.CONTROLCENTER_PROCESS.status}")

    def create_ui_part(self, part = 'label', ):
        return None

    def __init__(self, master):
        # Create StreamTools desktop ui
        self.master = master
        master.geometry("640x480+0+0")
        master.title("StreamTools Desktop Interface")
        
        # Get server address from config
        self.server_address = f"{s.config['server_bind_address']}:{s.config['server_port']}"
        #TODO: build this programatically
        # Set initial state
        init_status = "Control Center is not running"
        # Create and place 'Start ControlCenter' button
        self.start_cc_button = tk.Button(master, text="Start StreamTools Control Center", command=self.start_controlcenter)
        self.start_cc_button.place(relx=0.5, rely=0.6, anchor="center")
        # Create and place URL label
        self.cc_url_label = tk.Label(master, text=f"Stream Control Center URL: {self.server_address}")
        self.cc_url_label.place(relx=0.5, rely=0.8, anchor="center")
        # Create and place ControlCenter status label
        self.cc_status_label = tk.Label(master, text=f"{init_status}")
        self.cc_status_label.place(relx=0.5, rely=0.7, anchor="center")

        # Deactivate virtual environment when window is closed
        master.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        # Close application window
        self.master.destroy()

    def update_status_label(self,process):
        process.status = self.check_if_process_running(process)
        self.cc_status_label = tk.Label(text=f"StreamTools Control Center Status: {process.status}")

root = tk.Tk()
stream_tools = StreamTools(root)
root.mainloop()
