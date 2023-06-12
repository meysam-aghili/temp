netsh interface set interface "Wi-Fi" disable
netsh interface ipv4 set dns "Wi-Fi" static 178.22.122.100
netsh interface ipv4 add dns "Wi-Fi" 185.51.200.2 index=2
netsh interface set interface "Wi-Fi" enable
@pause