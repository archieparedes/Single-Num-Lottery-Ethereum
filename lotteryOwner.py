""" 
Created on Mar MON 12 17:59:11 2018
@author: Archie Paredes
Lottery Owner
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
            if contractAddress != None:
                break
        blockNumber = blockNumber - 1
        
contract = web3.eth.contract (abi = abi, address = contractAddress)
print ("Using contract address {:s}\n".format (contractAddress))

def deadline(contract):
    account = web3.eth.accounts[0]
    dl = int(input("Enter a deadline(ex. 5days = 432000): "))
    
    transactionHash = contract.transact({"from": account}).enterDeadline(dl)
    
def numSubmit(contract):
    print("**Requirement: After deadline** \n")
    account = web3.eth.accounts[0]
    num = int(input("What is the winning number?: "))
    revealDeadline = int(input("When is the deadline for choice revealing(ex. 5days = 432000): "))

    transactionHash = contract.transact({"from": account}).numberSubmission(num, revealDeadline)

def checkForWinner(contract):
    print("**Requirement: After reveal deadline** \n")
    print("The system will now find a winner")
    account = web3.eth.accounts[0]

    transactionHash = contract.transact({"from": account}).checkWinner()

def checkBalance(contract):
    for acc in web3.eth.accounts:
        balance = web3.eth.getBalance (acc)
        print ("{:s} has {:.020f} ETH".format (acc, float (web3.fromWei (balance, "ether"))))
    
    
print("Owner options: ")
print("1.) Enter a deadline. Type '1'")
print("2.) Enter a winning number and reveal deadline. (Valid only after deadline) Type '2'")
print("3.) Run the system to check for winner. (Valid only after reveal deadline) Type '3'")
print("4.) Check balance of accounts. Type '4'")

choice = 0

while(choice < 1 or choice > 4):
    choice = int(input("Please choose a valid option: "))

if(choice == 1):
    deadline(contract)
elif(choice == 2):
    numSubmit(contract)
elif(choice == 3):
    checkForWinner(contract)
elif(choice == 4):
    checkBalance(contract)
