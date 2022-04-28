#!/usr/bin/python3

# coding: utf-8


import json
import re
import requests

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkvpc.v2 import *
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion

def get_now_ip():
    url = "http://pv.sohu.com/cityjson"
    req = re.search('(\d{1,3}\.){3}\d{1,3}',requests.get(url).text)
    return (req.group())


def get_ListSecurityGroupRules():

    try:
        request = ListSecurityGroupRulesRequest()
        request.security_group_id = ""  #hw acl id
        response = client.list_security_group_rules(request)

        texts = response.to_json_object()["security_group_rules"]

        for text in texts:
            if (text["description"] == ""):  #select acl description
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

def add_SecurityGroupRules_OfficeIp(office_ip):
    try:
        request = CreateSecurityGroupRuleRequest()
        securityGroupRuleCreateSecurityGroupRuleOption = CreateSecurityGroupRuleOption(
            security_group_id="", #update acl conditions
            description="",
            direction="",
            remote_ip_prefix= office_ip
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
    
    #hw keys
    ak = ""
    sk = ""

    credentials = BasicCredentials(ak, sk) \

    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("")) \   #city
        .build()


    office_ip = get_now_ip()
    rules_id = get_ListSecurityGroupRules()
    del_ListSecurityGroupRules(rules_id)
    add_SecurityGroupRules_OfficeIp(office_ip)
