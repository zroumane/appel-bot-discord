import discord
from discord.ext import commands
import unicodedata
import os
import time


help_msg = """```
Les comandes suivantes peuvent être utilisés que par les membres ayants un rôle "professeur".
Elles s'appliquent que sur les membres ayant un rôle "élève".
Pour éxécuter ces commandes il faut être dans un salon vocal,
?appel    Pour lancer l'appel de tout les membres ayants le rôle "élève" dans le salon vocal
?appel a/b    Pour lancer l'appel de tout les membres ayants le rôle "Groupe A/B" dans le salon vocal
?présent    Pour avoir la liste de tout les membres présents ayants le rôle "élève" dans le salon vocal
?présent a/b   Pour avoir la liste de tout les membres présents ayants le rôle "Groupe A/B" dans le salon vocal
?groupe <nombre> <maxi_user>  Pour créer des salons vocaux permettant de faire des groupes d'élèves
?groupe supprimer   Pour supprimer tous les salons vocaux créés via la commande '?groupe...' sur ce serveur
?retour   Pour déplacer tous les membres connectés ayants le rôle "élève" dans son channel vocal
```"""

client = discord.Client()

client = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="zephyr#5410"))
    print('Connecté en tant que {0.user}'.format(client))


@commands.command()
async def appel(ctx, *args):
    for i in ctx.author.roles:
        role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
        if role.upper() == 'PROFESSEUR' or role.upper() == 'ADMINISTRATEUR':
            if not ctx.author.voice:
                msg = "Vous devez être dans un salon pour éxécuter la commande {0.author.mention}.".format(ctx)
                await ctx.send(msg)
                return
            else:   
                
                list_eleve = []
                if not args:
                    roletocall = 'ELEVE'
                elif args[0] == 'a' or args[0] == 'A':
                    roletocall = 'GROUPE A'
                elif args[0] == 'b' or args[0] == 'B':
                    roletocall = 'GROUPE B'
                else:
                    output = ''
                    for i in args:
                        output += i
                    msg = "'" + output + "' ne convient pas pour la commande ?appel {0.author.mention}.".format(ctx)
                    await ctx.send(msg)
                    return
                for i in ctx.guild.members:
                    for j in i.roles:
                        role = ''.join((c for c in unicodedata.normalize('NFD', str(j.name)) if unicodedata.category(c) != 'Mn'))
                        if role.upper() == roletocall:
                            list_eleve.append(i)

                voice_channel = ctx.author.voice.channel
                member = voice_channel.members
                for i in member:
                    for j in list_eleve:
                        if i == j:
                            del list_eleve[list_eleve.index(j)]
                if roletocall == 'GROUPE A':
                    arg = ' du groupe A '
                elif roletocall == 'GROUPE B':
                    arg = ' du groupe B '
                else:
                    arg = ' '
                if not list_eleve:
                    msg = 'Tous les élèves' + arg +  'sont présents pour le cours de {0.author.mention}.'.format(ctx)
                    await ctx.send(msg)
                    return
                else:
                    list_absent = []
                    for i in list_eleve:
                        list_absent.append(i.mention)
                    msg = 'Les élèves' + arg + ', '.join(list_absent) +' ne sont pas présents pour le cours de {0.author.mention}.'.format(ctx)
                    await ctx.send(msg)
                    return
    msg = "Tu n'as pas l'autorisation d'utiliser cette commande {0.author.mention}.".format(ctx)
    await ctx.send(msg)


@commands.command()
async def présent(ctx, *args):
    for i in ctx.author.roles:
        role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
        if role.upper() == 'PROFESSEUR' or role.upper() == 'ADMINISTRATEUR':
            if not ctx.author.voice:
                msg = "Vous devez être dans un salon pour éxécuter la commande {0.author.mention}.".format(ctx)
                await ctx.send(msg)
                return
            else:    
                voice_channel = ctx.author.voice.channel
                member = voice_channel.members
                list_présent = []
                if not args:
                    roletocall = 'ELEVE'
                elif args[0] == 'a' or args[0] == 'A':
                    roletocall = 'GROUPE A'
                elif args[0] == 'b' or args[0] == 'B':
                    roletocall = 'GROUPE B'
                else:
                    output = ''
                    for i in args:
                        output += i
                    msg = "'" + output + "' ne convient pas pour la commande ?présent {0.author.mention}.".format(ctx)
                    await ctx.send(msg)
                    return
                for i in member:
                    for j in i.roles:
                        role = ''.join((c for c in unicodedata.normalize('NFD', str(j.name)) if unicodedata.category(c) != 'Mn'))
                        if role.upper() == roletocall:
                            list_présent.append(i.mention)
                if roletocall == 'GROUPE A':
                    arg = ' du groupe A '
                elif roletocall == 'GROUPE B':
                    arg = ' du groupe B '
                else:
                    arg = ' '
                msg = 'Les élèves' + arg+ ', '.join(list_présent) + ' sont présents pour le cours de {0.author.mention}.'.format(ctx)
                await ctx.send(msg)
                return
    msg = "Tu n'as pas l'autorisation d'utiliser cette commande {0.author.mention}.".format(ctx)
    await ctx.send(msg)


@commands.command()
async def groupe(ctx, *args):
    for i in ctx.author.roles:
        role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
        if role.upper() == 'PROFESSEUR' or role.upper() == 'ADMINISTRATEUR':
            if not ctx.author.voice:
                msg = "Vous devez être dans un salon vocal pour éxécuter la commande {0.author.mention}.".format(ctx)
                await ctx.send(msg)
                return
            if not args:
                msg = "Vous devez renseigner le nombre de salon vocal à créer (ex: ?groupe 5) {0.author.mention}.".format(ctx)
                await ctx.send(msg)
                return
            arg = args[0]

            if str(arg) == 'supprimer':
                filename = 'groupe_' + str(ctx.guild.id) + '.txt'
                if os.path.isfile(filename):
                    with open(filename, 'r') as file:                          
                        to_del = file.readlines()
                        file.close()
                    nb = 0
                    for i in to_del:
                        i = i.replace("\n", " ")
                        i = i.replace(" ", "")
                        for j in ctx.guild.voice_channels:
                            if str(j.id) == str(i):
                                await j.delete()
                                nb += 1
                    os.remove(filename)
                    msg = str(nb) + " salons vocaux créés sur le serveur {0.guild.name} ont été supprimés".format(ctx)
                    await ctx.send(msg)
                    return
                else:
                    msg = "Aucun salon vocal '?groupe' n'a été créé sur ce serveur {0.author.mention}.".format(ctx)
                    await ctx.send(msg)
                    return
            try:
                if int(arg) <= 20:
                    arg = int(arg)
                    categrory_id = ctx.author.voice.channel.category_id
                    server = ctx.message.guild
                    position = ctx.author.voice.channel.position
                    for i in server.categories:
                        if i.id == categrory_id:
                            category = i
                            channel_list = []
                            try:
                                if int(args[1]) >= 2:
                                    for i in range(1, arg + 1):
                                        name = 'Groupe ' + str(i)
                                        channel = await server.create_voice_channel(name,category=category, position=position, user_limit=args[1])
                                        channel_list.append(channel)
                                    filename = 'groupe_' + str(ctx.guild.id) + '.txt'
                            except:
                                for i in range(1, arg + 1):
                                    name = 'Groupe ' + str(i)
                                    channel = await server.create_voice_channel(name,category=category, position=position)
                                    channel_list.append(channel)
                                filename = 'groupe_' + str(ctx.guild.id) + '.txt'
                            with open(filename, 'a') as file:
                                for i in channel_list:                              
                                    file.write(str(i.id) + "\n")
                                file.close()
                            msg = str(args[0]) + ' salons vocaux ont été créés en dessous de ' + ctx.author.voice.channel.name + ' pour le cours de {0.author.mention}.'.format(ctx)
                            await ctx.send(msg)
                            return
                    channel_list = []
                    try:
                        if int(args[1]) >= 2:    
                            for i in range(1, arg + 1):
                                name = 'Groupe ' + str(i)
                                channel = await server.create_voice_channel(name, position=position, user_limit=args[1])
                                channel_list.append(channel)
                            filename = 'groupe_' + str(ctx.guild.id) + '.txt'
                            with open(filename, 'a') as file:
                                for i in channel_list:                              
                                    file.write(str(i.id) + "\n")
                                file.close()
                            msg = str(args[0]) + ' salons vocaux ont été créés en dessous de ' + ctx.author.voice.channel.name + ' pour le cours de {0.author.mention}.'.format(ctx)
                            await ctx.send(msg)
                            return
                    except:
                        for i in range(1, arg + 1):
                            name = 'Groupe ' + str(i)
                            channel = await server.create_voice_channel(name, position=position, user_limit=args[1])
                            channel_list.append(channel)
                        filename = 'groupe_' + str(ctx.guild.id) + '.txt'
                        with open(filename, 'a') as file:
                            for i in channel_list:                              
                                file.write(str(i.id) + "\n")
                            file.close()
                        msg = str(args[0]) + ' salons vocaux ont été créés en dessous de ' + ctx.author.voice.channel.name + ' pour le cours de {0.author.mention}.'.format(ctx)
                        await ctx.send(msg)
                        return   
                elif int(arg) >= 21:             
                    msg = "La limite est 20 salons vocaux {0.author.mention}.".format(ctx)
                    await ctx.send(msg)  
                    return  
            except:
                output = ''
                for i in arg:
                    output += i
                msg = "'" + output + "' ne convient pas pour la commande ?appel {0.author.mention}.".format(ctx)
                await ctx.send(msg)
                return                       
    msg = "Tu n'as pas l'autorisation d'utiliser cette commande {0.author.mention}.".format(ctx)
    await ctx.send(msg)

@commands.command()
async def aide(ctx):
    for i in ctx.author.roles:
        role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
        if role.upper() == 'PROFESSEUR' or role.upper() == 'ADMINISTRATEUR':
            await ctx.send(help_msg)
            return
    msg = "Tu n'as pas l'autorisation d'utiliser cette commande {0.author.mention}.".format(ctx)
    await ctx.send(msg)

@commands.command()
async def retour(ctx):
    for i in ctx.author.roles:
        role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
        if role.upper() == 'PROFESSEUR' or role.upper() == 'ADMINISTRATEUR':
            if not ctx.author.voice:
                msg = "Vous devez être dans un salon vocal pour éxécuter la commande {0.author.mention}.".format(ctx)
                await ctx.send(msg)
                return
            salon = ctx.author.voice.channel
            for i in ctx.guild.roles:
                role = ''.join((c for c in unicodedata.normalize('NFD', str(i.name)) if unicodedata.category(c) != 'Mn'))
                if role.upper() == 'ELEVE':
                    await ctx.send("3 secondes avant le déplacement des {0} dans le salon {1}".format(i.mention, salon.name))
                    time.sleep(3)
                    for u in i.members:
                        if u.voice:
                            await u.move_to(salon)
            msg = "Les élèves ont été déplacé par {0.author.mention} dans le salon {1.name}.".format(ctx, salon)
            await ctx.send(msg)
            return
    msg = "Tu n'as pas l'autorisation d'utiliser cette commande {0.author.mention}.".format(ctx)
    await ctx.send(msg)


print(os.getenv('DISCORD_APP_TOKEN'))

client.remove_command('help')
client.add_command(présent)
client.add_command(appel)
client.add_command(aide)
client.add_command(groupe)
client.add_command(retour)
client.run(os.getenv('DISCORD_APP_TOKEN'))
