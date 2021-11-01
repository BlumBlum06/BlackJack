#importing
import requests
import json
from os import system
import time

from colorama import init
from termcolor import colored
init()

#setting money to 0 as a global variable
global money
money = 800

#getting the cards with 6 decks 
url = 'http://deckofcardsapi.com/api/deck/new/'
data = {'deck_count': '6'}

Cards = json.loads(requests.post(url, data).text)
DeckID = Cards['deck_id']

print("starting game...")
time.sleep(1)
print("getting cards...")
time.sleep(1)

#shuffle deck
print("shuffling deck...")
for i in range(5):
  requests.post(f'http://deckofcardsapi.com/api/deck/{DeckID}/shuffle/')

#drawing a random card from the deck
def DrawCard(howMany):
  url = f"http://deckofcardsapi.com/api/deck/{DeckID}/draw/"
  data = {'count': howMany}

  
  #getting the cards
  DrawedCard = requests.post(url, data)
  DrawedCard = json.loads(DrawedCard.text)["cards"]
  Cards = []
  for i in DrawedCard:
    Cards.append(i["value"] + "_" + i["suit"])

  return(Cards)

#adding the cards to a number
def AddCards(cards):
  number = 0
  for i in cards:
    i = i.split("_")[0]
    #adding number, and converting picture cards to numbers
    try:
      number += int(i)
    except:
      PictureCards = {
        "QUEEN": 10,
        "KING": 10,
        "JACK": 10,
        "ACE": 11
      }
      number += PictureCards[i]
  return(number)

def PrintCards(cards, hidden=False):
  CardString = ""
  index = 0
  for i in cards:
    index+=1
    if hidden and index == 1:
      CardString += " | " + colored("hidden", "red")
    else:
      i = i.split("_")
      CardString += " | " + colored(i[0], 'green') + colored(" of ", 'green') + colored(i[1], 'green')
  return(CardString + " | ")

def Bet():
  bet = int(input("how much do you want to bet: "))
  if bet > money:
    print(colored("You dont have that much money", "red"))
    Bet()

def Main():
  system("clear")
  #assigning two cards to dealer and player
  PlayersCards = DrawCard(2)
  DealersCards = DrawCard(2)

  print("")
  print(colored("GAME STARTED\n", 'red',))
  print(f"Bank: {money}\n")
  Bet()
  system("clear")
  print("dealers cards are:")
  print(PrintCards(DealersCards, True))
  print("\nyour cards are:")
  print(PrintCards(PlayersCards), "\n")
  
  

Main()