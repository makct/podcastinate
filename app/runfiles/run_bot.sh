#!/bin/bash
gunicorn --config=python:gunicorn_config run:app
