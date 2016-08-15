This repository contains various scripts I used during U-Boot and kernel
development for the Raspberry Pi. I'm hosting it on github mainly for easy
backup purposes:-) push-flashair.py is hopefully useful to people wanting to
automated interaction with Toshiba FlashAir devices.

For the FlashAir scripts to work, you'll need to enable some features in your
config file, such as `UPLOAD=1`. Here's a complete example:

    [WLANSD]
    DHCP_Enabled=No
    IP_Address=192.168.1.4
    Subnet_Mask=255.255.255.0
    Default_Gateway=192.168.1.1
    Preferred_DNS_Server=192.168.1.1

    [Vendor]
    CIPATH=/DCIM/100__TSB/FA000001.JPG
    APPMODE=5
    APPNAME=flashair2
    APPSSID=YOUR_SSID
    APPNETWORKKEY=YOUR_PASSWORD
    VERSION=FA9CAW3AW3.00.00
    CID=YOUR_CID
    PRODUCT=FlashAir
    VENDOR=TOSHIBA
    UPLOAD=1
    MASTERCODE=YOUR_MASTERCODE
    LOCK=1
    APPINFO=0100000000000000
    APPAUTOTIME=300000
    REDIRECT=0
