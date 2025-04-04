files = ['a','b','c','d','e','f','g','h']  # 가로(col)
ranks = ['8','7','6','5','4','3','2','1']  # 세로(row)

board = [
    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
    ['a2', 'b2', 'c2' ,'d2', 'e2', 'f2', 'g2', 'h2'],
    ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
]

def square_to_rc(square: str) -> tuple:
    """ 예: 'a2' -> (6, 0) """
    file = square[0]  # 'a' ~ 'h'
    rank = square[1]  # '1' ~ '8'
    col = files.index(file)
    row = ranks.index(rank)
    return row, col

def rc_to_square(row: int, col: int) -> str:
    """ 예: (6, 0) -> 'a2' """
    return files[col] + ranks[row]

turn = "white"
turn_count = 1

def turn_change(x):
    global turn
    global turn_count
    if x == 'white':
        turn = "black"
        return turn
    if x == "black":
        turn = "white"
        turn_count += 1
        return turn, turn_count



class piece:
    def __init__(self, role, color, pos):
        self.role = role
        self.color = color
        self.pos = pos
        self.active = True
        self.enpassant = False
        self.two_move_turn = None

def move(square):
    global turn
    global turn_count
    if turn == "white":
        if square[0] == "N":
            if square == night_move(white_night1):
                white_night1.pos = square
                turn = turn_change(turn)
            elif square == night_move(white_night2):
                white_night2.pos = square
                turn = turn_change(turn)
        elif square[0] == "B":
            if square == night_move(white_bishop1):
                white_bishop1.pos = square
                turn = turn_change(turn)
            elif square == night_move(white_bishop2):
                white_bishop2.pos = square
                turn = turn_change(turn)
        elif square[0] == "R":
            if square == night_move(white_rook1):
                white_rook1.pos = square
                turn = turn_change(turn)
            elif square == night_move(white_rook2):
                white_rook2.pos = square
                turn = turn_change(turn)
        elif square[0] == "Q":
            if square == night_move(white_queen):
                white_rook1.pos = square
                turn = turn_change(turn)
        else:
            if square == white_pawn_move(white_pawn1)[0]:
                white_pawn1.pos = square
                promotion(white_pawn1, square)
                if white_pawn_move(white_pawn1)[1] == True:
                    white_pawn1.enpassant = True
                    white_pawn1.two_move_turn = white_pawn_move(white_pawn1)[2]
            elif square == white_pawn_move(white_pawn2)[0]:
                white_pawn2.pos = square
                promotion(white_pawn2, square)
                if white_pawn_move(white_pawn2)[1] == True:
                    white_pawn2.enpassant = True
                    white_pawn2.two_move_turn = white_pawn_move(white_pawn2)[2]
            elif square == white_pawn_move(white_pawn3)[0]:
                white_pawn3.pos = square
                promotion(white_pawn3, square)
                if white_pawn_move(white_pawn3)[1] == True:
                    white_pawn3.enpassant = True
                    white_pawn3.two_move_turn = white_pawn_move(white_pawn3)[2]
            elif square == white_pawn_move(white_pawn4)[0]:
                white_pawn4.pos = square
                promotion(white_pawn4, square)
                if white_pawn_move(white_pawn4)[1] == True:
                    white_pawn4.enpassant = True
                    white_pawn4.two_move_turn = white_pawn_move(white_pawn4)[2]
            elif square == white_pawn_move(white_pawn5)[0]:
                white_pawn5.pos = square
                promotion(white_pawn5, square)
                if white_pawn_move(white_pawn5)[1] == True:
                    white_pawn5.enpassant = True
                    white_pawn5.two_move_turn = white_pawn_move(white_pawn5)[2]
            elif square == white_pawn_move(white_pawn6)[0]:
                white_pawn6.pos = square
                promotion(white_pawn6, square)
                if white_pawn_move(white_pawn6)[1] == True:
                    white_pawn6.enpassant = True
                    white_pawn6.two_move_turn = white_pawn_move(white_pawn6)[2]
            elif square == white_pawn_move(white_pawn7)[0]:
                white_pawn7.pos = square
                promotion(white_pawn7, square)
                if white_pawn_move(white_pawn7)[1] == True:
                    white_pawn7.enpassant = True
                    white_pawn7.two_move_turn = white_pawn_move(white_pawn7)[2]
            elif square == white_pawn_move(white_pawn8)[0]:
                white_pawn8.pos = square
                promotion(white_pawn8, square)
                if white_pawn_move(white_pawn8)[1] == True:
                    white_pawn8.enpassant = True
                    white_pawn8.two_move_turn = white_pawn_move(white_pawn8)[2]

    elif turn == "black":
        if square[0] == "N":
            if square == night_move(black_night1):
                black_night1.pos = square
                turn, turn_count = turn_change(turn)
            elif square == night_move(black_night2):
                black_night2.pos = square
                turn, turn_count = turn_change(turn)
        elif square[0] == "B":
            if square == night_move(black_bishop1):
                black_bishop1.pos = square
                turn, turn_count = turn_change(turn)
            elif square == night_move(black_bishop2):
                black_bishop2.pos = square
                turn, turn_count = turn_change(turn)
        elif square[0] == "R":
            if square == night_move(black_rook1):
                black_rook1.pos = square
                turn, turn_count = turn_change(turn)
            elif square == night_move(black_rook2):
                black_rook2.pos = square
                turn, turn_count = turn_change(turn)
        elif square[0] == "Q":
            if square == night_move(black_queen):
                black_rook1.pos = square
                turn, turn_count = turn_change(turn)
        else:
            if square == black_pawn_move(black_pawn1)[0]:
                black_pawn1.pos = square
                promotion(black_pawn1, square)
                if black_pawn_move(black_pawn1)[1] == True:
                    black_pawn1.enpassant = True
                    black_pawn1.two_move_turn = black_pawn_move(black_pawn1)[2]
            elif square == black_pawn_move(black_pawn2)[0]:
                black_pawn2.pos = square
                promotion(black_pawn2, square)
                if black_pawn_move(black_pawn2)[1] == True:
                    black_pawn2.enpassant = True
                    black_pawn2.two_move_turn = black_pawn_move(black_pawn2)[2]
            elif square == black_pawn_move(black_pawn3)[0]:
                black_pawn3.pos = square
                promotion(black_pawn3, square)
                if black_pawn_move(black_pawn3)[1] == True:
                    black_pawn3.enpassant = True
                    black_pawn3.two_move_turn = black_pawn_move(black_pawn3)[2]
            elif square == black_pawn_move(black_pawn4)[0]:
                black_pawn4.pos = square
                promotion(black_pawn4, square)
                if black_pawn_move(black_pawn4)[1] == True:
                    black_pawn4.enpassant = True
                    black_pawn4.two_move_turn = black_pawn_move(black_pawn4)[2]
            elif square == black_pawn_move(black_pawn5)[0]:
                black_pawn5.pos = square
                promotion(black_pawn5, square)
                if black_pawn_move(black_pawn5)[1] == True:
                    black_pawn5.enpassant = True
                    black_pawn5.two_move_turn = black_pawn_move(black_pawn5)[2]
            elif square == black_pawn_move(black_pawn6)[0]:
                black_pawn6.pos = square
                promotion(black_pawn6, square)
                if black_pawn_move(black_pawn6)[1] == True:
                    black_pawn6.enpassant = True
                    black_pawn6.two_move_turn = black_pawn_move(black_pawn6)[2]
            elif square == black_pawn_move(black_pawn7)[0]:
                black_pawn7.pos = square
                promotion(black_pawn7, square)
                if black_pawn_move(black_pawn7)[1] == True:
                    black_pawn7.enpassant = True
                    black_pawn7.two_move_turn = black_pawn_move(black_pawn7)[2]
            elif square == black_pawn_move(black_pawn8)[0]:
                black_pawn8.pos = square
                promotion(black_pawn8, square)
                if black_pawn_move(black_pawn8)[1] == True:
                    black_pawn8.enpassant = True
                    black_pawn8.two_move_turn = black_pawn_move(black_pawn8)[2]

def white_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    temp_row = row + 1
    two_move = False
    global turn_count
    if 0 <= temp_row <= 8:
        if square_check(rc_to_square(temp_row, col)):
            possible_moves.append(rc_to_square(temp_row, col))
        if row == 5 and 0 <= col + 1 <= 8:
            temp_square = rc_to_square(row, col + 1)
            for p in pieces_list:
                if p.pos == temp_square:
                    if p.role == "pawn":
                        if p.enpassant == True and p.two_move_turn == turn_count:
                            possible_moves.append(temp_square)
        if square_check(rc_to_square(temp_row, col)):
            if row == 5 and 0 <= col - 1 <= 8:
                temp_square = rc_to_square(row, col - 1)
                for p in pieces_list:
                    if p.pos == temp_square:
                        if p.role == "pawn":
                            if p.enpassant == True and p.two_move_turn == turn_count:
                                possible_moves.append(temp_square)
            if square_check(rc_to_square(temp_row, col)):
                possible_moves.append(rc_to_square(temp_row, col))
        if 0 <= col + 1 <= 8:
            if color_check(temp_row, col + 1):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        if 0 <= col - 1 <= 8:
            if color_check(temp_row, col - 1):
                possible_moves.append(rc_to_square(temp_row, col - 1))
    if row == 2:
        if square_check(rc_to_square(temp_row, col)):
            temp_row += 1
            if square_check(rc_to_square(temp_row, col)):
                possible_moves.append(rc_to_square(temp_row, col))
                two_move = True
                two_move_turn = turn_count
    return possible_moves, two_move, two_move_turn

def black_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    temp_row = row - 1
    global turn_count
    if 0 <= temp_row <= 8:
        if square_check(rc_to_square(temp_row, col)):
            possible_moves.append(rc_to_square(temp_row, col))
        elif row == 4 and 0 <= col + 1 <= 8:
            temp_square = rc_to_square(row, col + 1)
            for p in pieces_list:
                if p.pos == temp_square:
                    if p.role == "pawn":
                        if p.enpassant == True:
                            possible_moves.append(rc_to_square(temp_row, col + 1))
        elif square_check(rc_to_square(temp_row, col)):
            if row == 5 and 0 <= col - 1 <= 8:
                temp_square = rc_to_square(row, col - 1)
                for p in pieces_list:
                    if p.pos == temp_square:
                        if p.role == "pawn":
                            if p.enpassant == True:
                                possible_moves.append(rc_to_square(temp_row, col + 1))
        elif 0 <= col + 1 <= 8:
            if color_check(temp_row, col + 1):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        elif 0 <= col - 1 <= 8:
            if color_check(temp_row, col - 1):
                possible_moves.append(rc_to_square(temp_row, col - 1))
    elif row == 6:
        if square_check(rc_to_square(temp_row, col)):
            temp_row -= 1
            if square_check(rc_to_square(temp_row, col)):
                possible_moves.append(rc_to_square(temp_row, col))
    return possible_moves

def promotion(piece, square):
    row, col = square_to_rc(piece.pos)
    if row == 1 or row == 8:
        promotion_piece = square.find("=") + 2
        if promotion_piece == "N":
            piece.role = "knight"
        if promotion_piece == "B":
            piece.role = "bishop"
        if promotion_piece == "R":
            piece.role = "rook"
        if promotion_piece == "Q":
            piece.role = "queen"

def night_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    if row + 2 <= 8 and col + 1 <= 8:
        if square_check(rc_to_square(row + 2, col + 1)):
            possible_moves.append(rc_to_square(row + 2, col + 1))
    if row + 2 <= 8 and col - 1 <= 8:
        if square_check(rc_to_square(row + 2, col +- 1)):
            possible_moves.append(rc_to_square(row + 2, col - 1))
    if row - 2 <= 8 and col + 1 <= 8:
        if square_check(rc_to_square(row - 2, col + 1)):
            possible_moves.append(rc_to_square(row - 2, col + 1))
    if row - 2 <= 8 and col - 1 <= 8:
        if square_check(rc_to_square(row - 2, col - 1)):
            possible_moves.append(rc_to_square(row - 2, col - 1))
    if row + 1 <= 8 and col + 2 <= 8:
        if square_check(rc_to_square(row + 1, col + 2)):
            possible_moves.append(rc_to_square(row + 1, col + 2))
    if row - 1 <= 8 and col + 2 <= 8:
        if square_check(rc_to_square(row - 1, col + 2)):
            possible_moves.append(rc_to_square(row - 1, col + 2))
    if row + 1 <= 8 and col - 2 <= 8:
        if square_check(rc_to_square(row + 1, col - 2)):
            possible_moves.append(rc_to_square(row + 1, col - 2))
    if row - 1 <= 8 and col - 2 <= 8:
        if square_check(rc_to_square(row - 1, col - 2)):
            possible_moves.append(rc_to_square(row - 1, col - 2))
    return possible_moves

def rook_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col
    positive_row = 8 - row
    possible_moves = []
    for i in range(positive_column):
        if square_check(rc_to_square(row, col + i)):
            possible_moves.append(rc_to_square(row, col + i))
        else:
            break
    for i in range(col):
        if square_check(rc_to_square(row, col - i)):
            possible_moves.append(rc_to_square(row, col - i))
        else:
            break
    for i in range(positive_row):
        if square_check(rc_to_square(row + i, col)):
            possible_moves.append(rc_to_square(row + i, col))
        else:
            break
    for i in range(row):
        if square_check(rc_to_square(row - i, col)):
            possible_moves.append(rc_to_square(row - i, col))
        else:
            break
    return possible_moves

def bishop_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col
    possible_moves = []
    for i in range(positive_column):
        if square_check(rc_to_square(row + i, col + i)):
            possible_moves.append(rc_to_square(row + i, col + i))
        else:
            break
    for i in range(col):
        if square_check(rc_to_square(row - i, col - i)):
            possible_moves.append(rc_to_square(row - i, col - i))
        else:
            break
    return possible_moves

def queen_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col
    positive_row = 8 - row
    possible_moves = []
    for i in range(positive_column):
        if square_check(rc_to_square(row, col + i)):
            possible_moves.append(rc_to_square(row, col + i))
        else:
            break
    for i in range(col):
        if square_check(rc_to_square(row, col - i)):
            possible_moves.append(rc_to_square(row, col - i))
        else:
            break
    for i in range(positive_row):
        if square_check(rc_to_square(row + i, col)):
            possible_moves.append(rc_to_square(row + i, col))
        else:
            break
    for i in range(row):
        if square_check(rc_to_square(row - i, col)):
            possible_moves.append(rc_to_square(row - i, col))
        else:
            break
    for i in range(positive_column):
        if square_check(rc_to_square(row + i, col + i)):
            possible_moves.append(rc_to_square(row + i, col + i))
        else:
            break
    for i in range(col):
        if square_check(rc_to_square(row - i, col - i)):
            possible_moves.append(rc_to_square(row - i, col - i))
        else:
            break
    return possible_moves

def king_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []


def square_check(square: str) -> bool:
    for p in pieces_list:
        if p.pos == square:
            return False
    return True

def color_check(square: str, color: str) -> bool:
    for p in pieces_list:
        if p.pos == square and p.color != color:
            p.active = False
            return True
    return  False



white_pawn1 = piece("pawn", "white", "a2")
white_pawn2 = piece("pawn", "white", "b2")
white_pawn3 = piece("pawn", "white", "c2")
white_pawn4 = piece("pawn", "white", "d2")
white_pawn5 = piece("pawn", "white", "e2")
white_pawn6 = piece("pawn", "white", "f2")
white_pawn7 = piece("pawn", "white", "g2")
white_pawn8 = piece("pawn", "white", "h2")

white_night1 = piece("knight", "white", "b1")
white_night2 = piece("knight", "white", "g1")

white_bishop1 = piece("bishop", "white", "b1")
white_bishop2 = piece("bishop", "white", "f1")

white_rook1 = piece("rook", "white", "a1")
white_rook2 = piece("rook", "white", "h1")

white_king = piece("king", "white", "e1")
white_queen = piece("queen", "white", "d1")

black_pawn1 = piece("pawn", "black", "a7")
black_pawn2 = piece("pawn", "black", "b7")
black_pawn3 = piece("pawn", "black", "c7")
black_pawn4 = piece("pawn", "black", "d7")
black_pawn5 = piece("pawn", "black", "e7")
black_pawn6 = piece("pawn", "black", "f7")
black_pawn7 = piece("pawn", "black", "g7")
black_pawn8 = piece("pawn", "black", "h7")

black_night1 = piece("knight", "black", "b8")
black_night2 = piece("knight", "black", "g8")

black_bishop1 = piece("bishop", "black", "b8")
black_bishop2 = piece("bishop", "black", "f8")

black_rook1 = piece("rook", "black", "a8")
black_rook2 = piece("rook", "black", "h8")

black_king = piece("king", "black", "e8")
black_queen = piece("queen", "black", "d8")

pieces_list = [
    white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8, white_night1,
    white_night2, white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen, white_king, black_rook1, black_rook2,
    black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, black_night1,
    black_night2, black_bishop1, black_bishop2, black_queen, black_king
]
