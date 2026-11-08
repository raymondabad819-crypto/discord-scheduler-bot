import os
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

# Set up Discord bot intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Initialize the scheduler pinned strictly to AEDT (Sydney timezone)
scheduler = AsyncIOScheduler(timezone=ZoneInfo("Australia/Sydney"))

@client.event
async def on_ready():
    print(f"Logged in successfully as {client.user} (ID: {client.user.id})")
    
    # Configure your new custom recurring schedule using cron triggers (AEDT timezone)
    scheduler.add_job(send_scheduled_ping, 'cron', hour=14, minute=30, id='ping_230pm')
    scheduler.add_job(send_scheduled_ping, 'cron', hour=18, minute=0,  id='ping_600pm')
    scheduler.add_job(send_scheduled_ping, 'cron', hour=20, minute=30, id='ping_830pm')
    scheduler.add_job(send_scheduled_ping, 'cron', hour=22, minute=0,  id='ping_1000pm')
    scheduler.add_job(send_scheduled_ping, 'cron', hour=0,  minute=30, id='ping_1230am')
    
    # Start the background task loop
    scheduler.start()
    print("Scheduler active: Running with your updated AEDT schedule.")

async def send_scheduled_ping():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        role_mention = f"<@&{ROLE_ID}>"
        message_content = f"{role_mention} Crate dropped!"
        
        # allowed_mentions forces Discord to execute the role notification alert
        await channel.send(
            message_content, 
            allowed_mentions=discord.AllowedMentions(roles=True)
        )
        print(f"Successfully dispatched scheduled notification to channel {CHANNEL_ID}.")
    else:
        print(f"Error: Could not resolve channel ID {CHANNEL_ID}. Ensure the bot has access.")

# Execute the client loop
if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN is missing from environment variables.")
    else:
        client.run(TOKEN)
