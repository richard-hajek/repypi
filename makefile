# You may or may not use this file, it is a shorthand
.PHONY: build

build: 
	venv/bin/python3 -m build

deploy:
	venv/bin/python3 -m twine upload --repository pypi dist/*

clean:
	rm dist/*
	rm -r src/*egg*

prepare:
	bash -c '[ -f rename.py ] && ./rename.py && rm rename.py || true'
	bash -c '[ -d venv ] || python3 -m venv venv'
	venv/bin/pip3 install twine build
	venv/bin/pip3 install -e .

