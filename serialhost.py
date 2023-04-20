import json, serial, time

# channel = serial.Serial("/dev/cu.usbmodem487F301FFAAB1", baudrate=115200) # esp
channel = serial.Serial("/dev/cu.usbmodem1432203", baudrate=115200) # pico
channel.timeout = 0.05

while True:
    print("sending")
    channel.write(json.dumps({"test": "data"}).encode())
    channel.write(b'\n')
    time.sleep(0.01)
    print("recv")
    line = channel.readline()
    print(line.decode("utf8"))
    time.sleep(2)
