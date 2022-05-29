from distutils.version import LooseVersion
from turtle import clear
import discord
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
import requests
import json
from urllib.parse import quote

bot = commands.Bot(command_prefix='!')
client = discord.Client()

#global variables

api_key = ('RGAPI-7e7089f2-9108-43fa-84d6-175e8c57957d')


my_region ='euw1'
my_region2 ='na1'



@bot.event
async def on_ready():
    print("prêt à stalker")

@bot.command()
async def elo(message,arg, arg2=None):
    #1st arg is summoner name, 2nd arg is serv (default is set on euw, can be empty)
    blaze = arg
    serv = arg2
    #use for url purpose into api request
    if serv is None : 
        serveur = 'euw1'
    elif serv == 'na':
        serveur = 'na1'
    #Request to set id url, with the serv, the summoner name and the api key as variables
    idurl = (f'https://{serveur}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{blaze}?api_key={api_key}')
    print (blaze)
    print(idurl)
    #Get id value by requesting data from the json file that we can find on the url
    response = requests.get(idurl)
    json_puuid = response.json()
    userId = (json_puuid['id'])
    print(userId)
    #Get Url for player's data api call
    dataPlayerUrl = (f'https://{serveur}.api.riotgames.com/lol/league/v4/entries/by-summoner/{userId}?api_key={api_key}')
    print(dataPlayerUrl)
    #Get global player's data
    response = requests.get(dataPlayerUrl)
    json_dataPlayer = response.json()
    dataPlayer = (json_dataPlayer)
    #Have to initiate variable at -1 because 0 is a used value
    flexGames = -1
    soloGames = -1
    flexRank = -1
    flexTier = -1
    flexLp = -1
    soloTier = -1
    soloRank = -1
    soloLp = -1
    #Get Data from FlexQ

    for i in range(len(dataPlayer)):
        if dataPlayer[i]['queueType'] == "RANKED_FLEX_SR":
            flexTier = dataPlayer[i]['tier']
            flexRank = dataPlayer[i]['rank']
            flexLp = dataPlayer[i]['leaguePoints']
            flexWin = dataPlayer[i]['wins']
            flexLoose = dataPlayer[i]['losses']
            flexGames = (dataPlayer[i]['wins']) + (dataPlayer[i]['losses'])
            break
    for i in range(len(dataPlayer)):
        if dataPlayer[i]['queueType'] == "RANKED_SOLO_5x5":
            soloTier = dataPlayer[i]['tier']
            soloRank = dataPlayer[i]['rank']
            soloLp = dataPlayer[i]['leaguePoints']
            soloWin = dataPlayer[i]['wins']
            soloLoose = dataPlayer[i]['losses']
            soloGames = (dataPlayer[i]['wins']) + (dataPlayer[i]['losses'])
            break
    print(soloGames)
    print(flexGames)
    soloTierValue = 0
    flexTierValue = 0
    #SoloQ Value calculation
    if soloTier == "IRON" :
        soloTierValue += 100000
    elif soloTier == "BRONZE" :
        soloTierValue += 200000
    elif soloTier == "SILVER" :
        soloTierValue += 300000
    elif soloTier == "GOLD" :
        soloTierValue += 400000
    elif soloTier == "PLATINIUM" :
        soloTierValue += 500000
    elif soloTier == "DIAMOND" :
        soloTierValue += 600000
    elif soloTier == "MASTER" :
        soloTierValue += 700000
    elif soloTier == "GRANDMASTER" :
        soloTierValue += 800000
    elif soloTier == "CHALLENGER" :
        soloTierValue += 900000
    print(soloTierValue)
    if soloRank == "IV" : 
        soloTierValue += 10000    
    if soloRank == "III" :
        soloTierValue += 20000
    if soloRank == "II" : 
        soloTierValue += 30000
    if soloRank == "I" : 
        soloTierValue += 40000
    print(soloTierValue)
    soloTierValue += soloLp
    print(soloTierValue)
#FlexValue
    if flexTier == "IRON" :
        flexTierValue += 100000
    elif flexTier == "BRONZE" :
        flexTierValue += 200000
    elif flexTier == "SILVER" :
        flexTierValue += 300000
    elif flexTier == "GOLD" :
        flexTierValue += 400000
    elif flexTier == "PLATINIUM" :
        flexTierValue += 500000
    elif flexTier == "DIAMOND" :
        flexTierValue += 600000
    elif flexTier == "MASTER" :
        flexTierValue += 700000
    elif flexTier == "GRANDMASTER" :
        flexTierValue += 800000
    elif flexTier == "CHALLENGER" :
        flexTierValue += 900000
    print(flexTierValue)
    if flexRank == "IV" : 
        flexTierValue += 10000    
    if flexRank == "III" :
        flexTierValue += 20000
    if flexRank == "II" : 
        flexTierValue += 30000
    if flexRank == "I" : 
        flexTierValue += 40000
    print(flexTierValue)
    flexTierValue += flexLp
    print(flexTierValue)
    if flexTierValue > soloTierValue :
        ranktoprint = ("Rang flex Q")
        loosestoprint = flexLoose
        winstoprint = flexWin
        gametotal = (flexWin) / (flexGames)
        gametotaltoprint = gametotal * 100
        tierToPrint = flexTier.lower()
        tierToPrint = tierToPrint + "_"
        tierToPrint = tierToPrint + flexRank
        tierToPrint = tierToPrint + ".png"
    elif soloTierValue > flexTierValue :
        ranktoprint = ("Rang solo Q")
        loosestoprint = soloLoose
        winstoprint = soloWin
        gametotal = (soloWin) / (soloGames)
        gametotaltoprint = gametotal * 100
        gametotaltoprint = str(round(gametotaltoprint, 2))
        tierToPrint = soloTier.lower()
        tierToPrint = tierToPrint + "_"
        tierToPrint = (tierToPrint) + (soloRank)
        tierToPrint = tierToPrint + ".png"
        print(soloTier)
    embed = discord.Embed(title = blaze, description =("%s\n %sW/%s L \n %s " % (ranktoprint, winstoprint,  loosestoprint, gametotaltoprint)))
    file = discord.File(f'./img/{tierToPrint}', filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")
    await message.channel.send(file = file, embed=embed)


@bot.command()
async def stats(message,arg1, arg2=None):
       #Check for the user's puuid
    blaze = arg1
    serv = arg2
    if serv is None : 
        serveur = 'euw1'
    elif serv == 'na':
        serveur = 'na1'
    print (serveur)
    altserveur = str
    if serveur == 'na1':
        altserveur = ('https://americas.api.riotgames.com')
    else :
        altserveur = ('https://europe.api.riotgames.com')
    
    nomJoueur = blaze
    blaze = quote(blaze)
    puuidURL = (f'https://{serveur}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{blaze}?api_key={api_key}')
    response = requests.get(puuidURL)
    json_puuid = response.json()
    userPuuid = (json_puuid['puuid'])
    #await message.channel.send(json_puuid['puuid'])
    #Use puuid to find a list of 10 games
    listOfGameUrl = (f'{altserveur}/lol/match/v5/matches/by-puuid/{userPuuid}/ids?start=0&count=20&api_key={api_key}')
    '''await message.channel.send(listOfGameUrl) debug prupose '''
    responses2 = requests.get(listOfGameUrl)
    json_gamelistfile = responses2.json()
    gamelist = []
    gamelist.extend(json_gamelistfile[:10])
    #await message.channel.send(gamelist) 
    #KDA for 10 last game (only one game because of api limitation rn) 
   # avgKill = 0
   #  avgDeath = 0
   #  amountOfWins = 0
   #  amoutOfLooses = 0
   #  gameIndexor = 0
    #await message.channel.send(gamelist[0])
    oneGameUrl = (f'{altserveur}/lol/match/v5/matches/{gamelist[0]}?api_key={api_key}')
    #await message.channel.send(oneGameUrl)
    responses3 = requests.get(oneGameUrl)
    json_game = responses3.json()['info']['participants']
    print(userPuuid)
    print(oneGameUrl)
    DataJoueur = []   
    for i in range(len(json_game)):
        if json_game[i]['puuid']  == userPuuid:
            DataJoueur.append(json_game[i])
    #print(DataJoueur)
    ''' Get amount of kill on one game'''
    champ = [ sub['championName'] for sub in DataJoueur ]
    amountOfKill = [ sub['kills'] for sub in DataJoueur ]
    amountOfKill = amountOfKill[0]
    amountOfAssist = [ sub['assists'] for sub in DataJoueur ]
    amountOfAssist = amountOfAssist[0]
    amountOfDeath = [ sub['deaths'] for sub in DataJoueur ]
    amountOfDeath = amountOfDeath[0]
    if amountOfDeath == 0:
        kdaValue = (amountOfKill + amountOfAssist)
    else:
        kdaValue = (amountOfKill + amountOfAssist) / amountOfDeath
    kdaValue = str(round(kdaValue, 2))
    victory = [ sub['win'] for sub in DataJoueur ]
    victory = victory[0]
    if victory == True:
        victory ="Victoire"
    else : 
        victory ="Défaite"
    if victory == "Victoire" :
        colorhex = discord.Color.from_rgb(50,205,50)
    elif victory == "Défaite":
        colorhex = discord.Color.from_rgb(220,20,60)
    embed = discord.Embed(title = nomJoueur, description = (" %s/%s/%s" % (amountOfKill, amountOfDeath,  amountOfAssist)), color =colorhex)
    embed.add_field(name = "KDA", value = kdaValue)
    embed.add_field(name = "Champion", value = champ[0])
    embed.add_field(name = "Résultat", value = victory)
    embed.set_thumbnail(url=(f'http://ddragon.leagueoflegends.com/cdn/12.4.1/img/champion/{champ[0]}.png'))
    await message.channel.send(embed=embed)

@bot.command()
async def init(ctx):
    print("Ratio")

@bot.command()
async def stop(ctx):
    print("Ratio2")

@bot.command()
async def recap(ctx):
    print("Ratio3")

@bot.command()
async def stats5(message,arg1, arg2=None):
    #Check for the user's puuid
    blaze = arg1
    serv = arg2
    if serv is None : 
        serveur = 'euw1'
    elif serv == 'na1':
        serveur = 'na1'
    print (serveur)
    altserveur = str
    if serveur == 'na1':
        altserveur = ('https://americas.api.riotgames.com')
    else :
        altserveur = ('https://europe.api.riotgames.com')
    
    nomJoueur = blaze
    blaze = quote(blaze)
    puuidURL = (f'https://{serveur}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{blaze}?api_key={api_key}')
    response = requests.get(puuidURL)
    json_puuid = response.json()
    userPuuid = (json_puuid['puuid'])
    #await message.channel.send(json_puuid['puuid'])
    #Use puuid to find a list of 10 games
    listOfGameUrl = (f'{altserveur}/lol/match/v5/matches/by-puuid/{userPuuid}/ids?start=0&count=20&api_key={api_key}')
    '''await message.channel.send(listOfGameUrl) debug prupose '''
    responses2 = requests.get(listOfGameUrl)
    json_gamelistfile = responses2.json()
    gamelist = []
    gamelist.extend(json_gamelistfile[:6])
    #await message.channel.send(gamelist) 
    #KDA for 10 last game (only one game because of api limitation rn) 
    avgKill = 0
    avgDeath = 0
    avgAssist = 0
    amountOfWins = 0
    amoutOfLooses = 0
    gameIndexor = 0

    gameIndexor = 0
    while gameIndexor < 5:
    #await message.channel.send(gamelist[0])
        oneGameUrl = (f'{altserveur}/lol/match/v5/matches/{gamelist[gameIndexor]}?api_key={api_key}')
    #await message.channel.send(oneGameUrl)
        responses3 = requests.get(oneGameUrl)
        json_game = responses3.json()['info']['participants']
        print(gamelist[gameIndexor])
        DataJoueur = []   
        for i in range(len(json_game)):
            if json_game[i]['puuid']  == userPuuid:
                DataJoueur.append(json_game[i])
        amountOfKill = [ sub['kills'] for sub in DataJoueur ]
        avgKill = avgKill + amountOfKill[0]
        amountOfAssist = [ sub['assists'] for sub in DataJoueur ]
        avgAssist = avgAssist + amountOfAssist[0]
        amountOfDeath = [ sub['deaths'] for sub in DataJoueur ]
        avgDeath = avgDeath + amountOfDeath[0]
        gameIndexor = gameIndexor + 1
        victory = [ sub['win'] for sub in DataJoueur ]
        victory = victory[0]
    print(avgDeath)
    print(avgKill)
    print(avgAssist)
    avgKill = avgKill /5
    avgDeath = avgDeath /5
    avgAssist = avgAssist /5
    print(avgDeath)
    print(avgKill)
    print(avgAssist)
    gameIndexor = 0
    await message.channel.send("%s \nStats moyennes sur ses 5 dernières games %s/%s/%s " % (nomJoueur, avgKill, avgDeath,  avgAssist, ))

bot.run("OTM5NjgzOTc2NTcyOTY5MTAx.Yf8a5g.9_FLwd96NvZramwubOUcJ_0XM24")