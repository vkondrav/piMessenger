#!/bin/bash

command=$1

if [ $command == "reload" ]; then
	sudo systemctl stop pimessenger.service
	sudo systemctl start pimessenger.service
else
	sudo systemctl $command pimessenger.service
fi
