from telegram.ext import CommandHandler, Filters, MessageHandler



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


func_to_model = [
    (start, 'start', CommandHandler),
    (echo, Filters.text & (~Filters.command), MessageHandler)
]