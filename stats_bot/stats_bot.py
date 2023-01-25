import discord
import requests
import random
import json
import base64
import string
import time
from datetime import date,datetime,timedelta

client = discord.Client()

#def get_price():
#  headers = {
#    'Host': 'api.coingecko.com',
#    'Accept': '*/*'
#  }
#  a = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=stargaze',headers=headers,timeout=20)
#  if a.status_code == 200:
#    price = json.loads(a.text)[0]['current_price']
#    if price == None:
#      get_price()
#    else:
#      return price
#  else:
#    get_price()
def get_price()-> float:
   price = requests.get('https://api-osmosis.imperator.co/tokens/v2/price/STRD',timeout=30)
   data = price.json()['price']
   return round(float(data),3)


def get_circulating_supply():
    total_supply = get_supply()
    comm_pool = get_community_pool()
    return round(total_supply - comm_pool - 69070175612500 /1000000 ,2)

def get_market_cap():
    total_price = get_price()
    return total_price * get_circulating_supply()


def get_community_pool() -> float:
   pool = requests.get('https://lcd.stride-1.bronbro.io/cosmos/distribution/v1beta1/community_pool')
   community_pool = pool.json()['pool']
   for i in community_pool:
      if  i['denom'] == 'ustrd':
         return round(float(i['amount'])/1000000,2)

def get_supply() -> int:
   supply = requests.get('https://lcd.stride-1.bronbro.io/cosmos/bank/v1beta1/supply')
   data = supply.json()['supply']
   for i in data:
      if  i['denom'] == 'ustrd':
         return round(int(i['amount'])/1000000,2)

def get_bonded_tokens() -> int:
   tokens = requests.get('https://lcd.stride-1.bronbro.io/cosmos/staking/v1beta1/pool')
   bonded_tokens = tokens.json()['pool']['bonded_tokens']
   return int(bonded_tokens)

#def get_apr() -> float:
#    infl = get_inflation()
#    total_supply = get_supply()
#    bond_tokens = get_bonded_tokens()
#    return round(infl * (1 - (20 / 100)) / (bond_tokens / total_supply) *1000000 *100 ,2)

def get_apr() -> float:
    res = requests.get(url='https://lcd.stride-1.bronbro.io/mint/v1beta1/params', timeout=30).json()
    bond_tokens = get_bonded_tokens()
    reduction_period_in_epochs =  res['params']['reduction_period_in_epochs']
    epoch_provision = res['params']['genesis_epoch_provisions']
    staking = res['params']['distribution_proportions']['staking']
    return round(float(epoch_provision) * float(reduction_period_in_epochs) *float(staking) / float(bond_tokens) * 100,2)




def formatIt(hello):
  suffixes = ["", "K", "M", "B", "T"]
  hello = str("{:,}".format(hello))
  commas = 0
  x = 0
  while x < len(hello):
      if hello[x] == ',':
        commas += 1
      x += 1
  return hello.split(',')[0]+'.'+hello.split(',')[1][:-1] + suffixes[commas]

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  message = await client.get_channel(channelID).fetch_message(messageID)
  while(True):
    try:
      today = date.today().strftime("%B %d, %Y")
      price = get_price()
      marketCap = get_market_cap()
      maxSupply = 100000000
      circulatingSupply = get_circulating_supply()
      #inflation = get_inflation()*100
      unbondingPeriod = 14
      maxValidators = 100
      communityPool= get_community_pool()
      currentSupply = get_supply()
      totalBonded = get_bonded_tokens() /1000000
      bondedRatio = round(float(totalBonded/currentSupply)*100,2)
      APR = get_apr()
      messageToBeSent = ':calendar: **'+today+'** :calendar:\n**__Stirde Stats - Update/Minute__**\n\n'
      messageToBeSent = messageToBeSent+':dollar: `Price:` **$'+str(price)+'**\n:moneybag: `Market Capitalization:` **$'+str(formatIt(marketCap))+'**\n'
      messageToBeSent = messageToBeSent+'```Supply Stats```:left_luggage: `Max Supply:` **'+'{:,}'.format(int(maxSupply))+'**\n:briefcase: `Current Supply:` **'+'{:,}'.format(currentSupply)+'**\n:recycle: `Circulating Supply:` **'+'{:,}'.format(circulatingSupply)+'**\n:classical_building: `Community Pool:` **'+'{:,}'.format(communityPool)+'**\n'
      messageToBeSent = messageToBeSent+'```Staking Stats```:trophy: `APR:` **'+str(APR)+'%**\n:closed_lock_with_key: `Total Bonded:` **'+'{:,}'.format(int(totalBonded))+'**\n:bar_chart: `Bonded Ratio:` **'+str(bondedRatio)+'%**\n:unlock: `Unbonding Period:` **'+str(int(unbondingPeriod))+' Days**\n:technologist: `Max Validators:` **'+str(maxValidators)+'**\n'
      messageToBeSent = messageToBeSent+'```Resources```:lizard: `CoinGecko:` https://www.coingecko.com/en/coins/stride\n:test_tube: `Osmosis:` https://info.osmosis.zone/token/STRD\n:desktop: `Monitor:` https://monitor.bronbro.io/d/stride-stats\n:mag_right: `Mintscan:` https://www.mintscan.io/stride\n\n'
      messageToBeSent = messageToBeSent+'>>> ***Powered By <@419903072379338753>***'
      await message.edit(content=messageToBeSent)
      #message.channel.send("This is a Message")
      print('Updated on: '+str(datetime.now().strftime("%H:%M:%S")))
      time.sleep(57)
    except:
      continue

messageID = 106353217189364 #click on copy link in discord and pate into browser
channelID = 1063270165044797
BOT_TOKEN = ''
client.run(BOT_TOKEN)
