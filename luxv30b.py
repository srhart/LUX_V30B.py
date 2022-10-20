"""
MicroPython DF Robot B LUX V30B driver

MIT License
Copyright (c) 2022 Stephen Hart
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
   The description of this register is copied from the data sheet
     * ------------------------------------------------------------------------------------------
     * |    b7    |    b6    |    b5    |    b4    |    b3    |    b2    |    b1     |    b0    |
     * ------------------------------------------------------------------------------------------
     * |    0     |  MANUAL  |    0     |     0    |    CDR   |               TIM               |
     * ------------------------------------------------------------------------------------------
     *MANUAL  : Manual configuration register.
                0 represents the default automatic mode.In this mode ,CDR and TIM are automatically assigned.
     *          1 represents the configuration of manual mode.In this mode,CDR and TIM can be set by the user.
     *CDR     : Shunt ratio register.
     *          0 represents the default of not dividing,all the current of the photodiode into the ADC
     *          1 represents the division of 8,as long as 1/8 of the current of the photodiode changes to ADC. This mode is used in high brightness situations.
     *TIM[2:0]: Acquisition time.
     *        ------------------------------------------------------------------------------------------------
     *          TIM[2:0]  |  TIME(ms)  |                          Introduction                             |
     *        ------------------------------------------------------------------------------------------------
     *             000    |      800     |            Preferred mode in low light environment                |
     *        ------------------------------------------------------------------------------------------------
     *             001    |      400     |                               ---                                 |
     *        ------------------------------------------------------------------------------------------------
     *             010    |      200     |                               ---                                 |
     *        ------------------------------------------------------------------------------------------------
     *             011    |      100     |   In the strong light environment, select the mode preferentially |
     *        ------------------------------------------------------------------------------------------------
     *             100    |      50      |                       Manual mode only                            |
     *        ------------------------------------------------------------------------------------------------
     *             101    |      250     |                       Manual mode only                            |
     *        ------------------------------------------------------------------------------------------------
     *             110    |      12.5    |                       Manual mode only                            |
     *        ------------------------------------------------------------------------------------------------
     *             111    |      6.25    |                       Manual mode only                            |
     *        ------------------------------------------------------------------------------------------------
     *Accuracy that can be set in manual mode:
     *     -------------------------------------------------------------------------------------------------------------
     *     |                    Light conditions                        |                        |     TIM & CDR       |
     *     -------------------------------------------------------------------------------------------------------------
     *     |   Minimum accuracy    |   Maximum accuracy   |   Maximum   |  Acquisition time(ms)  |    TIM     |   CDR  |
     *     —------------------------------------------------------------------------------------------------------------
     *              0.054                     11.52            2938                800                000           0   
     *              0.09                      23.04            5875                400                001           0   
     *              0.18                      46.08            11750               200                010           0   
     *              0.36                      92.16            23501               100                011           0   
     *              0.36                      92.16            23501               800                000           1   
     *              0.72                      184.32           47002               50                 100           0   
     *              0.72                      184.32           47002               400                001           1   
     *              1.44                      368.64           94003               25                 101           0   
     *              1.44                      368.64           94003               200                010           1   
     *              2.88                      737.28           200000              12.5               110           0   
     *              2.88                      737.28           200000               100               011           1   
     *              5.76                      737.28           200000               6.25              111           0   
     *              5.76                      737.28           200000               50                100           1   
     *              11.52                     737.28           200000               25                101           1   
     *              23.04                     737.28           200000               12.5              110           1   
     *              46.08                     737.28           200000               6.25              111           1   
     *     —------------------------------------------------------------------------------------------------------------
  """

__version__ = '0.0.1'


# i2C Address
_LUXV30B_ADDRESS     = const(0x4a) # Can't be changed

# registers
_LUXV30B_RO_REG      = const(0x00) # 32A Lighting values
_LUXV30B_RO_LEN      = const(4) # Lenght of read only register bytes
_LUXV30B_CONFIG      = const(0x04) # Configuration

class LUXV30B_TIME_MODE():
    T800ms = 0
    T400ms = 1
    T200ms = 2
    T100ms = 3
    T50ms = 4
    T25ms = 5
    T12_5ms = 6
    T6_25ms = 7

class LUXV30B_CDR_MODE():
    CDR_0 = 0<<3
    CDR_1 = 1<<3

class LUXV30B_MANUAL_MODE():
    Auto = 0<<6
    Manual = 1<<6

class LUXV30B:
    def __init__(self, i2c=None, address=_LUXV30B_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.buf = bytearray(_LUXV30B_RO_LEN)
        self.conf = bytearray(1)
        self.conf[0]= 0x00 # Power on default

    def check(self, i2c):
        if i2c.scan().count(_LUXV30B_ADDRESS) == 0:
            raise OSError('LUX_V30B not found at I2C address {:#x}'.format(_LUXV30B_ADDRESS))

    def get_lux(self):
        buf = self.buf
        address = self.address
        self.i2c.readfrom_mem_into(address,_LUXV30B_RO_REG,buf)
        lf = buf[3]
        lf = (lf << 8)|buf[2]
        lf = (lf << 8)|buf[1]
        lf = (lf << 8)|buf[0]
        return float(lf * 1.4) / 1000

    def set_conf(self, mode, cdr, time):
        # TBD
        pass

    def get_conf(self):
        conf = self.conf
        address = self.address
        self.i2c.readfrom_mem_into(address,_LUXV30B_CONFIG,conf)
        self.conf = conf
        return self.conf
