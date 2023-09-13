from googletrans import Translator
from .user_interaction import ConsoleInteraction

# Default print and input replacement
print = ConsoleInteraction.user_output
input = ConsoleInteraction.user_input


TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}


def translate_text(text, target_language):
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    except Exception as e:
        return TEXT_COLOR['red'] + str(e) + TEXT_COLOR['reset']


langs_availible = ["'af': Afrikaans","'sq': Albanian","'am': Amharic","'ar': Arabic","'hy': Armenian","'az': Azerbaijani",
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

def show_languages():
    for l in langs_availible:
        print(l, richprint=True)

def translate_func(inp_split_lst):
    target_language_brackets = inp_split_lst[1]
    target_language = target_language_brackets.lstrip('(').rstrip(')')
    text = ' '.join(inp_split_lst[2:])
    print(translate_text(str(text), target_language))


def translator_main_func():
    print("\nInput 'commands' to see all the commands avalible!\n", richprint=True)

    while True:
        ask = input('>>> ')
        inp_split_lst = ask.split(' ')
        commands = ['translate_to', 'show_languages', 'close', 'exit']
        command = inp_split_lst[0].lower()

        if command == 'translate_to':
            translate_func(inp_split_lst)
        
        elif command == 'commands':
            print('\nCommands avalible:\n')
            for com in commands:
                print("-"+"'"+com+"'", richprint=True)
            print('For more information go to README.md\n', richprint=True)

        elif command == 'show_languages':
            print('\nLanguages avalible:\n')
            show_languages()
            print('\n')

        elif command in commands[-2:]:
            print('\nGood bye!')
            break

        else:
            print(TEXT_COLOR['red'] + f"\nUnknown command ({command})\nInput 'commands' to see all the commands avalible!\nFor more information go to README.md\n" + TEXT_COLOR['reset'])
