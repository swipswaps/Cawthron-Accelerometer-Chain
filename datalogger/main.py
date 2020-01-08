# Author: Kevin Tangfrom machine import Pin, I2C, SPIfrom ds3231_port import DS3231from pyb import RTC, UART#from serial import Serialimport utimeimport timeimport sysimport os# mode and pull are specified in case pullups are absent.if sys.platform == 'pyboard':  # Pin connections  scl_pin = Pin('X9', pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)  sda_pin = Pin('X10', pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)  #tx_pin = Pin('Y9', pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)  #rx_pin = Pin('Y10', pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)    i2c = I2C(-1, scl=scl_pin, sda=sda_pin)  ds3231 = DS3231(i2c)    """  uart = UART(3, 9600)  uart.init(9600, bits=8, parity=None, stop=1)  uart.write('testing')  """  else: # ESP32  print('Incompatible system detected, please connect a pyboard')  # Date initialisationrtc = RTC()timeCheck = ds3231.get_time() # Gets current timertc.datetime((timeCheck[0], timeCheck[1], timeCheck[2], timeCheck[6], timeCheck[3], timeCheck[4], timeCheck[5], 0)) # Syncs RTC clock to local time"""# Sets up RTC clock, uncomment to manually set the clock (NOTE: DAY OF WEEK AND TIME ZONE IS NOT WORKING)rtc.datetime((2020, 1, 7, 2, 11, 26, 25, 0))  # Comment out if already programmedds3231.save_time()# RTC Format: YY, MM, DD, Day of week (Mon = 1), hh, mm, ss, time zone# Example: 16/12/2019 @ Monday 16:13:00# = rtc.datetime((2019, 12, 16, 1, 16, 13, 0, 0))"""# Modbus setupuart_id = 0x03modbus_obj = Serial(uart_id)######################### READ COILS #########################slave_addr = 0xA0starting_address = 0x00coil_quantity = 100#coil_status = modbus_obj.read_coils(slave_addr, starting_address, coil_quantity)#print('Coil status: ' + ' '.join('{:d}'.format(x) for x in coil_status))# TODO: Have a WDT to ensure that the csv file is made# Checks to see if the csv file is empty, then writes the file if it is emptytry:  with open("/sd/accelerometer.csv") as fileEmptyTest:    emptyTest = fileEmptyTest.read(1)    if not emptyTest:      print('writing header')      log_header = open("/sd/accelerometer.csv", "a")      log_header.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header.close()    else:      print('csv file is not empty')except:  print('writing header')  log_header = open("/sd/accelerometer.csv", "a")  log_header.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header.close()# Retrieves datedef getDate():  return str(rtc.datetime()[2]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[0])# Retrieves timedef getTime():  return str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])while True:  print(getDate()) # Date  print(getTime()) # Time   print()    time.sleep(1)er = open("/sd/accelerometer