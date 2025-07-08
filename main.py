from poker.game import Game

game = Game(2, 1000, 40)
winner = game.play_game()
print(f"Winner: {winner}")