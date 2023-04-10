from telegram.ext import *
from telegram import *
import openai

openai.api_key = "YOUR OPENAI API KEY"          #   Enter your OpenAI Secret Key.
telegram_token = "YOUR TELEGRAM BOT TOKEN"      #   Enter your Telegram Bot Token.
conversation=[{"role": "system", "content": "You are a helpful assistant."}]    #   Defined the assistant role.

def main():
    app = Application.builder().token(telegram_token).build()           #   Created a Telegram app.
    app.add_handler(CommandHandler('start', start_command))             #   Added start_command function.
    app.add_handler(MessageHandler(filters.TEXT, handle_message))       #   Added handle_message function.
    app.add_error_handler(error)                                        #   Added error_handle function.
    app.run_polling()                                                   #   Started the app.

def reply(lastMessage):                                                 #   ChatGPT conversation function
    if(len(conversation)>=7):                                           #   The conversation has a limit. Only assistant role, last 3 messages and last 3 replies are saved. Other messages and replies are deleted.
        conversation.pop(1)
    conversation.append({"role": "user", "content": lastMessage})       #   Added last request.
    completion = openai.ChatCompletion.create(                          #   Sent completion request and received ChatGPT message.                  
        model="gpt-3.5-turbo",                                          #   Used "gpt-3.5-turbo" model. "gpt-4" can also be used.
        messages=conversation,                                          #   Sent all conversation.
        max_tokens=1000                                                 #   Defined as max 1000 tokens. Changeable value.
    )
    lastReply = completion.choices[0].message['content']                #   Read last reply from completion.
    conversation.append({"role": "assistant", "content": lastReply})    #   Added last reply.
    return lastReply                                                    #   Returned last reply.

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text                                     #   Read last Telegram message from user.
    await update.message.reply_text(reply(text))                        #   Sent ChatGPT message to Telegram user.

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! How can I help you?')       #   Replied to Telegram user.

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Error: {context.error}')                                    #   Printed error log.
    await update.message.reply_text('Please wait! If I don\'t respond within a few minutes, try again')     #   Replied to Telegram user.

if __name__ == "__main__":
    main()