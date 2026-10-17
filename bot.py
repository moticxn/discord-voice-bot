import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. Web Sunucusu (Render'ın kapanmasını önler)
app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktif ve Calisiyor!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 2. Discord Bot Ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# Kendi Ses Kanalı ID'nizi Buraya Yazın (Sadece Sayı)
VOICE_CHANNEL_ID = 1560835148520357998 
# ==========================================

@bot.event
async def on_ready():
    print(f"[+] Bot basariyla giris yapti: {bot.user}", flush=True)

    # Bot oturumunun tam baglanmasini bekleyelim
    await asyncio.sleep(3)
    
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if channel and isinstance(channel, discord.VoiceChannel):
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect(reconnect=True)
                print(f"[+] BASARILI: {channel.name} ses kanalina baglandi ve sabit kaldi!", flush=True)
            else:
                print("[!] Bot zaten bir ses kanalinda.", flush=True)
        else:
            print("[-] HATA: Belirtilen ID bir ses kanali degil veya bot kanali gormuyor!", flush=True)
    except Exception as e:
        print(f"[-] Sese baglanma hatasi: {e}", flush=True)

if __name__ == "__main__":
    keep_alive()
    
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: Render Environment kisminda DISCORD_TOKEN bulunamadi!", flush=True)
