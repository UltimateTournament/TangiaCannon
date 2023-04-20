import json
import time
import usb_cdc

print("Data serial echo to repl on!")

serial = usb_cdc.data

while True:
    # read the secondary serial line by line when there's data
    # note that this assumes that the host always sends a full line
    if serial.in_waiting > 0:
        data_in = serial.readline()

        # try to convert the data to a dict (with JSON)
        data = None
        if data_in:
            try:
                data = json.loads(data_in)
            except ValueError:
                data = {"raw": data_in}

        # by using a dictionary, you can add any entry and data into it
        # to transmit any command you want and parse it here
        if isinstance(data, dict):
            print("got a dict! content:", data)

    # this is where the rest of your code goes
    # if the code does a lot you don't need a call to sleep, but if possible
    # it's good to have the microcontroller sleep from time to time so it's
    # not constantly chugging
    time.sleep(0.01)
