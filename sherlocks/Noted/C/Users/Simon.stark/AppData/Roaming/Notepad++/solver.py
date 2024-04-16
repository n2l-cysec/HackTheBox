import datetime,re


# first flag 
# What is the full path of the script used by Simon for AWS operations?
def AWS_objects():
    config = open('config.xml', 'r').read()
    find = re.findall(r'<File filename="C:\\Users\\Simon.stark\\Documents\\Dev_Ops\\(.*?)" />', config)
    print(find[0])
AWS_objects()

# second flag
# The attacker duplicated some program code and compiled it on the system, knowing that the victim was a software engineer and had all the necessary utilities. They did this to blend into the environment and didn't bring any of their tools. This code gathered sensitive data and prepared it for exfiltration. What is the full path of the program's source file?
def MalwareSource():
    session = open('config.xml', 'r').read()
    find = re.findall(r'filename="(.*?)"', session)
    print(find[0])
MalwareSource()

# third flag
# What's the name of the final archive file containing all the data to be exfiltrated?
def ResultsMalware():
    sourcemw = open('backup/LootAndPurge.java@2023-07-24_145332', 'r').read()
    find = re.findall(r'zipFilePath = "C:\\Users\\Simon.stark\\Desktop\\(.*?)"', sourcemw)
    print(find[0])
ResultsMalware()

# fourth flag
# What's the timestamp in UTC when attacker last modified the program source file?
# we get timestamp low and high from session.xml
def calculateTime():
    timestamp_low = -1354503710
    timestamp_high = 31047188

    full_timestamp = (timestamp_high << 32) | (timestamp_low & 0xFFFFFFFF)

    timestamp_seconds = full_timestamp / 10**7
    timestamp = datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=timestamp_seconds)
    print(timestamp)
calculateTime()

#fifth flag
#The attacker wrote a data extortion note after exfiltrating data. What is the crypto wallet address to which attackers demanded payment?
# open https://pastebin.com/CwhBVzPq with password sdklY57BLghvyh5FJ#fion_7 ( we get from SOurce malware java )
# 0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca

# sixth flag
#What's the email address of the person to contact for support?
#CyberJunkie@mail2torjgmxgexntbrmhvgluavhj7ouul5yar6ylbvjkxwqf6ixkwyd.onion