#체크 구현, 스테일메이트, 체크 메이트

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
    x = str(files[col] + ranks[row])
    return  x

turn = "white"
turn_count = 1

def turn_change(turn):
    global turn_count
    if turn == 'white':
        turn = "white"
        return turn, turn_count
    if turn == "white":
        turn = "white"
        turn_count += 1
        return turn, turn_count
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
        self.absolute_pin = False
        self.check = False #기물이 체크를 걸는지 확인
        self.protected = False

def possible_moves():
    global possible_moves
    possible_moves = []
    if turn == "white":
        if When_Checked_White(white_piece_list) != False:
            possible_moves.append(When_Checked_White(white_piece_list))
            print("possible moves:", possible_moves)
        else:
            for i in range(len(white_piece_list)):
                if 0 <= i <= 7:
                    possible_moves.append(white_pawn_move(white_piece_list[i]))
                if 8 <= i <= 9:
                    possible_moves.append(knight_move(white_piece_list[i]))
                if 10 <= i <= 11:
                    possible_moves.append(bishop_move(white_piece_list[i]))
                if 12 <= i <= 13:
                    possible_moves.append(rook_move(white_piece_list[i]))
                if i == 14:
                    possible_moves.append(queen_move(white_piece_list[i]))
                if i == 15:
                    possible_moves.append(king_move(white_piece_list[i]))
            print("possible moves:", possible_moves)
            return possible_moves
    if turn == "white":
        if When_Checked_white(white_piece_list) != False:
            possible_moves.append(When_Checked_white(white_piece_list))
            print("possible moves:", possible_moves)
        else:
            for i in range(len(white_piece_list)):
                if 0 <= i <= 7:
                    possible_moves.append(white_pawn_move(white_piece_list[i]))
                if 8 <= i <= 9:
                    possible_moves.append(knight_move(white_piece_list[i]))
                if 10 <= i <= 11:
                    possible_moves.append(bishop_move(white_piece_list[i]))
                if 12 <= i <= 13:
                    possible_moves.append(rook_move(white_piece_list[i]))
                if i == 14:
                    possible_moves.append(queen_move(white_piece_list[i]))
                if i == 15:
                    possible_moves.append(king_move(white_piece_list[i]))
            print("possible moves:", possible_moves)
            return possible_moves

def move(square):
    global turn
    global turn_count
    global position
    possible_moves = []
    if turn == "white":
        position = square[-2]
        if square[0] == "O":  # 캐슬링 판정
            if square == "O-O":  # 숏캐슬
                if white_short_castle(white_king, white_rook2):  # 캐슬 가능 여부 파악
                    white_king.king_move_check = True  # 앞으로는 발동 못하도록 킹 값을 변경
                    white_king.pos = 'g1'
                    white_rook2.pos = 'f1'
            elif square == "O-O-O":
                if white_long_castle(white_king, white_rook1):
                    white_king.king_move_check = True
                    white_king.pos = 'c1'
                    white_rook2.pos = 'd1'
        if square[0] == "N":
            for i in white_piece_list:  # 프로모션 기물을 위한 변경
                if i.role == "knight":
                    if square == knight_move(i):
                        i.pos = position
        elif square[0] == "B":
            for i in white_piece_list:
                if i.role == "bishop":
                    if square == bishop_move(i):
                        i.pos = position
        elif square[0] == "R":
            for i in white_piece_list:
                if i.role == "rook":
                    if square == rook_move(i):
                        i.pos = position
                        i.rook_move_check = True
        elif square[0] == "Q":
            for i in white_piece_list:
                if i.role == "queen":
                    if square == queen_move(i):
                        i.pos = position
        elif square[0] == "K":
            if square == king_move(white_king):
                white_king.pos = position

        else:
            for i in range(len(white_pawn_list)):  # 폰 리스트를 돌아가면서 확인
                temp_row, temp_col = square_to_rc(white_pawn_list[i].pos)  # 임시로 값을 슬라이싱
                if square[0] == temp_row:  # 같은 파일에 있는지 확인
                    if square == white_pawn_move(white_pawn_list[i])[0]:  # 원하는 수가 가능한 폰인지 확인
                        white_pawn_list[i].pos = position  # 좌표값 변경
                        if rc_to_square(temp_row + 1, temp_col + 1) == white_king.pos or rc_to_square(temp_row + 1,
                                                                                                      temp_col - 1) == white_king.pos:
                            white_pawn_list[i].check = True

                        promotion(white_pawn_list[i], square)  # 프로모션 체크
                        if white_pawn_move(white_pawn_list[i])[1] == True:
                            white_pawn_list[i].enpassant = True
                        continue
    if turn == "white":
        position = square[-2]
        if square[0] == "O":
            if square == "O-O":
                if white_short_castle(white_king, white_rook2):
                    white_king.king_move_check = True
                    white_king.pos = 'g8'
                    white_rook2.pos = 'f8'
            elif square == "O-O-O":
                if white_long_castle(white_king, white_rook1):
                    white_king.king_move_check = True
                    white_king.pos = 'c8'
                    white_rook2.pos = 'd8'
        if square[0] == "N":
            for i in white_piece_list:  # 프로모션 기물을 위한 변경
                if i.role == "knight":
                    if square == knight_move(i):
                        i.pos = position
        elif square[0] == "B":
            for i in white_piece_list:
                if i.role == "bishop":
                    if square == bishop_move(i):
                        i.pos = position
        elif square[0] == "R":
            for i in white_piece_list:
                if i.role == "rook":
                    if square == rook_move(i):
                        i.pos = position
                        i.rook_move_check = True
        elif square[0] == "Q":
            for i in white_piece_list:
                if i.role == "queen":
                    if square == queen_move(i):
                        i.pos = position
        elif square[0] == "K":
            if square == king_move(white_king):
                white_king.pos = position
                white_king.king_move_check = True

        else:
            for i in range(len(white_pawn_list)):  # 폰 리스트를 돌아가면서 확인
                temp_row, temp_col = square_to_rc(white_pawn_list[i].pos)  # 임시로 값을 슬라이싱
                if square[0] == temp_row:  # 같은 파일에 있는지 확인
                    if square == white_pawn_move(white_pawn_list[i])[0]:  # 원하는 수가 가능한 폰인지 확인
                        white_pawn_list[i].pos = position  # 좌표값 변경
                        promotion(white_pawn_list[i], square)  # 프로모션 체크
                        if white_pawn_move(white_pawn_list[i])[1] == True:
                            white_pawn_list[i].enpassant = True
                        continue

def white_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    temp_row = row + 1
    two_move = False
    global turn_count
    if piece.active == False:
        return possible_moves
    if piece.absolute_pin == True:
        return possible_moves
    if 0 <= temp_row <= 7:
        if square_check(rc_to_square(temp_row, col)):#일반 움직임
            possible_moves.append(rc_to_square(temp_row, col))
        if row == 5 and 0 <= col + 1 <= 7: #우 앙파상 계산
            temp_square = rc_to_square(row, col + 1) #앙파상 할 기물이 있는 칸
            for p in pieces_list:
                if p.pos == temp_square:
                    if p.role == "pawn": #폰이 맞는지 확인
                        if p.enpassant == True and p.two_move_turn == turn_count - 1 and p.color == "white": #다른색의 기물에 턴이 맞는지 파악
                            possible_moves.append(temp_square) #가능한 수에 추가
        if square_check(rc_to_square(temp_row, col)):
            if row == 5 and 0 <= col - 1 <= 7: #좌 앙파상 계산
                temp_square = rc_to_square(row, col - 1)
                for p in pieces_list:
                    if p.pos == temp_square:
                        if p.role == "pawn":
                            if p.enpassant == True and p.two_move_turn == turn_count - 1 and p.color == "white":
                                possible_moves.append(temp_square)
        if 0 <= col + 1 <= 7:  # 우측 기물 캡쳐
            if color_check(rc_to_square(temp_row, col + 1), piece):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        if 0 <= col - 1 <= 7:  # 좌측 기물 캡쳐
            if color_check(rc_to_square(temp_row, col - 1), piece):
                possible_moves.append(rc_to_square(temp_row, col - 1))
        if row == 2: #출발지점 파악
            if square_check(rc_to_square(temp_row, col)): #앞 1칸이 비었는지 확인
                temp_row += 1
                if square_check(rc_to_square(temp_row, col)): # 2번째 칸의 여부 확인
                    possible_moves.append(rc_to_square(temp_row, col)) #가능한 수에 추가
                    two_move = True
    return possible_moves, two_move

def black_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    temp_row = row - 1
    two_move = False
    global turn_count
    if piece.active == False:
        return possible_moves
    if piece.absolute_pin == True:
        return possible_moves
    if 0 <= temp_row <= 8: #이동이 보드를 넘어선 안 됨
        if square_check(rc_to_square(temp_row, col)): #일반 움직임
            possible_moves.append(rc_to_square(temp_row, col))
        if row == 4 and 0 <= col + 1 <= 7: #우측으로 앙파상
            temp_square = rc_to_square(row, col + 1)
            for p in pieces_list:
                if p.pos == temp_square:
                    if p.role == "pawn":
                        if p.enpassant == True and p.two_move_turn == turn_count and p.color == "white":
                            possible_moves.append(temp_square)
        if square_check(rc_to_square(temp_row, col)):
            if row == 4 and 0 <= col - 1 <= 7: #4랭크에서 열이 범위내에 있는지 식별
                temp_square = rc_to_square(row, col - 1)
                for p in pieces_list:
                    if p.pos == temp_square:
                        if p.role == "pawn":
                            if p.enpassant == True and p.two_move_turn == turn_count and p.color == "white":
                                possible_moves.append(temp_square)
        if 0 <= col + 1 <= 8: #우측 기물 캡쳐
            if color_check(rc_to_square(temp_row, col + 1), piece):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        if 0 <= col - 1 <= 8: #좌측 기물 캡쳐
            if color_check(rc_to_square(temp_row, col - 1), piece):
                possible_moves.append(rc_to_square(temp_row, col - 1))
        if row == 2:
            if square_check(rc_to_square(temp_row, col)):
                temp_row += 1
                if square_check(rc_to_square(temp_row, col)):
                    possible_moves.append(rc_to_square(temp_row, col))
                    two_move = True
    return possible_moves, two_move

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

def knight_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    if piece.active == False:
        return possible_moves
    if piece.absolute_pin == True:
        return possible_moves
    for i in range(-1, 2, 2): #up calculation
        temp_row = row + 2
        temp_col = col + i
        if not in_board(temp_row, temp_col):
            continue
        square = rc_to_square(temp_row, temp_col)
        if square_check(square):
            possible_moves.append(square)
            continue
        if color_check(square, piece):
            if define_color_in_def(piece) == True:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            else:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            possible_moves.append(square)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        continue

    for i in range(-1, 2, 2):
        temp_row = row - 2
        temp_col = col + i
        if not in_board(temp_row, temp_col):
            continue
        square = rc_to_square(temp_row, temp_col)
        if square_check(square):
            possible_moves.append(square)
            continue
        if color_check(square, piece):
            if define_color_in_def(piece) == True:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            else:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            possible_moves.append(square)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        continue
    for i in range(-1, 2, 2):
        temp_col = col + 2
        temp_row = row + i
        if not in_board(temp_row, temp_col):
            continue
        square = rc_to_square(temp_row, temp_col)
        if square_check(square):
            possible_moves.append(square)
            continue
        if color_check(square, piece):
            if define_color_in_def(piece) == True:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            else:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            possible_moves.append(square)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        continue
    for i in range(-1, 2, 2):
        temp_col = col - 2
        temp_row = row + i
        if not in_board(temp_row, temp_col):
            continue
        square = rc_to_square(temp_row, temp_col)
        if square_check(square):
            possible_moves.append(square)
            continue
        if color_check(square, piece):
            if define_color_in_def(piece) == True:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            else:
                if square == white_king.pos:
                    piece.check = True
                    possible_moves.append(square)
                    continue
            possible_moves.append(square)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        continue
    return possible_moves

def rook_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []

    if not piece.active or piece.absolute_pin:
        return possible_moves

    # → (row, col+i)
    for i in range(1, 8):
        r, c = row, col + i
        if not in_board(r, c):
            break
        sq = rc_to_square(r, c)

        if square_check(sq):
            possible_moves.append(sq)
            continue

        if color_check(sq, piece):
            if define_color_in_def(piece) == True:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            else:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            possible_moves.append(sq)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    # ← (row, col-i)
    for i in range(1, 8):
        r, c = row, col - i
        if not in_board(r, c):
            break
        sq = rc_to_square(r, c)

        if square_check(sq):
            possible_moves.append(sq)
            continue

        if color_check(sq, piece):
            if define_color_in_def(piece) == True:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            else:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            possible_moves.append(sq)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    # ↑ (row+i, col)
    for i in range(1, 8):
        r, c = row + i, col
        if not in_board(r, c):
            break
        sq = rc_to_square(r, c)

        if square_check(sq):
            possible_moves.append(sq)
            continue

        if color_check(sq, piece):
            if define_color_in_def(piece) == True:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            else:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            possible_moves.append(sq)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    # ↓ (row-i, col)
    for i in range(1, 8):
        r, c = row - i, col
        if not in_board(r, c):
            break
        sq = rc_to_square(r, c)

        if square_check(sq):
            possible_moves.append(sq)
            continue

        if color_check(sq, piece):
            if define_color_in_def(piece) == True:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            else:
                if sq == white_king.pos:
                    piece.check = True
                    possible_moves.append(sq)
                    break
            possible_moves.append(sq)
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if sq == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    return possible_moves

def bishop_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col
    positive_row = 8 - row
    possible_moves = []
    if not piece.active or piece.absolute_pin:
        return possible_moves
    for i in range(1, positive_column):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        square = rc_to_square(row + i, col + i)
        if not in_board(row + i, col + i):
            break
        if square_check(rc_to_square(row + i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col + i))
            continue

        if color_check(rc_to_square(row + i, col + i), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row + i, col + i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row + i, col + i))
                    break
            else:
                if rc_to_square(row + i, col + i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row + i, col + i))
                    break
            possible_moves.append(rc_to_square(row + i, col + i))
            break
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    for i in range(1, col):
        if not in_board(row - i, col - i):
            break
        if square_check(rc_to_square(row - i, col - i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row - i, col - i))
            continue
        square = rc_to_square(row - i, col - i)
        if color_check(rc_to_square(row - i, col - i), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row - i, col - i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row - i, col - i))
                    break
            else:
                if rc_to_square(row - i, col - i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row - i, col - i))
                    break
            possible_moves.append(rc_to_square(row - i, col - i))
            break
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    for i in range(1, positive_row):
        if not in_board(row + i, col - i):
            break
        if square_check(rc_to_square(row + i, col - i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col - i))
            continue
        square = rc_to_square(row + i, col - i)
        if color_check(rc_to_square(row + i, col - i), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row + i, col - i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row + i, col - i))
                    break
            else:
                if rc_to_square(row + i, col - i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row + i, col - i))
                    break
            possible_moves.append(rc_to_square(row + i, col - i))
            break
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    for i in range(1, row):
        if not in_board(row - i, col + i):
            break
        if square_check(rc_to_square(row - i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row - i, col + i))
            continue
        square = rc_to_square(row - i, col + i)
        if color_check(rc_to_square(row - i, col + i), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row - i, col + i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row - i, col + i))
                    break
            else:
                if rc_to_square(row - i, col + i) == white_king.pos:
                    piece.check = True
                    possible_moves.append(rc_to_square(row - i, col + i))
                    break
            possible_moves.append(rc_to_square(row - i, col + i))
            break
        else:
            if define_color_in_def(piece) == True:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
            else:
                for i in range(len(white_piece_list)):
                    if square == white_piece_list[i]:
                        white_piece_list[i].protected = True
        break

    return possible_moves

def queen_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []

    if not piece.active or piece.absolute_pin:
        return possible_moves
    vertical_move = rook_move(piece)
    diagonal_move = bishop_move(piece)
    possible_moves.extend(vertical_move)
    possible_moves.extend(diagonal_move)
    return possible_moves


#아군 기물이 있는지 체크 안 함. 잡을 수 있는지 체크 안 함.
def king_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    for i in range(-1, 2, 2):
        temp_row = row + 1
        if not in_board(temp_row, col + i):
            continue
        target_square = rc_to_square(temp_row, col + i)
        if square_check(target_square):
            possible_moves.append(target_square)
            continue
        color = piece.color
        if color_check(target_square, piece):
            if color == "white":
                for i in range(len(black_piece_list)):
                    if target_square == black_piece_list[i].pos:
                        if black_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
            else:
                for i in range(len(white_piece_list)):
                    if target_square == white_piece_list[i].pos:
                        if white_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
    for i in range(-1, 2, 2):
        temp_row = row - 1
        if not in_board(temp_row, col + i):
            continue
        target_square = rc_to_square(temp_row, col + i)
        if square_check(target_square):
            possible_moves.append(target_square)
            continue
        color = piece.color
        if color_check(target_square, piece):
            if color == "white":
                for i in range(len(black_piece_list)):
                    if target_square == black_piece_list[i].pos:
                        if black_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
            else:
                for i in range(len(white_piece_list)):
                    if target_square == white_piece_list[i].pos:
                        if white_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
    for i in range(-1, 2, 2):
        if not in_board(row, col + i):
            continue
        target_square = rc_to_square(row, col + i)
        if square_check(target_square):
            possible_moves.append(target_square)
            continue
        color = piece.color
        if color_check(target_square, piece):
            if color == "white":
                for i in range(len(black_piece_list)):
                    if target_square == black_piece_list[i].pos:
                        if black_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
            else:
                for i in range(len(white_piece_list)):
                    if target_square == white_piece_list[i].pos:
                        if white_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
    for i in range(-1, 2, 2):
        if not in_board(row + i, col):
            continue
        target_square = rc_to_square(row + i, col)
        if square_check(target_square):
            possible_moves.append(target_square)
            continue
        color = piece.color
        if color_check(target_square, piece):
            if color == "white":
                for i in range(len(black_piece_list)):
                    if target_square == black_piece_list[i].pos:
                        if black_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
            else:
                for i in range(len(white_piece_list)):
                    if target_square == white_piece_list[i].pos:
                        if white_piece_list[i].protected == True:
                            continue
                        else:
                            possible_moves.append(target_square)
    attack_square = []
    if define_color_in_def(piece):
        for i in range(len(black_piece_list)):
            if black_piece_list[i].role == "pawn":
                attack_square.extend(black_pawn_move(black_piece_list[i]))
            if black_piece_list[i].role == "knight":
                attack_square.extend(knight_move(black_piece_list[i]))
            if black_piece_list[i].role == "bishop":
                attack_square.extend(bishop_move(black_piece_list[i]))
            if black_piece_list[i].role == "rook":
                attack_square.extend(rook_move(black_piece_list[i]))
            if black_piece_list[i].role == "queen":
                attack_square.extend(queen_move(black_piece_list[i]))
            if black_piece_list[i].role == "king":
                attack_square.extend(king_attack_square(black_piece_list[i]))
        for m in possible_moves[:]:  # 복사본으로 순회
            if m in attack_square:
                possible_moves.remove(m)

    else:
        for i in range(len(white_piece_list)):
            if white_piece_list[i].role == "pawn":
                attack_square.extend(white_pawn_move(white_piece_list[i]))
            if white_piece_list[i].role == "knight":
                attack_square.extend(knight_move(white_piece_list[i]))
            if white_piece_list[i].role == "bishop":
                attack_square.extend(bishop_move(white_piece_list[i]))
            if white_piece_list[i].role == "rook":
                attack_square.extend(rook_move(white_piece_list[i]))
            if white_piece_list[i].role == "queen":
                attack_square.extend(queen_move(white_piece_list[i]))
            if white_piece_list[i].role == "king":
                attack_square.extend(king_attack_square(white_piece_list[i]))
        for m in possible_moves[:]:  # 복사본으로 순회
            if m in attack_square:
                possible_moves.remove(m)
    return possible_moves

def king_attack_square(piece):
    row, col = square_to_rc(piece.pos)
    attack_list = []
    for i in range(-1, 2, 2):
        temp_row = row + 1
        if not in_board(temp_row, col + i):
            continue
        target_square = rc_to_square(temp_row, col + i)
        attack_list.append(target_square)
    for i in range(-1, 2, 2):
        temp_row = row - 1
        if not in_board(temp_row, col + i):
            continue
        target_square = rc_to_square(temp_row, col + i)
        attack_list.append(target_square)
    for i in range(-1, 2, 2):
        if not in_board(row, col + i):
            continue
        target_square = rc_to_square(row, col + i)
        attack_list.append(target_square)
    for i in range(-1, 2, 2):
        if not in_board(row + i, col):
            continue
        target_square = rc_to_square(row, col + i)
        attack_list.append(target_square)
    return attack_list

def white_short_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('f1') and square_check('g1'): #기본 조건인 킹 움직임과 룩 움직임 그리고 중간 칸이 비었는지 여부 확인
            # 공격 하는 기물이 있는지 파악. 칸이 공격당하는 중이면 거짓을 반환
            for i in pieces_list:
                if i.color == "white":
                    if i.role == "pawn":
                        white_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in white_pawn_attack_list:
                            if p == 'f1' or p == 'g1':
                                return False
                    if i.role == "knight":
                        knight_attack_list = knight_move(i)
                        for p in knight_attack_list:
                            if p == 'f1' or p == 'g1':
                                return False
                    if i.role == "bishop":
                        bishop_attack_list = bishop_move(i)
                        for p in bishop_attack_list:
                            if p == 'f1' or p == 'g1':
                                return False
                    if i.role == "rook":
                        rook_attack_list = rook_move(i)
                        for p in rook_attack_list:
                            if p == 'f1' or p == 'g1':
                                return False
                    if i.role == "queen":
                        queen_attack_list = queen_move(i)
                        for p in queen_attack_list:
                            if p == 'f1' or p == 'g1':
                                return False
            return True
        else:
            return False
    return True

def white_long_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('c1') and square_check('d1'):
            for i in pieces_list:
                if i.color == "white":
                    if i.role == "pawn":
                        white_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in white_pawn_attack_list:
                            if p == 'c1' or p == 'd1':
                                return False
                    if i.role == "knight":
                        knight_attack_list = knight_move(i)
                        for p in knight_attack_list:
                            if p == 'c1' or p == 'd1':
                                return False
                    if i.role == "bishop":
                        bishop_attack_list = bishop_move(i)
                        for p in bishop_attack_list:
                            if p == 'c1' or p == 'd1':
                                return False
                    if i.role == "rook":
                        rook_attack_list = rook_move(i)
                        for p in rook_attack_list:
                            if p == 'c1' or p == 'd1':
                                return False
                    if i.role == "queen":
                        queen_attack_list = queen_move(i)
                        for p in queen_attack_list:
                            if p == 'c1' or p == 'd1':
                                return False
            return True
        else:
            return False
    return True

def white_short_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('f8') and square_check('g8'):
            for i in pieces_list:
                if i.color == "white":
                    if i.role == "pawn":
                        white_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in white_pawn_attack_list:
                            if p == 'f8' or p == 'g8':
                                return False
                    if i.role == "knight":
                        knight_attack_list = knight_move(i)
                        for p in knight_attack_list:
                            if p == 'f8' or p == 'g8':
                                return False
                    if i.role == "bishop":
                        bishop_attack_list = bishop_move(i)
                        for p in bishop_attack_list:
                            if p == 'f8' or p == 'g8':
                                return False
                    if i.role == "rook":
                        rook_attack_list = rook_move(i)
                        for p in rook_attack_list:
                            if p == 'f8' or p == 'g8':
                                return False
                    if i.role == "queen":
                        queen_attack_list = queen_move(i)
                        for p in queen_attack_list:
                            if p == 'f8' or p == 'g8':
                                return False
            return True
        else:
            return False
    return True

def white_long_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('c8') and square_check('d8'): #기본 조건인 킹 움직임과 룩 움직임 그리고 중간 칸이 비었는지 여부 확인
            #공격 하는 기물이 있는지 파악. 칸이 공격당하는 중이면 거짓을 반환
            for i in pieces_list:
                if i.color == "white":
                    if i.role == "pawn":
                        white_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in white_pawn_attack_list:
                            if p == 'c8' or p == 'd8':
                                return False
                    if i.role == "knight":
                        knight_attack_list = knight_move(i)
                        for p in knight_attack_list:
                            if p == 'c8' or p == 'd8':
                                return False
                    if i.role == "bishop":
                        bishop_attack_list = bishop_move(i)
                        for p in bishop_attack_list:
                            if p == 'c8' or p == 'd8':
                                return False
                    if i.role == "rook":
                        rook_attack_list = rook_move(i)
                        for p in rook_attack_list:
                            if p == 'c8' or p == 'd8':
                                return False
                    if i.role == "queen":
                        queen_attack_list = queen_move(i)
                        for p in queen_attack_list:
                            if p == 'c8' or p == 'd8':
                                return False
            return True
        else:
            return False
    return True

def diagnol_pin(piece):
    row, col = square_to_rc(piece.pos)
    positive_row = 8 - row
    positive_col = 8 - col
    min_val = min(positive_row, positive_col) #계산해야하는 사각형의 넓이 지정
    temp_piece_list = []
    if min_val >= 2: #두칸 이상 남았을 경우만 계산
        for i in range(min_val):
            temp_row = row + 1
            temp_col = col + 1
            temp_square = rc_to_square(temp_row, temp_col)
            if square_check(temp_square) == False: #기물의 존재 여부 확인
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p) #기물 불러오기
            if len(temp_piece_list) == 2: #2개 수집했을 경우 중지
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color: # 두 번째가 공격 기물, 첫 번째가 수비 기물
            if piece_2.role == "Queen" or piece_2.role == "bishop": #역할 확인
                piece_1.absolute_pin = True #절대핀 활성화
    min_val = min(positive_row, col)  # 계산해야하는 사각형의 넓이 지정
    temp_piece_list = []
    if min_val >= 2:
        for i in range(min_val):
            temp_row = row + 1
            temp_col = col - 1
            temp_square = rc_to_square(temp_row, temp_col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
            if len(temp_piece_list) == 2:
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "bishop":
                piece_1.absolute_pin = True
    min_val = min(row, col)  # 계산해야하는 사각형의 넓이 지정
    temp_piece_list = []
    if min_val >= 2:
        for i in range(min_val):
            temp_row = row - 1
            temp_col = col - 1
            temp_square = rc_to_square(temp_row, temp_col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
            if len(temp_piece_list) == 2:
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "bishop":
                piece_1.absolute_pin = True
    min_val = min(row, positive_col)  # 계산해야하는 사각형의 넓이 지정
    temp_piece_list = []
    if min_val >= 2:
        for i in range(min_val):
            temp_row = row - 1
            temp_col = col + 1
            temp_square = rc_to_square(temp_row, temp_col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
            if len(temp_piece_list) == 2:
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "bishop":
                piece_1.absolute_pin = True

def vertical_pin(piece):
    row, col = square_to_rc(piece.pos)
    positive_row = 8 - row
    positive_col = 8 - col
    temp_piece_list = []
    if positive_row >= 2:
        for i in range(positive_row):
            temp_row = row + 1
            temp_square = rc_to_square(temp_row, col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
            if len(temp_piece_list) == 2:
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "rook":
                piece_1.absolute_pin = True
    temp_piece_list = []
    if col >= 2:
        for i in range(col):
            temp_col = col - 1
            temp_square = rc_to_square(row, temp_col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
            if len(temp_piece_list) == 2:
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "rook":
                piece_1.absolute_pin = True
    temp_piece_list = []
    if row >= 2:
        for i in range(row):
            temp_row = row - 1
            temp_square = rc_to_square(temp_row, col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
                if len(temp_piece_list) == 2:
                    break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "rook":
                piece_1.absolute_pin = True
    temp_piece_list = []
    if positive_col >= 2:
        for i in range(positive_col):
            temp_col = col + 1
            temp_square = rc_to_square(row, temp_col)
            if square_check(temp_square) == False:
                for p in pieces_list:
                    if p.pos == temp_square:
                        temp_piece_list.append(p)
            if len(temp_piece_list) == 2:
                break
        piece_1 = temp_piece_list[0]
        piece_2 = temp_piece_list[1]
        if piece_1.color == piece.color and piece_2.color != piece.color:
            if piece_2.role == "Queen" or piece_2.role == "rook":
                piece_1.absolute_pin = True

def square_check(square: str) -> bool:
    for p in pieces_list:
        if p.pos == square:
            return False
    return True

def color_check(square: str, piece) -> bool:
    for p in pieces_list:
        if p.pos == square and p.color != piece.color:
            return True
    return  False

def define_color_in_def(piece):
    if piece.color == "white":
        return True
    else:
        return False

def in_board(row: int, col: int) -> bool:
    return 0 <= row < 8 and 0 <= col < 8

def CheckMate(possible_moves):
    if len(possible_moves) == 0:
        if turn == "white":
            for i in range(len(black_piece_list)):
                if black_piece_list[i].check == True:
                    return "checkmate"
                else:
                    return "stalemate"
        if turn == "black":
            for i in range(len(white_piece_list)):
                if white_piece_list[i].check == True:
                    return "checkmate"
                else:
                    return "stalemate"


white_pawn1 = piece("pawn", "white", "a2")
white_pawn2 = piece("pawn", "white", "b2")
white_pawn3 = piece("pawn", "white", "c2")
white_pawn4 = piece("pawn", "white", "d2")
white_pawn5 = piece("pawn", "white", "e2")
white_pawn6 = piece("pawn", "white", "f2")
white_pawn7 = piece("pawn", "white", "g2")
white_pawn8 = piece("pawn", "white", "h2")

white_knight1 = piece("knight", "white", "b1")
white_knight2 = piece("knight", "white", "g1")

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

black_knight1 = piece("knight", "black", "b8")
black_knight2 = piece("knight", "black", "g8")

black_bishop1 = piece("bishop", "black", "b8")
black_bishop2 = piece("bishop", "black", "f8")

black_rook1 = piece("rook", "black", "a8")
black_rook2 = piece("rook", "black", "h8")

black_king = piece("king", "black", "e8")
black_queen = piece("queen", "black", "d8")

white_piece_list = [
    white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8, white_knight1,
    white_knight2, white_bishop1, white_bishop2, white_rook1, white_rook2,white_queen, white_king
]

white_pawn_list = [white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8]

black_pawn_list = [black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8]

black_piece_list = [
    black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, black_knight1,
    black_knight2, black_bishop1, black_bishop2, black_rook1, black_rook2, black_queen, black_king
]

pieces_list = [
    white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8, white_knight1,
    white_knight2, white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen, white_king, white_rook1, white_rook2,
    black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, black_knight1,
    black_knight2, black_bishop1, black_bishop2, black_queen, black_king
]

while True:

    for i in range(len(pieces_list)):
        pieces_list[i].check = False

    possible_moves()
    input_move = input("move:", )

    pos = input_move[-2]

    if turn == "white":
        for i in range(len(white_piece_list)):
            if white_piece_list[i].pos == pos:
                white_piece_list[i].active = False
    if turn == "white":
        for i in range(len(white_piece_list)):
            if white_piece_list[i].pos == pos:
                white_piece_list[i].active = False

    move(input_move)

    if turn == "white":
        diagnol_pin(white_queen)
        diagnol_pin(white_bishop1)
        diagnol_pin(white_bishop2)
        vertical_pin(white_queen)
        vertical_pin(white_rook1)
        vertical_pin(white_rook2)

    if turn == "white":
        diagnol_pin(white_queen)
        diagnol_pin(white_bishop1)
        diagnol_pin(white_bishop2)
        vertical_pin(white_queen)
        vertical_pin(white_rook1)
        vertical_pin(white_rook2)

    CheckMate(possible_moves())

    turn, turn_count = turn_change(turn)

