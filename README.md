HTU21D
======

Use the [HTU21D](https://cdn-shop.adafruit.com/datasheets/1899_HTU21D.pdf) temperature and humidity sensor
on the Raspberry Pi.

## Prerequisites

* python-smbus

## Usage

```
from HTU21D import HTU21D

print HTU21D(1).read_temperature()
```

## License
I hereby place this code in the public domain.
