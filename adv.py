from room import Room
from player import Player
from world import World
import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Setting Variables
curr = player.current_room
rooms = dict()
path = list()
reverse_exits = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
visited = list()

visited.append(curr.id)
path.append(curr.id)
rooms[curr.id] = dict()
for room_exits in curr.get_exits():
    rooms[curr.id][room_exits] = '?'

def choose_path(room_id):
    for exit in rooms[room_id]:
        if rooms[room_id][exit] == '?':
            return exit

    del visited[-1]
    for new_exit, room_num in rooms[visited[-1]].items():
        if room_num == room_id:
            return reverse_exits[new_exit]

while len(rooms) < len(world.rooms):
    move = choose_path(player.current_room.id)
    player.travel(move)
    traversal_path.append(move)

    if player.current_room.id is not visited[-1]:
        visited.append(player.current_room.id)
        path.append(player.current_room.id)
    
    if player.current_room.id not in rooms.keys():
        rooms[player.current_room.id] = dict()
        
        for new_exit in player.current_room.get_exits():
            rooms[player.current_room.id][new_exit] = '?'
    
    if rooms[player.current_room.id][reverse_exits[move]] == '?':
        rooms[visited[-2]][move] = player.current_room.id
        rooms[player.current_room.id][reverse_exits[move]] = visited[-


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
