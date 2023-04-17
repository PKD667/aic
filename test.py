def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    moves = 0

    while True:
        current_player = players[moves % 2]
        print_board(board)
        print(f"Player {current_player}, make your move (row, col):")

        try:
            row, col = map(int, input().split(","))
        except ValueError:
            print("Invalid input, please enter row and column separated by a comma.")
            continue

        if row < 0 or row > 2 or col < 0 or col > 2 or board[row][col] != " ":
            print("Invalid move, please choose an empty cell within the board.")
            continue

        board[row][col] = current_player
        moves += 1

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if moves == 9:
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()
