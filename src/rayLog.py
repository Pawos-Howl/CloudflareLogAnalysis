import re

class CloudflareRayLog():
    def __init__(self,jsonEntry:dict):
        #self.json_raw=jsonEntry
        #self.json_data:dict=json.loads(jsonEntry)
        #if not isinstance(self.json_data,dict):
        #    raise ValueError(f"FAILED TO PARSE JSON:\n{self.json_raw}")
        # whats needed fur this is the asn, http version, and the number of items in the UA
        self.entryDict=jsonEntry

        self.ip=                  self.entryDict["clientIP"]
        self.action=              self.entryDict["action"]
        self.clientASNDescription=self.entryDict["clientASNDescription"]
        self.requestHost=         self.entryDict["clientRequestHTTPHost"]
        self.requestMethod=       self.entryDict["clientRequestHTTPMethodName"]
        self.requestProto=        self.entryDict["clientRequestHTTPProtocol"]
        self.requestPath=         self.entryDict["clientRequestPath"]
        self.datetime=            self.entryDict["datetime"]
        self.rayName=             self.entryDict["rayName"]
        self.userAgent=           self.entryDict["userAgent"]

    def userAgentLength(self)->int:
        """Returns the length of the userAgent in params (parenthesis segments count once)
        WARNING: UNTESTED"""
        length=0
        isParen=False
        for block in self.userAgent:
            # just in case
            if len(block) < 1: continue

            if not isParen: length+=1

            if block[0] == "(":   isParen = True
            elif block[-1] == ")": isParen = False
        
        return length

    def ipVersion(self)->int:
        """Returns 4 if the version of the IP protocol is IPv4, and returns 6 otherwise (since the regex is too big for me)"""
        # https://regexbox.com/regex-templates/ip
        ipv4=r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return ipv4.match(self.ip)
