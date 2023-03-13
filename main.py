import os 
import telebot 
import pytube 
 
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
 
bot = telebot.TeleBot(BOT_TOKEN) 
 
 
@bot.message_handler(commands=['start', 'hello']) 
def send_welcome(message): 
    bot.reply_to(message, "Howdy, how are you doing?") 
 
@bot.message_handler(func=lambda msg: True) 
def echo_all(message): 
    if message.text.startswith('https://www.youtube.com'): 
        try: 
            youtube_video = pytube.YouTube(message.text) 
            video_stream = youtube_video.streams.order_by('resolution').desc().first() 
             
            print("VIDEO STREAM: ", video_stream) 
 
            if video_stream is None: 
                bot.reply_to(message, 'Sorry, no video stream available') 
            else: 
                video_stream.download('./') 
                video_title = youtube_video.title 
                video_path = f'./{video_title}.mp4' 
                with open(video_path, 'rb') as video_file: 
                    print("VIDEO FILE: ", video_file)
                    bot.send_document(message.chat.id, video_file, caption="video_title", timeout=60) 
                     
                # os.remove(video_path) 
        except Exception as e: 
            print(str(e)) 
            bot.reply_to(message, 'Sorry, I could not download and send the video') 
    else: 
        bot.reply_to(message, message.text) 
 
bot.infinity_polling()
