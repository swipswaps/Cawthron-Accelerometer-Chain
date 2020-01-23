# Datalogger code for Cawthron Institute's mussel farm accelerometer chain# Author: Kevin Tangfrom machine import Pin, I2C, SPI, UART, WDTfrom ds3231_port import DS3231from pyb import RTCimport utimeimport timeimport sysimport os# Modesglobal DATA_RATE_1HZglobal DATA_RATE_2HZglobal MODEDATA_RATE_1HZ = 'one'DATA_RATE_2HZ = 'two'MODE = DATA_RATE_2HZ # Choose modes here (DATA_RATE_1HZ or DATA_RATE_2HZ)# Enable Watchdog timer. UNCOMMENT WHEN IN USE. COMMENT OUT IF CHANGES ARE NEEDED IN IDEwdt = WDT(timeout=15000) # enable with a timeout of 15 secondsif sys.platform == 'pyboard':  # Pin connections  tx_enable = Pin('X20', mode=Pin.OUT)    # RTC initialisation  i2c = I2C(1)   ds3231 = DS3231(i2c)    # UART initialisation  uart = UART(4, 115200) # Pins X1 and X2  uart.init(115200, bits=8, parity=None, stop=1, timeout=250) # Blocking UART  else:   print('Incompatible system detected, please connect a pyboard')  # Date initialisationrtc = RTC()timeCheck = ds3231.get_time() # Gets current timertc.datetime((timeCheck[0], timeCheck[1], timeCheck[2], timeCheck[6], timeCheck[3], timeCheck[4], timeCheck[5], 0)) # Syncs RTC clock to local time"""# Sets up RTC clock, uncomment to manually set the clock (NOTE: DAY OF WEEK AND TIME ZONE IS NOT WORKING)rtc.datetime((2020, 1, 22, 3, 15, 14, 50, 0))  # Comment out if already programmedds3231.save_time()# RTC Format: YY, MM, DD, Day of week (Mon = 1), hh, mm, ss, time zone# Example: 16/12/2019 @ Monday 16:13:00# = rtc.datetime((2019, 12, 16, 1, 16, 13, 0, 0))"""# Function to create and write headers for the accelerometer csvdef writeHeaders():  print('writing headers')  log_header1 = open("/sd/accelerometer1.csv", "a")  log_header1.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header1.close()  log_header2 = open("/sd/accelerometer2.csv", "a")  log_header2.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header2.close()  log_header3 = open("/sd/accelerometer3.csv", "a")  log_header3.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header3.close()  log_header4 = open("/sd/accelerometer4.csv", "a")  log_header4.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header4.close()  log_header5 = open("/sd/accelerometer5.csv", "a")  log_header5.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header5.close()  log_header6 = open("/sd/accelerometer6.csv", "a")  log_header6.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header6.close()  log_header7 = open("/sd/accelerometer7.csv", "a")  log_header7.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header7.close()  log_header8 = open("/sd/accelerometer8.csv", "a")  log_header8.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header8.close()  log_header9 = open("/sd/accelerometer9.csv", "a")  log_header9.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header9.close()  log_header10 = open("/sd/accelerometer10.csv", "a")  log_header10.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header10.close()# Checks to see if the csv file is empty, then writes the file if it is emptytry:  with open("/sd/accelerometer1.csv") as fileEmptyTest:    emptyTest = fileEmptyTest.read(1)    if not emptyTest:      writeHeaders()    else:      print('csv file is not empty')except OSError: # File does not exist, make the files and headers  writeHeaders()# Retrieves datedef getDate():  return str(rtc.datetime()[2]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[0])# Retrieves timedef getTime():  return str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])# Sleep timerdef rest():  if MODE == DATA_RATE_1HZ:    time.sleep(0.75)  else:    time.sleep(0.25)  # Reading UART value and converting to stringdef uartProcess():  test = uart.read()  dataString = str(test)[2:-4]  dataString = dataString.split('...')  splitString = [i.split(',') for i in dataString]  return splitString# Resets receiver data buffers and respective sleep values based on mode selection on first starttx_enable.value(1)uart.write(MODE)tx_enable.value(0)while True:  wdt.feed()  print(getDate()) # Date  print(getTime()) # Time    # Requests data from receivers  wdt.feed()  tx_enable.value(1)  uart.write('0')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '0'):    print('nice')    for i in range(len(splitString)):      log_header1 = open("/sd/accelerometer1.csv", "a")      log_header1.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header1.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('1')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '1'):    print('transmit')    for i in range(len(splitString)):      log_header2 = open("/sd/accelerometer2.csv", "a")      log_header2.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header2.close()    pyb.LED(3).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('2')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '2'):    for i in range(len(splitString)):      log_header3 = open("/sd/accelerometer3.csv", "a")      log_header3.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header3.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('3')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '3'):    for i in range(len(splitString)):      log_header4 = open("/sd/accelerometer4.csv", "a")      log_header4.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header4.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('4')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '4'):    for i in range(len(splitString)):      log_header5 = open("/sd/accelerometer5.csv", "a")      log_header5.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header5.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('5')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '5'):    for i in range(len(splitString)):      log_header6 = open("/sd/accelerometer6.csv", "a")      log_header6.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header6.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('6')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '6'):    for i in range(len(splitString)):      log_header7= open("/sd/accelerometer7.csv", "a")      log_header7.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header7.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('7')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '7'):    for i in range(len(splitString)):      log_header8= open("/sd/accelerometer8.csv", "a")      log_header8.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header8.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('8')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '8'):    for i in range(len(splitString)):      log_header9 = open("/sd/accelerometer9.csv", "a")      log_header9.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header9.close()    pyb.LED(4).on()    rest()    wdt.feed()  tx_enable.value(1)  uart.write('9')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '9'):    for i in range(len(splitString)):      log_header10 = open("/sd/accelerometer10.csv", "a")      log_header10.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")      log_header10.close()    pyb.LED(4).on()    rest()    print()  pyb.LED(4).off()  pyb.LED(3).off()