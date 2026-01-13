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
    return files[col] + ranks[row]

turn = "white"
turn_count = 1

def turn_change(turn):
    global turn_count
    if turn == 'white':
        turn = "black"
        return turn, turn_count
    if turn == "black":
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

def possible_moves():
    global possible_moves
    possible_moves = []
    if turn == "white":
        possible_moves.append(When_Checked_White(black_piece_list))
        if len(possible_moves) > 0:
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
    if turn == "black":
        possible_moves.append(When_Checked_black(white_piece_list))
        if len(possible_moves) > 0:
            print("possible moves:", possible_moves)
        else:
            for i in range(len(black_piece_list)):
                if 0 <= i <= 7:
                    possible_moves.append(black_pawn_move(black_piece_list[i]))
                if 8 <= i <= 9:
                    possible_moves.append(knight_move(black_piece_list[i]))
                if 10 <= i <= 11:
                    possible_moves.append(bishop_move(black_piece_list[i]))
                if 12 <= i <= 13:
                    possible_moves.append(rook_move(black_piece_list[i]))
                if i == 14:
                    possible_moves.append(queen_move(black_piece_list[i]))
                if i == 15:
                    possible_moves.append(king_move(black_piece_list[i]))
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
                if i.role == "night":
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
    if turn == "black":
        position = square[-2]
        if square[0] == "O":
            if square == "O-O":
                if black_short_castle(black_king, black_rook2):
                    black_king.king_move_check = True
                    black_king.pos = 'g8'
                    black_rook2.pos = 'f8'
            elif square == "O-O-O":
                if black_long_castle(black_king, black_rook1):
                    black_king.king_move_check = True
                    black_king.pos = 'c8'
                    black_rook2.pos = 'd8'
        if square[0] == "N":
            for i in black_piece_list:  # 프로모션 기물을 위한 변경
                if i.role == "night":
                    if square == knight_move(i):
                        i.pos = position
        elif square[0] == "B":
            for i in black_piece_list:
                if i.role == "bishop":
                    if square == bishop_move(i):
                        i.pos = position
        elif square[0] == "R":
            for i in black_piece_list:
                if i.role == "rook":
                    if square == rook_move(i):
                        i.pos = position
                        i.rook_move_check = True
        elif square[0] == "Q":
            for i in black_piece_list:
                if i.role == "queen":
                    if square == queen_move(i):
                        i.pos = position
        elif square[0] == "K":
            if square == king_move(black_king):
                black_king.pos = position
                white_king.king_move_check = True

        else:
            for i in range(len(black_pawn_list)):  # 폰 리스트를 돌아가면서 확인
                temp_row, temp_col = square_to_rc(black_pawn_list[i].pos)  # 임시로 값을 슬라이싱
                if square[0] == temp_row:  # 같은 파일에 있는지 확인
                    if square == black_pawn_move(black_pawn_list[i])[0]:  # 원하는 수가 가능한 폰인지 확인
                        black_pawn_list[i].pos = position  # 좌표값 변경
                        promotion(black_pawn_list[i], square)  # 프로모션 체크
                        if black_pawn_move(black_pawn_list[i])[1] == True:
                            black_pawn_list[i].enpassant = True
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
        if 0 <= col + 1 <= 8:  # 우측 기물 캡쳐
            if color_check(rc_to_square(temp_row, col + 1), piece):
                possible_moves.append(rc_to_square(temp_row, col + 1))
        if 0 <= col - 1 <= 8:  # 좌측 기물 캡쳐
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
    if row + 2 <= 8 and col + 1 <= 8:
        if color_check(rc_to_square(row + 2, col + 1), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row + 2, col + 1) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row + 2, col + 1) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row + 2, col + 1))
    if row + 2 <= 8 and col - 1 <= 8:
        if color_check(rc_to_square(row + 2, col - 1), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row + 2, col - 1) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row + 2, col - 1) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row + 2, col - 1))
    if row - 2 <= 8 and col + 1 <= 8:
        if color_check(rc_to_square(row - 2, col + 1), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row - 2, col + 1) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row - 2, col + 1) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row - 2, col + 1))
    if row - 2 <= 8 and col - 1 <= 8:
        if color_check(rc_to_square(row - 2, col - 1), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row - 2, col - 1) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row - 2, col - 1) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row - 2, col - 1))
    if row + 1 <= 8 and col + 2 <= 8:
        if color_check(rc_to_square(row + 1, col + 2), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row + 1, col + 2) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row + 1, col + 2) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row + 1, col + 2))
    if row - 1 <= 8 and col + 2 <= 8:
        if color_check(rc_to_square(row - 1, col + 2), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row - 1, col + 2) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row - 1, col + 2) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row - 1, col + 2))
    if row + 1 <= 8 and col - 2 <= 8:
        if color_check(rc_to_square(row + 1, col - 2), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row + 1, col - 2) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row + 1, col - 2) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row + 1, col - 2))
    if row - 1 <= 8 and col - 2 <= 8:
        if color_check(rc_to_square(row - 1, col - 2), piece):
            if define_color_in_def(piece) == True:
                if rc_to_square(row - 1, col - 2) == black_king.pos:
                    piece.check = True
                    return piece.check
            else:
                if rc_to_square(row - 1, col - 2) == white_king.pos:
                    piece.check = True
                    return piece.check
            possible_moves.append(rc_to_square(row - 1, col - 2))
    return possible_moves

def rook_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col #우로 남은 칸 계산
    positive_row = 8 - row #위로 남은 칸 계산
    possible_moves = []
    if piece.active == False:
        return possible_moves
    if piece.absolute_pin == True:
        return possible_moves
    for i in range(positive_column):
        if square_check(rc_to_square(row, col + i)): #막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col + i))
            if square_check(rc_to_square(row, col + i)) == False: #막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col + i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row, col + i) == black_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row, col + i) == white_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row, col + i))
                    return possible_moves # 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(col):
        if square_check(rc_to_square(row, col - i)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col - i))
            if square_check(rc_to_square(row, col - i)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col - i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row, col - i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row, col - i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row, col - i))
                    return possible_moves# 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(positive_row):
        if square_check(rc_to_square(row + i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row + i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row + i, col), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row + i, col) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row + i, col) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row + i, col))
                    return possible_moves # 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(row):
        if square_check(rc_to_square(row - i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row - i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row - i, col), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row -i , col) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row - i, col) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row - i, col))
                    return  possible_moves# 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    return possible_moves

def bishop_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col
    positive_row = 8 - row
    possible_moves = []
    if piece.active == False:
        return possible_moves
    if piece.absolute_pin == True:
        return possible_moves
    for i in range(positive_column):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row + i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col + i))
            if square_check(rc_to_square(row + i, col + i)) == False:
                if color_check(rc_to_square(row + i, col + i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row + i, col + i) == black_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row + i, col + i) == white_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row + i, col + i))
                    return possible_moves
    for i in range(col):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row - i, col - i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row - i, col - i))
            if square_check(rc_to_square(row - i, col - i)) == False:
                if color_check(rc_to_square(row - i, col - i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row - i, col - i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row - i, col - i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row - i, col - i))
                    return possible_moves

    for i in range(positive_row):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row + i, col - i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col - i))
            if square_check(rc_to_square(row + i, col - i)) == False:
                if color_check(rc_to_square(row + i, col - i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row + i, col - i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row + i, col - i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row + i, col - i))
                    return possible_moves
    for i in range(row):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row - i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row - i, col + i))
            if square_check(rc_to_square(row - i, col + i)) == False:
                if color_check(rc_to_square(row - i, col + i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row - i, col + i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row - i, col + i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row - i, col + i))
                    return possible_moves
    return possible_moves

def queen_move(piece):
    row, col = square_to_rc(piece.pos)
    positive_column = 8 - col  # 우로 남은 칸 계산
    positive_row = 8 - row  # 위로 남은 칸 계산
    possible_moves = []
    if piece.active == False:
        return possible_moves
    if piece.absolute_pin == True:
        return possible_moves
    for i in range(positive_column):
        if square_check(rc_to_square(row, col + i)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col + i))
            if square_check(rc_to_square(row, col + i)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col + i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row, col + i) == black_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row, col + i) == white_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row, col + i))
                    return possible_moves  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(col):
        if square_check(rc_to_square(row, col - i)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row, col - i))
            if square_check(rc_to_square(row, col - i)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row, col - i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row, col - i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row, col - i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row, col - i))
                    return possible_moves  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(positive_row):
        if square_check(rc_to_square(row + i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row + i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row + i, col), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row + i, col) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row + i, col) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row + i, col))
                    return possible_moves  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(row):
        if square_check(rc_to_square(row - i, col)):  # 막히지 않고 갈 수 있는 칸을 계산
            possible_moves.append(rc_to_square(row - i, col))
            if square_check(rc_to_square(row + i, col)) == False:  # 막혔을 경우 잡을 수 있는지 계산
                if color_check(rc_to_square(row - i, col), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row - i, col) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row - i, col) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row - i, col))
                    return possible_moves  # 잡는 수까지만 계산하고 값을 반환
                else:
                    return possible_moves
    for i in range(positive_column):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row + i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col + i))
            if square_check(rc_to_square(row + i, col + i)) == False:
                if color_check(rc_to_square(row + i, col + i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row + i, col + i) == black_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row + i, col + i) == white_king.pos:
                            piece.check = True
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row + i, col + i))
                    return possible_moves
    for i in range(col):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row - i, col - i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row - i, col - i))
            if square_check(rc_to_square(row - i, col - i)) == False:
                if color_check(rc_to_square(row - i, col - i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row - i, col - i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row - i, col - i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row - i, col - i))
                    return possible_moves

    for i in range(positive_row):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row + i, col - i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row + i, col - i))
            if square_check(rc_to_square(row + i, col - i)) == False:
                if color_check(rc_to_square(row + i, col - i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row + i, col - i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row + i, col - i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row + i, col - i))
                    return possible_moves
    for i in range(row):  # 이동은 이등변 삼각형으로 이루어지기 때문에 기준은 하나로 충분
        if square_check(rc_to_square(row - i, col + i)):  # 우 상향 방향 이동 계산. 막히지 않고 갈 수 있는 거리
            possible_moves.append(rc_to_square(row - i, col + i))
            if square_check(rc_to_square(row - i, col + i)) == False:
                if color_check(rc_to_square(row - i, col + i), piece):
                    if define_color_in_def(piece) == True:
                        if rc_to_square(row - i, col + i) == black_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    else:
                        if rc_to_square(row - i, col + i) == white_king.pos:
                            piece.check = True
                            del possible_moves[:len(possible_moves) - i]
                            return piece.check, possible_moves
                    possible_moves.append(rc_to_square(row - i, col + i))
                    return possible_moves
    return possible_moves

#아군 기물이 있는지 체크 안 함. 잡을 수 있는지 체크 안 함.
def king_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []  #가능한 움직임을 전부 측정하고 이동이 실제로 가능한지는 이후에 판단
    possible_moves.append(rc_to_square(row + 1, col))
    possible_moves.append(rc_to_square(row + 1, col + 1))
    possible_moves.append(rc_to_square(row + 1, col - 1))
    possible_moves.append(rc_to_square(row , col + 1))
    possible_moves.append(rc_to_square(row, col - 1))
    possible_moves.append(rc_to_square(row - 1, col))
    possible_moves.append(rc_to_square(row - 1, col + 1))
    possible_moves.append(rc_to_square(row - 1, col - 1))

    for i in range(len(possible_moves)):
        if square_check(possible_moves[i].pos) == False:
            possible_moves.remove(possible_moves[i])
        else:
            if color_check(possible_moves[i].pos, piece) == False:
                possible_moves.remove(possible_moves[i])

    opposite_color_pieces = [] #공격 가능한 기물의 리스트
    for i in pieces_list: #킹을 공격할 기물들을 선별
        if i.color != piece.color:
            opposite_color_pieces.append(i)
            opposite_color = i.color

    for i in opposite_color_pieces:
        if i.role == "pawn":
            if opposite_color == "white":
                black_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                for p in black_pawn_attack_list:
                    possible_moves.remove(p)
            if opposite_color == "black":
                black_pawn_attack_list, dummy_data_1 = black_pawn_move(i)
                for p in black_pawn_attack_list:
                    possible_moves.remove(p)
        if i.role == "night":
            night_attack_list = knight_move(i)
            for p in night_attack_list:
                possible_moves.remove(p)
        if i.role == "bishop":
            bishop_attack_list = bishop_move(i)
            for p in bishop_attack_list:
                possible_moves.remove(p)
        if i.role == "rook":
            rook_attack_list = rook_move(i)
            for p in rook_attack_list:
                possible_moves.remove(p)
        if i.role == "queen":
            queen_attack_list = queen_move(i)
            for p in queen_attack_list:
                possible_moves.remove(p)
        if i.role == "king":  #킹끼리는 공격 경로에 들어갈 수 없음. 그러나 재귀함수는 이용이 어려움으로 따로 계산
            temp_row, temp_col = square_to_rc(i.pos)
            temp_possible_moves = []
            temp_possible_moves.append(rc_to_square(temp_row + 1, temp_col))
            temp_possible_moves.append(rc_to_square(temp_row + 1, temp_col + 1))
            temp_possible_moves.append(rc_to_square(temp_row + 1, temp_col - 1))
            temp_possible_moves.append(rc_to_square(temp_row, temp_col + 1))
            temp_possible_moves.append(rc_to_square(temp_row, temp_col - 1))
            temp_possible_moves.append(rc_to_square(temp_row - 1, temp_col))
            temp_possible_moves.append(rc_to_square(temp_row - 1, temp_col + 1))
            temp_possible_moves.append(rc_to_square(temp_row - 1, temp_col - 1))
            for p in temp_possible_moves:
                possible_moves.remove(p)


def white_short_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('f1') and square_check('g1'): #기본 조건인 킹 움직임과 룩 움직임 그리고 중간 칸이 비었는지 여부 확인
            # 공격 하는 기물이 있는지 파악. 칸이 공격당하는 중이면 거짓을 반환
            for i in pieces_list:
                if i.color == "black":
                    if i.role == "pawn":
                        black_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in black_pawn_attack_list:
                            if p == 'f1' or p == 'g1':
                                return False
                    if i.role == "night":
                        night_attack_list = knight_move(i)
                        for p in night_attack_list:
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
                if i.color == "black":
                    if i.role == "pawn":
                        black_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in black_pawn_attack_list:
                            if p == 'c1' or p == 'd1':
                                return False
                    if i.role == "night":
                        night_attack_list = knight_move(i)
                        for p in night_attack_list:
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

def black_short_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('f8') and square_check('g8'):
            for i in pieces_list:
                if i.color == "black":
                    if i.role == "pawn":
                        black_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in black_pawn_attack_list:
                            if p == 'f8' or p == 'g8':
                                return False
                    if i.role == "night":
                        night_attack_list = knight_move(i)
                        for p in night_attack_list:
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

def black_long_castle(piece, piece2):
    if piece.role == "king" and piece2.role == "rook":
        if piece.king_move_check == False and piece2.rook_move_check == False\
                and square_check('c8') and square_check('d8'): #기본 조건인 킹 움직임과 룩 움직임 그리고 중간 칸이 비었는지 여부 확인
            #공격 하는 기물이 있는지 파악. 칸이 공격당하는 중이면 거짓을 반환
            for i in pieces_list:
                if i.color == "black":
                    if i.role == "pawn":
                        black_pawn_attack_list, dummy_data_1 = white_pawn_move(i)
                        for p in black_pawn_attack_list:
                            if p == 'c8' or p == 'd8':
                                return False
                    if i.role == "night":
                        night_attack_list = knight_move(i)
                        for p in night_attack_list:
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

global check_list_black
global check_list_white

def When_Checked_White(black_piece_list):
    global white_piece_list
    for i in range(len(black_piece_list)):
        if black_piece_list[i].check == True:
            check_list_white = []
            if black_piece_list[i].role == "knight":
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 8<= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))
            if black_piece_list[i].role == "pawn":
                check_list_white = []
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 8<= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))
            if black_piece_list[i].role == "bishop" or "queen":
                attack_list = bishop_move(black_piece_list[i])
                check_list_white = []
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 8<= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))
            if black_piece_list[i].role == "rook" or "queen":
                attack_list = rook_move(black_piece_list[i])
                check_list_white = []
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 8<= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == black_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))

def When_Checked_black(white_piece_list):
    global black_piece_list
    for i in range(len(white_piece_list)):
        if white_piece_list[i].check == True:
            check_list_white = []
            if white_piece_list[i].role == "knight":
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 8 <= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))
            if white_piece_list[i].role == "pawn":
                check_list_white = []
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 8 <= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))
            if white_piece_list[i].role == "bishop" or "queen":
                attack_list = bishop_move(white_piece_list[i])
                check_list_white = []
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 8 <= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))
            if white_piece_list[i].role == "rook" or "queen":
                attack_list = rook_move(white_piece_list[i])
                check_list_white = []
                for x in range(len(white_piece_list)):
                    if 0 <= x <= 7:
                        temp_data, dummy_data = white_pawn_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 8 <= x <= 9:
                        temp_data = knight_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = bishop_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if 10 <= x <= 11:
                        temp_data = rook_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 12:
                        temp_data = queen_move(white_piece_list[x])
                        for y in range(len(temp_data)):
                            if temp_data[y] == white_piece_list[i].pos or temp_data[y] == attack_list:
                                check_list_white.append(temp_data[y])
                    if x == 13:
                        check_list_white.append(king_move(white_piece_list[x]))

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

white_piece_list = [
    white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8, white_night1,
    white_night2, white_bishop1, white_bishop2, white_rook1, white_rook2,white_queen, white_king
]

white_pawn_list = [white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8]

black_pawn_list = [black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8]

black_piece_list = [
    black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, black_night1,
    black_night2, black_bishop1, black_bishop2, black_rook1, black_rook2, black_queen, black_king
]

pieces_list = [
    white_pawn1, white_pawn2, white_pawn3, white_pawn4,white_pawn5, white_pawn6, white_pawn7, white_pawn8, white_night1,
    white_night2, white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen, white_king, black_rook1, black_rook2,
    black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, black_night1,
    black_night2, black_bishop1, black_bishop2, black_queen, black_king
]

while True:

    possible_moves()
    input_move = input("move:", )

    pos = input_move[-2]

    if turn == "white":
        for i in range(len(black_piece_list)):
            if black_piece_list[i].pos == pos:
                black_piece_list[i].active = False
    if turn == "black":
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

    if turn == "black":
        diagnol_pin(black_queen)
        diagnol_pin(black_bishop1)
        diagnol_pin(black_bishop2)
        vertical_pin(black_queen)
        vertical_pin(black_rook1)
        vertical_pin(black_rook2)

    CheckMate(possible_moves())

    turn, turn_count = turn_change(turn)

