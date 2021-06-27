# import pyTigerGraph as tg 
# import argparse
# from rich.console import Console
# console = Console()

# conn = tg.TigerGraphConnection(host="http://127.0.0.1")
# while(True):
#     cmd = ""
#     console.print(conn.gsql(cmd))

# import asyncio
# import urllib.parse
# import sys

from rich.console import Console

import base64
import asyncio
import aiohttp


console = Console()
url = 'http://127.0.0.1:14240/gsqlserver/gsql/command'


async def main(cmd="",endpoint="",cookie={},graph=""):
    # Filtering for the cookie, saving it into a varibale
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as s:
        cookies = s.cookie_jar.filter_cookies('http://127.0.0.1:14240')
        cookies["clientCommit"] = "3887cbd1d67b58ba6f88c50a069b679e20743984"
        # for key, cookie in cookies.items():
        #     if key == 'test':
        #         cookie_value = cookie.value4
        # StreamReader

    # Using the cookie value to do anything you want:
    # e.g. sending a weird request containing the cookie in the header instead.
        usrPass = "tigergraph:tigergraph"
        b64Val = base64.b64encode(usrPass.encode()).decode()
        headers = {"Authorization": "Basic {}".format(b64Val)}
        async with s.post(url, headers=headers,data="INSTALL QUERY ALL") as r:
            
            try:
                print(await r.json())
            except:
                print(await r.text())
            # console.print(res["welcomeMessage"])
            # if res["error"] == True:
            #     console.print(res["message"])

            # console.input(res["shellPrompt"])
            
            


loop = asyncio.get_event_loop()
loop.run_until_complete(main())


# clientCommit 3887cbd1d67b58ba6f88c50a069b679e20743984
# cookieJSON.put("clientCommit", commitClient);
# cookieJSON.put("graph", graphName);
#  cookieJSON.put("fromGsqlClient", true); // used in handler

# standard Python
# async def tcp_echo_client(url):
#     url = urllib.parse.urlsplit(url)
#     # if url.scheme == 'https':
#     #     reader, writer = await asyncio.open_connection(
#     #         url.hostname, 14240, ssl=True)
#     # else:
#     #     reader, writer = await asyncio.open_connection(
#     #         url.hostname, 14240)
#     reader, writer = await asyncio.open_connection('127.0.0.1', 14240)


#     query = (
#         f"HEAD {url.path or '/'} HTTP/1.0\r\n"
#         f"Host: {url.hostname}\r\n"
#         f"\r\n"
#     )
#     writer.write(query.encode())
#     while True:
#         line = await reader.readline()
#         if not line:
#             break

#         line = line.decode().rstrip()
#         if line:
#             print(f'HTTP header> {line}')

#     print(f'Send: ls')
#     writer.write("ls".encode())
#     await writer.drain()
#     data = await reader.read(100)
#     print(f'Received: {data.decode()!r}')



# asyncio.run(tcp_echo_client('http://127.0.0.1:14240/gsqlserver/gsql/login'))