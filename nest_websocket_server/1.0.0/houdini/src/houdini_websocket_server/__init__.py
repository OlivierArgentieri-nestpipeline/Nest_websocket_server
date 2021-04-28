print("=========================")
print("Websocket server running")
print("=========================")

#import maya.cmds
#import maya.utils as maya_utils
import sys
from threading import Thread

from simple_websocket_server import WebSocketServer, WebSocket


class SimpleEcho(WebSocket):
    def function_to_process(self):
        import json
        import maya.cmds
        aa = json.loads(self.data)
        print(aa)
        cmd = aa["msg"]
        print(cmd)
        try:
            exec("print('aaaa')")
            exec(cmd)
            #self.send_message(self.data)
        except Exception as e:
            print(e)
        
    def handle(self):
        self.function_to_process()

    def connected(self):
        print(self.address, "connected")

    def handle_close(self):
        print(self.address, "closed")



def start_server():
    server = WebSocketServer("0.0.0.0", 8765, SimpleEcho)
    server.serve_forever()

def stop_server():
    sys.exit()


thread = Thread(target=start_server, args=())
thread.start()