import os
import asyncio
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import urllib.request
import time

# Flask (UptimeRobot ve Self-Ping için Keep-Alive)
app = Flask('')

@app.route('/')
def home():
    return "Bot Aktif ve Çalışıyor!", 200

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Kendi kendini pingleme (Self-Ping) mekanizması
def self_ping():
    # Render kendi URL'ini otomatik olarak bu çevresel değişkene atar
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if not url:
        url = "https://discord-voice-bot-1-olga.onrender.com" # Garanti/Yedek URL
    
    while True:
        try:
            time.sleep(240) # Her 4 dakikada bir kendi adresine istek atar
            urllib.request.urlopen(url)
            print("[+] Self-ping atıldı, sunucu canlı tutuluyor.", flush=True)
        except Exception as e:
            print(f"[-] Self-ping hatası: {e}", flush=True)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    # Self-ping thread'ini arka planda başlatıyoruz
    p = Thread(target=self_ping)
    p.daemon = True
    p.start()

# Discord Bot Tanımı
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
VOICE_CHANNEL_ID = 1560835148520357998  # Kendi Ses Kanalı ID'n
# ==========================================

async def force_connect():
    await bot.wait_until_ready()
    await asyncio.sleep(3) # Discord bağlantısının tam oturması için kısa bekleme
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
        if channel and isinstance(channel, discord.VoiceChannel):
            voice_client = channel.guild.voice_client
            
            if voice_client and voice_client.is_connected():
                if voice_client.channel.id != channel.id:
                    await voice_client.move_to(channel)
                return

            if voice_client:
                try:
                    await voice_client.disconnect(force=True)
                except Exception:
                    pass
                await asyncio.sleep(2)

            await channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
            print(f"[+] Başarıyla sese bağlandı: {channel.name}", flush=True)
    except Exception as e:
        print(f"[-] Ses bağlantı hatası: {e}", flush=True)

@bot.event
async def on_ready():
    print(f"[+] Bot giriş yaptı: {bot.user}", flush=True)
    bot.loop.create_task(force_connect())
    if not maintain_voice.is_running():
        maintain_voice.start()

@tasks.loop(seconds=15)
async def maintain_voice():
    if not bot.is_closed():
        try:
            channel_id = int(VOICE_CHANNEL_ID)
            channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
            if channel and channel.guild:
                voice_client = channel.guild.voice_client
                if not voice_client or not voice_client.is_connected():
                    print("[!] Ses kopuk, tekrar bağlanılıyor...", flush=True)
                    await force_connect()
        except Exception as e:
            print(f"[-] Döngü hatası: {e}", flush=True)

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: DISCORD_TOKEN bulunamadı!", flush=True)
