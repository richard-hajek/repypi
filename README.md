# Project name

You may use this template to create Python packages quickly.

## Setup

### Minimal installation

- [ ] Clone this repo `https://github.com/richard-hajek/python-setuptools-package-template.git`
- [ ] Run `make prepare`

### Full installation

- [ ] Remove `.git` folder
- [ ] In your setup.cfg
  - [ ] Change install_requirements in `[options]` to fit your needs
  - [ ] Change console_scripts in `[options.entry_points]` to fit your needs ( or delete it )
  - [ ] Change `name`, `version`, `author`, `author_email`, `description`, `version`
- [ ] Add your own README
- [ ] Add LICENSE

## Running the code

You have several options of running any source code you write. In any case, always source the venv before `source venv/bin/activate`

### Run as `__main__`

```bash
python main.py [args]
```

> This will work **if** you never import from any other directory than from the same one.
If you ever import a module from a different folder **this will not work**. 

### Run as module

```bash
pip install -e . # Run at least once
python -m project_name.main [args]
```

> This method will correctly construct the Python library tree, so you can import from any directory you like

### Run as entrypoint

See [Full Installation](#Full-installation) and [python - How to setup entry_points in setup.cfg - Stack Overflow](https://stackoverflow.com/questions/48884796/how-to-setup-entry-points-in-setup-cfg/48891252)