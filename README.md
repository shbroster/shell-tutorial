# Shell Tutorial

An interactive shell tutorial with accompanying presentation.

## Following Along in the Shell

Simply checkout this repository and open your shell in the checked-out directory.

## Presentation

## Installation

```shell
python3.10 -m venv venv --prompt shell-tutorial
source venv/bin/activate
pip install -r requirements.txt
python -m bash_kernel.install
cp -R venv/share/jupyter/nbconvert ~/Library/Jupyter/nbconvert
```

## Running the Presentation

```shell
source venv/bin/activate
jupyter nbconvert shell_tutorial.ipynb --to slides --post serve
deactivate
```

## Editing the Slides

```shell
source venv/bin/activate
jupyter jupyter notebook
deactivate
```
