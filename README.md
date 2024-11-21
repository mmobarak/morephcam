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
    git \
    cmake
```

## Set up Python

### Install Python3

```bash
sudo apt install \
    python3 \
    python3-pip 
```

### Install Raspberry Pi Camera Python Package

```bash
sudo apt install -y python3-picamera2
```

## Set Up Our Project

### Create the Python Virtual Environment

In this project's local repository:

```bash
python -m venv --system-site-packages .venv
source .venv/bin/activate
```

### Install our Python dependencies

```bash
pip install -r requirements.txt
```
