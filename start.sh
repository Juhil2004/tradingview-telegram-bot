#!/bin/bash
uvicorn app:app --bind 0.0.0.0:$PORT
