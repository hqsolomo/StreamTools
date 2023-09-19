class ST_Process:
    
    def __init__(self, process, status = None, label = None):
        self.process = process
        self.status = status
        self.label = label

    def terminate(self):
        self.process.terminate()

    def pid(self):
        return self.process.pid