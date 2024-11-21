# Pi Camera Face Morph

This project implements a set of face morphing experiments that will serve as the basis of a few digital art projects. Images will initially be captured usong a Raspberry Pi Camera V2 that hangs off a Raspberry Pi 4.

Watch this space for more info...

## Basic Pi Setup

After installing the Desktop version of Bookworm, update packages and add dev tools. Some of these tools may already be installed but are included here in case you opt for a Lite installation of Bookworm.

```bash
sudo apt update
sudo apt full-upgrade
```

```bash
sudo apt install \
    git
```

## Set up Python

### Install Python3

```bash
sudo apt install \
    python3 \
    python3-pip 
```

### Create a Python Virtual Environment

Bookworm is strict about installing pakages in the global Python so we create a venv as our default python. This lets us `pip install` more tools like `Pipenv` to manage the virtual environments for our projects.

```bash
python -m venv --system-site-packages ~/env
```

In your `.bashrc` add the following to use your private python.

```bash
# set PATH so it includes user's default Python bin if it exists
if [ -d "$HOME/env/bin" ] ; then
    PATH="$HOME/env/bin:$PATH"
fi
```

### Install Pipenv to manage our project environments

```bash
bash # so that we pick up the new PATH
pip install pipenv
```

## Set Up Our Project

In this project's local repository:

```bash
pipenv install
```
