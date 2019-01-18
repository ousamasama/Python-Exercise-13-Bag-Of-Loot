import sqlite3
import sys

lootbag_db = '/Users/sama/workspace/python-exercise-13/lootbag.db'

def getChildren():
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()

        for row in cursor.execute('SELECT * FROM Children'):
            print(row)

def getChild(child):
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()

        cursor.execute(f'''SELECT Name, ChildId
                           FROM Children
                           WHERE Name = '{child}'
                        ''')

    child = cursor.fetchone()
    print(child)
    return child

# 1.
# Add a toy to the bag o' loot, and label it with the child's name who will receive it. 
# The first argument must be the word add. 
# The second argument is the gift to be delivered. 
# The third argument is the name of the child.

def addToy(toy):
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()
        child_name = toy["child"]
        try:
            cursor.execute(
               f'''
                INSERT INTO TOYS
                SELECT ?, ?, Children.ChildId
                FROM Children
                WHERE Children.Name = "{child_name}"
                ''', (None, toy["name"])
            )
        except sqlite3.OperationalError as err:
            print("This is the add error", err)

        first_val = list(toy.values())[0]
        second_val = list(toy.values())[1]
        print(f'{second_val} was given a {first_val}.')
# 2.
# Remove a toy from the bag o' loot in case a child's status changes before delivery starts.
def removeToy(toy):
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()
        child_name = toy["child"]
        try:
            cursor.execute(
               f'''
                DELETE FROM TOYS
                WHERE TOYS.ChildId in ( select Children.ChildId from Children WHERE Children.Name = "{child_name}")
                AND Toys.Name = "{toy["name"]}"
                '''
            )
        except sqlite3.OperationalError as err:
            print("This is the remove error", err)

        first_val = list(toy.values())[0]
        second_val = list(toy.values())[1]
        print(f'{second_val} were taken from {first_val}.')
#3.
# Produce a list of children currently receiving presents.
list_of_receiving_children = list()
def getReceivingChildren():
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()

        for row in cursor.execute(f'SELECT * FROM Children WHERE Delivered = "{1}"'):
            list_of_receiving_children.append(row[1])

# 4.
# List toys in the bag o' loot for a specific child.
list_of_received_toys = list()
def getChildsToys(child):
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()

        # can add Children.Name to SELECT to pull name
        cursor.execute(f'''SELECT Toys.Name
                           FROM Toys
                           JOIN Children ON Children.ChildId = Toys.ChildId
                           WHERE Children.Name = '{child}'
                        ''')
    
    child = cursor.fetchall()

    if not child:
        print("This child received no presents.")
    else:
        for i in child:
            list_of_received_toys.append(i[0])

    return child

# 5.
# Specify when a child's toys have been delivered.

def getDeliveredStatus(child):
    with sqlite3.connect(lootbag_db) as conn:
        cursor = conn.cursor()

        cursor.execute(f'''SELECT Children.Name, Children.Delivered
                           FROM Children
                           WHERE Children.Name = '{child}'
                        ''')

    child = cursor.fetchone()
    if child[1] == 1:
        print(child)
        print(f"Presents have been already been delivered to {child[0]}.")
    else:
        print(child)
        print(f"Presents have not been delivered to {child[0]}.")
    return child

if __name__ == "__main__":
    # getChildren()
    #
    # getChild("Olive")
    # 1.
        if sys.argv[1] == "add":
            addToy({
                "name": sys.argv[2],
                "child": sys.argv[3]
            })
    # addToy({
    #     "name": "Pair of Dirty Socks",
    #     "child": "Olive"
    #     })
    # Output: Olive was given a Dirty Socks.
    # 2.
        if sys.argv[1] == "remove":
             removeToy({
                "child": sys.argv[2],
                "name": sys.argv[3]
                })
    # removeToy({
    #     "child": "Olive",
    #     "name": "Pair of Dirty Socks"
    # })
    # Output: Socks were taken from Olive.
    # 3.
        # if sys.argv[1] == "ls":
        #     getReceivingChildren()
        #     clean_list_of_receiving_children = ' and '.join(list_of_receiving_children)
        #     print(f'{clean_list_of_receiving_children} are receiving gifts.')
    # getReceivingChildren()
    # clean_list_of_receiving_children = ' and '.join(list_of_receiving_children)
    # print(f'{clean_list_of_receiving_children} are receiving gifts.')
    # Output: Kiwi and Olive are receiving gifts.
    # 4.
        # if sys.argv[1] == "ls" and sys.argv[2]:
        #     getChildsToys(sys.argv[2])
        #     print(f"This child received " + ' and '.join(list_of_received_toys) + ".")
        # not working as intended
        # elif sys.argv[1] == "ls":
        #     getReceivingChildren()
        #     clean_list_of_receiving_children = ' and '.join(list_of_receiving_children)
        #     print(f'{clean_list_of_receiving_children} are receiving gifts.')
    # getChildsToys("Kiwi")
    # print(f"This child received " + ' and '.join(list_of_received_toys) + ".")
    # Output: This child received Leftover Pizza and Fluffy Bone.
    # getChildsToys("Marcy")
    # Output: This child received no presents.
    # 5.
        if sys.argv[1] == "delivered":
            getDeliveredStatus(sys.argv[2])
    # getDeliveredStatus("Olive")
    # Output: Presents have been already been delivered to Olive.
    # getDeliveredStatus("Marcy")
    # Output: Presents have not been delivered to Marcy.
        