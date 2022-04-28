#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys
import json
import re
import requests

from typing import List
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models


def get_now_ip():
    url = "http://pv.sohu.com/cityjson"
    req = re.search('(\d{1,3}\.){3}\d{1,3}',requests.get(url).text)
    new_ip = open('/home/data/yun/ip.txt','w')
    new_ip.write(req.group())
    new_ip.close()
    return (req.group())

def get_old_ip():
    f = open('/home/data/ip.txt','r')
    oldIP = f.read().strip()
    f.close()
    return oldIP

def create_client():
    config = open_api_models.Config(
            # AccessKey ID,Secret
            access_key_id='',
            access_key_secret=''
        )
        # ecs city domain
    config.endpoint = ''
    return Ecs20140526Client(config)

def del_rules(old_ip):
    client = create_client()
    revoke_security_group_request = ecs_20140526_models.RevokeSecurityGroupRequest(
            region_id='',  #del acl conditions
            security_group_id='',
            port_range='',
            ip_protocol='',
            description='',
            source_group_id='',
            source_cidr_ip=old_ip
        )
    client.revoke_security_group(revoke_security_group_request)    

def add_rules(new_ip):
    client = create_client()
    authorize_security_group_request = ecs_20140526_models.AuthorizeSecurityGroupRequest(
            ip_protocol='',  # insert acl value
            port_range='',
            security_group_id='',
            region_id='',
            source_cidr_ip=new_ip,
            description='office ip'
        )
    client.authorize_security_group(authorize_security_group_request)


if __name__ == "__main__":
    old_ip = get_old_ip()
    del_rules(old_ip)
    new_ip = get_now_ip()
    add_rules(new_ip) 