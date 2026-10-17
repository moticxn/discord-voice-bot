import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask Sunucusu
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
    print(f"[+] Bot giriş yaptı: {bot.user}")
    
    # Ses kütüphanesinin yüklü olup olmadığını kontrol et
    if not discord.opus.is_loaded():
        try:
            discord.opus.load_opus()
            print("[+] Opus kütüphanesi başarıyla yüklendi.")
        except Exception as e:
            print(f"[-] Opus yüklenirken hata: {e}")

    # Sese bağlanma görevi
    await asyncio.sleep(3)
    try:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if not channel:
            channel = await bot.fetch_channel(VOICE_CHANNEL_ID)
            
        if channel and isinstance(channel, discord.VoiceChannel):
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print(f"[+] BAŞARILI: {channel.name} kanalına bağlanıldı!")
            else:
                print("[!] Bot zaten seste.")
        else:
            print("[-] HATA: Kanal bulunamadı veya ses kanalı değil!")
    except Exception as e:
        print(f"[-] Sese bağlanma hatası: {e}")

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: Token bulunamadı!")
