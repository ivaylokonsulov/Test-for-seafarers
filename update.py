from sys import argv, exit
from cs50 import SQL
import csv
import random

db = SQL("sqlite:///tests.db")

# Opening TSV file and writing to database
with open(argv[1], 'r') as csvfile:

    # Create reader to read from
    reader = csv.reader(csvfile, delimiter="\t")

    # Iterating over each row
    for row in reader:
        db.execute("INSERT INTO test3 (question, a, b, c, d, correct) VALUES (?, ?, ?, ?, ?, ?)", row[0], row[1], row[2], row[3], row[4], row[5])

# Test

# Finding the maximum id contained in the database
#maxa = db.execute("SELECT id FROM test1 ORDER BY id DESC LIMIT 0, 1")

# Defining variables
#i = 0
#random_chisla = list()

#while i < 60:

    #chislo = random.randint(1,maxa[0]["id"])

    #if chislo not in random_chisla:
        #random_chisla.append(chislo)
    #else:
        #i -= 1
    #i += 1
#print(random_chisla)
#print(len(random_chisla))
#i = 0

#test = [{} for _ in range(60)]

#while i < 60:
    #test[i] = db.execute("SELECT * FROM test1 WHERE id = ?", random_chisla[i])
    #print(test[i][0])
    #i += 1
#i = 0
#random_chisla.clear()