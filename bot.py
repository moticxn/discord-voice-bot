import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. Flask Web Sunucusu (Render'ın port isteğini karşılar ve 7/24 ayakta tutar)
app = Flask('')

@app.route('/')
def home():
    return "Discord Ses Botu 7/24 Aktif ve Çalışıyor!"

def run():
    # Render'ın atadığı portu otomatik alır, yoksa varsayılan 10000 kullanır
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Bot ve Ses Ayarları (Gerekli Intent'ler açık)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# BURAYA DİKKAT: Aşağıdaki tırnak içindeki sayıları silip, Discord'daki ses kanalının ID'sini yapıştır!
VOICE_CHANNEL_ID = 1560815998536515607  # Örn: 118239481029384123

@bot.event
async def on_ready():
    print(f"[+] {bot.user} olarak Discord'a başarıyla giriş yapıldı!")
    
    # Bot açıldığı gibi ses kanalına otomatik bağlanır
    try:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel:
            # Eğer bot zaten sesteyse tekrar bağlanmaya çalışmaz
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print(f"[+] {channel.name} ses kanalına başarıyla bağlandı!")
            else:
                print("[!] Bot zaten bir ses kanalında.")
        else:
            print("[-] HATA: Belirtilen ses kanalı bulunamadı! Kanal ID'sini kontrol et.")
    except Exception as e:
        print(f"[-] Ses kanalına bağlanırken hata oluştu: {e}")

# 3. Sistemi Başlatma
if __name__ == "__main__":
    # Önce Flask sunucusunu arka planda başlat
    keep_alive()
    
    # Discord Token'ını Render Environment Variables'tan güvenli şekilde çek
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if not TOKEN:
        print("[-] HATA: DISCORD_TOKEN bulunamadı! Render panelinden Environment Variables kısmını kontrol et.")
    else:
        bot.run(TOKEN)
