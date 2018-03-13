""" 
Created on Mar MON 12 17:58:23 2018
@author: Archie Paredes
Lottery Player
"""
import json
import hashlib
import sys
from web3 import Web3, HTTPProvider, IPCProvider
from pprint import pprint

web3 = Web3 (HTTPProvider ("http://localhost:9545"))

with open ("abi.json") as f:
    abi = json.load (f)

if len (sys.argv) == 2:
    contractAddress = sys.argv[1]
else:
    blockNumber = web3.eth.blockNumber
    contractAddress = None
    while contractAddress == None and blockNumber >= 0:
        block = web3.eth.getBlock (blockNumber)
        for txHash in block.transactions:
            tx = web3.eth.getTransactionReceipt (txHash)
            contractAddress = tx.get ("contractAddress") 
            if(contractAddress != None):
                break
        blockNumber = blockNumber - 1
        
contract = web3.eth.contract (abi = abi, address = contractAddress)
print ("Using contract address {:s}\n".format (contractAddress))

def play():
    accountIndex = int(input("What number player are you? Enter 1 to 4: "))
    numGuess = 0
    while(numGuess < 1 or numGuess > 45):
        numGuess = int(input("Please enter your number from 1 to 45: "))
    securityNum = 0
    while(securityNum < 1 or securityNum > 5000):
        securityNum = int(input("For security reasons, enter  number from 1 to 5000: "))
    print("Remember your security number: {}".format(securityNum))

    account = web3.eth.accounts[accountIndex]

    transactionHash = contract.transact({"from": account, "value":web3.toWei(0.01, "ether")}).play(numGuess,securityNum)


    print("Player number {}, using account {}, to play on contract {}".format(accountIndex, account, contractAddress))


def reveal():
    accountIndex = int(input("What number player are you? Enter 1 to 4: "))
    account = web3.eth.accounts[accountIndex]
    
    print("Player number {}, using account {}, to play on contract {}".format(accountIndex, account, contractAddress))

    transactionHash = contract.transact({"from": account}).revealChoice()

def winner():
    accountIndex = int(input("What number player are you? Enter 1 to 4: "))
    securityNum = int(input("For security reasons, what was your number from 1 to 5000: "))
    account = web3.eth.accounts[accountIndex]
    
    print("Player number {}, using account {}, to play on contract {}".format(accountIndex, account, contractAddress))
    
    transactionHash = contract.transact({"from": account}).winCollect(securityNum)

def checkBalance(contract):
    for acc in web3.eth.accounts:
        balance = web3.eth.getBalance (acc)
        print ("{:s} has {:.020f} ETH".format (acc, float (web3.fromWei (balance, "ether"))))
    



print("Player Options:")
print("1.) Play a number. (Valid only before deadline) Type: '1'")
print("2.) Reveal your choice to the host. (Valid only after deadline and before reveal deadline) Type '2'")
print("3.) Claim prize if you've won. (Valid only player has won and revealed choice before reveal deadline) Type '3'")
print("4.) Check balance of accounts. Type '4'")

choice = 0
while(choice < 1 or choice > 4):
    choice = int(input("Please choose a valid option: "))
if(choice == 1):
    play()
elif(choice == 2):
    reveal()
elif(choice == 3):
    winner()
elif(choice == 4):
    checkBalance(contract)

        


          
