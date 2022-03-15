import random

stock_pcs = []
player_pieces = []
comp_pieces = []
starting_player = None
starting_double = None


class DominoPiece:
    def __init__(self, head: int, tail: int):
        self.head = head
        self.tail = tail

    def __eq__(self, other):
        return (self.head == other.head and self.tail == other.tail) or (
                self.head == other.tail and self.tail == other.head)

    def is_double(self):
        return self.head == self.tail

    def __str__(self):
        return f"[{self.head}, {self.tail}]"

    def __repr__(self):
        return f"[{self.head}, {self.tail}]"

    def greater_side(self):
        if self.head >= self.tail:
            return self.head
        else:
            return self.tail


def get_starting_piece():
    max_double_number = -1
    max_double_piece = None
    player = None
    global player_pieces
    global comp_pieces

    pp_doubles = [p for p in player_pieces if p.is_double()]
    cp_doubles = [p for p in comp_pieces if p.is_double()]

    while pp_doubles == [] and cp_doubles == []:
        player_pieces, comp_pieces = distribute_pieces(stock_pcs)

    for p in pp_doubles:
        if p.greater_side() > max_double_number:
            max_double_number = p.greater_side()
            max_double_piece = p
            player = "computer"

    for p in cp_doubles:
        if p.greater_side() > max_double_number:
            max_double_number = p.greater_side()
            max_double_piece = p
            player = "player"

    if player == "player":
        comp_pieces.remove(max_double_piece)
    if player == "computer":
        player_pieces.remove(max_double_piece)

    return player, max_double_piece


def distribute_pieces(ss: list):
    pp = []
    cp = []
    for i in range(7):
        pp.append(ss.pop(random.randint(0, 27 - i)))
    for j in range(7):
        cp.append(ss.pop(random.randint(0, 20 - j)))
    return pp, cp


def generate_domino_set():
    domino_set = []
    for i in range(0, 7):
        for j in range(0, 7):
            piece = DominoPiece(i, j)
            if piece not in domino_set:
                domino_set.append(piece)
    return domino_set


if __name__ == '__main__':
    stock_pcs = generate_domino_set()
    player_pieces, comp_pieces = distribute_pieces(stock_pcs)
    starting_player, starting_double = get_starting_piece()

    print("Stock pieces:", stock_pcs)
    print("Computer pieces:", comp_pieces)
    print("Player pieces:", player_pieces)
    print("Domino snake:", [starting_double])
    print("Status:", starting_player)
