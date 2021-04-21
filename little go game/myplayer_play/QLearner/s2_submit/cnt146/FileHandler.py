import pickle


def read_input(n, path="input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()
        piece_type = int(lines[0])

        previous_board = []
        board = []
        for line in lines[1:n + 1]:
            line_list = []
            for x in line.rstrip("\n"):
                line_list.append(int(x))
            previous_board.append(line_list)

        for line in lines[n + 1:2 * n + 1]:
            line_list = []
            for x in line.rstrip("\n"):
                line_list.append(int(x))
            board.append(line_list)

        return piece_type, previous_board, board


def write_output(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def read_q_table(path="QTable.pkl"):
    pkl_file = open(path, 'rb')
    mydict = pickle.load(pkl_file)
    pkl_file.close()
    return mydict


def write_q_table(table, path="QTable.pkl"):
    output = open(path, 'wb')
    pickle.dump(table, output)
    output.close()
