#!/usr/bin/python3
# -*- coding: utf-8 -*-"

import dns.resolver
import time

myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['172.17.0.2']
myResolver.port = 53
filename = "./monitor-log/peach-dns-log"

try:
    myAnswers = myResolver.resolve("baidu.com", lifetime=2)
except:
    with open(filename,'a')as file:
        file.write(time.strftime("%Y-%m-%d %X", time.localtime()) + " " + myResolver.nameservers + " dns error\n")
    print("error")
else:
    print("success")