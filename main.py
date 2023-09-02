import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

MENU, START, PLAYING = range(3)

board = [[" " for _ in range(3)] for _ in range(3)]

current_player = "X"
winner = None

def display_board(update, context):
    text = ""
    for row in board:
        text += " | ".join(row) + "\n"
        text += "---------\n"
    update.message.reply_text(text)

def start_game(update, context):
    global board, current_player, winner
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None
    display_board(update, context)
    update.message.reply_text("Новая игра началась. Ход игрока X.")

def make_move(update, context):
    global board, current_player, winner
    text = update.message.text
    if text.isdigit():
        move = int(text)
        row = (move - 1) // 3
        col = (move - 1) % 3
        if 1 <= move <= 9 and board[row][col] == " ":
            board[row][col] = current_player
            display_board(update, context)
            if check_winner(row, col):
                update.message.reply_text(f"Игрок {current_player} победил!")
                winner = current_player
            elif is_board_full():
                update.message.reply_text("Ничья!")
            else:
                current_player = "O" if current_player == "X" else "X"
                update.message.reply_text(f"Ход игрока {current_player}.")
        else:
            update.message.reply_text("Некорректный ход. Попробуйте ещё раз.")
    else:
        update.message.reply_text("Введите число от 1 до 9.")

def check_winner(row, col):
    if all(board[row][i] == current_player for i in range(3)) or \
       all(board[i][col] == current_player for i in range(3)):
        return True
    if (row == col and all(board[i][i] == current_player for i in range(3))) or \
       (row + col == 2 and all(board[i][2 - i] == current_player for i in range(3))):
        return True
    return False

def is_board_full():
    return all(cell != " " for row in board for cell in row)

def main():
    updater = Updater(token="ключ", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_game))
    dispatcher.add_handler(CommandHandler("help", start_game))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r'^[1-9]$'), make_move)],
        states={},
        fallbacks=[]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
