netsh interface set interface "Wi-Fi" disable
netsh interface ipv4 set dns "Wi-Fi" dhcp
netsh interface set interface "Wi-Fi" enable
@pause