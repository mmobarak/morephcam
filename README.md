# Pi Camera Face Morph

This project implements a set of face morphing experiments that will serve as the basis of a few digital art projects. Images will initially be captured using a Raspberry Pi Camera V2 that hangs off a Raspberry Pi 4.

Watch this space for more info...

## Basic Pi Setup

After installing the Desktop version of Bookworm, update packages and add dev tools that may be required when installing Python packages. Some of these tools may already be installed but are included here in case you opt for a Lite installation of Bookworm.

```bash
sudo apt update
sudo apt full-upgrade
```

```bash
sudo apt install \
    git \
    cmake \
    ninja-build \
    autoconf \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev
```

## Set up Python

### Install Python3

```bash
sudo apt install \
    python3 \
    python3-pip 
```

### Use uv For Dependencies

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Raspberry Pi Camera Python Package

```bash
sudo apt install -y python3-picamera2
```

## Set Up Our Project

### Clone this repository

```bash
git clone https://github.com/mmobarak/morphcam.git
```


