#Benjamin Roark
#The lone survivor



import random
# Define color class
class TextColor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Reset to default color


# print a main menu and the commands
print(TextColor.MAGENTA + "The Lone Survivor: A Zombie Text Based Game")
print(TextColor.MAGENTA + "In a post apocalyptic New York, there is one survivor left who must face the challenges of establishing\na home within the destroyed city. Will you survive or Will you sub come to the Walkers?\n")
print(TextColor.MAGENTA + "To Win collect all 12 Items and get to the safe zone Queens")
print(TextColor.MAGENTA + "Move commands: go South, go North, go East, go West")
print(TextColor.MAGENTA + "To pick up items use: yes or no")



# Initialize the map
rooms = {
    'Times Square': {'North': 'Central Park', 'East': 'Broadway', 'South': 'Fifth Avenue'},
    'Central Park': {'South': 'Times Square'},
    'Broadway': {'West': 'Times Square', 'East': 'Wall Street'},
    'Wall Street': {'West': 'Broadway', 'North': 'Statue of Liberty'},
    'Statue of Liberty': {'South': 'Wall Street', 'East': 'East Village'},
    'East Village': {'West': 'Statue of Liberty', 'North': 'SoHo'},
    'SoHo': {'South': 'East Village', 'East': 'Little Italy'},
    'Little Italy': {'West': 'SoHo', 'North': 'Chinatown'},
    'Chinatown': {'South': 'Little Italy', 'East': 'Brooklyn Bridge'},
    'Brooklyn Bridge': {'West': 'Chinatown', 'North': 'Williamsburg'},
    'Williamsburg': {'South': 'Brooklyn Bridge', 'East': 'Queens'},
    'Queens': {'West': 'Williamsburg', 'South': 'Fifth Avenue'},
    'Fifth Avenue': {'North': 'Times Square', 'South': 'Central Park'},
}

# Define the room items (same block concept applies)
room_items = {
    'Times Square': [],
    'Central Park': ["Dirty Water", "Jeans"],
    'Broadway': ["Colt 1911"],
    'Wall Street': [],
    'Statue of Liberty': ["Heavy Jacket", "Clean Water"],
    'East Village': ["Glock", "Fruit"],
    'SoHo': ["Boxed Goods"],
    'Little Italy': ["Remington 870", "Cargo Pants"],
    'Chinatown': [],
    'Brooklyn Bridge': ["Sandwich", "Rifle"],
    'Williamsburg': [],
    'Queens': []
}

# Collect all available items in the game to check for win condition
all_items_in_game = [item for sublist in room_items.values() for item in sublist]

# Initialize player variables
player_inventory = []
current_room = 'Times Square'
player_health = 100


# Function to check for walkers
def check_for_walkers():
    chance_of_walkers = random.randint(0, 100)
    if chance_of_walkers > 60:
        print("You encounter walkers!")
        combat_walkers()
    else:
        print("The area seems clear of walkers.")


# Function to collect items in the room with user input
def collect_items(room):
    global room_items
    # Check if the room exists in room_items before accessing
    if room in room_items:
        if room_items[room]:
            print(f"You find the following items: {room_items[room]}")
            # Prompt player to choose if they want to pick up items
            pick_up = input("Do you want to pick up these items? (yes/no): ").strip().lower()
            if pick_up == 'yes':
                player_inventory.extend(room_items[room])
                room_items[room] = []  # Remove items once collected
                print("Items added to your inventory.")
            else:
                print("You chose not to pick up the items.")
        else:
            print("No items left in this room.")
    else:
        print("This room has no items or does not exist in the item list.")


# Function to combat walkers
def combat_walkers():
    global player_health
    gun_break_chance = 10  # 10% chance for a gun to break

    # Check if the player has any guns
    if any(item in player_inventory for item in ["Glock", "Colt 1911", "Rifle", "Remington 870"]):
        # Check for a functional gun
        functional_guns = [gun for gun in ["Glock", "Colt 1911", "Rifle", "Remington 870"] if gun in player_inventory]

        if functional_guns:
            # Simulate combat
            print("You successfully fight off the walkers.")

            # Check if the gun breaks
            if random.randint(1, 100) <= gun_break_chance:
                broken_gun = random.choice(functional_guns)  # Choose a random gun to break
                player_inventory.remove(broken_gun)  # Remove the broken gun from inventory
                print(f"Your {broken_gun} broke during the fight!")
            else:
                print("You used your gun to defeat the walkers.")
        else:
            # If all guns are broken, take damage
            print("All your guns are broken! You cannot fight off the walkers!")
            player_health -= 30
            print(f"You are injured. Current health: {player_health}")
            if player_health <= 0:
                print("You have been killed by the walkers.")
                exit()  # End the game if health reaches zero
    else:
        player_health -= 30
        print(f"You are injured. Current health: {player_health}")
        if player_health <= 0:
            print("You have been killed by the walkers.")
            exit()  # End the game if health reaches zero


# Function to move between rooms
def move_to_room(direction):
    global current_room
    if direction in rooms[current_room]:
        current_room = rooms[current_room][direction]
        print(f"\nYou have moved to {current_room}.")
        check_for_walkers()
        collect_items(current_room)
    else:
        print(TextColor.RED + "You can't go that way!")


# Function to check if all items have been collected
def all_items_collected():
    return set(player_inventory) == set(all_items_in_game)


# Main game loop
def game_loop():
    global player_health, current_room
    while player_health > 0:
        print(TextColor.RESET + f"\nYou are in {current_room}.")

        # Display possible directions to move
        if current_room in rooms:
            directions = ', '.join(rooms[current_room].keys())
            print(TextColor.GREEN + f"You can move: {directions}")

        # Check if the player has collected all items
        if all_items_collected():
            print("Congratulations! You have collected all items. You win!")
            break
        else:
            print(TextColor.RESET + f"You have collected {len(player_inventory)}/{len(all_items_in_game)} items. Keep searching!")

        # Prompt the player for a command
        command = input(TextColor.RESET + "Enter a direction to move (North, South, East, West) or 'exit' to quit: ").strip().capitalize()

        # Handle player command
        if command in ['North', 'South', 'East', 'West']:
            move_to_room(command)
        elif command == 'Exit':
            print("Stopping the game. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

    if player_health <= 0:
        print("Game Over")


# Start the game loop
game_loop()

input(TextColor.YELLOW + "Press Enter to close the Game")