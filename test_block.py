import time
import random
from transaction import Transaction
from block import Block
from key import BitcoinAccount

random.seed()
wallet = BitcoinAccount()
condition=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

difficulty = 2

first_block = Block("Block1", "Premier bloc", 0, "")

tx = Transaction(50, "mohamed", "justine", time.time())

first_block.addTransaction(tx)
first_block.mine(random.randrange(5),random.choice(condition))

print("First block is: ")

print(first_block)

last_hash = first_block.hash

second_block = Block("Block2", "Deuxieme bloc", 1, first_block.hash)

second_block.mine(random.randrange(5), random.choice(condition))

print("Second block is: ")

print(second_block)
print(second_block.verifyHash(second_block.nonce))
