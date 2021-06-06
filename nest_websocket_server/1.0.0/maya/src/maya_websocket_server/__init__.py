print("=========================")
print("Websocket server running")
print("=========================")

import maya.cmds as cmds
import maya.utils as maya_utils
import json
import sys
from threading import Thread
import logging
from simple_websocket_server import WebSocketServer, WebSocket


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

def start_server():
    server = WebSocketServer("0.0.0.0", 0, MayaWebSocketServer)
    server.serve_forever()

def stop_server():
    sys.exit()


thread = Thread(target=start_server, args=())
thread.start()