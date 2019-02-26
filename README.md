Sonopi Digi
===
![project phase](https://img.shields.io/badge/project%20phase-PCB%20designing-green.svg)

Sonopi Digi is a hat card for Raspberry Pi to add a S/PDIF digital sound output capability.<br>
This hardware design is published under open source lincence. You can use and modify this design freely. There is also no limitation in commercial use.

In order to export digital sound signal, Sonopi use a [Cirrus Logic WM8804](https://www.cirrus.com/products/wm8804/) as a S/PDIF transmitter.
There are many kind of Raspberry Pi Hats installed WM8804 in the world. This IC is a defacto standard to add a S/PDIF output functionality to Raspberry Pi.

## Projcect Status
I've finished PoC on a bread board. That worked fine<br>
I start to design PCB.

## Design Goals
1. **Target to casual use and reasnable cost**<br>
Sonopy Digi is not a device for audiophiles. It's a just simple solution to realize connectivity to audio amplifier without serious noise. I don't expect to install expensive parts and also don't expect to stick to beautiful circuit patterning to improve analog characteristics.<br>
Sonopi Digi should be realized with minimum components, and should be eliminated analog circuit portion. Therefore, only optical output is installed on this product. An coaxial output which need analog driver circuit is not suitable to Sonopi Digi design policy.

2. **Not necessory any additional software**<br>
I don't want to make any software to use Sonopy Digi. Sonopi Digi should be designed to work by using standard device driver and standard device tree overlay configuration.<br>
Specifically, Sonopi Digi is designed to work when following line is added to `/boot/config.txt`.

    ```
    dtoverlay=hifiberry-digi
    ```

## Design Overview
The keypoint of Sonopi Digi hardware design is configuring WM8804 to adapt to following device driver and device tree configuration.

- [hifiberry-digi-overlay.dts](https://github.com/raspberrypi/linux/blob/e2d2941326922b63d722ebc46520c3a2287b675f/arch/arm/boot/dts/overlays/hifiberry-digi-overlay.dts)
- [rpi-wm8804-soundcard.c](https://github.com/raspberrypi/linux/blob/e2d2941326922b63d722ebc46520c3a2287b675f/sound/soc/bcm/rpi-wm8804-soundcard.c)

These files shows following condition regarding WM8804 configuration.

- Must be driven 27MHz crystal oscillation circuit
- Must be configureed with 2 wire software mode.
- I2C device address must be 0x3b

That means WM8804 pin condition should be as below.

WM8804 PIN        |   Configuration
------------------|-------------------------------------------------
XIN(11), XOP(10)  | 27MHz crystal
RSTB(6)           | Pull up to 3.3V
SDIN(3)           | Raspberry Pi I2C1 SDA pin
GPO0(2)           | Pull down to GND
CSB(5)            | Pull up to 3.3V
SCLK(1)           | Raspberry Pi I2C1 SCL
BCLK(14)          | Raspberry Pi I2S BCLK
LRCLK(15)         | Raspberry Pi I2S LRCLK
DIN(13)           | Raspberry Pi I2S DOUT
TXO(17)           | Optical S/PDIF transmitter module

## PoC Result
The PoC is concluded with great success.

<p align="center">
<img alt="description" src="https://raw.githubusercontent.com/wiki/opiopan/sonopi-digi/images/poc.jpg" width=600>
</p>

