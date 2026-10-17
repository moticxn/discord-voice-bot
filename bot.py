import os
import asyncio
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Bot ve Ses Ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# BURAYA Kendi Ses Kanalı ID'ni Yaz (Sadece sayı olacak, tırnak içinde değil)
VOICE_CHANNEL_ID = 1560835148520357998  

@bot.event
async def on_ready():
    print(f"[+] {bot.user} olarak Discord'a başarıyla giriş yapıldı!")
    
    # Bağlantının ve önbelleğin oturması için 3 saniye bekliyoruz
    await asyncio.sleep(3)
    
    try:
        channel_id = int(VOICE_CHANNEL_ID)
        
        # Önce cache'e bakar, bulamazsa doğrudan API'den (fetch) çeker (Hata almayı %100 engeller)
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
            
        if channel and isinstance(channel, discord.VoiceChannel):
            # Bot zaten seste mi kontrol et
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print(f"[+] {channel.name} ses kanalına başarıyla bağlandı!")
            else:
                print("[!] Bot zaten bir ses kanalında.")
        else:
            print("[-] HATA: Yazdığın ID bir ses kanalı değil veya bot bu kanalı görmüyor!")
            
    except Exception as e:
        print(f"[-] Ses kanalına bağlanırken hata oluştu: {e}")

# 3. Sistemi Başlatma
if __name__ == "__main__":
    keep_alive()
    
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if not TOKEN:
        print("[-] HATA: DISCORD_TOKEN bulunamadı! Render panelinden Environment Variables kısmını kontrol et.")
    else:
        bot.run(TOKEN)
