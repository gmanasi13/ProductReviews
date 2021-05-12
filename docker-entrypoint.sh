#!/bin/sh
#set -e
set -x
export FLASK_APP=app.py

case "$1" in
	deploy)
		python3 app.py
		;;
	test )
		python3 test_isi.py
		;;
esac
