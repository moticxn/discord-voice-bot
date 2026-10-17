import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask Web Sunucusu
app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktif!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# Discord Bot Ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# BURAYA Kendi Ses Kanalı ID'ni Yaz (Tırnak olmadan, sadece sayı)
VOICE_CHANNEL_ID = 1560815998536515607  

@bot.event
async def on_ready():
    print(f"[+] Bot giriş yaptı: {bot.user}", flush=True)
    
    # Opus kütüphanesini kontrol et
    if not discord.opus.is_loaded():
        try:
            discord.opus.load_opus()
            print("[+] Opus kütüphanesi başarıyla yüklendi.", flush=True)
        except Exception as e:
            print(f"[-] Opus yüklenirken hata: {e}", flush=True)

    # Sese bağlanma süreci
    await asyncio.sleep(3)
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if channel and isinstance(channel, discord.VoiceChannel):
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print(f"[+] BAŞARILI: {channel.name} ses kanalına bağlanıldı!", flush=True)
            else:
                print("[!] Bot zaten bir ses kanalında.", flush=True)
        else:
            print("[-] HATA: Belirtilen ID bir ses kanalı değil veya bot göremiyor!", flush=True)
    except Exception as e:
        print(f"[-] Sese bağlanma hatası: {e}", flush=True)

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: DISCORD_TOKEN bulunamadı!", flush=True)
