#!/usr/bin/python3
from smbus import SMBus
import time

I2C_ADDR = 0x40
CMD_TRIG_TEMP_HM = 0xE3
CMD_TRIG_HUMID_HM = 0xE5
CMD_TRIG_TEMP_NHM = 0xF3
CMD_TRIG_HUMID_NHM = 0xF5
CMD_WRITE_USER_REG = 0xE6
CMD_READ_USER_REG = 0xE7
CMD_RESET = 0xFE

class HTU21D:
    def __init__(self, busno):
        self.bus = SMBus(busno)
        self.reset()

    def read_temperature(self):
        nreads = 6
        while nreads != 0:
            try:
                msb, lsb, crc = self.bus.read_i2c_block_data(I2C_ADDR, CMD_TRIG_TEMP_HM, 3)
                if(crc != self._calculate_checksum(msb,lsb)):
                    raise IOError("I2c: Bad CRC")
                break
            except OSError:
                time.sleep(0.5)
                nreads = nreads - 1
        if nreads == 0:
            raise IOError("I2c I/O Error")
        return -46.85 + 175.72 * (msb * 256 + lsb) / 65536
     
    def read_humidity(self):
        nreads = 6
        while nreads != 0:
            try:
                msb, lsb, crc = self.bus.read_i2c_block_data(I2C_ADDR, CMD_TRIG_HUMID_HM, 3)
                if(crc != self._calculate_checksum(msb,lsb)):
                    raise IOError("I2c: Bad CRC")
                break
            except OSError:
                time.sleep(0.5)
                nreads = nreads - 1
        if nreads == 0:
            raise IOError("I2c I/O Error")
        return -6 + 125 * (msb * 256 + lsb) / 65536.0

    def reset(self):
        self.bus.write_byte(I2C_ADDR, CMD_RESET)
        time.sleep(0.015)

    @staticmethod
    def _calculate_checksum(msb,lsb):
        """5.7 CRC Checksum using the polynomial given in the datasheet"""
        # CRC
        POLYNOMIAL = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0
        # calculates 8-Bit checksum with given polynomial
        for b in msb,lsb:
            crc ^= b
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc = (crc << 1)
        return crc


if __name__ == '__main__':
    htu = HTU21D(1)
    try:
       print( "T=",htu.read_temperature())
       print( "H=",htu.read_humidity())
    except IOError as e:
       print( e )
