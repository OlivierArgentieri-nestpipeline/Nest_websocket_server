print("=========================")
print("Websocket server running")
print("=========================")

import os
import maya.cmds as cmds
import maya.utils as maya_utils
import json
import sys
from threading import Thread
import logging
from simple_websocket_server import WebSocketServer, WebSocket
from regedit import Regedit


class MayaWebSocketServer(WebSocket):
    def function_to_process(self, data):
        
        import maya.cmds as cmds
        print(data)
        
        out = ""
        if("print" in data):
            data = data.replace("print", "out = str")
        try:
            exec(data)
            logging.info("Maya Server out: {}".format(out))
            
            self.send_message(json.dumps(out))
            print(json.dumps(out))
            print('aaa')
        except Exception as exec_error:
            print('aaa error')
            cmds.warning("Maya Server, Exception processing Function: {}".format(exec_error))
            # self.send_message(exec_error)
        
    def handle(self):
        jo = json.loads(self.data)["msg"]
        self.cmd = jo
        if '#identify#' in self.cmd.lower():
            self.on_identify()
            return
            
        maya_utils.executeInMainThreadWithResult(self.function_to_process, self.cmd)
        
    def connected(self):
        self.on_identify()
        print(self.address, "connected")

    def handle_close(self):
        print(self.address, "closed")

    # --- actions callback --- # 
    def on_identify(self):
        exec_name = sys.executable.rsplit('\\',1)[1]
        exec_name = exec_name.split('.')[0]

        data ="name = cmds.file(q=True, sn=True).split('/')[-1]\nname = name if len(name)>0 else 'unsaved'\nprint(json.dumps({'fileName': name, 'execName': '" + exec_name + "'}, sort_keys=True))"
        maya_utils.executeInMainThreadWithResult(self.function_to_process, data)


class MyWebSocketClass(WebSocketServer):
    WebSocketServer.port = 0
    def __init__(self, host, port, websocketclass):
        super(MyWebSocketClass, self).__init__(host, port, websocketclass)
        WebSocketServer.port = self.serversocket.getsockname()[1]
        Regedit.set_reg(os.getenv('REGISTRY_PORT_PATH'), str(WebSocketServer.port), str(WebSocketServer.port))

# register on exit callback
def exit_handler():
    Regedit.rem_reg_value(os.getenv('REGISTRY_PORT_PATH'), str(WebSocketServer.port))
    
cmds.scriptJob(
    event=["quitApplication", exit_handler],
    protected=True
)

def start_server():
    server = MyWebSocketClass("0.0.0.0", 0, MayaWebSocketServer)
    server.serve_forever()

def stop_server():
    sys.exit()


thread = Thread(target=start_server, args=())
thread.start()