#스테일메이트, 체크 메이트. 폰 움직임

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

def white_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    if piece.active == True or piece.absolute_pin == True:
        return possible_moves
    if row == 2:
        for i in range(2):
            temp_row = row +  1
            square = rc_to_square(temp_row, col)
            if not square_check(square):
                break
            else: possible_moves.append(square)
    temp_row = row + 1
    if in_board(temp_row, col):
        square = rc_to_square(temp_row, col)
        possible_moves.append(square)

    for i in range(-1, 2, 2):
        temp_col = col +  i
        if not in_board(temp_row, temp_col):
            continue
        square = rc_to_square(temp_row, temp_col)
        if color_check(square, piece):
            possible_moves.append(square)
        else:
            for i in range(len(white_piece_list)):
                if white_piece_list[i].pos == square:
                    white_piece_list[i].protected = True

    if row == 5:
        for i in range(-1, 2, 2):
            temp_col = col + i
            if not in_board(temp_row, temp_col):
                continue
            square = rc_to_square(temp_row, temp_col)
            for i in range(len(black_pawn_list)):
                if square == black_pawn_list[i].pos:
                    if black_pawn_list[i].enpassant == True:
                        if in_board(temp_row, temp_col):
                            possible_moves.append(rc_to_square(temp_row, temp_col))
    return possible_moves


def black_pawn_move(piece):
    row, col = square_to_rc(piece.pos)
    possible_moves = []
    if piece.active == True or piece.absolute_pin == True:
        return possible_moves
    if row == 7:
        for i in range(2):
            temp_row = row - 1
            square = rc_to_square(temp_row, col)
            if not square_check(square):
                break
            else:
                possible_moves.append(square)
    temp_row = row - 1
    if in_board(temp_row, col):
        square = rc_to_square(temp_row, col)
        possible_moves.append(square)

    for i in range(-1, 2, 2):
        temp_col = col + i
        if not in_board(temp_row, temp_col):
            continue
        square = rc_to_square(temp_row, temp_col)
        if color_check(square, piece):
            possible_moves.append(square)
        else:
            for i in range(len(white_piece_list)):
                if white_piece_list[i].pos == square:
                    white_piece_list[i].protected = True

    if row ==4:
        for i in range(-1, 2, 2):
            temp_col = col + i
            if not in_board(temp_row, temp_col):
                continue
            square = rc_to_square(temp_row, temp_col)
            for i in range(len(white_pawn_list)):
                if square == white_pawn_list[i].pos:
                    if white_pawn_list[i].enpassant == True:
                        if in_board(temp_row, temp_col):
                            possible_moves.append(rc_to_square(temp_row, temp_col))
    return possible_moves

def promotion():
    if turn == "white":
        for i in range(len(white_pawn_list)):
            row, col = square_to_rc(white_pawn_list[i].pos)
            if  row == 8:
                promotion_list = ["knight", "bishop", "rook", "queen"]
                return promotion_list
    else:
        for i in range(len(black_pawn_list)):
            row, col = square_to_rc(black_pawn_list[i].pos)
            if row == 1:
                promotion_list = ["knight", "bishop", "rook", "queen"]
                return promotion_list

def pawn_two_move(piece, square):
    if piece.role == "pawn":
        row, col = square_to_rc(piece.pos)
        target_row, target_col = square_to_rc(square)
        if abs(row - target_row) == 2:
            piece.enpassant = True

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
    if piece.color == "white":
        if white_short_castle(piece, white_rook1):
            possible_moves.append(rc_to_square(row, col + 2))
        if white_long_castle(piece, white_rook2):
            possible_moves.append(rc_to_square(row, col - 2))
    if piece.color == "black":
        if black_short_castle(piece, black_rook1):
            possible_moves.append(rc_to_square(row, col + 2))
        if black_long_castle(piece, black_rook2):
            possible_moves.append(rc_to_square(row, col - 2))
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

def black_short_castle(piece, piece2):
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

def black_long_castle(piece, piece2):
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

def castle_check(piece, square):
    row, col = square_to_rc(piece.pos)
    target_row, target_col = square_to_rc(square.pos)
    if piece.role == "king":
        if turn == "white":
            if col - target_col == 2:
                white_rook1.pos = "f1"
            if col - target_col == -2:
                white_rook2.pos = "d1"
        else:
            if col - target_col == 2:
                black_rook1.pos = "f8"
            if col - target_col == -2:
                black_rook2.pos = "d8"


def diagonal_pin(piece):
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

def when_checked_white(turn):
    check_pieces = []
    possible_moves = []
    attack_list = []
    if turn == "white":
        for i in range(len(black_piece_list)):
            if black_piece_list[i].check == True:
                check_pieces.append(black_piece_list[i])
                if len(check_pieces) > 1:
                    possible_moves.append(king_move(white_king))
                    return possible_moves
                if black_piece_list[i].role == "pawn":
                    attack_list.append(black_piece_list[i].pos)
                    possible_moves.extend(check_move(attack_list, "white"))
                if black_piece_list[i].role == "knight":
                    attack_list.append(black_piece_list[i].pos)
                    possible_moves.extend(check_move(attack_list, "white"))
                if black_piece_list[i].role == "rook":
                    row, col = square_to_rc(black_piece_list[i])
                    target_row, target_col = square_to_rc(white_king.pos)
                    cal_row = row - target_row
                    cal_col = col - target_col
                    if cal_row != 0:
                        if cal_row < 0:
                            for i in range(len(cal_row) + 1):
                                row += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                        elif cal_row > 0:
                            for i in range(len(cal_row) + 1):
                                row -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_col != 0:
                        if cal_col < 0:
                            for i in range(len(cal_col) + 1):
                                col += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                        elif cal_col > 0:
                            for i in range(len(cal_col) + 1):
                                col -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                if black_piece_list[i].role == "bishop":
                    row, col = square_to_rc(black_piece_list[i])
                    target_row, target_col = square_to_rc(white_king.pos)
                    cal_row = row - target_row
                    cal_col = col - target_col
                    if cal_row < 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row > 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row > 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row < 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                if black_piece_list[i].role == "queen":
                    row, col = square_to_rc(black_piece_list[i])
                    target_row, target_col = square_to_rc(white_king.pos)
                    cal_row = row - target_row
                    cal_col = col - target_col
                    if cal_row < 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row > 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row > 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row < 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "white"))
                    if cal_row != 0:
                        if cal_row < 0:
                            for i in range(len(cal_row) + 1):
                                row += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                        if cal_row > 0:
                            for i in range(len(cal_row) + 1):
                                row -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_col != 0:
                        if cal_col < 0:
                            for i in range(len(cal_col) + 1):
                                col += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                        if cal_col > 0:
                            for i in range(len(cal_col) + 1):
                                col -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                    elif cal_row != 0:
                        if cal_row < 0:
                            for i in range(len(cal_row) + 1):
                                row += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
                        elif cal_row > 0:
                            for i in range(len(cal_row) + 1):
                                row -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "white"))
    if turn == "black":
        for i in range(len(white_piece_list)):
            if white_piece_list[i].check == True:
                check_pieces.append(white_piece_list[i])
                if len(check_pieces) > 1:
                    possible_moves.append(king_move(black_king))
                    return possible_moves
                if white_piece_list[i].role == "pawn":
                    attack_list.append(white_piece_list[i].pos)
                    possible_moves.extend(check_move(attack_list, "black"))
                if white_piece_list[i].role == "knight":
                    attack_list.append(white_piece_list[i].pos)
                    possible_moves.extend(check_move(attack_list, "black"))
                if white_piece_list[i].role == "rook":
                    row, col = square_to_rc(white_piece_list[i])
                    target_row, target_col = square_to_rc(black_king.pos)
                    cal_row = row - target_row
                    cal_col = col - target_col
                    if cal_row != 0:
                        if cal_row < 0:
                            for i in range(len(cal_row) + 1):
                                row += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                        elif cal_row > 0:
                            for i in range(len(cal_row) + 1):
                                row -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_col != 0:
                        if cal_col < 0:
                            for i in range(len(cal_col) + 1):
                                col += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                        elif cal_col > 0:
                            for i in range(len(cal_col) + 1):
                                col -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                if white_piece_list[i].role == "bishop":
                    row, col = square_to_rc(white_piece_list[i])
                    target_row, target_col = square_to_rc(black_king.pos)
                    cal_row = row - target_row
                    cal_col = col - target_col
                    if cal_row < 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row > 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row > 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row < 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                if white_piece_list[i].role == "queen":
                    row, col = square_to_rc(white_piece_list[i])
                    target_row, target_col = square_to_rc(black_king.pos)
                    cal_row = row - target_row
                    cal_col = col - target_col
                    if cal_row < 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row > 0 and cal_col < 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col += i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row > 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row -= i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row < 0 and cal_col > 0:
                        for i in range(len(cal_row) + 1):
                            row += i
                            col -= i
                            square = rc_to_square(row, col)
                            attack_list.append(square)
                            possible_moves.extend(check_move(attack_list, "black"))
                    if cal_row != 0:
                        if cal_row < 0:
                            for i in range(len(cal_row) + 1):
                                row += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                        if cal_row > 0:
                            for i in range(len(cal_row) + 1):
                                row -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_col != 0:
                        if cal_col < 0:
                            for i in range(len(cal_col) + 1):
                                col += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                        if cal_col > 0:
                            for i in range(len(cal_col) + 1):
                                col -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                    elif cal_row != 0:
                        if cal_row < 0:
                            for i in range(len(cal_row) + 1):
                                row += i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
                        elif cal_row > 0:
                            for i in range(len(cal_row) + 1):
                                row -= i
                                square = rc_to_square(row, col)
                                attack_list.append(square)
                                possible_moves.extend(check_move(attack_list, "black"))
    return possible_moves

def check_move(attack_list, color):
    possible_moves = []
    if color == "white":
        for i in range(len(white_piece_list)):
            if white_piece_list[i].role == "pawn":
                piece_move_list = white_pawn_move(white_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if white_piece_list[i].role == "knight":
                piece_move_list = knight_move(white_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if white_piece_list[i].role == "bishop":
                piece_move_list = bishop_move(white_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if white_piece_list[i].role == "rook":
                piece_move_list = rook_move(white_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if white_piece_list[i].role == "queen":
                piece_move_list = queen_move(white_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if white_piece_list[i].role == "king":
                possible_moves.extend(king_move(white_piece_list[i]))
            return possible_moves
    if color == "black":
        for i in range(len(black_piece_list)):
            if black_piece_list[i].role == "pawn":
                piece_move_list = black_pawn_move(black_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if black_piece_list[i].role == "knight":
                piece_move_list = knight_move(black_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if black_piece_list[i].role == "bishop":
                piece_move_list = bishop_move(black_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if black_piece_list[i].role == "rook":
                piece_move_list = rook_move(black_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if black_piece_list[i].role == "queen":
                piece_move_list = queen_move(black_piece_list[i])
                sorted_list = [i for i in piece_move_list if i in attack_list]
                possible_moves.extend(sorted_list)
            if black_piece_list[i].role == "king":
                possible_moves.extend(king_move(black_piece_list[i]))
            return possible_moves

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
        diagonal_pin(white_queen)
        diagonal_pin(white_bishop1)
        diagonal_pin(white_bishop2)
        vertical_pin(white_queen)
        vertical_pin(white_rook1)
        vertical_pin(white_rook2)

    if turn == "white":
        diagonal_pin(white_queen)
        diagonal_pin(white_bishop1)
        diagonal_pin(white_bishop2)
        vertical_pin(white_queen)
        vertical_pin(white_rook1)
        vertical_pin(white_rook2)

    turn, turn_count = turn_change(turn)

