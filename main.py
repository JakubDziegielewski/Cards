from poker.game import Game

result = 0
for _ in range(1):
    game = Game(2, 2000, 200)
    winner = game.play_game()
    if winner == 0:
        result += 1
    else:
        result -= 1
print(f"result: {result}")