import telebot
import win32api
import win32print
import converter
import requests

with open('bot.txt', 'r') as f:
    token = f.read()
bot = telebot.TeleBot(token)
print('Id: ' + str(bot.get_me().id) + ' Name: ' + bot.get_me().first_name)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Привет, пришли мне файл, который необходимо распечатать.')

@bot.message_handler(content_types=['document'])
def print_file(message):
    doc_id = message.document.file_id
    file_info = bot.get_file(doc_id)
    file_format = file_info.file_path.split('.')[1]
    file_name = file_info.file_path.split('/')[-1]

    if file_format == 'txt' or file_format == 'docx' or file_format == 'doc' or file_format == 'pdf':
        download_file(f'http://api.telegram.org/file/bot{token}/{file_info.file_path}')

        currentprinter = win32print.GetDefaultPrinter()
        win32api.ShellExecute(0, "print", file_name, '/d:"%s"' % currentprinter, ".", 0)

        bot.send_message(message.from_user.id, 'распечатывание...')
        print('printnig ' + file_name)
    elif file_format == 'png' or file_format == 'jpg':
        download_file(f'http://api.telegram.org/file/bot{token}/{file_info.file_path}')
        
        converter.convert_img_to_pdf(file_name)
        currentprinter = win32print.GetDefaultPrinter()
        win32api.ShellExecute(0, "print", "converted.pdf", '/d:"%s"' % currentprinter, ".", 0)

        bot.send_message(message.from_user.id, 'распечатывание...')
        print('printnig ' + file_name)
    else:

        bot.send_message(message.from_user.id, 'данный тип файла невозможно распечатать')


def download_file(url):
    local_filename = url.split('/')[-1]
    
    r = requests.get(url,allow_redirects = True)

    open( local_filename, "wb").write(r.content)


bot.polling(True, 0)