name = "nest_websocket_server"
version = "1.0.0"


variants = [
    ["maya"],
    ["houdini"]
]

requires = [
    "simple_websocket_server",
    "regedit"
]

def commands():
    env.PATH.append("{root}/src")
    env.PYTHONPATH.append("{root}/src")
    env.MAYA_SCRIPT_PATH.append("{root}/src")
    env.HOUDINI_SCRIPT_PATH.append("{root}/src")
    
    # Server settings
    env.REGISTRY_PORT_PATH.append("SOFTWARE\\VueSocket\\ports")