#!/bin/bash
exec &> >(tee -a "/var/logs/podcastinate_web.log")
python /opt/podcastinate/app/run.py
