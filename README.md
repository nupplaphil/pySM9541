# SM9541 Python library

This Python library allows you to read data from the SM9541 Ultra-Low Pressure Digital Sensor on a Raspberry Pi, Pi2 or similar device.
Requirements

This library requires that you have installed the smbus-library

On Raspbian, you can install this package with the following commands:

sudo apt-get update
sudo apt-get install python-smbus

## Usage

To read a single set of data points from the SME9541, connect your Pi or Pi2 to the SM9541 breakout using I2C and run the following command from this folder:

python SM9541_Example.py

## Credits

