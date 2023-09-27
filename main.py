import os
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import asyncio

#  Variables de entorno
secret = os.environ['token']
channel_id = os.environ['channel']

intents = discord.Intents.default()

client = commands.Bot(command_prefix='$', intents=intents)
app = Flask(__name__)

#  Ruta de inicio
@app.route('/')
def index():
  return "Servidor funcionando"

# Ruta que recibe  el post del webhook
@app.route('/github-webhook', methods=['POST'])
def githubWebhookHandler():
  data = request.get_json()
  if data.get("repository", {}).get("name") == "bot-discord-with-github" or data.get("repository", {}).get("name") == "DIDACTI-K":
    print("Se ejecutó con el filtro de repositorio")
    if 'X-GitHub-Event' in request.headers:
      event_type = request.headers['X-GitHub-Event']

      if event_type == 'push':
        channel = client.get_channel(int(channel_id))
        if channel:
          pusher_name = data.get("pusher", {}).get("name")
          repository_name = data.get("repository", {}).get("name")

          commits = data.get("commits", [])

          message = f"*-- @everyone --*\nSe ha realizado un push en repositorio **{repository_name}** por **{pusher_name}**.\n\n{'Commits:' if len(commits) > 1 else 'commit:'}\n"

          for commit in commits:
            commit_message = commit.get("message")
            message += f"-> {commit_message}\n"

          print(f'Se ha realizado un push en GitHub.')
          client.loop.create_task(channel.send(message))
  else:
    print("Se ejecutó sin el filtro de repositorio")
    if 'X-GitHub-Event' in request.headers:
      event_type = request.headers['X-GitHub-Event']

      if event_type == 'push':
        channel = client.get_channel(int(channel_id))
        if channel:
          pusher_name = data.get("pusher", {}).get("name")
          repository_name = data.get("repository", {}).get("name")

          commits = data.get("commits", [])

          message = f"*-- @everyone --*\nSe ha realizado un push en repositorio **{repository_name}** por **{pusher_name}**.\n\n{'Commits:' if len(commits) > 1 else 'commit:'}\n"

          for commit in commits:
            commit_message = commit.get("message")
            message += f"-> {commit_message}\n"

          print(f'Se ha realizado un push en GitHub.')
          client.loop.create_task(channel.send(message))
  return jsonify({'message': 'OK'})

@client.event
async def on_ready():
  print(f'Bot connectado como {client.user.name}')

# Método de ejecución del bot de discord
async def start_bot():
  await client.start(secret)

# Método de ejecución de servidor flask
def start_server():
  app.run(host='0.0.0.0', port=5000)

loop = asyncio.get_event_loop()
bot_task = loop.create_task(start_bot())
server_task = loop.run_in_executor(None, start_server)

# Ejecutar ambas tareas en paralelo
loop.run_until_complete(asyncio.gather(bot_task, server_task))