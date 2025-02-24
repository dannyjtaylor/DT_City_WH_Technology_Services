from random import randrange

def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console.
    print("+-------+-------+-------+")
    print("|       |       |       |")
    print("|", board[0][0], "|", board[0][1], "|", board[0][2], sep="   ", end= "   |\n")
    print("|       |       |       |")
    print("+-------+-------+-------+")
    print("|       |       |       |")
    print("|", board[1][0], "|", board[1][1], "|", board[1][2], sep="   ", end= "   |\n")
    print("|       |       |       |")
    print("+-------+-------+-------+")
    print("|       |       |       |")
    print("|", board[2][0], "|", board[2][1], "|", board[2][2], sep="   ", end= "   |\n")
    print("|       |       |       |")
    print("+-------+-------+-------+")

def enter_move(board):
    # The function accepts the board's current status, asks the user about their move, 
    # checks the input, and updates the board according to the user's decision.
    temp = 1
    move = int(input("Enter your move: "))
    if move not in range(1,10):
        print("Move Invalid")
        return -1
            
    for i in range(0,3):
        print("Entered first loop")
        for j in range(0,3):
            print(board[i][j])
            print("Entered inner loop")
            if temp == move:
                print("TEMP EQ MOVE")
                if board[i][j] == 'O':
                    print("You already moved here")
                    return -1
                elif board[i][j] == 'X':
                    print("Computer already moved here")
                    return -1
                else:
                    board[i][j] = 'O'
                    return -1
            temp += 1

def make_list_of_free_fields(board):
    print("Entered make_list_of_free")
    # The function browses the board and builds a list of all the free squares; 
    # the list consists of tuples, while each tuple is a pair of row and column numbers.
    free_fields = ()
    for i in range(3):
        for j in range(3):
            if type(board[i][j] == int):
                free_fields += (i,j)
                #print(free_fields)

    return free_fields

def victory_for(board, sign):
    # The function analyzes the board's status in order to check if 
    # the player using 'O's or 'X's has won the game
    for i in range(3):
        for j in range(3):
            counter = 0
        if board[i][j] == sign:
            counter += 1
        if counter == 3:
            return True
        
    for k in range(3):
        for l in range(3):
            counter = 0
            if board[l][k] == sign:
                counter += 1
            if counter == 3:
                return True
            
    for m in range(3):
        counter = 0
        if board[m][m] == sign:
            counter += 1
        if counter == 3:
            return True
        
    if board[0][2] == sign and board[1][1] == sign and board [2][0] == sign:
        return True
    
    return False

def draw_move(board):
    print("Entered draw_move")
    # The function draws the computer's move and updates the board.
    while(10):
        r1 = randrange(3)
        #print("r1 gen")
        r2 = randrange(3)
        #print("r2 gen")
        if (r1,r2) in make_list_of_free_fields(board):
            print("ENTERED")
            board[r1][r2] = 'X'
            return

board = [[1,2,3],[4,'X',6],[7,8,9]]

while(not victory_for(board,'O') and not victory_for(board,'X')):
    display_board(board)
    if enter_move(board) == -1:
        print("passed1")
        display_board(board)
        print("\n")
        draw_move(board)
        print("passed2")


    
#print(board)
    