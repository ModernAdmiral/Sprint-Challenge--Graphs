from room import Room
from player import Player
from world import World
from util import Stack, Queue
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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# vertices = {
#     0: [(3, 5), {'n': 1}],
#     1: [(3, 6), {'s': 0, 'n': 2}],
#     2: [(3, 7), {'s': 1}]
# }

# Use DFT to traverse the entirety of the graph and store it as array of id's
# Convert those to directions.
# Backtracking will be involved. Use BFS for that

# traversal_path = []


# def create_rooms_list(player):

# use dft to traverse the graph:
ss = Stack()
ss.push(player.current_room)
visited = []

while ss.size() > 0:
    current = ss.pop()
    if current.id not in visited:
        visited.append(current.id)
        directions = current.get_exits()
        for direction in directions:
            ss.push(current.get_room_in_direction(direction))
print('visited', visited)


def get_shortest_path(start, end):
    # return list of shortest path id's from start to end using BFS
    qq = Queue()
    qq.enqueue([start])
    visited = set()

    while qq.size() > 0:
        path = qq.dequeue()
        if path[-1] not in visited:
            # mark room as visited
            visited.add(path[-1])
            if path[-1] == end:
                return path
            else:
                # find exits and find neig
                exits = world.rooms[path[-1]].get_exits()
                for direction in exits:
                    # add the neighbor to the queue
                    neighbor = world.rooms[path[-1]
                                           ].get_room_in_direction(direction)
                    print("unpack path? ", *path, "neigbor.id", neighbor.id)
                    qq.enqueue([*path, neighbor.id])


print("test shortest path", get_shortest_path(
    player.current_room.id, visited[1]))


# CONVERT VISITED ARRAY TO DIRECTIONS
final_list = []


for i in range(len(visited) - 1):
    # check if the next room is a neighbor, if it is, return which direction its in
    print('destination_id', visited[i+1])
    direction = player.current_room.is_neighbor(visited[i+1])
    print('direction', direction)
    # if it is a neihgbor, append which direction its in to final list and travel there
    if direction:
        player.travel(direction)
        final_list.append(direction)
    # if not a neighbor, backtrack
    else:
        # BACKTRACK
        # get the shortest path starting at the current room and ending at the destination_id
        backtrack = get_shortest_path(player.current_room.id, visited[i+1])
        print("backtrack", backtrack)
        print("backtrack except the first value", backtrack[1:])
        for room_id in backtrack[1:]:
            direction = player.current_room.is_neighbor(room_id)
            print("backtrack direction", direction)
            player.travel(direction)
            final_list.append(direction)

    # Driver Code


# traversal_path = convert_ids_to_directions(visited, player)
traversal_path = final_list

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
