import ipaddress, ssl, wifi, socketpool, adafruit_requests, os, gc

class WiFiController:
  InstructionLaunchOne = "launch_one"
  InstructionLaunchAll = "launch_all"
  InstructionLaunchFake = "launch_fake"

  def __init__(self) -> None:
    for network in wifi.radio.start_scanning_networks():
      print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
        network.rssi, network.channel))
    wifi.radio.stop_scanning_networks()

    print("Connecting to %s"%os.getenv("CIRCUITPY_WIFI_SSID"))
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print("Connected to %s!"%os.getenv("CIRCUITPY_WIFI_SSID"))
    print("My IP address is", wifi.radio.ipv4_address)

    self.ipv4 = ipaddress.ip_address("8.8.4.4")
    print("Ping google.com: %f ms" % (wifi.radio.ping(self.ipv4)*1000))

    self.pool = socketpool.SocketPool(wifi.radio)
    self.requests = adafruit_requests.Session(self.pool, ssl.create_default_context())
    self.token = os.getenv("TANGIA_TOKEN")
    self.api = os.getenv("TANGIA_API")
    print("all setup! ready to check the network")

  def pollInteractions(self):
    """
    Returns either `None` or a dict:
    ```
    {
      "Instruction": "launch_one" | "launch_all" | "launch_fake",
      "ExecutionID": string
    }
    ```
    """
    url = self.api + "/cannon/pending"
    print("Polling interactions from", url)
    response = self.requests.get(url, headers={"Authorization": "Bearer {}".format(self.token)})
    if response.status_code == 204:
      print("got nothing")
      return None
    elif response.status_code > 299:
      print("got high status code", response.status_code, response.text)
      return None
    else:
      return response.json()

  def ackInteraction(self, aeID):
    url = self.api + "/v2/actions/ack/{}".format(aeID)
    print("Acking action execution at", url)
    response = self.requests.post(url, headers={"Authorization": "Bearer {}".format(self.token)})
    print("ack response code:", response.status_code)
    gc.collect()
