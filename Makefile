.PHONY: build

setup: create-env init

create-env:
	python3 -m venv env

install:
	./env/bin/python3 -m pip install $(package)

uninstall:
	./env/bin/pip3 uninstall $(package)

lock:
	./env/bin/pip3 freeze > requirements.txt

list:
	./env/bin/pip3 list

init:
	./env/bin/pip3 install -r requirements.txt

test:
	./execute_tests.sh 

build:
	python3 setup.py bdist_wheel

publish:
	twine upload dist/* --verbose

remove-old-builds:
	rm -rf ./.eggs ./build ./dist ./python_etl_pipeline.egg-info
