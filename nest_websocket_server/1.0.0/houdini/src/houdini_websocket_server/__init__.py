print("=========================")
print("Websocket server running")
print("=========================")

import os
import hou
import json
import sys
from threading import Thread
import logging
from simple_websocket_server import WebSocketServer, WebSocket
from regedit import Regedit
import atexit


class HoudiniWebSocketServer(WebSocket):
    def function_to_process(self, data):
    
        out = ""
        if("print" in data):
            data = data.replace("print", "out = str")
        try:
            exec(data)
            logging.info("Houdini Server out: {}".format(out))
            
            self.send_message(json.dumps(out))
            print(json.dumps(out))
            print('aaa')
        except Exception as exec_error:
            print('aaa error')
            cmds.warning("Houdini Server, Exception processing Function: {}".format(exec_error))
            # self.send_message(exec_error)
        
    def handle(self):
        jo = json.loads(self.data)["msg"]
        self.cmd = jo
        if '#identify#' in self.cmd.lower():
            self.on_identify()
            return
            
        self.function_to_process(self.cmd)
        
    def connected(self):
        self.on_identify()
        print(self.address, "connected")

    def handle_close(self):
        print(self.address, "closed")

    # --- actions callback --- # 
    def on_identify(self):
        name = hou.hipFile.name() if hou.hipFile.name() != 'untitled.hip' else 'unsaved'
        exec_name = sys.executable.rsplit('\\', 1)[1]
        exec_name = exec_name.split('.')[0]
        data = json.dumps({'fileName': name, 'execName': exec_name}, sort_keys=True, indent=4)
        print(data)
        self.send_message(data)
        #self.close()
        
        # self.function_to_process(data)

class MyWebSocketClass(WebSocketServer):
    WebSocketServer.port = 0
    def __init__(self, host, port, websocketclass):
        super(MyWebSocketClass, self).__init__(host, port, websocketclass)
        WebSocketServer.port = self.serversocket.getsockname()[1]
        Regedit.set_reg(os.getenv('REGISTRY_PORT_PATH'), str(WebSocketServer.port), str(WebSocketServer.port))


def exit_handler():
    print(Regedit.rem_reg_value(os.getenv('REGISTRY_PORT_PATH'), str(WebSocketServer.port)))
    
atexit.register(exit_handler)




def start_server():
    server = MyWebSocketClass("0.0.0.0", 0, HoudiniWebSocketServer)
    server.serve_forever()

def stop_server():
    sys.exit()

thread = Thread(target=start_server, args=())
thread.start()