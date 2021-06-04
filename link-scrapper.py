#!/bin/python3
from bs4 import BeautifulSoup
import sys
import time
from urllib.parse import unquote, quote, urlencode
import urllib.request

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# How long to sleep on each failed connection attempt
# Will increase by this amount after each successive failure
# if delay = 60, first: 60, second: 120, third: 180, etc
delay = 60

def tryURL(url):
    """ Try to connect until successful, keep waiting a bit longer and trying again """
    connected = False

    fullDelay = delay
    while not connected:
        try:
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
            connected = True
        except:
            print("Failed to connect to " + url + "\nTrying again in: " + str(fullDelay) + " seconds.")
            time.sleep(fullDelay)
            fullDelay += delay

    return response

def getLinks(url):
    links = []
    response = tryURL(url)
    soup = BeautifulSoup(response, "html5lib")
    links = []

    for a in soup.findAll('a'):
        a = a.get("href")

        print(a, url)

        if url[-1] != "/" and a[0] != "/":
            url = url + "/"

        if url[-1] == "/" and a[0] == "/":
            url = url[:-1]

        if a[:4] != "http":
            links.append(url + a)
        else:
            links.append(a)

    return links

if __name__ == "__main__":
    if (len(sys.argv)) != 2:
        print("Usage: link-scrapper.py URL")
        exit()

    url = sys.argv[1]
    links = getLinks(url)

    for link in links:
        print(link)

