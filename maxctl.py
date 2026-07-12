#!/usr/bin/env python
# Drive the Max MCP Node socket.io server (port 5002, namespace /mcp) directly,
# bypassing the (dead) server.py. Reads a JSON file: {"commands":[...], "requests":[...]}.
import sys, json, time, uuid, socketio

NS = "/mcp"
URL = "http://127.0.0.1:5002"

sio = socketio.Client(logger=False, engineio_logger=False)
responses = []

@sio.on("response", namespace=NS)
def on_response(data):
    responses.append(data)

def main():
    spec = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.load(sys.stdin)
    sio.connect(URL, namespaces=[NS], wait_timeout=5)
    for cmd in spec.get("commands", []):
        sio.emit("command", cmd, namespace=NS)
        time.sleep(spec.get("delay", 0.06))
    for req in spec.get("requests", []):
        req = dict(req); req["request_id"] = str(uuid.uuid4())
        sio.emit("request", req, namespace=NS)
    time.sleep(spec.get("wait", 0.6))
    sio.disconnect()
    print(json.dumps({"ok": True, "responses": responses}))

if __name__ == "__main__":
    main()
