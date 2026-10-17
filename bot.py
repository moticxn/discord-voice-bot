import os
import asyncio
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# 1. Flask Web Sunucusu (Render keep-alive)
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
    print(f"[+] Bot başarıyla giriş yaptı: {bot.user}", flush=True)
    await asyncio.sleep(3)
    await connect_to_voice()
    # Bağlantı koruma döngüsünü başlat
    if not maintain_voice.is_running():
        maintain_voice.start()

async def connect_to_voice():
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if channel and isinstance(channel, discord.VoiceChannel):
            voice_client = channel.guild.voice_client
            if voice_client and voice_client.is_connected():
                if voice_client.channel.id != channel.id:
                    await voice_client.move_to(channel)
            else:
                if voice_client:
                    await voice_client.disconnect(force=True)
                    await asyncio.sleep(2)
                # Özel parametrelerle ses bağlantısını sabitleme
                await channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
                print(f"[+] BAŞARILI: {channel.name} ses kanalına stabil olarak bağlandı!", flush=True)
    except Exception as e:
        print(f"[-] Sese bağlanma hatası: {e}", flush=True)

# 3. Sürekli Kontrol Mekanizması (Bot sesten düşerse anında ve hatasız toplar)
@tasks.loop(seconds=15)
async def maintain_voice():
    if not bot.is_closed():
        try:
            channel_id = int(VOICE_CHANNEL_ID)
            channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
            if channel and channel.guild:
                voice_client = channel.guild.voice_client
                if not voice_client or not voice_client.is_connected():
                    print("[!] Bağlantı koptuğu tespit edildi, stabil şekilde yeniden bağlanılıyor...", flush=True)
                    await connect_to_voice()
        except Exception as e:
            print(f"[-] Döngü koruma hatası: {e}", flush=True)

@maintain_voice.before_loop
async def before_maintain_voice():
    await bot.wait_until_ready()

if __name__ == "__main__":
    keep_alive()
    
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: Render Environment kısmında DISCORD_TOKEN bulunamadı!", flush=True)
