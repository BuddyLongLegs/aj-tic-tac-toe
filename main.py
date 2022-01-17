# important variables

TOKEN = 'Telegram Token'
SITE = 'Web Server URL'

# initialising bot
import telebot
bot = telebot.TeleBot(TOKEN, threaded = False)
bot.delete_webhook()

# initialising flask app
import os
from flask import Flask,request
app = Flask(__name__)

# setting up logger
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#importing classes
from objects import SinglePlayer, MultiPlayer

# custom filters for bot
def is_admin(message : telebot.types.Message):
    return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']

def is_private(message : telebot.types.Message):
    if message.chat.type == 'private':
    # print(message.chat.type)
        return True
    return False

def getName(message : telebot.types.Message):
    if message.from_user.username :
        name = message.from_user.username
    else:
        name = str(message.from_user.first_name)
        if message.from_user.last_name:
            name += str(message.from_user.last_name)
    return name


"""All Private command handler handlers"""

@bot.message_handler(commands=['start'])
def pStart(message : telebot.types.Message):
    if is_private(message):
        name=getName(message)
        SinglePlayer.new(message.chat.id, name)
        bot.send_message(message.chat.id, "Click /newgame to start a new Tic-Tac-Toe game.")

@bot.message_handler(commands=["newgame"])
def pNewGame(message : telebot.types.Message):
    if is_private(message):
        SinglePlayer.newGame(message.chat.id, getName(message))
        a = SinglePlayer.getBoard(message.chat.id)
        markup = a.inputMarkup()
        bot.send_message(message.chat.id, "Your Turn First", reply_markup=markup)

@bot.message_handler(commands=["help"], )
def pHelp(message : telebot.types.Message):
    if is_private(message):
        bot.send_message(message.chat.id, """
❌⭕❌⭕❌⭕❌⭕
/start   - restart the bot
/newgame - start a new game
/stats   - view stats
/help    - show help 
❌⭕❌⭕❌⭕❌⭕
    """)

@bot.message_handler(commands=["stats"])
def pStats(message : telebot.types.Message):
    if is_private(message):
        sta = SinglePlayer.stats(message.chat.id)
        try:
            wd=((sta['win'])/(sta['games']))
        except ZeroDivisionError:
            wd=0
        bot.send_message(message.chat.id, f"""
❌⭕❌⭕❌⭕❌⭕
```
Games Played   - {sta['games']}
Wins           - {sta['win']}
Ties           - {sta['tie']}
Loses          - {sta['lose']}

Win Ratio      - {"{:.2f}".format(wd)} { '🔥' if (wd>0.19) else ''}{ '🔥' if (wd>0.29) else ''}{ '🔥' if (wd>0.39) else ''}
```
❌⭕❌⭕❌⭕❌⭕
    """)

def pGameLoop(call):
    if call.data == "pass":
        return
    n = int(call.data)
    brd = SinglePlayer.getBoard(call.message.chat.id)
    brd.all_items = [brd.a1, brd.a2, brd.a3, brd.b1, brd.b2, brd.b3, brd.c1, brd.c2, brd.c3]
    if brd.all_items[n-1]==0:
        brd.entry(n, 'X')
        brd.modify(call.message.chat.id)
        check = brd.validate()
        if check == True:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "You won the game! 🥳\n\n Press /newgame to start a New Game.")
            SinglePlayer.win(call.message.chat.id)
        
        elif check == 'Draw':
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "It's a Tie! 🙄\n\n Press /newgame to start a New Game.")
            SinglePlayer.tie(call.message.chat.id)

        else:
            bot.edit_message_text("Bot's Turn", call.message.chat.id, call.message.id, reply_markup=brd.inputMarkup(no_input=True))
            brd.ai_move()
            brd.modify(call.message.chat.id)
            bot_check = brd.validate()
            if bot_check == True:
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, "You won the game! 🥳\n\n Press /newgame to start a New Game.")
                SinglePlayer.win(call.message.chat.id)
            elif bot_check == "Lose":
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, "Oops, You lost! 😟\n\n Press /newgame to start a New Game.")
                SinglePlayer.lose(call.message.chat.id)
            
            elif bot_check == False:
                bot.edit_message_text("Your Turn", call.message.chat.id, call.message.id, reply_markup=brd.inputMarkup())

            else:
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, "It's a Tie! 🙄\n\n Press /newgame to start a New Game.")
                SinglePlayer.tie(call.message.chat.id)

@bot.callback_query_handler(func=lambda call:True)
def call_back_director(call):
    if is_private(call.message):
        pGameLoop(call)
    else:
        pass


"""!!! for development only !!!"""
# bot.infinity_polling()

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    try:
        bot.remove_webhook()
        bot.set_webhook(url=(SITE + TOKEN))
    except Exception:
        pass
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=(SITE + TOKEN))
    return "HIIII", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))