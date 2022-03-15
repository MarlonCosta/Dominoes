import random

stock_pcs = []
player_pieces = []
comp_pieces = []
status = None
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


def get_starting_player_and_piece():
    global player_pieces, status, comp_pieces
    max_double_number = -1
    max_double_piece = None

    #   Filtering doubles
    pp_doubles = [p for p in player_pieces if p.is_double()]
    cp_doubles = [p for p in comp_pieces if p.is_double()]

    #   Reshufle if there is no doubles
    while pp_doubles == [] and cp_doubles == []:
        player_pieces, comp_pieces = distribute_pieces(stock_pcs)

    #   Both for loops define the highest double piece on players possession
    for p in pp_doubles:
        if p.greater_side() > max_double_number:
            max_double_number = p.greater_side()
            max_double_piece = p
            status = "computer"

    for p in cp_doubles:
        if p.greater_side() > max_double_number:
            max_double_number = p.greater_side()
            max_double_piece = p
            status = "player"

    # Removes the Domino snake from the player set
    if status == "player":
        comp_pieces.remove(max_double_piece)
    if status == "computer":
        player_pieces.remove(max_double_piece)

    return status, max_double_piece


def distribute_pieces(stock_set: list):
    player_pcs = []
    computer_pcs = []
    for i in range(7):
        player_pcs.append(stock_set.pop(random.randint(0, 27 - i)))
    for j in range(7):
        computer_pcs.append(stock_set.pop(random.randint(0, 20 - j)))
    return player_pcs, computer_pcs


def generate_domino_set():
    domino_set = []
    for i in range(0, 7):
        for j in range(0, 7):
            piece = DominoPiece(i, j)
            if piece not in domino_set:
                domino_set.append(piece)
    return domino_set


def print_interface():
    print("======================================================================")
    print(f"Stock size: {len(stock_pcs)}")
    print(f"Computer pieces: {len(comp_pieces)}\n")
    print(starting_double)
    print("\nYour pieces:")
    [print(f"{count}: {piece}") for count, piece in enumerate(player_pieces, 1)]

    if status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


if __name__ == '__main__':
    stock_pcs = generate_domino_set()
    player_pieces, comp_pieces = distribute_pieces(stock_pcs)
    status, starting_double = get_starting_player_and_piece()
    print_interface()
