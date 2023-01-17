#!/usr/bin/python3

# coding: utf-8

import sys

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkvpc.v2 import *
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion

def get_ListSecurityGroupRules():

    try:
        request = ListSecurityGroupRulesRequest()
        request.security_group_id = group_id
        response = client.list_security_group_rules(request)

        texts = response.to_json_object()["security_group_rules"]

        for text in texts:
            if (text["description"] == "office-ip"):
               rules_id = text["id"]
               break
        return (rules_id)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

def del_ListSecurityGroupRules(rules_id):
    try:
        request = DeleteSecurityGroupRuleRequest()
        request.security_group_rule_id = rules_id
        response = client.delete_security_group_rule(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)    

def add_SecurityGroupRules_OfficeIp(new_ip):
    try:
        request = CreateSecurityGroupRuleRequest()
        securityGroupRuleCreateSecurityGroupRuleOption = CreateSecurityGroupRuleOption(
            security_group_id=group_id,
            description="office-ip",
            direction="ingress",
            remote_ip_prefix= new_ip
        )
        request.body = CreateSecurityGroupRuleRequestBody(
            security_group_rule=securityGroupRuleCreateSecurityGroupRuleOption
        )
        response = client.create_security_group_rule(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)    



if __name__ == "__main__":
    
    ak = sys.argv[1]
    sk = sys.argv[2]
    region_id = sys.argv[3]
    group_id = sys.argv[4]
    new_ip = sys.argv[5]

    credentials = BasicCredentials(ak, sk) \

    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of(region_id)) \
        .build()

    rules_id = get_ListSecurityGroupRules()
    del_ListSecurityGroupRules(rules_id)
    add_SecurityGroupRules_OfficeIp(new_ip)
