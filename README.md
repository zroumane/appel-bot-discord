# appel-bot-discord

Bot discord permettant de faire l'appel d'un role automatiquement.
[Ajouter le bot a votre discord](https://discord.com/oauth2/authorize?client_id=692301073867866133&permissions=3072&scope=bot)

## Self-hosting :

Installer le module [discord.py](https://github.com/Rapptz/discord.py)
```bash
pip install discord 
```
Ajouter votre secret token de bot à une variable d'environnement nommé `DISCORD_BOT_TOKEN`
```bash
python bot.py
```

## Commande : 
> La commande  **?appel @rôle** peut être utilisée uniquement par les membres ayants un rôle 'professeur' ou 'administrateur' ou 'admin' ou ayant les permissions administrateur sur le serveur. Pour exécuter la commande il faut être dans un salon vocal. La commande renvoie la liste des membres présent et absent dans le channel vocal ou vous êtes par rapport à tous les membres ayant le rôle ciblé en argument de la commande.