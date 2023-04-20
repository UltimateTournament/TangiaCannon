import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import os
import gc

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"

print("Hello World!")

for network in wifi.radio.start_scanning_networks():
  print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
    network.rssi, network.channel))
wifi.radio.stop_scanning_networks()

print("Connecting to %s"%os.getenv("CIRCUITPY_WIFI_SSID"))
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print("Connected to %s!"%os.getenv("CIRCUITPY_WIFI_SSID"))
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

def runtest():
  print("Fetching text from", TEXT_URL)
  response = requests.get(TEXT_URL)
  print("-" * 40)
  print(response.text)
  print("-" * 40)

  print("Fetching json from", JSON_QUOTES_URL)
  response = requests.get(JSON_QUOTES_URL)
  print("-" * 40)
  print(response.json())
  print("-" * 40)

  gc.collect()
  print("done")
