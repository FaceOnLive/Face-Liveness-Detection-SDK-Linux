#!/bin/bash

exec python3 app.py &
exec python3 gradio/demo.py