import discord
from discord.ext import commands
import sys, traceback
import config as cfg
from commons import mongoIO

def get_config():
    if cfg.DEBUG==True:
        return cfg.debugConf
    else:
        return cfg.conf

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = get_config().PREFIXES
    if mongoIO.isBlacklisted(message.author):
        return ' '
    if not message.guild:
        return ' '
    guildPref = None
    if message.guild:
        guildPref = mongoIO.getSetting(message.guild.id, 'prefix')
    if guildPref is not None:
        prefixes.append(guildPref)
    return commands.when_mentioned_or(*prefixes)(bot, message)

load_extensions = ['cogs.owner', 'cogs.admin',  'cogs.images', 'cogs.errorhandler', 'cogs.fun', 'cogs.settings', 'cogs.information', 'cogs.osu', 'cogs.help', 'cogs.music'] 
bot = commands.AutoShardedBot(command_prefix=get_prefix, description='Sunny Bot', activity=discord.Streaming(name='#shameless_self_promotion', type=1, url='https://www.twitch.tv/niceaesthetic'))
bot.remove_command('help')

print(r"""                                                      
  .--.--.                                                  
 /  /    '.                                                
|  :  /`. /          ,--,      ,---,      ,---,            
;  |  |--`         ,'_ /|  ,-+-. /  | ,-+-. /  |           
|  :  ;_      .--. |  | : ,--.'|'   |,--.'|'   |     .--,  
 \  \    `. ,'_ /| :  . ||   |  ,"' |   |  ,"' |   /_ ./|  
  `----.   \|  ' | |  . .|   | /  | |   | /  | |, ' , ' :  
  __ \  \  ||  | ' |  | ||   | |  | |   | |  | /___/ \: |  
 /  /`--'  /:  | : ;  ; ||   | |  |/|   | |  |/ .  \  ' |  
'--'.     / '  :  `--'   \   | |--' |   | |--'   \  ;   :  
  `--'---'  :  ,      .-./   |/     |   |/        \  \  ;  
             `--`----'   '---'      '---'          :  \  \ 
                                                    \  ' ; 
                                                     `--`  
""")

if __name__ == '__main__':
    for extension in load_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')

@bot.event
async def on_guild_join(guild):
    mongoIO.addServer(guild)

bot.run(get_config().TOKEN, bot=True, reconnect=True)
