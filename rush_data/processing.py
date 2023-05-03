# database rush.txt found at https://www.michaelfogleman.com/static/rush/rush.txt

# Save all boards without walls ('x') to a new file
# Additionally, split into difficulty categories
with open("rush.txt", 'r') as source, \
        open("no_walls_full.txt", 'w') as no_walls_full, \
        open("no_walls.txt", 'w') as no_walls, \
        open("no_walls_basic.txt", 'w') as no_walls_basic, \
        open("no_walls_easy.txt", 'w') as no_walls_easy, \
        open("no_walls_medium.txt", 'w') as no_walls_medium, \
        open("no_walls_hard.txt", 'w') as no_walls_hard, \
        open("no_walls_hard.txt", 'w') as no_walls_expert:
    num_boards = num_expert = num_hard = num_medium = num_easy = num_basic = 0
    for i, line in enumerate(source):
        num_moves, board_string, graph_size = line.split(" ")
        num_moves = int(num_moves)
        if num_moves < 10:
            break  # can stop looping since list is sorted in decreasing order
        # If the graph is large, solving takes time. Only use boards where solving takes less than around 5 seconds.
        if "x" not in board_string and int(graph_size) <= 20000:
            no_walls_full.write(str(num_boards) + "," + line.replace(" ", ","))  # format for csv
            no_walls.write(board_string + "\n")
            num_boards += 1
            # Split into difficulties
            if num_moves <= 15:
                num_basic += 1
                no_walls_basic.write(board_string + "\n")
            elif num_moves <= 20:
                num_easy += 1
                no_walls_easy.write(board_string + "\n")
            elif num_moves <= 25:
                num_medium += 1
                no_walls_medium.write(board_string + "\n")
            elif num_moves <= 30:
                num_hard += 1
                no_walls_hard.write(board_string + "\n")
            else:
                num_expert += 1
                no_walls_expert.write(board_string + "\n")

# I found: 357426, 273040, 61768, 17238, 4043, 1336 without filtering graph size
# And:  when graph size is at most 20000
print(num_boards, num_basic, num_easy, num_medium, num_hard, num_expert)
# I also found largest_graph = 541934
