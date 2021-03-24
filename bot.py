import os
import unicodedata
import discord
from discord.ext import commands
from discord.utils import get


# Tous les roles qui peuvent utiliser la commande, que des majuscules pas d'accent
admin_role = ['PROFESSEUR', 'ADMINISTRATEUR', 'ADMIN']


# Message d'aide (?aide)
help_msg = "> La commande  **?appel @rôle** peut être utilisée uniquement par les membres ayants un rôle 'professeur' ou 'administrateur' ou 'admin' ou ayant les permissions administrateur sur le serveur. Pour exécuter la commande il faut être dans un salon vocal. La commande renvoie la liste des membres présent et absent dans le channel vocal ou vous êtes par rapport à tous les membres ayant le rôle ciblé en argument de la commande."


# Bolean auteur admin
async def check_if_admin(ctx):
  if ctx.author.guild_permissions.administrator:
    return True
  for i in ctx.author.roles:
    role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
    if role.upper() in admin_role:
      return True
  msg = "Tu n'as pas l'autorisation d'utiliser cette commande {0.author.mention}.".format(ctx)
  await ctx.send(msg)
  return False


# Bolean auteur dans un channel vocal
async def check_if_vocal(ctx):
  if not ctx.author.voice:
    msg = "Vous devez être dans un salon pour éxécuter la commande {0.author.mention}.".format(ctx)
    await ctx.send(msg)
    return False
  return True


# Commande ?appel
@commands.command()
async def appel(ctx, *args):
  
  if not await check_if_admin(ctx):
    return
  
  if not await check_if_vocal(ctx):
    return

  try: 
    role_id = int(''.join(filter(lambda i: i.isdigit(), *args)))
    role = ctx.guild.get_role(role_id)
    role_members = role.members 
  except: 
    msg = "'" + str(*args) + "' ne convient pas pour la commande ?appel {0.author.mention}.".format(ctx)
    await ctx.send(msg)
    return

  channel_members = []
  for member in ctx.author.voice.channel.members:
    if role in member.roles:
      channel_members.append(member)
  
  absent_members = list(set(role_members) - set(channel_members))


  msg = 'Appel du rôle {0.mention} dans le salon `{1.author.voice.channel.name}`.\n'.format(role, ctx)
  
  msg += '**Absent :**\n> '

  if not absent_members:
      msg += 'Tous les membres ayant le rôle {0.mention} sont présents.\n'.format(role)
  else:
      msg += ', '.join([i.mention for i in absent_members])
      msg += '\n'
  msg += '**Présent :**\n> '

  if not channel_members:
      msg += 'Tous les membres ayant le rôle {0.mention} sont absents.\n'.format(role)
  else:
      msg += ', '.join([i.mention for i in channel_members])

  await ctx.send(msg)
  return


# Commande ?aide

@commands.command()
async def aide(ctx):
  if not await check_if_admin(ctx):
    return
  await ctx.send(help_msg)
  return


# Initialisation

intents = discord.Intents().all()
client = discord.Client()
client = commands.Bot(command_prefix='?', intents=intents)


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="?aide"))
  print('Connecté en tant que {0.user}'.format(client))


client.remove_command('help')
client.add_command(aide)
client.add_command(appel)
client.run(os.getenv('DISCORD_BOT_TOKEN'))