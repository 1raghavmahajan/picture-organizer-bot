# bot.py
import os
import discord
import pickle

DEFAULT_PICTURES_CHANNEL_NAME = 'pictures'

TOKEN = os.environ['TOKEN']


extensions = ["ase",	"art",	"bmp",	"blp",	"cd5",	"cit",	"cpt",	"cr2",	"cut",	"dds",	"dib",	"djvu",	"egt",	"exif",	"gif",	"gpl",	"grf",	"icns",	"ico",	"iff",	"jng",	"jpeg",	"jpg",	"jfif",	"jp2",	"jps",	"lbm",	"max",	"miff",	"mng",	"msp",	"nitf",	"ota",	"pbm",	"pc1",	"pc2",	"pc3",	"pcf",	"pcx",	"pdn",	"pgm",	"PI1",	"PI2",	"PI3",	"pict",	"pct",	"pnm",	"pns",	"ppm",	"psb",	"psd",	"pdd",	"psp",	"px",	"pxm",	"pxr",	"qfx",	"raw",	"rle",	"sct",	"sgi",	"rgb",	"int",	"bw",	"tga",	"tiff",	"tif",	"vtf",	"xbm",	"xcf",	"xpm",	"3dv",	"amf",	"ai",	"awg",	"cgm",	"cdr",	"cmx",	"dxf",	"e2d",	"egt",	"eps",	"fs",	"gbr",	"odg",	"svg",	"stl",	"vrml",	"x3d",	"sxd",	"v2d",	"vnd",	"wmf",	"emf",	"art",	"xar",	"png",	"webp",	"jxr",	"hdp",	"wdp",	"cur",	"ecw",	"iff",	"lbm",	"liff",	"nrrd",	"pam",	"pcx",	"pgf",	"sgi",	"rgb",	"rgba",	"bw",	"int",	"inta",	"sid",	"ras",	"sun",	"tga"]


class ServerData:
    def __init__(self,server_id=0, channel_id=0, links_channel=0, mon = []):
        self.server_id = server_id
        self.channel_id = channel_id
        self.links_channel = links_channel
        self.monitor_ch = mon
    
    def __str__(self):
        return f'server_id: {self.server_id}, channel_id: {self.channel_id}, monitored_channels:{self.monitor_ch}'
    
    def print(self, guild):
        return f'Server_Name: {guild.name}, Picture_Channel_Name: {guild.get_channel(self.channel_id)}, Monitored_Channels: {[guild.get_channel(n) for n in self.monitor_ch]} '


storage = {}
try:
    storage = pickle.load(open('serverdata', 'rb'))
except:
    pass


client = discord.Client()


async def initialSetup(message):
    g = message.guild
    ms = message.content.split()

    if len(ms) != 2:
        await message.channel.send(content='Invalid Parameters')
        return
    if g.id in storage:
        await message.channel.send(content='Already Initialised')
        return
    
    await message.channel.send(content='Initialising...')

    storage[g.id] = ServerData(g.id)

    author_role = message.author.roles[len(message.author.roles)-1]
    
    if ms[1] == '-c':
        overwrites = {
            g.default_role: discord.PermissionOverwrite(create_instant_invite = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, add_reactions = False, read_messages = False, send_messages = False, send_tts_messages = False, manage_messages = False, embed_links = False, attach_files = False, read_message_history = False, mention_everyone = False, external_emojis = False),
            g.me: discord.PermissionOverwrite(create_instant_invite = True, manage_channels = True, manage_permissions = True, add_reactions = True, read_messages = True, send_messages = True, manage_messages = True, embed_links = True, read_message_history = True)
        }
        pw_channel = await g.create_text_channel(DEFAULT_PICTURES_CHANNEL_NAME, position=0, overwrites=overwrites)
        storage[g.id] = ServerData(g.id, pw_channel.id)
        await message.delete()
        await message.channel.send(content=f'Created channel {DEFAULT_PICTURES_CHANNEL_NAME}. Done.')

    else:
        name = ms[1]
        channel = discord.utils.get(g.text_channels, name=name)
        if channel is not None:
            storage[g.id].channel_id = channel.id
            await message.delete()
            await message.channel.send(content=f'Set pictures channel to {channel.name}. Done.')
        else:
            await message.channel.send(content='Invalid Channel')

    pickle.dump(storage, open('serverdata','wb'))

async def setChannel(message):
    g = message.guild
    ms = message.content.split()

    if g.id not in storage:
        await message.channel.send(content='Bot not initialised')
        return

    if len(ms) == 3:
        name1 = ms[1]
        channel = discord.utils.get(g.text_channels, name=name1)
        if channel is not None:
            storage[g.id].channel_id = channel.id
            await message.channel.send(content=f'Changed picture channel to {channel.name}')
        else:
            await message.channel.send(content='Invalid Picture Channel')        
        
        name2 = ms[2]
        channel = discord.utils.get(g.text_channels, name=name2)
        if channel is not None:
            storage[g.id].channel_id = channel.id
            await message.channel.send(content=f'Changed links channel to {channel.name}')
        else:
            await message.channel.send(content='Invalid Links Channel')

    else:
        await message.channel.send(content='Invalid parameters')
        return
    
    pickle.dump(storage, open('serverdata','wb'))

async def addChannel(message):
    g = message.guild
    ms = message.content.split()

    if g.id not in storage:
        await message.channel.send(content='Bot not initialised, please initialise bot before adding a channel')
        return

    if len(ms) == 2:
        name = ms[1]
        channel = discord.utils.get(g.text_channels, name=name)
        if channel is not None and channel.id != storage[g.id].channel_id:
            storage[g.id].monitor_ch.append(channel.id)
            await message.channel.send(content=f'Added {channel.name} to monitored channels')
        else:
            await message.channel.send(content='Invalid Channel')
    else:
        await message.channel.send(content='Invalid parameters')
        return
    
    pickle.dump(storage, open('serverdata','wb'))

async def generateHelp(message):
    content = """Hello
    Picture Organizer Bot enables you to organize pictures in their discords servers. This bot makes a pics channel with all the pictures.

    Commands:
    pic!init [-c]
        Initialises the bot. 
        [-c] creates channel 'pictures' for all the pictures.
    pic!add channel_name
        Add a monitored channel
    pic!set picture_channel_name links_channel_name
        To change the pictures channel.
    """
    await message.channel.send(content=content)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    # guild = discord.utils.get(client.guilds, name=GUILD)

    print(f'{client.user} is connected to the following guilds:')
    
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
        if guild.id in storage:
            print(f'Guild config:\n{storage[guild.id].print(guild)}')
        else:
            print('Guild not configured yet')

    act = discord.Game("pic!help")
    await client.change_presence(activity=act)


@client.event
async def on_message(message):
    g = message.guild
    ms = message.content.split()

    # pps!setup
    if len(ms)>0:
        if ms[0] == 'pic!init':
            await initialSetup(message)
        elif ms[0] == 'pic!set':
            await setChannel(message)
        elif ms[0] == 'pic!help':
            await generateHelp(message)
        elif ms[0] == 'pic!add':
            await addChannel(message)

    if g.id in storage:
        if message.channel.id in storage[g.id].monitor_ch:
            if len(message.attachments)>0:
                print("monitored")
                print(message.content)
                print("has pics")
                
                files = []
                pp = True
                for att in message.attachments:
                    ex = att.filename.split('.')[-1]
                    if ex not in extensions:
                        pp = False
                        break
                    f = await att.to_file()
                    files.append(f)

                pchannel = g.get_channel(storage[g.id].channel_id)
                if pp and pchannel is not None:

                    cont = message.content
                    msg = await pchannel.send(content=f'**{message.author.display_name}:** {cont}', files=files)
                    to_add = f'Pics at {msg.jump_url}'

                    if cont == '':
                        cont = f'**{message.author.display_name}:** {msg.jump_url}'
                    else:
                        cont = f'**{message.author.display_name}:** {cont} --- {to_add}'

                    await message.channel.send(content = cont)
                    await message.delete()
            
            elif len(message.embeds)>0:
                print("monitored")
                print(message.content)
                print("has links")

                links_channel = g.get_channel(storage[g.id].channel_id)
                cont = f'**{message.author.display_name}:** '

                first = True
                for embed in message.embeds
                    if first:
                        cont = cont + f'{message.content} --- Find the original message at {message.jump_url}'
                        msg = await links_channel.send(content=f'**{message.author.display_name}:** {cont}', embed = embed)
                        first = False
                    else:
                        msg = await links_channel.send(content=f'**{message.author.display_name}:** {cont}', embed = embed)


client.run(TOKEN)
