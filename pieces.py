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
        self.role = role #기물의 역할
        self.color = color #기물의 색
        self.pos = pos #기물의 포지션
        self.active = True #기물 캡쳐 상태 확인
        self.enpassant = False #앙파상 가능 상태를 확인
        self.two_move_turn = None #앙파상 측정용. 움직인 턴을 기록
        self.rook_move_check = False #캐슬링에서 룩의 움직임을 판별
        self.king_move_check = False #캐슬링에서 킹의 움직임 판별

def move(square):
    global turn
    global turn_count
    if turn == "white": #흰색 기물의 실제 움직임 발동
        if square[0] == "N":
            if square == night_move(white_night1):
                white_night1.pos = square
                turn = turn_change(turn)
            elif square == night_move(white_night2):
                white_night2.pos = square
                turn = turn_change(turn)
        elif square[0] == "B":
            if square == bishop_move(white_bishop1):
                white_bishop1.pos = square
                turn = turn_change(turn)
            elif square == bishop_move(white_bishop2):
                white_bishop2.pos = square
                turn = turn_change(turn)
        elif square[0] == "R":
            if square == rook_move(white_rook1):
                white_rook1.pos = square
                white_rook1.rook_move_check = True
                turn = turn_change(turn)
            elif square == rook_move(white_rook2):
                white_rook2.pos = square
                white_rook2.rook_move_check = True
                turn = turn_change(turn)
        elif square[0] == "Q":
            if square == queen_move(white_queen):
                white_queen.pos = square
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
        if square_check(rc_to_square(temp_row, col)):#일반 움직임
            possible_moves.append(rc_to_square(temp_row, col))
        if row == 5 and 0 <= col + 1 <= 8: #우 앙파상 계산
            temp_square = rc_to_square(row, col + 1) #앙파상 할 기물이 있는 칸
            for p in pieces_list:
                if p.pos == temp_square:
                    if p.role == "pawn": #폰이 맞는지 확인
                        if p.enpassant == True and p.two_move_turn == turn_count - 1 and p.color == "white": #다른색의 기물에 턴이 맞는지 파악
                            possible_moves.append(temp_square) #가능한 수에 추가
        if square_check(rc_to_square(temp_row, col)):
            if row == 5 and 0 <= col - 1 <= 8: #좌 앙파상 계산
                temp_square = rc_to_square(row, col - 1)
                for p in pieces_list:
                    if p.pos == temp_square:
                        if p.role == "pawn":
                            if p.enpassant == True and p.two_move_turn == turn_count - 1 and p.color == "black":
                                possible_moves.append(temp_square)
        if 0 <= col + 1 <= 8: #우측 기물 캡쳐
            if color_check(temp_row, col + 1):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        if 0 <= col - 1 <= 8: #좌측 기물 캡쳐
            if color_check(temp_row, col - 1):
                possible_moves.append(rc_to_square(temp_row, col - 1))
        if row == 2: #출발지점 파악
            if square_check(rc_to_square(temp_row, col)): #앞 1칸이 비었는지 확인
                temp_row += 1
                if square_check(rc_to_square(temp_row, col)): # 2번째 칸의 여부 확인
                    possible_moves.append(rc_to_square(temp_row, col)) #가능한 수에 추가
                    two_move = True
                    two_move_turn = turn_count #앙파상 확인용 추가
    return possible_moves, two_move, two_move_turn

def black_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    temp_row = row - 1
    two_move = False
    global turn_count
    if 0 <= temp_row <= 8: #이동이 보드를 넘어선 안 됨
        if square_check(rc_to_square(temp_row, col)): #일반 움직임
            possible_moves.append(rc_to_square(temp_row, col))
        if row == 4 and 0 <= col + 1 <= 8: #우측으로 앙파상
            temp_square = rc_to_square(row, col + 1)
            for p in pieces_list:
                if p.pos == temp_square:
                    if p.role == "pawn":
                        if p.enpassant == True and p.two_move_turn == turn_count and p.color == "white":
                            possible_moves.append(temp_square)
        if square_check(rc_to_square(temp_row, col)):
            if row == 4 and 0 <= col - 1 <= 8: #4랭크에서 열이 범위내에 있는지 식별
                temp_square = rc_to_square(row, col - 1)
                for p in pieces_list:
                    if p.pos == temp_square:
                        if p.role == "pawn":
                            if p.enpassant == True and p.two_move_turn == turn_count and p.color == "white":
                                possible_moves.append(temp_square)
        if 0 <= col + 1 <= 8: #우측 기물 캡쳐
            if color_check(temp_row, col + 1):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        if 0 <= col - 1 <= 8: #좌측 기물 캡쳐
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

def promotion(piece, square):
    row, col = square_to_rc(piece.pos)
    if row == 1 or row == 8: #보드 끝에 도달했는지 파악
        promotion_piece = square.find("=") + 2 #기보 인식
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
        if color_check(rc_to_square(row + 2, col + 1)):
            possible_moves.append(rc_to_square(row + 2, col + 1))
    if row + 2 <= 8 and col - 1 <= 8:
        if color_check(rc_to_square(row + 2, col +- 1)):
            possible_moves.append(rc_to_square(row + 2, col - 1))
    if row - 2 <= 8 and col + 1 <= 8:
        if color_check(rc_to_square(row - 2, col + 1)):
            possible_moves.append(rc_to_square(row - 2, col + 1))
    if row - 2 <= 8 and col - 1 <= 8:
        if color_check(rc_to_square(row - 2, col - 1)):
            possible_moves.append(rc_to_square(row - 2, col - 1))
    if row + 1 <= 8 and col + 2 <= 8:
        if color_check(rc_to_square(row + 1, col + 2)):
            possible_moves.append(rc_to_square(row + 1, col + 2))
    if row - 1 <= 8 and col + 2 <= 8:
        if color_check(rc_to_square(row - 1, col + 2)):
            possible_moves.append(rc_to_square(row - 1, col + 2))
    if row + 1 <= 8 and col - 2 <= 8:
        if color_check(rc_to_square(row + 1, col - 2)):
            possible_moves.append(rc_to_square(row + 1, col - 2))
    if row - 1 <= 8 and col - 2 <= 8:
        if color_check(rc_to_square(row - 1, col - 2)):
            possible_moves.append(rc_to_square(row - 1, col - 2))
    return possible_moves

def rook_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col #우로 남은 칸 계산
    positive_row = 8 - row #위로 남은 칸 계산
    possible_moves = []
    for i in range(positive_column):
        if square_check(rc_to_square(row, col + i)): #막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col + i))
            if square_check(rc_to_square(row, col + i)) == False: #막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col + i)):
                    possible_moves.append(rc_to_square(row, col + i))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(col):
        if square_check(rc_to_square(row, col - i)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col - i))
            if square_check(rc_to_square(row, col + i)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col - i)):
                    possible_moves.append(rc_to_square(row, col - i))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(positive_row):
        if square_check(rc_to_square(row + i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row + i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row + i, col)):
                    possible_moves.append(rc_to_square(row + i, col))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(row):
        if square_check(rc_to_square(row - i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row - i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row - i, col)):
                    possible_moves.append(rc_to_square(row - i, col))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    return possible_moves

def bishop_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col
    possible_moves = []
    for i in range(positive_column): #이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row + i, col + i)): # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col + i))
            if square_check(rc_to_square(row + i, col + i)) == False:
                if color_check(row + i, col + i):
                    possible_moves.append(rc_to_square(row + i, col + i))
                    return
        else:
            return
    for i in range(col):
        if square_check(rc_to_square(row - i, col - i)): #좌 하향 방향 이동 계산
            possible_moves.append(rc_to_square(row - i, col - i))
            if square_check(rc_to_square(row - i, col - i)) == False:
                if color_check(row - i, col - i):
                    possible_moves.append(rc_to_square(row - i, col - i))
                    return
        else:
            return
    for i in range(col):
        if square_check(rc_to_square(row + i, col - i)): #좌 상향 방향 이동 계산
            possible_moves.append(rc_to_square(row + i, col - i))
            if square_check(rc_to_square(row + i, col - i)) == False:
                if color_check(row + i, col - i):
                    possible_moves.append(rc_to_square(row + i, col - i))
                    return
        else:
            return
    for i in range(positive_column): #이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row - i, col + i)): # 우 하향 방향 이동 계산
            possible_moves.append(rc_to_square(row - i, col + i))
            if square_check(rc_to_square(row - i, col + i)) == False:
                if color_check(row - i, col + i):
                    possible_moves.append(rc_to_square(row - i, col + i))
                    return
        else:
            return
    return possible_moves

def queen_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col  # 우로 남은 칸 계산
    positive_row = 8 - row  # 위로 남은 칸 계산
    possible_moves = []
    for i in range(positive_column):
        if square_check(rc_to_square(row, col + i)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col + i))
            if square_check(rc_to_square(row, col + i)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col + i)):
                    possible_moves.append(rc_to_square(row, col + i))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(col):
        if square_check(rc_to_square(row, col - i)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col - i))
            if square_check(rc_to_square(row, col + i)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col - i)):
                    possible_moves.append(rc_to_square(row, col - i))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(positive_row):
        if square_check(rc_to_square(row + i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row + i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row + i, col)):
                    possible_moves.append(rc_to_square(row + i, col))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(row):
        if square_check(rc_to_square(row - i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row - i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row - i, col)):
                    possible_moves.append(rc_to_square(row - i, col))
                    return  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return
        else:
            return
    for i in range(positive_column):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row + i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col + i))
            if square_check(rc_to_square(row + i, col + i)) == False:
                if color_check(row + i, col + i):
                    possible_moves.append(rc_to_square(row + i, col + i))
                    return
        else:
            return
    for i in range(col):
        if square_check(rc_to_square(row - i, col - i)):  # 좌 하향 방향 이동 계산
            possible_moves.append(rc_to_square(row - i, col - i))
            if square_check(rc_to_square(row - i, col - i)) == False:
                if color_check(row - i, col - i):
                    possible_moves.append(rc_to_square(row - i, col - i))
                    return
        else:
            return
    for i in range(col):
        if square_check(rc_to_square(row + i, col - i)):  # 좌 상향 방향 이동 계산
            possible_moves.append(rc_to_square(row + i, col - i))
            if square_check(rc_to_square(row + i, col - i)) == False:
                if color_check(row + i, col - i):
                    possible_moves.append(rc_to_square(row + i, col - i))
                    return
        else:
            return
    for i in range(positive_column):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row - i, col + i)):  # 우 하향 방향 이동 계산
            possible_moves.append(rc_to_square(row - i, col + i))
            if square_check(rc_to_square(row - i, col + i)) == False:
                if color_check(row - i, col + i):
                    possible_moves.append(rc_to_square(row - i, col + i))
                    return
        else:
            return
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
