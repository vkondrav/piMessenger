#!/bin/bash

command=$1

if [ $command == "reload" ]; then
	sudo systemctl stop pimessenger.service
	sudo systemctl start pimessenger.service
        sudo service motion stop
        sudo service motion start
else
	sudo systemctl $command pimessenger.service
fi
