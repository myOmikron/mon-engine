#!/usr/bin/env python

import uvicorn


uvicorn.run("q_web.asgi:application", host="127.0.0.1", port=8000)
