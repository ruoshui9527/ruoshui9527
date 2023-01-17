#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient



def create_client():
    config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
    config.endpoint = ecs_city
    return Ecs20140526Client(config)


def del_rules():
    client = create_client()
    revoke_security_group_request = ecs_20140526_models.RevokeSecurityGroupRequest(
            region_id=region_id,
            security_group_id=security_group_id,
            port_range='-1/-1',
            ip_protocol='all',
            description='office-ip',
            source_cidr_ip=old_ip
        )
    client.revoke_security_group(revoke_security_group_request)    



def add_rules():
    client = create_client()
    authorize_security_group_request = ecs_20140526_models.AuthorizeSecurityGroupRequest(
            ip_protocol='all',
            port_range='-1/-1',
            security_group_id=security_group_id,
            region_id=region_id,
            source_cidr_ip=new_ip,
            description='office-ip'
        )
    client.authorize_security_group(authorize_security_group_request)



if __name__ == "__main__":
    access_key_id = sys.argv[1]
    access_key_secret = sys.argv[2]
    security_group_id = sys.argv[3]
    region_id = sys.argv[4]
    ecs_city = sys.argv[5]
    old_ip = sys.argv[6]
    new_ip = sys.argv[7]
    del_rules()
    add_rules() 
