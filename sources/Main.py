import network

#Please change accordingly
ssid = "ssid"
password = "pw"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass

print('network config: ', wlan.ifconfig())