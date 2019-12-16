#Resources:
#- https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
import Adafruit_DHT

if __name__ == "__main__":
    sensor = Adafruit_DHT.DHT11
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
