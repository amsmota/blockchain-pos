# Blockchain - Proof Of Stake (training)

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Debug](#debug)
- [APIs](#apis)
- [Transactions](#transactions)
- [Scripts](#scripts)
- [To Be Done](#tbd)


## About <a name = "about"></a>

This project allows you to create and run a full blockchain network on your computer using the Proof of Stake algorithm that you can change or customize and check in realtime the consequences of those changes. 

You can add and remove Nodes at your will, you can check the status of Transactions, Blocks, Stakes and Accounts available in the APIs, and you can easelly create your own APIs. There are also two Python test scripts that allow you to invoke more complex operations.

All the the code is based on the course [Build your own Proof Of Stake Blockchain](https://deloittedevelopment.udemy.com/course/build-your-own-proof-of-stake-blockchain/learn/lecture/23371648) by [Lukas Hubl](https://deloittedevelopment.udemy.com/user/lukas-hubl-2/) on Udemy (kudos to him). However, it was heavelly changed by me, including bug fixes, changed or improved functionalities and some additions.

Please note that the code is not a simple copy of the course code, I actually tried to write my own code in the beggining of each module just by looking at the Agenda, and then comparing my code with the course code. This allowed me to better undertsand not only the code but the logic behind it, even if most of the times my code was wrong and I had to replace it with the course code, albeit some added changes.

## Getting Started <a name = "getting_started"></a>
### Prerequisites

This project is based on **Python3** so a little knowledge of the language is [recommended](https://wiki.python.org/moin/BeginnersGuide/Programmers) but not essencial. It is a simple enough language to understand and allow to change or add the code herein. Please make sure you have [Python3](https://wiki.python.org/moin/BeginnersGuide/Download) installed on your computer and check if [pip](https://pip.pypa.io/en/stable/installation/) is installed with it. If not install both.


### Installing

Once you have **Python3**  and **pip**, clone this repo in you computer. Then change to the directory where it was cloned and install the necessary packages for the project:
```
pip install -r requirements.txt
```

That's it, you are now reay to start the demo/training.

## Usage <a name = "usage"></a>

Once you have finished the instalation process you can simply start creating Blockchain Nodes by opening a command line window and run the following command:

```
python3 Main.py localhost 10000 5000
```
This command invokes the Main module with the paramaters ```host```, ```node port``` and ```api port```. This three parameters are mandatory, but there are a few more optional ones for this command (see below).

You can open as many CLI windows and start ```blockchain nodes``` in it, just make sure you use diferent numbers for both ```node port``` and ```api port```.

Once you do that you will see something like this:
![Screenshot 1](https://user-images.githubusercontent.com/7815917/156602668-0ab75213-6a66-4dd7-bdbe-857b197651fb.png)


Note in the image that we started this node on ports ```10002``` and ```5002```, and that this node connected itself to node ```localhost:10001```. This node is a *special* node, called the ```genesis node```. There are two requirements for this genesis node.

1. it needs to be the first node to start
2. it must use port 10001
2. it is a "well know" node, and for that reason we create it with a specific Private Key
``` 
python3 Main.py localhost 10001 5001 keys/genesisPrivateKey.pem
```
This node will be the first forger in our blockchain (with a stake of 1) so it will be the first to create new ```blocks```.

Here's 4 nodes running at the same time:

![Screenshot 2](https://user-images.githubusercontent.com/7815917/156602780-98cccf3a-8e04-4c2a-bd57-f954eb40c4af.png)

## Debug <a name = "debug"></a>
There are two options for debugging, by passing one of this params as the **last param** in the command

- --debugg=5678
- --debugp=5678

The first one (ending in **g**) will start the node in debug mode and will be listening for debug clients on port 5678.

The second one (ending in **p**) will start the node in debug mode on port 5678 and will **pause** the excuting waitng for a debug client to connect. 

You can use any port you wish on each node, as long as they are diferent in each.

This a example of a "well know" node with a staker PK and debugging on port 5678:
```
python3 Main.py localhost 10003 5003 keys/stakerPrivateKey.pem --debugg=5678
```
For a standard node (one whose PK will be random) it will be just
```
python3 Main.py localhost 10003 5003 --debugg=5678
```
## APIs <a name = "apis"></a>

There are a number of APIs now that are designed to be easelly invoked on the browser

```
- GET /pkey             return the PublicKey of the node
- GET /accounts         return all the Accounts in the network, including the amount of 'money' they have
- GET /stakes           return all the Accounts that are Stakers, and the amount of their stake
- GET /stakes/<amount>  adds the specifies <amount> to the node stake account
- GET /blockchain       return the entire state (Block and Transactions) of the Blockchain
- GET /transactions     return the Transactions currently existing in the TransactionPool
```
One more endpoint exists, this one to be invoked from a script like the HTTPTesting script

```
- POST /transaction     creates a new Transaction in the TransactionPool
```
Here's a example of the Blockchain state with 2 Blocks

![Screenshot 3](https://user-images.githubusercontent.com/7815917/156602884-904a2a53-ea8a-4700-a687-5f0c959b7ebd.png)


## Transactions <a name = "ransactions"></a>

There are 3 types of Transactions tat can be created using the POST /transaction API:

EXCHANGE
TRANSFER
STAKE


## Scripts <a name = "scripts"></a>

There are two scripts at the moment:

- HTTPTesting
- PoSTesting

As it says in the tin, the first is used to test the APIs, at the moment what it does is POST 10 TRANSFER transactions.

The second is to test several scenarios of the Proof Of Stake algorithm.

Please feel free to change both scripts and create new ones as you wish.

## To Be Done <a name = "tbd"></a>

- at the moment a Block is forged per 1 Transaction, create a API to change it at runtime
- review the need for a genesis node
- review the connection of nodes on startup and shutdown
