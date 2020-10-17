# coinpot autoroll mimic
import random
import hashlib
import time


# autoroll configs
stake = 10
tokens = 40000
HighOrLow = "High"
MultiplyBy = 2
winChance = round(100/MultiplyBy)
maxNumberOfRoll = 100 # False for unlimited
pause = 0 #in seconds
stopRollWhenProfit = False # int value for limited value
stopRollWhenLoss = 50
onWin = {
  "stopRoll":"False",
  "High/Low":"High",
  "Multiplier":"NC",
  "stake":"NC"
  } 

onLose = {
  "stopRoll":"False",
  "High/Low":"Low",
  "Multiplier":"NC",
  "stake":"NC"
  }

randomClientSeed = True

availableChar = list("0123456789abcdef")


def getNumber(client,server):
  string = client+":"+server
  hashed = hashlib.sha512(string.encode("utf-8")).hexdigest()
  f8 = hashed[:8]
  decimal = int(f8,16)
  res = decimal % 1000
  return res

def getSeed(availableChar):
	'''generate and returns client and servver seed'''	
	client = ""
	server =""
	for i in range(8):
		client = client + random.choice(availableChar)
	for i in range(32):
		server = server + random.choice(availableChar)
	return client,server


def getLuckeyNumber():
	'''get corresponging number accorging to high or low'''
	global HighOrLow
	if HighOrLow == "High":
		return "500 - 999"
	else:
		return "000 - 499"

def autoroll():
	'''once this funciton runs this will keep rolling until the certain circumstance is reached'''

	global stake,tokens,maxNumberOfRoll,onLose,onWin,pause,stopRollWhenLoss,stopRollWhenProfit,HighOrLow,winChance
	count = 1
	for i in range(maxNumberOfRoll):
		client,server = getSeed(availableChar)		
		number = getNumber(client,server)

		txt = f"Roll {getLuckeyNumber()} to win {MultiplyBy} times your stake of {stake} token ({winChance}% win chance)"
		print(txt)
		print("you rolled",number,"so ",winOrLose(number),"\n")
		changeHighOrLow(number)
		time.sleep(pause)


def unlimitedAutoroll():
	while True:
		client,server = getSeed(availableChar)		
		number = getNumber(client,server)
		txt = f"Roll {getLuckeyNumber()} to win {MultiplyBy} times your stake of {stake} token ({winChance}% win chance)"
		print(txt)
		print("you rolled",number,"so ",winOrLose(number))
		changeHighOrLow(number)
		time.sleep(pause)

# change multiplier to High or low according to setting
def changeHighOrLow(number):
	global HighOrLow
	if winChance == 50:
		highRange = "s"
	if HighOrLow == "High":
		if number >= 500:
			#win
			HighOrLow = onWin['High/Low']
		else:
			#loss
			HighOrLow = onLose['High/Low']
		
	else:
		if number <= 499:
			#3win
			HighOrLow = onWin["High/Low"]
		else:
			#loss
			HighOrLow = onLose["High/Low"]
	

def winOrLose(rolledNumber):
	global tokens

	if HighOrLow == "High":
		if rolledNumber >= 500:
			tokens+=1
			return f"you won {stake*MultiplyBy} tokens"
		else:
			tokens-=1
			return f"you lose {stake} tokens"
	else:
		if rolledNumber <= 499:
			tokens +=1
			return f"you won {stake*MultiplyBy} tokens"
		else:
			tokens -=1
			return f"you lose {stake} tokens"
		


# unlimitedAutoroll()
autoroll()
print(tokens)
