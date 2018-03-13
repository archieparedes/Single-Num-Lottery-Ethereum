/*
Created on Mar WED 07 15:30:12 2018
@author: Archie Paredes
Single Number Lottery
*/

pragma solidity ^0.4.0;

contract LOTTERY{
    address public owner; // host
    
    // PLAYER DATA STORAGE
    uint public numberOfPlayers = 0; 
    address[4] public played; // stores address of players
    uint256[4] plays; // this will log all the guess
    bytes32[4] security; // sha256 security 
    int[4] reveal; // every player starts with 0. if revealed, their value will turn to 1
    
    // WIN INFORMATION
    uint256 public winningNum; // The winning number
    uint public numberOfWinner = 0; // amount of winners
    int[4] setWinner; // every player starts with 0. if they're a winner, value changes to 1.
    int winClaim = 0; 
    
    // DEADLINE INFORMATION
    uint public deadline;
    uint public revealDeadline; // after deadline
    
    event Played(address player);

    function LOTTERY() public{
        owner = msg.sender;
    }
      
    function enterDeadline(uint256 deadlineDays) external {
        require(msg.sender == owner);
        deadline = now + deadlineDays;
    }

    function play(uint256 guess, uint256 securityNum) external payable{ //play with commit
        require(msg.value == 0.01 ether);
        require(now <= deadline); // comment out if testing
        plays[numberOfPlayers] = guess;
        security[numberOfPlayers] = testUint256(securityNum);
        addPlayer(msg.sender);
    }
    
    function testUint256(uint256 securityNum) public pure returns(bytes32){
        return sha256(securityNum);
    }
    
    function addPlayer(address player) private{ // adds players
        for(uint i = 0; i < numberOfPlayers; i++){
            require(player != played[i]);
        }
        assert(played[numberOfPlayers] == 0);
        played[numberOfPlayers] = player; // stores address of player
        reveal[numberOfPlayers] = 0; // 0 means they have not revealed their choice
        setWinner[numberOfPlayers] = 0; //0 means they have not won yet
        numberOfPlayers++; // next player slot
        Played(player);
    }

    function numberSubmission (uint256 num, uint256 revDeadlineDays) external{ // Owner submits winning number and a reveal deadline
        require(now > deadline); // comment out if testing
        require(msg.sender == owner); // owner only
        revealDeadline = now + revDeadlineDays; // sets deadline for players
        winningNum = num; // winning number setter
    }

    function revealChoice() external{ 
        require(msg.sender != owner);
        require(now < revealDeadline); // comment out if testing
        for(uint i = 0; i < numberOfPlayers; i++){
            if(msg.sender == played[i]){
                reveal[i] = 1; // if 1, they have revealed their choice
            }
        }
    }
    
    function checkWinner() external{ // owner will activate this to reveal winners
        require(now >= revealDeadline); // check winner after reveal deadline only // comment out if testing
        require(msg.sender == owner); // only owner can modify
        for(uint i = 0; i < numberOfPlayers; i++){
            if(plays[i] == winningNum && reveal[i] == 1){ // they have to reveal their number before the deadline and have their number equal to winning number
               numberOfWinner++;
               setWinner[i] = 1; // if 1, then the player is a winner;
            }
        } 
    }
    
    function winCollect(uint256 securityNum) external{
        require(now >= revealDeadline); // timeline has to be passed the reveal deadline // comment out if testing
        for(uint i = 0; i< numberOfPlayers; i++){
            if(msg.sender == played[i]){ // makes sure the system is looking at the correct index
                require(setWinner[i] == 1); // 1 means they have won, which is a requirement
                require(testUint256(securityNum) == security[i]);// security info has to be the same as the information stored. required number
                played[i].send ((this.balance) / numberOfWinner); // send ether to winner
                winClaim++; // this increases if a player claimed their prize properly
            }
        }
        if(winClaim == int(numberOfWinner)){
            selfdestruct(owner); // if all prizes collected, end lottery
        }
    }
}