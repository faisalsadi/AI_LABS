# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import chess
# import chess.engine
#
# def alpha_beta_search(board, depth, alpha, beta, maximizing_player):
#     if depth == 0 or board.is_checkmate():
#         return chess.evaluate_board(board)
#     if maximizing_player:
#         value = -float("inf")
#         for move in board.legal_moves:
#             board.push(move)
#             value = max(value, alpha_beta_search(board, depth - 1, alpha, beta, False))
#             alpha = max(alpha, value)
#             board.pop()
#             if alpha >= beta:
#                 break
#         return value
#     else:
#         value = float("inf")
#         for move in board.legal_moves:
#             board.push(move)
#             value = min(value, alpha_beta_search(board, depth - 1, alpha, beta, True))
#             beta = min(beta, value)
#             board.pop()
#             if alpha >= beta:
#                 break
#         return value
#
# def find_mate(board, depth):
#     best_move = None
#     best_value = -float("inf")
#     for move in board.legal_moves:
#         board.push(move)
#         value = alpha_beta_search(board, depth - 1, -float("inf"), float("inf"), False)
#         board.pop()
#         if value > best_value:
#             best_value = value
#             best_move = move
#     return best_move
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# def checkmate_in_n_moves(posistion , n):
#     # Create a copy of the board to avoid modifying the original
#     if n == 0:
#         return False
#     board = chess.Board(posistion)
#     moves= list(board.legal_moves)
#     if board.is_checkmate():
#         return  True
#     for move in moves:
#         board.push(move)
#         if checkmate_in_n_moves(board.fen(),n-1):
#             return  True
#         board.pop()
#     return False
#
# # Alpha-beta pruning
# # def alpha_beta_pruning(board, n, alpha, beta):
# #     if n == 0 or board.is_checkmate():
# #         return -1 if board.is_checkmate() else 0
# #     best_value = float('-inf')
# #     for move in board.legal_moves:
# #         board.push(move)
# #         value = -alpha_beta_pruning(board, n-1, -beta, -alpha)
# #         board.pop()
# #         best_value = max(best_value, value)
# #         alpha = max(alpha, value)
# #         if alpha >= beta:
# #             break
# #     return best_value
# #
# # def checkmate_in_n_moves(board, n):
# #     # Move ordering
# #     legal_moves = sorted(board.legal_moves, key=lambda move: board.is_capture(move), reverse=True)
# #     # Transposition tables
# #     trans_table = {}
# #     for move in legal_moves:
# #         board.push(move)
# #         fen = board.fen()
# #         if fen in trans_table:
# #             value = trans_table[fen]
# #         else:
# #             # Quiescence search
# #             if abs(board.evaluation()) < 100:
# #                 value = 0
# #             else:
# #                 value = alpha_beta_pruning(board, n-1, float('-inf'), float('inf'))
# #             trans_table[fen] = value
# #         board.pop()
# #         if value == -1:
# #             return True
# #     return False
#
#
#
#
# def is_mate_in_k_steps(fen, k):
#     board = chess.Board(fen)
#     engine = chess.engine.SimpleEngine.popen_uci("stockfish")
#
#     for i in range(k):
#         if board.is_checkmate():
#             engine.quit()
#             return True
#         if not any(board.generate_legal_moves()):
#             engine.quit()
#             return False
#
#         info = engine.analyse(board, chess.engine.Limit(time=0.100))
#         best_move = info["pv"][0]
#         board.push(best_move)
#
#     engine.quit()
#     return board.is_checkmate()
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#     # board=chess.Board(fen)
#     # print(board)
#     # Example usage:
#     #board = chess.Board(fen)
#     print(is_mate_in_k_steps(fen, 8))
#

##################################################

import chess
import time
PAWN_VALUE = 1
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 9
KING_VALUE = 100

def evaluate_position(board):
  score = 0

  # Material advantage
  score += len(board.pieces(chess.PAWN, chess.WHITE)) * PAWN_VALUE
  score += len(board.pieces(chess.KNIGHT, chess.WHITE)) * KNIGHT_VALUE
  score += len(board.pieces(chess.BISHOP, chess.WHITE)) * BISHOP_VALUE
  score += len(board.pieces(chess.ROOK, chess.WHITE)) * ROOK_VALUE
  score += len(board.pieces(chess.QUEEN, chess.WHITE)) * QUEEN_VALUE

  score -= len(board.pieces(chess.PAWN, chess.BLACK)) * PAWN_VALUE
  score -= len(board.pieces(chess.KNIGHT, chess.BLACK)) * KNIGHT_VALUE
  score -= len(board.pieces(chess.BISHOP, chess.BLACK)) * BISHOP_VALUE
  score -= len(board.pieces(chess.ROOK, chess.BLACK)) * ROOK_VALUE
  score -= len(board.pieces(chess.QUEEN, chess.BLACK)) * QUEEN_VALUE

  # Piece mobility
  score += len(list(board.legal_moves))

  # # King safety
  # king_square = board.king(chess.WHITE)
  # for square in chess.SquareSet(king_square) & board.Attacks[chess.KING]:
  #   if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
  #     score += 1
  #
  # king_square = board.king(chess.BLACK)
  # for square in chess.SquareSet(king_square) & board.Attacks[chess.KING]:
  #   if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
  #     score -= 1
  #
  #
  # # Pawn structure
  # for pawn in board.pieces(chess.PAWN, chess.WHITE):
  #   if board.piece_at(pawn + 1) == chess.Pawn or board.piece_at(pawn - 1) == chess.Pawn:
  #     score += 1
  #
  # for pawn in board.pieces(chess.PAWN, chess.BLACK):
  #   if board.piece_at(pawn + 1) == chess.Pawn or board.piece_at(pawn - 1) == chess.Pawn:
  #     score -= 1

  return score

def minimax(board, depth, alpha, beta, maximizing_player):
  # Check if the game is over or if we have reached the maximum depth
  if board.is_game_over() or depth == 0:
    return evaluate_position(board), None

  # Generate all possible moves from the current position
  moves = list(board.legal_moves)

  # Initialize the best move
  best_move = None

  if maximizing_player:
    # Maximizing player
    best_score = float('-inf')
    for move in moves:
      # Make the move and evaluate the resulting position
      board.push(move)
      score, _ = minimax(board, depth - 1, alpha, beta, False)
      board.pop()

      # Update the best score and move if necessary
      if score > best_score:
        best_score = score
        best_move = move

      # Update alpha if necessary
      alpha = max(alpha, score)

      # Cut off the search if beta <= alpha
      if beta <= alpha:
        break

    return best_score, best_move

  else:
    # Minimizing player
    best_score = float('inf')
    for move in moves:
      # Make the move and evaluate the resulting position
      board.push(move)
      score, _ = minimax(board, depth - 1, alpha, beta, True)
      board.pop()

      # Update the best score and move if necessary
      if score < best_score:
        best_score = score
        best_move = move

      # Update beta if necessary
      beta = min(beta, score)

      # Cut off the search if beta <= alpha
      if beta <= alpha:
        break

    return best_score, best_move

if __name__ == '__main__':
  # Initialize the chess board using the FEN notation
  board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

  # Set the maximum depth for the minimax algorithm
  depth = 5

  start = time.time()
  score, best_move = minimax(board, depth, float('-inf'), float('inf'), True)
  end = time.time()

  # Print the best move and the running time
  print('Best move:', best_move)
  print('Best score:', score)
  print('Running time:', end - start, 'seconds')
