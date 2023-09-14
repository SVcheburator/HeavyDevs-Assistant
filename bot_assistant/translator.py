import pickle
from googletrans import Translator
from collections import UserDict
from datetime import datetime
from .user_interaction import ConsoleInteraction
from .activity_chart import Charts, chart_main_func

# Default print and input replacement
print = ConsoleInteraction.user_output
input = ConsoleInteraction.user_input

TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}

LANGS_AVAILIBLE = ["'af': Afrikaans","'sq': Albanian","'am': Amharic","'ar': Arabic","'hy': Armenian","'az': Azerbaijani",
"'eu': Basque","'be': Belarusian","'bn': Bengali","'bs': Bosnian","'bg': Bulgarian","'ca': Catalan",
"'ceb': Cebuano","'ny': Chichewa","'zh-cn': Chinese (Simplified)","'zh-tw': Chinese (Traditional)","'co': Corsican",
"'hr': Croatian","'cs': Czech","'da': Danish","'nl': Dutch","'en': English","'eo': Esperanto","'et': Estonian",
"'tl': Filipino","'fi': Finnish","'fr': French","'fy': Frisian","'gl': Galician",
"'ka': Georgian","'de': German","'el': Greek","'gu': Gujarati","'ht': Haitian Creole","'ha': Hausa",
"'haw': Hawaiian","'iw': Hebrew","'he': Hebrew (Obsolete)","'hi': Hindi","'hmn': Hmong",
"'hu': Hungarian","'is': Icelandic","'ig': Igbo","'id': Indonesian","'ga': Irish","'it': Italian",
"'ja': Japanese","'jw': Javanese","'kn': Kannada","'kk': Kazakh","'km': Khmer","'ko': Korean",
"'ku': Kurdish (Kurmanji)","'ky': Kyrgyz","'lo': Lao","'la': Latin","'lv': Latvian","'lt': Lithuanian",
"'lb': Luxembourgish","'mk': Macedonian","'mg': Malagasy","'ms': Malay","'ml': Malayalam","'mt': Maltese",
"'mi': Maori","'mr': Marathi","'mn': Mongolian","'my': Myanmar (Burmese)","'ne': Nepali","'no': Norwegian",
"'or': Odia (Oriya)","'ps': Pashto","'fa': Persian","'pl': Polish","'pt': Portuguese","'pa': Punjabi",
"'ro': Romanian","'ru': Russian","'sm': Samoan","'gd': Scots Gaelic","'sr': Serbian","'st': Sesotho",
"'sn': Shona","'sd': Sindhi","'si': Sinhala","'sk': Slovak","'sl': Slovenian","'so': Somali",
"'es': Spanish","'su': Sundanese","'sw': Swahili","'sv': Swedish","'tg': Tajik","'ta': Tamil",
"'te': Telugu","'th': Thai","'tr': Turkish","'uk': Ukrainian","'ur': Urdu","'ug': Uyghur",
"'uz': Uzbek","'vi': Vietnamese","'cy': Welsh","'xh': Xhosa","'yi': Yiddish","'yo': Yoruba","'zu': Zulu"]

class TranslationSaves(UserDict):
    def __init__(self, ch) -> None:
        super().__init__()
        self.chart = ch

    def save_translation(self, tr_data_tpl):
        now = datetime.now()
        time_key = str(now.strftime("%Y-%m-%d (%H:%M:%S)"))
        self.data[time_key] = tr_data_tpl
        
    # Autosave functions
    def load_from_file(self, file):
        try:
            with open(file, "rb") as fh:
                self.data = pickle.load(fh)
        except:
            return "The file with saved addressbook not found, corrupted or empty."

    def save_to_file(self, file):
        with open(file, "wb") as fh:
            pickle.dump(self.data, fh)
    
    def __str__(self):
        history = '\n'
        for k, v in self.data.items():
            history += f'{k}:\n{v[0]}\n ↓↓↓\n{v[1]}\n\n'

        return history[:-1]


ch = Charts('Addressbook chart')

tr_s = TranslationSaves(ch)

# Functions
def show_languages():
    for l in LANGS_AVAILIBLE:
        print(l, richprint=True)

def translate_text(text, target_language):
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language)
        tr_s.save_translation((text, translated_text.text))
        tr_s.chart.add_point()
        return translated_text.text
    except Exception as e:
        return TEXT_COLOR['red'] + str(e) + TEXT_COLOR['reset']

def translate_func(inp_split_lst):
    try:
        target_language_brackets = inp_split_lst[1]
        target_language = target_language_brackets.lstrip('(').rstrip(')')
        text = ' '.join(inp_split_lst[2:])
        if len(text) > 0:
            print('\n' + translate_text(str(text), target_language) + '\n')
        else:
            raise IndexError
    except IndexError:
        print(TEXT_COLOR['red'] + "Incorrect input!\nInput should be 'translate_to (*lang*) *your_text*'!" + TEXT_COLOR['reset'])

def translator_main_func():
    tr_s.load_from_file('save_translations.bin')
    print("\nInput 'commands' to see all the commands avalible!\n", richprint=True)

    while True:
        tr_s.save_to_file('save_translations.bin')

        ask = input('>>> ')
        inp_split_lst = ask.split(' ')
        commands = ['translate_to (*lang*) *your_text*', 'show_languages', 'show_history', 'show_chart', 'close', 'exit']
        command = inp_split_lst[0].lower()

        if command == 'translate_to':
            translate_func(inp_split_lst)
        
        elif command == 'commands':
            print('\nCommands avalible:\n')
            for com in commands:
                print("-"+"'"+com+"'", richprint=True)

        elif command == 'show_languages':
            print('\nLanguages avalible:\n')
            show_languages()
            print('\n')
        
        elif command == 'show_history':
            if len(tr_s) > 0:
                print(tr_s)
            else:
                print('\nYour translations history is empty now!\n')
        
        elif command == 'show_chart':
            chart_main_func(ch)

        elif command in commands[-2:]:
            print('\nGood bye!')
            break

        else:
            print(TEXT_COLOR['red'] + f"\nUnknown command ({command})\nInput 'commands' to see all the commands avalible!\n" + TEXT_COLOR['reset'])
