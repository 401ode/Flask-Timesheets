#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_script import Manager, Server
from state_time import app

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 5000))
))

if __name__ == "__main__":
    manager.run()