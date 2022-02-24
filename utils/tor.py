#!/usr/env python3

from stem.control import Controller


controller = Controller.from_port(address="127.0.0.1", port=9051)
try:
    controller.authenticate()
except Exception as e:
    print(e)

host = "127.0.0.1"
port = 8080

hidden_svc_dir = "/app/hidden_service/"

controller.set_options([
    ("HiddenServiceDir", hidden_svc_dir),
    ("HiddenServicePort", "80 %s:%s" % (host, str(port)))
])

svc_name = open(hidden_svc_dir + "/hostname", "r").read().strip()
print("#" * 84)
print("# Local Service: http://%s:%s" % (host, port))
print("# Tor Hidden Service: %s" % svc_name)
print("#" * 84)
