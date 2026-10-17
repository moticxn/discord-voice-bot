import os
import asyncio
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# Flask Sunucusu (Render UptimeRobot için)
app = Flask('')

@app.route('/')
def home():
    return "Bot Aktif!", 200

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
# Ses Kanalı ID'nizi Buraya Yazın
VOICE_CHANNEL_ID = 1560835148520357998  
# ==========================================

@bot.event
async def on_ready():
    print(f"[+] Bot giriş yaptı: {bot.user}", flush=True)
    await asyncio.sleep(3)
    await connect_to_voice()
    if not maintain_voice.is_running():
        maintain_voice.start()

async def connect_to_voice():
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
        if channel and isinstance(channel, discord.VoiceChannel):
            voice_client = channel.guild.voice_client
            if voice_client and voice_client.is_connected():
                if voice_client.channel.id != channel.id:
                    await voice_client.move_to(channel)
            else:
                if voice_client:
                    await voice_client.disconnect(force=True)
                    await asyncio.sleep(2)
                await channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
                print(f"[+] Başarıyla sese bağlandı: {channel.name}", flush=True)
    except Exception as e:
        print(f"[-] Ses bağlantı hatası: {e}", flush=True)

@tasks.loop(seconds=15)
async def maintain_voice():
    if not bot.is_closed():
        try:
            channel_id = int(VOICE_CHANNEL_ID)
            channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
            if channel and channel.guild:
                voice_client = channel.guild.voice_client
                if not voice_client or not voice_client.is_connected():
                    print("[!] Ses bağlantısı koptu, yeniden bağlanılıyor...", flush=True)
                    await connect_to_voice()
        except Exception as e:
            print(f"[-] Döngü hatası: {e}", flush=True)

@maintain_voice.before_loop
async def before_maintain_voice():
    await bot.wait_until_ready()

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("[-] HATA: DISCORD_TOKEN bulunamadı!", flush=True)
