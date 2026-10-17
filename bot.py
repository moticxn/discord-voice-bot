import discord
from discord.ext import commands
import os

# Bot izinleri (Intents) ayarları
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

# Bot hazır olduğunda çalışacak kısım
@client.event
async def on_ready():
    print(f"[+] {client.user} olarak giriş yapıldı!")
    
    # Bağlanılacak ses kanalının ID'si
    # (Kendi ses kanalı ID'niz ile değiştirin)
    CHANNEL_ID = 1560815998536515607  
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f"[+] Başarılı! '{channel.name}' ses kanalına giriş yapıldı.")
        except Exception as e:
            print(f"[-] Ses kanalına bağlanırken hata oluştu: {e}")
    else:
        print("[-] Kanal bulunamadı! Lütfen CHANNEL_ID değerini kontrol edin.")

# Tokeni Render üzerindeki "DISCORD_TOKEN" ortam değişkeninden güvenli şekilde çeker
TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN:
    client.run(TOKEN)
else:
    print("[-] HATA: 'DISCORD_TOKEN' ortam değişkeni bulunamadı! Render paneline eklediğinizden emin olun.")
