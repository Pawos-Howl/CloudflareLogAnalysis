#! /usr/bin/env python3
# fluff having a linter
import json, os, argparse

class LogItem():
    """For each item in logs"""

    def __init__(self,jsonEntry:dict):
        #self.json_raw=jsonEntry
        #self.json_data:dict=json.loads(jsonEntry)
        #if not isinstance(self.json_data,dict):
        #    raise ValueError(f"FAILED TO PARSE JSON:\n{self.json_raw}")
        self.entry_dict=jsonEntry

        self.ip=                  self.entry_dict["clientIP"]
        self.action=              self.entry_dict["action"]
        self.clientASNDescription=self.entry_dict["clientASNDescription"]
        self.requestHost=         self.entry_dict["clientRequestHTTPHost"]
        self.requestMethod=       self.entry_dict["clientRequestHTTPMethodName"]
        self.requestProto=        self.entry_dict["clientRequestHTTPProtocol"]
        self.requestPath=         self.entry_dict["clientRequestPath"]
        self.datetime=            self.entry_dict["datetime"]
        self.rayName=             self.entry_dict["rayName"]
        self.userAgent=           self.entry_dict["userAgent"]

class LogAnalysis():
    """analyze all of the logs as an input"""
    def __init__(self,json_file:PathLike):
        if not os.path.exists(json_file): raise FileNotFoundError(f"JSON FILE {json_file} MISSING")
        fd=open(json_file,'r',encoding='utf-8')
        self.json_raw=fd.read()
        fd.close()
        self.json_data:list=json.loads(self.json_raw)
        self.logItems:LogItem=(LogItem(s) for s in self.json_data)
    
    def pullBadIPs(self, threshold:int)->list[str]:
        """returns a list of bad ips based on how many times they sent requests
        threshold is an int for the max times a request can be sent"""
        ipStats={}
        for x in self.logItems:
            if not x.ip in ipStats.keys():
                ipStats[x.ip]=1
            else:
                ipstats[x.ip]+=1
                # seperate to make me feel happy :p
        # done with the loop, analysis time
        badIPs=[]
        for x in ipStats.keys():
            if ipStats.get(x) > threshold:
                badIPs.append(x)
        return badIPs



if __name__ == "__main__":
    parser=argparse.ArgumentParser(prog="Cloudflare Log Analyzer",
        description="Analyzes Cloudflare logs in a fairly basic way. written very late at night",
        epilog="wruffwruffwruff")
    parser.add_argument('filename')
    parser.add_argument("-c",dest='badIpThreshold',type=int,default=0)
    args=parser.parse_args()
    # by this point, args.filename should exist
    mainclass = LogAnalysis(args.filename)
    print(mainclass.pullBadIPs(args.badIpThreshold))
