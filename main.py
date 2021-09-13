import os
import discord
import requests
import json
import random
from replit import db


b20token = os.environ['b20TOKEN']
client = discord.Client()

sad_words = ["sad", "depressed", "grumpy"]

starter_encouragements = [
  "cheer up",
  "carry on",
  "get over it"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

def update_encouragements(new_enc):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(new_enc)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [new_enc]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starter_encouragements
  if "encouragements" is db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)


client.run(b20token)

