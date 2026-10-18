cat << 'EOF' > discord_bot.py
import discord
import random
import string
import requests
import asyncio

TOKEN = "MTU2MTA4NDY1MjAzMzE0NjkzMA.GJ_UUg.FMps3QGVkXnxOVqJ91WMOgbd_8YJABtssN0CgY"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# قاموس لتتبع حالة التشغيل التلقائي لكل سيرفر/روم
loop_status = {}

def check_tiktok_username(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 404:
            return True
    except Exception:
        pass
    return False

@client.event
async def on_ready():
    print(f'✅ البوت يعمل بوضع فحص 1000 يوزر لكل دورة: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    letters = string.ascii_lowercase
    digits = string.digits
    channel_id = message.channel.id

    # أمر إيقاف الفحص المستمر
    if message.content.startswith('!stop'):
        if channel_id in loop_status:
            loop_status[channel_id] = False
            await message.channel.send("🛑 تم إيقاف الفحص المستمر بنجاح يا عم مصطفى.")
        else:
            await message.channel.send("⚠️ لا يوجد فحص شغال حالياً في هذا الروم.")
        return

    # أمر فحص ثلاثي (1000 يوزر لكل دورة)
    if message.content.startswith('!check3'):
        await message.channel.send("هلا عمي مصطفى انا حاليا قاعد يفحص تكفى استنى شوي ⏳ (جاري فحص 1000 يوزر في كل دورة)")
        loop_status[channel_id] = True
        
        while loop_status.get(channel_id, False):
            found_users = []
            checked_count = 0
            
            # فحص 1000 يوزر في الدورة الواحدة
            while checked_count < 1000 and loop_status.get(channel_id, False):
                u = "".join(random.choices(letters + digits, k=3))
                checked_count += 1
                if check_tiktok_username(u):
                    found_users.append(f"`{u}`")
                    # إذا جاب دفعة حلوة يرسلها ويكمل
                    if len(found_users) >= 5:
                        break
                        
            if found_users and loop_status.get(channel_id, False):
                await message.channel.send(f"🎯 **تم فحص {checked_count} يوزر ثلاثي والعثور على المتاح:**\n" + " ".join(found_users))
            elif loop_status.get(channel_id, False):
                await message.channel.send(f"🔄 انتهت دورة فحص 1000 يوزر ثلاثي، جاري بدء الدورة التالية...")
            
            await asyncio.sleep(2)

    # أمر فحص رباعي (1000 يوزر لكل دورة)
    elif message.content.startswith('!check4'):
        await message.channel.send("هلا عمي مصطفى انا حاليا قاعد يفحص تكفى استنى شوي ⏳ (جاري فحص 1000 يوزر في كل دورة)")
        loop_status[channel_id] = True
        
        while loop_status.get(channel_id, False):
            found_users = []
            checked_count = 0
            
            # فحص 1000 يوزر في الدورة الواحدة
            while checked_count < 1000 and loop_status.get(channel_id, False):
                u = "".join(random.choices(letters + digits, k=4))
                checked_count += 1
                if check_tiktok_username(u):
                    found_users.append(f"`{u}`")
                    if len(found_users) >= 5:
                        break
                        
            if found_users and loop_status.get(channel_id, False):
                await message.channel.send(f"🎯 **تم فحص {checked_count} يوزر رباعي والعثور على المتاح:**\n" + " ".join(found_users))
            elif loop_status.get(channel_id, False):
                await message.channel.send(f"🔄 انتهت دورة فحص 1000 يوزر رباعي، جاري بدء الدورة التالية...")
            
            await asyncio.sleep(2)

client.run(TOKEN)
EOF
