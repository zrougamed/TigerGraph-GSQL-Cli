from requests.models import cookiejar_from_dict
from rich.console import Console
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from time import sleep
import time
import argparse 
import requests 
import json
import base64
import asyncio
import aiohttp
import sys
import re 
#coding=utf-8
import sys
import math


class ProgressBar(object):

    FG = '\033[38;5;{}m'
    BG = '\033[48;5;{}m'
    RESETFG = '\033[39m'
    RESETBG = '\033[49m'

    COLORS = {
        'fill': [33],
        'border': [None],
        'text': [235]
    }

    def __init__(self, width=80, **kwargs):
        self.width = width
        self.progress = 0.0

        self.colors = dict(self.COLORS)
        for k, v in kwargs.items():
            if k in self.COLORS:
                if type(v) in (int, str, type(None)):
                    v = [v]
                self.colors[k] = v

    def _progressive_color(self, n):
        colorset = self.colors[n]
        n = len(colorset)
        return colorset[int(math.ceil(self.progress * n) - 1)]

    def setfg(self, colortype):
        c = self._progressive_color(colortype)
        if c is not None:
            sys.stdout.write(self.FG.format(c))
        else:
            self.resetfg()

    def resetfg(self):
        sys.stdout.write(self.RESETFG)

    def setbg(self, colortype):
        c = self._progressive_color(colortype)
        if c is not None:
            sys.stdout.write(self.BG.format(c))
        else:
            self.resetbg()

    def resetbg(self):
        sys.stdout.write(self.RESETBG)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass

    def render(self):
        # Topbar
        self.setfg('border')
        sys.stdout.write(u'▁' * self.width)
        sys.stdout.write('\n')

        # Left edge
        sys.stdout.write(u'█')

        # Contents
        self.setfg('fill')
        full_width = (self.width - 2) * self.progress
        blocks = int(full_width)
        remainder = full_width - blocks

        sys.stdout.write(u'█' * blocks)

        if remainder:
            sys.stdout.write(u' ▏▎▍▌▋▊▉█'[int(remainder * 8)])

        sys.stdout.write(u' ' * (self.width - 3 - blocks))

        # Right edge
        self.setfg('border')
        sys.stdout.write(u'█')
        sys.stdout.write('\n')

        # Bottom bar
        sys.stdout.write(u'▔' * self.width)
        sys.stdout.write('\n')

        # Interior text indicator
        percent = ' ' + str(int(self.progress * 100)) + '%'
        if blocks >= len(percent):
            sys.stdout.write('\x1b7\x1b[2G\x1b[2A')
            self.setbg('fill')
            self.setfg('text')
            sys.stdout.write(percent)
            sys.stdout.write('\x1b8')

        self.resetfg()
        self.resetbg()
        sys.stdout.flush()

    def start(self):
        self.render()

    def set(self, progress):
        """
        Set progress to a specific value and redraw.

        :param progress: Fraction of the bar to fill. Clamped to [0, 1].
        """
        self.progress = min(max(progress, 0.0), 1.0)

        # Restore cursor position and redraw
        sys.stdout.write('\x1b[?25l')
        sys.stdout.write('\x1b[3F')
        self.render()
        sys.stdout.write('\x1b[?25h')

    def tick(self, amount):
        """
        Increment progress by the specified fraction and redraw.
        """
        self.set(amount)



 # command

host = "http://127.0.0.1:14240"
port = "14240"


# Console 
console = Console()


# Variables 
cookies = aiohttp.CookieJar()
nbActual = 0
nbTotal = 0
diff = 0


# UTILITIES 

REGEX = "\[.*?\]\s*([0-9]\d*|0)+%.*\(([1-9]\d*|0)\/([1-9]\d*|0)\)"
GSQL_SEPERATOR = "__GSQL__"
GSQL_COOKIES = "__GSQL__COOKIES__"

COMMAND_ENDPOINT = "command"
FILE_ENDPOINT = "file"
LOGIN_ENPOINT = "login"

VERSION = ""
VERSION_COMMIT = {
    "2.4.0": "f6b4892ad3be8e805d49ffd05ee2bc7e7be10dff",
    "2.4.1": "47229e675f792374d4525afe6ea10898decc2e44",
    "2.5.0": "bc49e20553e9e68212652f6c565cb96c068fab9e",
    "2.5.2": "291680f0b003eb89da1267c967728a2d4022a89e",
    "2.6.0": "6fe2f50ab9dc8457c4405094080186208bd2edc4",
    "2.6.2": "47be618a7fa40a8f5c2f6b8914a8eb47d06b7995",
    "3.0.0": "c90ec746a7e77ef5b108554be2133dfd1e1ab1b2",
    "3.0.5": "a9f902e5c552780589a15ba458adb48984359165",
    "3.1.0": "e9d3c5d98e7229118309f6d4bbc9446bad7c4c3d",
    "3.1.1": "375a182bc03b0c78b489e18a0d6af222916a48d2",
    "3.1.2": "3887cbd1d67b58ba6f88c50a069b679e20743984",
}


#   private static final String DEFAULT_USER = "tigergraph";
#   private static final String DEFAULT_PASSWORD = "tigergraph";

#   private static final String ENDPOINT_COMMAND = "command";
#   private static final String ENDPOINT_VERSION = "version";
#   private static final String ENDPOINT_HELP = "help";
#   private static final String ENDPOINT_LOGIN = "login";
#   private static final String ENDPOINT_RESET = "reset";
#   private static final String ENDPOINT_LOCK = "lock";
#   private static final String ENDPOINT_FILE = "file";
#   private static final String ENDPOINT_DIALOG = "dialog";
#   private static final String ENDPOINT_GET_INFO = "getinfo";
#   private static final String ENDPOINT_ABORT_CLIENT_SESSION = "abortclientsession";
#   private static final String ENDPOINT_UDF = "userdefinedfunction";

p = None

GSQL_PATH = "/gsqlserver/gsql/"

url = '{}{}{}'

async def main(cmd="",endpoint="",cookie={},graph="",user="tigergraph",password="tigergraph"):
    global cookies,nbActual,nbTotal,diff
    global p
    async with aiohttp.ClientSession(cookie_jar=cookies) as s:
        cookies = s.cookie_jar.filter_cookies('http://127.0.0.1:14240')
        cookies["clientCommit"] = "3887cbd1d67b58ba6f88c50a069b679e20743984"
        usrPass = "{}:{}".format(user,password)
        b64Val = base64.b64encode(usrPass.encode()).decode()
        headers = {"Authorization": "Basic {}".format(b64Val)}

        data=""
        data ="""
        USE GRAPH MyGraph
        CREATE QUERY sdqsdsdksdfsdddddd4sd5sds54dssd() FOR GRAPH MyGraph {
            PRINT "CAA";
        }
        INSTALL QUERY ALL
        
        """
        while (data != "exit"):
            async with s.post(url.format(host,GSQL_PATH,FILE_ENDPOINT), headers=headers,data=data) as r:
                async for data, _ in r.content.iter_chunks():
                    if GSQL_SEPERATOR not in data.decode():
                        # is it a progressbar ? 
                        result = re.search(REGEX, str(data.decode()))
                        if result != None:
                            # print(result)
                            # print(int(result.group(1)))
                            # print(result.group(1))
                            if p == None:
                                p = ProgressBar(width=80)
                                p.start()

                            console.show_cursor(False)
                            # progress.print(int(result.group(1)))
                            # console.print(p.tick(int(result.group(1))))
                            # print(int(result.group(1)))
                            for i in range(int(result.group(1))):
                                p.tick(int(result.group(1))/100.0)
                                # time.sleep(0.2)
                            # console.file.write("\r")
                            console.show_cursor(True)
                            # console.print()
                            # console.out(data.decode())
                        else:
                            console.print(data.decode().strip())

                    elif GSQL_COOKIES in data.decode():

                        try:
                            cookies = json.loads((data.decode()).split("__,")[1])
                        except:
                            pass

            data = console.input("[blue]GSQL > ")

            
            

def loops():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




def login(user="tigergraph",password="tigergraph"):
    global VERSION
    cookies = {}
    for ver in VERSION_COMMIT:
        cookies["clientCommit"] = VERSION_COMMIT[ver]
        cookies["fromGraphStudio"] = True
        cookies["fromGsqlClient"] = True
        usrPass = "{}:{}".format(user,password)
        b64Val = base64.b64encode(usrPass.encode()).decode()
        headers = {
            "Content-Language": "en-US",
            # "Authorization": "Basic {}".format(b64Val),
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Java/1.8.0",
            "Cookie": json.dumps(cookies)
        }
        # print(headers)
        # print(url.format(host,GSQL_PATH,LOGIN_ENPOINT))
        res = requests.post(url.format(host,GSQL_PATH,LOGIN_ENPOINT),headers=headers,data=b64Val)
        # print(res.text)
        try:
            # print("####### BEGIN #######")
            # print(res.text)
            # print(ver)
            # print("+++++++ END ++++++++++")
            if res.json()["isClientCompatible"] == True:
                VERSION = ver
                print(res.json()["error"])
                print(res.json()["message"])
                print(res.json()["welcomeMessage"])
                break
        except:
            pass

user = "tigergraph"
password = "tigergraph"
login(user,password)
print(VERSION)

if VERSION :
    loops()