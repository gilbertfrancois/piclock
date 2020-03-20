# piclock

A clock for Raspberry Pi with Adafruit PiTFT 2.8" screen. The project is written in Python, using pygame, rendering
directly to the framebuffer `/dev/fb0`. 

## Installation

Install the Adafruit screen as described [here](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2) and follow the directions for _PiTFT as Text Console (best for Raspbian 'Lite')_.

Run `poetry install` or install manually the dependencies listed in `pyproject.toml`

## Run

With poetry:
```
cd src/piclock
poetry run python3 main.py
```

With system python:
```
cd src/piclock
python3 main.py
```

![piclock](images/IMG_5926.jpeg)
