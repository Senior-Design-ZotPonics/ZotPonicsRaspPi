#Resources:
#- https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
import Adafruit_DHT
import time

if __name__ == "__main__":
    sensor = Adafruit_DHT.DHT11
    pin = 4
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print("Humidity(%):",humidity,"|", "Temperature(C):", temperature)
        time.sleep(2)
