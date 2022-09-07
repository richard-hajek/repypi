# RePyPI

Imagine, you just got hired to fix a legacy Python project. But the previous project maintainer did not bother to add versions to requirements.txt. If you know when was that project made, you can use `repypi` to populate `requirements.txt` with what was newest at the time! `repypi` will not touch any requirement lines that it fails to parse or that already have a version spec.

## Install

You may install using `pip install repypi` or `pipx install repypi`

## Usage

Example `requirements.txt`

```txt
# This is a comment
numpy
tensorflow
pandas
```

RePyPI can modify requirements.txt to contain newest packages on 01/01/2018

```bash
repypi -r requirements.txt -d "01/01/2018" 
```

With the resulting file being:

```
# This is a comment
numpy==1.14.0rc1
tensorflow==1.4.1
pandas==0.22.0
```

### Other examples

```bash
# Get newest version of wget now
repypi -p wget 
# wget==3.2

# Get newest version of wget at 1st of January 2015
repypi -p wget -d "01/01/2015"
# wget==2.2

```