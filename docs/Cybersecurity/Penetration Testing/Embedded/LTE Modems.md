## General Information

There are several communications protocols used by modems. Years ago all modems used `PPP`, but even if your modern modem supports `PPP` you probably don't want to use it since it doesn't support very high bandwidth. For modern modems you will probably want to use either `MBIM` or `QMI`.

- `MBIM`, or Mobile Broadband Interface Model, is an official USB standard created by the USB Implementors Forum.
- `QMI` or Qualcomm Mobile Station Modem Interface was developed by Qualcomm and is only supported by Qualcomm chips. Many Qualcomm chips like the Sierra MC7455 support both `MBIM` and `QMI`.Both `MBIM` and `QMI` are actually just using existing Ethernet over USB standards with an added signalling channel.
- `MBIM` is just the NCM protocol + a signalling channel and QMI is just the ECM protocol + a signalling channel.
- `ECM` is the Ethernet Control Model and NCM is the Network Control Model. ECM is an earlier standard and has some issues with latency while NCM resolves those issues and is designed for high speed operation.

When configuring your modem, some settings can be changed with AT commands and others using the QMI signalling channel.

