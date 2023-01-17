#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import re
import requests
from requests.adapters import HTTPAdapter

def get_old_ip():
    f = open('/home/data/yun/ip.txt','r')
    oldIP = f.read().strip()
    f.close()
    return oldIP

def get_now_ip():
    s = requests.session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    req = s.get('http://ifconfig.me', timeout=5)
    return (req.text)

def wirte_now_ip():
    text = open('/home/data/yun/ip.txt','w')
    text.write(new_ip)
    text.close

if __name__ == "__main__":
    old_ip = get_old_ip()
    new_ip = get_now_ip()
    #ali Fill in the value of the corresponding parameter
    os.system("python3 /home/data/yun/ali.py ali-key ali-secret \
        security_group_id region_id ecs_city " +old_ip+" "+new_ip)

    #hw Fill in the value of the corresponding parameter
    os.system("python3 /home/data/yun/hw.py ak sk \
         region_id group_id "+new_ip)
    wirte_now_ip()
