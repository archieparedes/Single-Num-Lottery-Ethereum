Created on Mar TUE 07 15:33:41 2018
@author: Archie Paredes
Single Number Lottery README

Programming Languages Used:
	- Python3
	- Solidity

Software Used:
	- Python3 IDE
	- remix.ethereum.org online Solidity IDE

Description: Lottery is a game where a player guess a few numbers, and if their numbers are drawn, they win some money. This project, however, 
	is somewhat similar to the game, but instead, a single number is played and the owner picks the number. In addition, instead of
	using real currency, this uses ethereum. Since this is just a test, we will be using fake ethereum address consisting of 5 users, and
	starting each users off with 100 ether.

How it works: Basically, each player is assigned to their own index. Index 0 is player 1, index 2 is player 3, and etc... 
    After a player plays their choice, they only have to memorize their random number. Their random number is tested in testUint256 
    and stored in a bytes32 array called security. Afterwards, they have to reveal choice to the system once the deadline has passed. 
    They start off with 0, meaning they haven't revealed their choice. Once reveal() is activated, their value turns to 1 in the reveal array.
    If the player reveals and wins, they have to re-enter their random number to be tested again in testUint256. If it matches the
    first test, they can properly claim their prize if they have won. They will be set as a winner (1) in setWinner array and numberOfWinners
    will go up by 1 for each winner found. Multiple winners can be chosen to which the balance is split evenly amoung the winners. 
    At the end, the lottery is done once all winners claim their prize.

***********************************************************************************************************************************************
OWNER LIMIT: 1
PLAYER LIMIT: 4
Recommendations before running:
	- Use Ubuntu Windows Subsystem, or linuxOS
	- Use Google Chrome
	- If you want to test instantly without waiting on deadlines comment out the deadline requirements in lotterGame.sol


How to run :
	1.) have one terminal run testrpc: type 'testrpc --port 9545 --accounts 5 --seed foobar'
	2.) Upload lotterGame.sol to remix.ethereum.org
	3.) Click on the Run tab
		a.) Set environment to Web3 Provider
			I.) set Web3 Provider Endpoint to http://localhost:9545
	4.) Choose the first account
	5.) Click Create


Afterwards:
	As an Owner/Host steps:
		1.) On a seperate terminal, direct to the main lottery folder
		2.) type: python3 lotteryOwner.py
		3.) Choose a valid option

	As a Player steps:
		1.) On a seperate terminal, direct to the main lottery folder
		2.) type: python3 lotteryPlayer.py
		3.) Choose a valid option


