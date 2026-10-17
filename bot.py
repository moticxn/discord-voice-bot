import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Render port uyarısını çözmek ve botu uyanık tutmak için Flask web sunucusu
app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktif!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Web sunucusunu başlat
keep_alive()

# Discord Bot ayarları
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"[+] {client.user} olarak giriş yapıldı!")
    
    # Kendi ses kanalı ID'niz
    CHANNEL_ID = 1560815998536515607  
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f"[+] Başarılı! '{channel.name}' ses kanalına giriş yapıldı.")
        except Exception as e:
            print(f"[-] Hata: {e}")
    else:
        print("[-] Kanal bulunamadı!")

TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN:
    client.run(TOKEN)
else:
    print("[-] HATA: 'DISCORD_TOKEN' ortam değişkeni bulunamadı!")
