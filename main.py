import discord
import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


client = discord.Client()

def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  jsonData = json.loads(response.text)
  quote = "\"" + jsonData[0]["q"] + "\" -" + jsonData[0]["a"]
  return quote

def lookupWikipedia(keyword, checkword):

    try:
      with urlopen("https://en.wikipedia.org/wiki/" + keyword) as site:
        soup = BeautifulSoup(site, "html.parser")
        paragraphs = soup.find_all("p")
        for p in paragraphs:
          text = p.get_text()
          if checkword in text:
            return re.sub(r'\[.*?\]', "", text)
      return "Couldn't find something."
    except:
      return "Something went wrong; check your spelling or try again later."

@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("$inspire"):
    quote = getQuote()
    await message.channel.send(quote)
  
  #operations functions
  if message.content.startswith("$add"):
    text = message.content
    numbers = text.split(" ")
    added = int(numbers[1]) + int(numbers[2])
    await message.channel.send(numbers[1] + " plus " + numbers[2] + " is " + str(added))
  if message.content.startswith("$multiply"):
      text = message.content
      numbers = text.split(" ")
      multiplied = int(numbers[1]) * int(numbers[2])
      await message.channel.send(numbers[1] + " times " + numbers[2] + " is " + str(multiplied))
  if message.content.startswith("$divide"):
    text = message.content
    numbers = text.split(" ")
    if numbers[2] == "0":
      message.channel.send("I can't divide by zero")
    else:
      divided = int(numbers[1]) / int(numbers[2])
      await message.channel.send(numbers[1] + " divided by " + numbers[2] + " is " + str(divided))
  if message.content.startswith("$subtract"):
    text = message.content
    numbers = text.split(" ")
    subtracted = int(numbers[1]) - int(numbers[2])
    await message.channel.send(numbers[1] + " subtracted by " + numbers[2] + " is " + str(subtracted))
  
  if message.content.startswith("$define"):
      words = message.content.split(" ")
      words.pop(0)
      await message.channel.send(lookupWikipedia("_".join(words), "e"))



client.run(os.getenv('TOKEN'))