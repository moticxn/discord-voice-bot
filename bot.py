import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. Flask Web Sunucusu (Render port gereksinimi ve UptimeRobot için)
app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktif ve Çalışıyor!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Bot Ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Botun otomatik gireceği ses kanalının ID'sini buraya yaz
VOICE_CHANNEL_ID = 1560815998536515607  # Burayı kendi ses kanalının ID'si ile değiştir

@bot.event
async def on_ready():
    print(f"[+] {bot.user} olarak Discord'a başarıyla giriş yapıldı!")
    
    # Bot açılır açılmaz ses kanalına otomatik bağlanır
    try:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()
            print(f"[+] {channel.name} ses kanalına başarıyla bağlandı!")
        else:
            print("[-] HATA: Belirtilen ses kanalı bulunamadı, ID'yi kontrol et.")
    except Exception as e:
        print(f"[-] Ses kanalına bağlanırken hata oluştu: {e}")

# 3. Sistemi Başlatma
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if not TOKEN:
        print("HATA: DISCORD_TOKEN bulunamadı!")
    else:
        bot.run(TOKEN)
