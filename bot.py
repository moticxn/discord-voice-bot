import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask Web Sunucusu (Render timeout koruması)
app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktif ve Çalışıyor!"

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

# ==========================================
# Kendi Ses Kanalı ID'nizi Buraya Yazın (Sadece Sayı)
VOICE_CHANNEL_ID = 1560835148520357998  
# ==========================================

@bot.event
async def on_ready():
    print(f"[+] Bot başarıyla giriş yaptı: {bot.user}", flush=True)

    await asyncio.sleep(3)
    
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if channel and isinstance(channel, discord.VoiceChannel):
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                # Discord.py'nin kendi yerleşik ses koruması aktif
                await channel.connect(reconnect=True, timeout=60.0)
                print(f"[+] BAŞARILI: {channel.name} ses kanalına bağlandı ve sabit kaldi!", flush=True)
            else:
                print("[!] Bot zaten bir ses kanalında.", flush=True)
        else:
            print("[-] HATA: Belirtilen ID bir ses kanalı değil veya bot göremiyor!", flush=True)
    except Exception as e:
        print(f"[-] Sese bağlanma hatası: {e}", flush=True)

if __name__ == "__main__":
    keep_alive()
    
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: Render Environment kısmında DISCORD_TOKEN bulunamadı!", flush=True)
