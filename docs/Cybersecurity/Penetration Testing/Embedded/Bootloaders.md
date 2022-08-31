## Building U-Boot

A script to prepare your build environment and then build U-Boot for Renesas RCar3:

```bash
#!/bin/bash

echo "Installing required packages"
sudo apt-get install gcc-aarch64-linux-gnu -y
sudo apt-get install srecord -y
sudo apt-get install lzop -y
sudo apt-get install libssl-dev -y

echo "Downloading U-boot source code"
git clone https://gitlab.denx.de/u-boot/u-boot.git
cd u-boot
git checkout -b my_working_branch v2022.07

echo "Preparing the build environment"
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
make rcar3_ulcb_defconfig rcar3_salvator-x_defconfig
make
```
