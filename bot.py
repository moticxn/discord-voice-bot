import discord
from discord.ext import commands

TOKEN = "MTU2MDgxNjE2MDE4NDcyOTYzMA.GkzI-E.mWCpPr3_j-xXZaNKaTsRSiT-CgqqGBoNdjUj9w"
CHANNEL_ID = 1560815998536515607 

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"[+] Bot başarıyla giriş yaptı: {bot.user.name}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect(self_deaf=True)
            print(f"[+] Başarılı! {channel.name} ses kanalına giriş yapıldı ve nöbet başladı.")
        except Exception as e:
            print(f"[!] Sese bağlanırken hata oluştu: {e}")
    else:
        print("[!] HATA: Belirtilen kanal ID'si bulunamadı veya bir ses kanalı değil!")

bot.run(TOKEN)