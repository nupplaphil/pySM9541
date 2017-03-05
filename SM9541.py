# MIT License

# Copyright (c) 2017 Philipp Holzer, Karin Aicher

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import smbus
import logging

# SM9541 default address.
SM9541_I2CADDR = 0x28

SM9541_PMIN = -5             # Full Scale Minimum (for SM9541-100C-S-C-3-S)
SM9541_PMAX = 100            # Full Scale Maximum (for SM9541-100C-S-C-3-S)
SM9541_DIGOUTPMIN = 1638     # Pressure Output Minimum
SM9541_DIGOUTPMAX = 14745    # Pressure Output Maximal


class SM9541(object):

    def __init__(self):
        self._logger = logging.getLogger('SM9541')

        self._device = smbus.SMBus(1)
        self._sensP = (float)(SM9541_DIGOUTPMAX - SM9541_DIGOUTPMIN) / (
                      (SM9541_PMAX - SM9541_PMIN))

        self._load_calibration()

    def _load_calibration(self):
        self._device.write_quick(SM9541_I2CADDR)

    # Acquire block from sensor
    # ToDo: Read only neccessary 4 bytes
    def _read_register(self):
        # get full 32 byte register of the current block
        return self._device.read_i2c_block_data(SM9541_I2CADDR, 0)

    # Evaluate field (first 2 bits in first byte)
    #  00 ... Normal operation, good data packet
    #  01 ... Device in Command Mode (not normal operation)
    #  10 ... Stale data: Data that has already been fetched
    #  11 ... Diagnostic condition exists
    def _read_status(self, values):
        return (values[0] & 0xC0) >> 6

    def _read_raw_pressure(self, values):
        # part 1 (last 6 bits in first byte, shifted away for next bits)
        part1 = (values[0] & 0x3F) << 8
        # part 2 (8 bits in second byte)
        part2 = values[1]
        # Concatenate first and second part of the bitstream
        return part1 | part2

    def _read_raw_temperature(self, values):
        # part 1 (shifted away for next bits)
        part1 = values[0] << 3
        # part 2 (only first three bits)
        part2 = (values[1] & 0xE0) >> 5
        # Concatenate first and second part of the bitstream
        return part1 | part2

    def _read_pressure(self, values):
        raw_pressure = self._read_raw_pressure(values[:2])

        # Pressure from Counts to Scale
        return ((float)((raw_pressure - SM9541_DIGOUTPMIN) / self._sensP) +
                SM9541_PMIN)

    def _read_temperature(self, values):
        raw_temperature = self._read_raw_temperature(values[2:4])

        # Temperature constant transformation
        return ((float)(raw_temperature * 200) / 2048) - 50

    def read_all(self):
        values = self._read_register()
        return [
                self._read_status(values),
                self._read_pressure(values),
                self._read_temperature(values)
                ]

    def read_pressure(self):
        values = self._read_register()
        return self._read_pressure(values)

    def read_temperature(self):
        values = self._read_register()
        return self._read_temperature(values)
