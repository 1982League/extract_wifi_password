import subprocess
import re

cmnd_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
wifi_profile_names = (re.findall("All User Profile     : (.*)\r", cmnd_output))
all_wifi_list = list()

if len(wifi_profile_names) != 0:
    for wifi_name in wifi_profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", wifi_name], capture_output = True).stdout.decode()
        
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = wifi_name
            profile_pass = subprocess.run(["netsh", "wlan", "show", "profile", wifi_name, "key=clear"], capture_output = True).stdout.decode()
            pwd = re.search("Key Content            : (.*)\r", profile_pass)
        
            if pwd == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = pwd[1]
        
            all_wifi_list.append(wifi_profile)

for x in range(len(all_wifi_list)):
    print(all_wifi_list[x])
