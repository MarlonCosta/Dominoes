import random


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
        return self.__repr__()

    def __repr__(self):
        return f"[{self.head}, {self.tail}]"

    def greater_side(self):
        if self.head >= self.tail:
            return self.head
        else:
            return self.tail


class DominoSnake:
    def __init__(self):
        self.head = None
        self.tail = None
        self.pieces = []

    def add_piece(self, piece: DominoPiece, side: str = "+"):
        if side == "-":
            self.pieces.insert(0, piece)
        elif side == "+":
            self.pieces.append(piece)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if len(self.pieces) <= 6:
            return str(self.pieces)
        else:
            return f"{self.pieces[0:2] + ['...'] + self.pieces[-3:]} "


def get_starting_player_and_piece():
    global player_pieces, status, comp_pieces
    max_double_number = -1
    max_double_piece = None

    #   Filtering doubles
    pp_doubles = [p for p in player_pieces if p.is_double()]
    cp_doubles = [p for p in comp_pieces if p.is_double()]

    #   Reshuffle if there is no doubles
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


def get_piece_from_stock():
    if status == "player":
        player_pieces.append(stock_pcs.pop(random.randint(0, len(stock_pcs))))
    if status == "computer":
        comp_pieces.append(stock_pcs.pop(random.randint(0, len(stock_pcs))))


def print_interface():
    print("======================================================================")
    print(f"Stock size: {len(stock_pcs)}")
    print(f"Computer pieces: {len(comp_pieces)}\n")
    print(domino_snake)
    print("\nYour pieces:")
    [print(f"{count}: {piece}") for count, piece in enumerate(player_pieces, 1)]


def computer_move():
    global status
    index = random.randint(0, len(comp_pieces) - 1)
    domino_snake.add_piece(comp_pieces.pop(index), "+" if bool(random.getrandbits(1)) else "-")


def player_move(index: int):
    global status
    if index == 0:
        get_piece_from_stock()
    else:
        domino_snake.add_piece(player_pieces[abs(index) - 1], "+" if index >= 0 else "-")
        player_pieces.remove(player_pieces[abs(index) - 1])
    print_interface()


def take_turn():
    global status
    if status == "player":
        try:
            player_input = int(input("Status: It's your turn to make a move. Enter your command."))
            player_move(player_input)
            status = "computer"
        except ValueError:
            print("Invalid input. Please try again.")
    if status == "computer":
        input("Status: Computer is about to make a move. Press Enter to continue...")
        computer_move()
        status = "player"


def check_victory():
    if len(player_pieces) == 0:
        return "player"
    elif len(comp_pieces) == 0:
        return "computer"
    else:
        return None


def play_game():
    while not check_victory():
        print_interface()
        take_turn()
    else:
        if check_victory() == "player":
            print("Status: The game is over. You won!")
        elif check_victory() == "computer":
            print("Status: The game is over. Computer won!")
        else:
            print()

stock_pcs = []
player_pieces = []
comp_pieces = []
status = None
starting_double = None
domino_snake = DominoSnake()

if __name__ == '__main__':
    stock_pcs = generate_domino_set()
    player_pieces, comp_pieces = distribute_pieces(stock_pcs)
    status, starting_double = get_starting_player_and_piece()
    domino_snake.add_piece(starting_double)
    play_game()
