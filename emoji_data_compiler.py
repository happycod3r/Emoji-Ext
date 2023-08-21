# file_parsers.py
from emoji_data.data_dict import EMOJI_DATA, LANGUAGES
from core import is_emoji
import unicodedata
import os
import re


_CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

def _create_data_file(path: str):
    if os.path.exists(path):
        with open(path, 'w') as file:
            file.close()
            return True
    with open(path, 'x') as file:
        file.close()
        return True 

def _write_data(data: str, output_file: str):
    if os.path.exists(output_file):
        with open(output_file, "a", encoding="utf-8") as outfile:
            outfile.write(data)
            outfile.close()
            return True
    return False  

def _unicode(emojis):
    emoji_string = emojis
    unicode_values = []
    for i in range(0, len(emoji_string)):
        unicode_values.append(ord(emoji_string[i].encode('utf-16', 'surrogatepass').decode('utf-16')))
    unicode_strings = []
    for codepoint in unicode_values:
        unicode_strings.append(f"U+{codepoint:04X}")        
    return unicode_strings

def _escape_sequence(emoji):
    escape_sequence = f""
    if emoji is not None:
        if len(emoji) > 1:
            for i, char in enumerate(emoji):
                unicode_code_point = ord(emoji[i])
                escape_sequence += f"\\U{unicode_code_point:08X} "
            return escape_sequence  
        unicode_code_point = ord(emoji[0])
        escape_sequence = f"\\U{unicode_code_point:08X}"
        return escape_sequence

def translate_emoji_name(lang):
    return {emj: EMOJI_DATA[emj][lang] for emj in EMOJI_DATA if lang in EMOJI_DATA[emj]}

def adapt_emoji_name(text: str, lang: str, emj: str) -> str:
    # Use NFKC-form (single character instead of character + diacritic)
    # Unicode.org files should be formatted like this anyway, but emojiterra is not consistent
    text = unicodedata.normalize('NFKC', text)

    # Fix German clock times "12:30 Uhr" -> "12.30 Uhr"
    text = re.sub(r"(\d+):(\d+)", r"\1.\2", text)

    # Remove white space
    text = "_".join(text.split(" "))

    emoji_name = ":" + (
        text
        .lower()
        .removeprefix("flag:_")
        .replace(":", "")
        .replace(",", "")
        .replace('"', "")
        .replace("\u201e", "")
        .replace("\u201f", "")
        .replace("\u202f", "")
        .replace("\u229b", "")
        .replace("\u2013", "-")
        .replace(",_", ",")
        .strip()
        .replace(" ", "_")
        .replace("_-_", "-")
    ) + ":"

    if lang == "de":
        emoji_name = emoji_name.replace("\u201c", "").replace("\u201d", "")
        emoji_name = re.sub(r"(hautfarbe)_und_([a-z]+_hautfarbe)", r"\1,\2", emoji_name)

    if lang == "fa":
        emoji_name = emoji_name.replace('\u200c', "_")
        emoji_name = emoji_name.replace('\u200f', "_")
        emoji_name = emoji_name.replace('\u060c', "_")
        emoji_name = re.sub("_+", "_", emoji_name)

    if lang == "zh":
        emoji_name = ":" + (
            text
            .replace(":", "")
            .replace(",", "")
            .replace('-', "")
            .replace("\u201e", "")
            .replace("\u201f", "")
            .replace("\u202f", "")
            .replace("\u229b", "")
            .replace(",_", ",")
            .strip()
            .replace(" ", "_")
        ) + ":"

        if '日文' in emoji_name:
            # Japanese buttons
            emoji_name = emoji_name.replace('日文的', '').replace('按钮', '').replace('“', '').replace('”', '')

        if '箭头' in emoji_name:
            # Arrows
            emoji_name = emoji_name.replace('_', '').replace('!', '')

        if '按钮' in emoji_name:
            # English buttons
            emoji_name = emoji_name.replace('_', '')

        if '型血' in emoji_name:
            emoji_name = emoji_name.replace('_', '')

        if '中等-' in emoji_name:
            emoji_name = emoji_name.replace('中等-', '中等')

        if emoji_name.startswith(':旗_'):
            # Countries
            emoji_name = emoji_name.replace(':旗_', ':')

        hardcoded = {
            '\U0001f1ed\U0001f1f0': ':香港:',  # 🇭🇰
            '\U0001f1ee\U0001f1e9': ':印度尼西亞:',  # 🇮🇩
            '\U0001f1f0\U0001f1ff': ':哈薩克:',  # 🇰🇿
            '\U0001f1f2\U0001f1f4': ':澳門:',  # 🇲🇴
            '\U0001f1e8\U0001f1ec': ':刚果_布:',  # 🇨🇬
            '\U0001f1e8\U0001f1e9': ':刚果_金:',  # 🇨🇩
            '\U0001f193': ':FREE按钮:',  # 🆓
            '\U0001f238': ':申:',  # 🈸
            '\U0001f250': ':得:',  # 🉐
            '\U0001f22f': ':指:',  # 🈯
            '\U0001f232': ':禁:',  # 🈲
            '\u3297\ufe0f': ':祝:',  # ㊗️
            '\u3297': ':祝:',  # ㊗
            '\U0001f239': ':割:',  # 🈹
            '\U0001f21a': ':无:',  # 🈚
            '\U0001f237\ufe0f': ':月:',  # 🈷️
            '\U0001f237': ':月:',  # 🈷
            '\U0001f235': ':满:',  # 🈵
            '\U0001f236': ':有:',  # 🈶
            '\U0001f234': ':合:',  # 🈴
            '\u3299\ufe0f': ':秘:',  # ㊙️
            '\u3299': ':秘:',  # ㊙
            '\U0001f233': ':空:',  # 🈳
            '\U0001f251': ':可:',  # 🉑
            '\U0001F23A': ':营:',  # 🈺
            '\U0001F202\ufe0f': ':服务:',  # 🈂️
            '\U0001F202': ':服务:',  # 🈂
        }

        if emj in hardcoded:
            emoji_name = hardcoded[emj]

    emoji_name = (emoji_name
        .replace("____", "_")
        .replace("___", "_")
        .replace("__", "_")
        .replace("--", "-"))

    return emoji_name

EMOJIS = {}

def _extract_emoji_test_data_from_file(emoji_test_txt: str):
    
    """
    Extracts emoji data line by line to dict
    
    This function parses the emoji-test.txt file found on Unicode.org at
    https://unicode.org/Public/emoji/latest/emoji-test.txt
    
    The parser generates a string representation of a dictionary containing the data from t
    he emoji-test.txt file for each emoji and yields the dict representation string to be
    printed or written to file. 
    
    Each emoji is stored in a dictionary with the following keys and value
    types:
    
    "\U0001F600": {  # 😀
        "index": "1",
        "group": "Smileys & Emotion",
        "subgroup": "face-smiling",
        "status": fully_qualified,
        "emoji": "😀",
        "e": 1.0,
        "unicodes": ['U+1F600'],
        "codepoints": ['1F600'],
        "sequences": ['\\U0001F600'],
        "category": "So",
        "name": ":grinning_face:",
        "en": ":grinning_face:",
        "es": ":cara_sonriendo:",
        "ja": ":にっこり笑う:",
        "ko": ":활짝_웃는_얼굴:",
        "pt": ":rosto_risonho:",
        "it": ":faccina_con_un_gran_sorriso:",
        "fr": ":visage_rieur:",
        "de": ":grinsendes_gesicht:",
        "fa": ":خنده:",
        "id": ":wajah_gembira:",
        "zh": ":嘿嘿:",
    """
   
    current_group = None
    current_subgroup = None
    current_status = None
    current_codepoint = None
    current_emoji = None
    current_version = None
    current_emoji_name = None
    real_index = 0 # The index of the line we actually start counting from.
    
    with open(emoji_test_txt, 'r', encoding='utf-8') as file:
        
        for current_line, line in enumerate(file):
            
            line = line.strip()

            # Get the group...
            if line.startswith("# group:"):
                current_group = line.split("# group:")[1].strip()
                EMOJIS[current_group] = {}
            # Get subgroup...
            elif line.startswith("# subgroup:"):
                current_subgroup = line.split("# subgroup:")[1].strip()
                EMOJIS  [current_group][current_subgroup] = {}
            # Get the codepoint and status...
            elif line.startswith(("0", "1", "2", "3")):
                line_parts = line.split(";")
                current_codepoint = line_parts[0].strip()
                line_data = line_parts[1].strip().split(" ")
                current_status = line_data[0].strip().replace("-", "_")
                
                emj_name = ""
                for item in line_data:
                    # Get the emoji...
                    if is_emoji(item):
                        current_emoji = item
                    # Get the version...
                    elif item.startswith("E") and item[1].isdigit(): # Account for any names that may start with "E"
                        item_parts = item.strip().split("E")
                        for part in item_parts:
                            if part == "":
                                continue
                            if part[0].isdigit():
                                current_version = part
                    elif item == '' or item == '#':
                        continue
                    elif item == "component" or item == "fully-qualified" or item == "minimally-qualified" or item == "unqualified":
                        continue
                    # Get the emoji name...
                    elif item == "flag:":
                        emj_name += item
                    elif item.startswith("_"): #--\
                        emj_name += item           #-- So we don't end up with names like this: _some__emoji_name__
                    elif item.endswith("_"):   #--/  
                        emj_name += item
                    else:
                        emj_name += f"_{item.strip()}" # Everything left over is the name
                        
                current_emoji_name = emj_name
                
                if current_emoji_name.startswith("_"):
                    current_emoji_name = current_emoji_name.lstrip("_")     
                current_emoji_name = adapt_emoji_name(current_emoji_name, "en", current_emoji)
           
                
            # Filter out the file header section
            if current_line < 35: # Table data starts on line #35.
                continue
            
            real_index = real_index + 1
            
            if current_emoji is not None: 
                emoji_sequence = _escape_sequence(current_emoji)
                sequence_string = ""
                
                for sequence in emoji_sequence.strip().split(" "):
                    sequence_string += sequence
                
                emoji_sequence = sequence_string
                
                # Compile the data...
                EMOJIS[emoji_sequence] = {}
                EMOJIS[emoji_sequence]["index"] = real_index
                EMOJIS[emoji_sequence]["group"] = current_group
                EMOJIS[emoji_sequence]["subgroup"] = current_subgroup
                EMOJIS[emoji_sequence]["status"] = current_status
                EMOJIS[emoji_sequence]["emoji"] = current_emoji
                EMOJIS[emoji_sequence]["e"] = current_version
                EMOJIS[emoji_sequence]["unicodes"] = _unicode(current_emoji)
                EMOJIS[emoji_sequence]["codepoints"] = current_codepoint.split(" ")
                EMOJIS[emoji_sequence]["sequences"] = emoji_sequence.split(" ")
                EMOJIS[emoji_sequence]["category"] = unicodedata.category(current_emoji[0])
                EMOJIS[emoji_sequence]["name"] = current_emoji_name
                
                # Get the name in different langauges
                LANG_STRING = f""
                for lang in LANGUAGES:
                    emoji_in_langs = translate_emoji_name(lang)
                    if current_emoji in emoji_in_langs:
                        emoji_name_in_lang = (emoji_in_langs[current_emoji])
                        EMOJIS[emoji_sequence][lang] = emoji_name_in_lang
                        LANG_STRING += f"""        "{lang}": "{emoji_name_in_lang }",\n"""
                 
                DATA = f"""    "{emoji_sequence}": {{  # {current_emoji}
        "index": "{real_index}",
        "group": "{current_group}",
        "subgroup": "{current_subgroup}",
        "status": {current_status},
        "emoji": "{current_emoji}",
        "e": {current_version},
        "unicodes": {_unicode(current_emoji)},
        "codepoints": {current_codepoint.split(" ")},
        "sequences": {emoji_sequence.split(" ")},
        "category": "{unicodedata.category(current_emoji[0])}",
        "name": "{current_emoji_name}",
{LANG_STRING}
    }},\n"""
                
                yield [DATA, [real_index, current_group, current_subgroup, current_status,
                              current_emoji, current_version, current_emoji_name,
                              _unicode(current_emoji), current_codepoint.split(" "),
                              emoji_sequence.split(" ")], unicodedata.category(current_emoji[0])]

def construct_data_file():
    emoji_test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "emoji_data")
    emoji_test_file = os.path.join(emoji_test_file, "emoji-v15-data")
    emoji_test_file = os.path.join(emoji_test_file, "emoji-test.txt")
    output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "emoji_data")
    output_path = os.path.join(output_path, "data_dict.py")

    _create_data_file(output_path)

    _write_data(
"""
# emoji-v15-data-dict.py
# 💥 💤
# !!! ⚠️ DO NOT EDIT THIS FILE ⚠️ !!!
# Don't edit this file or things will 💥 and this module will be 💤💤💤 ...
# unless you know what you're doing! This file is used by other parts of the 
# module and you may and probably will encounter errors when trying to update 
# or regenerate it later. You wil also encounter errors with the modules
# core functions.
#
# This file is automatically generated by running emoji_data_compiler.py
# It builds on the original EMOJI_DATA dict which can be found in the 
# emoji module http://github.com/carpedm20/emoji and contains a dictionary 
# holding all current emoji data and properties.
# 
# This data was extracted from the following files which can be found on 
# Unicode.org at:
#   🔹https://unicode.org/Public/emoji/latest/emoji-test.txt
#   🔹https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt
#
# The emoji-test.txt file 
# https://unicode.org/Public/emoji/latest/emoji-test.txt or you can run 
# the download_emoji_test_data function in utils/download_emoji_data.py to
# download the latest files. 
# 
# Once you download the latest data from Unicode.org you can run 
# emoji_data_comiler.py to recompile this file and regenerate the EMOJIS dict
# with updated information.
#                           
#  Emoji Version Info: http://www.unicode.org/reports/tr51/#Versioning
#  +----------------+-------------+------------------+-------------------+
#  | Emoji Version  |    Date     | Unicode Version  | Data File Comment |
#  +----------------+-------------+------------------+-------------------+
#  | N/A            | 2010-10-11  | Unicode 6.0      | E0.6              |
#  | N/A            | 2014-06-16  | Unicode 7.0      | E0.7              |
#  | Emoji 1.0      | 2015-06-09  | Unicode 8.0      | E1.0              |
#  | Emoji 2.0      | 2015-11-12  | Unicode 8.0      | E2.0              |
#  | Emoji 3.0      | 2016-06-03  | Unicode 9.0      | E3.0              |
#  | Emoji 4.0      | 2016-11-22  | Unicode 9.0      | E4.0              |
#  | Emoji 5.0      | 2017-06-20  | Unicode 10.0     | E5.0              |
#  | Emoji 11.0     | 2018-05-21  | Unicode 11.0     | E11.0             |
#  | Emoji 12.0     | 2019-03-05  | Unicode 12.0     | E12.0             |
#  | Emoji 12.1     | 2019-10-21  | Unicode 12.1     | E12.1             |
#  | Emoji 13.0     | 2020-03-10  | Unicode 13.0     | E13.0             |
#  | Emoji 13.1     | 2020-09-15  | Unicode 13.0     | E13.1             |
#  | Emoji 14.0     | 2021-09-14  | Unicode 14.0     | E14.0             |
#  | Emoji 15.0     | 2022-09-13  | Unicode 15.0     | E15.0 <-- current |
#  +---------------------------------------------------------------------+

__all__ = [
    'STATUS' , 'LANGUAGES', 'EMOJI_CATEGORIES', 'EMOJI_DATA', 'BASIC_EMOJIS'
]             

component = 1
fully_qualified = 2
minimally_qualified = 3
unqualified = 4

STATUS = {
    "component": component,
    "fully_qualified": fully_qualified,
    "minimally_qualified": minimally_qualified,
    "unqualified": unqualified
}

LANGUAGES = ['en', 'es', 'ja', 'ko', 'pt', 'it', 'fr', 'de', 'fa', 'id', 'zh']

EMOJI_CATEGORIES = {
    "smileys": [
        "smiling_and_affectionate",
        "tongues_hands_and_accessories",
        "neutral_and_skeptical",
        "sleepy_and_unwell",
        "concerned_and_negative",
        "costume_creature_and_animal"
    ],     
    "people": [
        "hands_and_body_parts",
        "people_and_appearance",
        "gestures_and_expressions",
        "activities_and_sports",
        "professions_roles_and_fantasies",
        "families_couples"
    ], 
    "animals_and_nature": [
        "mammals_and_marsupials",
        "birds",
        "marine_and_reptiles",
        "bugs",
        "plants_flowers_and_nature",
        "sky_and_weather"
    ], 
    "food_and_drink": [
        "fruits",
        "vegetables",
        "prepared_foods",
        "asian_foods",
        "sweets_and_deserts",
        "drinks_and_dishware"
    ],
    "activity": [
        "events_and_celebration",
        "sports_and_awards",
        "games_and_culture"
    ],
    "travel_and_places": [
        "maps_and_geography",
        "buildings_and_places",
        "land_travel",
        "air_and_sea_travel"
    ], 
    "objects": [
        "clothing_and_appearence",
        "music_and_sound",
        "it_and_av",
        "office_and_stationary",
        "money_and_time",
        "tools_and_household_items"
    ],
    "symbols": [
        "hearts_shapes_and_emotions",
        "locations_and_warning",
        "arrows_and_av",
        "identities_and_beliefs",
        "alphanumerics",
        "other_symbols"
    ],
    "flags": [
        "color_and_identity",
        "africa",
        "the_americas",
        "asia_and_the_middle_east",
        "europe",
        "oceania_island_nations_and_territories"
    ]
}

BASIC_EMOJIS = {
    "smileys": {
        "smiling_and_affectionate": [
        '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '😉', 
        '😊', '😇', '🥰', '😍', '🤩', '😘', '😗', '😚', '😙', '🥲', 
        '😏'
        ],
        "tongues_hands_and_accessories": [
        '😋', '😛', '😜', '🤪', '😝', '🤗', '🤭', '🫢', '🫣', '🤫',
        '🤔', '🫡', '🤤', '🤠', '🥳', '🥸', '😎', '🤓', '🧐'
        ],
        "neutral_and_skeptical": [
        '🙃', '🫠', '🤐', '🤨', '😐', '😑', '😶', '🫥', '😶‍🌫️', '😒',
        '🙄', '😬', '😮‍💨', '🤥'
        ],
        "sleepy_and_unwell": [
        '😌', '😔', '😪', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧',
        '🥵', '🥶', '🥴', '😵', '😵‍💫', '🤯', '🥱'
        ],
        "concerned_and_negative": [
        '😕', '🫤', '😟', '🙁', '☹️', '😮', '😯', '😲', '😳', '🥺',
        '🥹', '😦', '😧', '😨', '😰', '😥', '😢', '😭', '😱', '😖',
        '😣', '😞', '😓', '😩', '😫', '😤', '😡', '😠', '🤬', '👿'
        ],
        "costume_creature_and_animal": [
        '😈', '👿', '💀', '☠️', '💩', '🤡', '👹', '👺', '👻', '👽', 
        '👾', '🤖', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿',
        '😾', '🙈', '🙉', '🙊'
        ]
    },
    "people": {
        "hands_and_body_parts": [
            '👋', '🤚', '🖐️', '✋', '🖖', '🫱', '🫲', '🫳', '🫴', '👌',
            '🤌', '🤏', '✌️', '🤞', '🫰', '🤟', '🤘', '🤙', '👈', '👉',
            '👆', '🖕', '👇', '☝️', '🫵', '👍', '👎', '✊', '👊', '🤛',
            '🤜', '👏', '🙌', '🫶', '👐', '🤲', '🤝', '🙏', '✍️', '💅',
            '🤳', '💪', '🦾', '🦿', '🦵', '🦶', '👂', '🦻', '👃', '🧠',
            '🫀', '🫁', '🦷', '🦴', '👀', '👅', '👄', '🫦', '👣', '🧬', 
            '🩸'
        ],
        "people_and_appearance": [
            '👶', '🧒', '👦', '👧', '🧑', '👱', '👨', '🧔', '🧔‍♂️', '🧔‍♀️',
            '👨‍🦰', '👨‍🦱', '👨‍🦳', '👨‍🦲', '👩', '👩‍🦰', '🧑‍🦰', '👩‍🦱', '🧑‍🦱', '👩‍🦳',
            '🧑‍🦳', '👩‍🦲', '🧑‍🦲', '👱‍♀️', '👱‍♂️', '🧓', '👴', '👵', '🧏', '🧏‍♂️',
            '🧏‍♀️', '👳', '👳‍♂️', '👳‍♀️', '👲', '🧕', '🤰', '🫃', '🫄', '👼',
            '🗣️', '👤', '👥', '🦰', '🦱', '🦳', '🦲'
        ],
        "gestures_and_expressions": [
            '🙍‍♂️', '🙍‍♀️', '🙎', '🙎‍♂️', '🙎‍♀️', '🙅', '🙅‍♂️', '🙅‍♀️', '🙆', '🙆‍♂️',
            '🙆‍♀️', '💁', '💁‍♂️', '💁‍♀️', '🙋', '🙋‍♂️', '🙋‍♀️', '🧏', '🧏‍♂️', '🧏‍♀️',
            '🙇', '🙇‍♂️', '🙇‍♀️', '🤦', '🤦‍♂️', '🤦‍♀️', '🤷', '🤷‍♂️', '🤷‍♀️'
        ],
        "activities_and_sports": [
            '🤱', '👩‍🍼', '🧑‍🍼', '💆', '💆‍♂️', '💆‍♀️', '💇', '💇‍♂️', '💇‍♀️', '🚶',
            '🚶‍♂️', '🚶‍♀️', '🧍', '🧍‍♂️', '🧍‍♀️', '🧎', '🧎‍♂️', '🧎‍♀️', '🧑‍🦯', '👨‍🦯',
            '👩‍🦯', '🧑‍🦼', '👨‍🦼', '👩‍🦼', '🧑‍🦽', '👨‍🦽', '👩‍🦽', '🏃', '🏃‍♂️', '🏃‍♀️',
            '💃', '🕺', '🕴️', '👯', '👯‍♂️', '👯‍♀️', '🧖', '🧖‍♂️', '🧖‍♀️', '🧗',
            '🧗‍♂️', '🧗‍♀️', '🤺', '🏇', '⛷️', '🏂', '🏌️', '🏌️‍♂️', '🏌️‍♀️', '🏄',
            '🏄‍♂️', '🏄‍♀️', '🚣', '🚣‍♂️', '🚣‍♀️', '🏊', '🏊‍♂️', '🏊‍♀️', '⛹️', '⛹️‍♂️',
            '⛹️‍♀️', '🏋️', '🏋️‍♂️', '🏋️‍♀️', '🚴', '🚴‍♂️', '🚴‍♀️', '🚵', '🚵‍♂️', '🚵‍♀️',
            '🤸', '🤸‍♂️', '🤸‍♀️', '🤼', '🤼‍♂️', '🤼‍♀️', '🤽', '🤽‍♂️', '🤽‍♀️', '🤾',
            '🤾‍♂️', '🤾‍♀️', '🤹', '🤹‍♂️', '🤹‍♀️', '🧘', '🧘‍♂️', '🧘‍♀️', '🛀', '🛌'   
        ],
        "professions_roles_and_fantasies": [
            '🧑‍⚕️', '👨‍⚕️', '👩‍⚕️', '🧑‍🎓', '👨‍🎓', '👩‍🎓', '🧑‍🏫', '👨‍🏫', '👩‍🏫', '🧑‍⚖️',
            '👨‍⚖️', '👩‍⚖️', '🧑‍🌾', '👨‍🌾', '👩‍🌾', '🧑‍🍳', '👨‍🍳', '👩‍🍳', '🧑‍🔧', '👨‍🔧',
            '👩‍🔧', '🧑‍🏭', '👨‍🏭', '👩‍🏭', '🧑‍💼', '👨‍💼', '👩‍💼', '🧑‍🔬', '👨‍🔬', '👩‍🔬',
            '🧑‍💻', '👨‍💻', '👩‍💻', '🧑‍🎤', '👨‍🎤', '👩‍🎤', '🧑‍🎨', '👨‍🎨', '👩‍🎨', '🧑‍✈️',
            '👨‍✈️', '🧑‍🚀', '👨‍🚀', '👩‍🚀', '🧑‍🚒', '👨‍🚒', '👩‍🚒', '👮', '👮‍♂️', '👮‍♀️',
            '🕵️', '🕵️‍♂️', '🕵️‍♀️', '💂', '💂‍♂️', '💂‍♀️', '🥷', '👷', '👷‍♂️', '👷‍♀️',
            '🫅', '🤴', '👸', '🤵', '🤵‍♂️', '🤵‍♀️', '👰', '👰‍♂️', '👰‍♀️', '🎅',
            '🤶', '🧑‍🎄', '🦸', '🦸‍♂️', '🦸‍♀️', '🦹', '🦹‍♂️', '🦹‍♀️', '🧙', '🧙‍♂️',
            '🧙‍♀️', '🧚', '🧚‍♂️', '🧚‍♀️', '🧛', '🧛‍♂️', '🧛‍♀️', '🧜', '🧜‍♂️', '🧜‍♀️',
            '🧝', '🧝‍♂️', '🧝‍♀️', '🧞', '🧞‍♂️', '🧞‍♀️', '🧟', '🧟‍♂️', '🧟‍♀️', '🧌',
            '👯', '👯‍♂️', '👯‍♀️'
        ],
        "families_couples": [
            '🧑‍🤝‍🧑', '👭', '👫', '👬', '💏',
            '👩‍❤️‍💋‍👨', '👨‍❤️‍💋‍👨', '👩‍❤️‍💋‍👩', '💑', '👩‍❤️‍👨',
            '👨‍❤️‍👨', '👩‍❤️‍👩', '👪', '👨‍👩‍👦', '👨‍👩‍👧',
            '👨‍👩‍👧‍👦', '👨‍👩‍👦‍👦', '👨‍👩‍👧‍👧', '👨‍👨‍👦', '👨‍👨‍👧',
            '👨‍👨‍👧‍👦', '👨‍👨‍👦‍👦', '👨‍👨‍👧‍👧', '👩‍👩‍👦', '👩‍👩‍👧',
            '👩‍👩‍👧‍👦', '👩‍👩‍👦‍👦', '👩‍👩‍👧‍👧', '👨‍👦', '👨‍👦‍👦',
            '👨‍👧', '👨‍👧‍👦', '👨‍👧‍👧', '👩‍👦', '👩‍👦‍👦', '👩‍👧',
            '👩‍👧‍👦', '👩‍👧‍👧', '👩‍👨‍👧‍👧', '👩‍👦‍👧', '👩‍👨‍👦‍👦',
            '👨‍👨‍👦‍👧', '👩‍👨‍👧‍👦', '👨‍👦‍👧', '👩‍👨‍👦', '👩‍👩‍👦‍👧',
            '👩‍👨‍👦‍👧', '👩‍👨‍👧', '👨‍👩‍👦‍👧'
        ]
    },
    "animals_and_nature": {
        "mammals_and_marsupials": [
            '🐵', '🐒', '🦍', '🦧', '🐶', '🐕', '🦮', '🐕‍🦺', '🐩', '🐺',
            '🦊', '🦝', '🐱', '🐈', '🐈‍⬛', '🦁', '🐯', '🐅', '🐆', '🐴',
            '🐎', '🦄', '🦓', '🦌', '🦬', '🐮', '🐂', '🐃', '🐄', '🐷', 
            '🐖', '🐗', '🐽', '🐏', '🐑', '🐐', '🐪', '🐫', '🦙', '🦒', 
            '🐘', '🦣', '🦏', '🦛', '🐭', '🐁', '🐀', '🐹', '🐰', '🐇', 
            '🐿️', '🦫', '🦔', '🦇', '🐻', '🐻‍❄️', '🐨', '🐼', '🦥', '🦦', 
            '🦨', '🦘', '🦡', '🐾'
        ],
        "birds": [
            '🦃', '🐔', '🐓', '🐣', '🐤', '🐥', '🐦', '🐦', '🐧', '🕊️',
            '🦅', '🦆', '🦢', '🦉', '🦤', '🪶', '🦩', '🦚', '🦜', '🪹', 
            '🪺'
        ],
        "marine_and_reptiles": [
            '🐸', '🐊', '🐢', '🦎', '🐍', '🐲', '🐉', '🦕', '🦖', '🐳',
            '🐋', '🐬', '🦭', '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🪸', 
            '🦀', '🦞', '🦐', '🦑', '🦪'
        ],
        "bugs": [
            '🐌', '🦋', '🐛', '🐜', '🐝', '🪲', '🐞', '🦗', '🪳', '🕷️',
            '🕸️', '🦂', '🦟', '🪰', '🪱', '🦠'
        ],
        "plants_flowers_and_nature": [
            '💐', '🌸', '💮', '🪷', '🏵️', '🌹', '🥀', '🌺', '🌻', '🌼', 
            '🌷', '🌱', '🪴', '🌲', '🌳', '🌴', '🌵', '🌾', '🌿', '☘️', 
            '🍀', '🍁', '🍂', '🍃', '🍄', '🪨', '🪵'
        ],
        "sky_and_weather": [
            '❤️‍🔥', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙',
            '🌚', '🌛', '🌜', '☀️', '🌝', '🌞', '🪐', '⭐', '🌟', '🌠',
            '🌌', '☁️', '⛅', '⛈️', '🌤️', '🌥️', '🌦️', '🌧️', '🌨️', '🌩️',
            '🌪️', '🌫️', '🌬️', '🌀', '🌈', '🌂', '☂️', '☔', '⛱️', '⚡',
            '❄️', '☃️', '⛄', '☄️', '💧', '🌊' 
        ]
    },
    "food_and_drink": {
        "fruits": [
            '🍇', '🍈', '🍉', '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍏',
            '🍐', '🍑', '🍒', '🍓', '🫐', '🥝', '🍅', '🫒', '🥥'
        ],
        "vegetables": [
            '🥑', '🍆', '🥔', '🥕', '🌽', '🌶️', '🫑', '🥒', '🥬', '🥦', 
            '🧄', '🧅', '🥜', '🫘', '🌰'
        ],
        "prepared_foods": [
            '🍞', '🥐', '🥖', '🫓', '🥨', '🥯', '🥞', '🧇', '🧀', '🍖',
            '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯',
            '🫔', '🥙', '🧆', '🥚', '🍳', '🥘', '🍲', '🫕', '🥣', '🥗',
            '🍿', '🧈', '🧂', '🥫', '🍝'
        ],
        "asian_foods": [
            '🍱', '🍘', '🍙', '🍚', '🍛', '🍜', '🍠', '🍢', '🍣', '🍤',
            '🍥', '🥮', '🍡', '🥟', '🥠', '🥡'
        ],
        "sweets_and_deserts": [
            '🍦', '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫',
            '🍬', '🍭', '🍮', '🍯'
        ],
        "drinks_and_dishware": [
            '🍼', '🥛', '☕', '🫖', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹',
            '🍺', '🍻', '🥂', '🥃', '🫗', '🥤', '🧋', '🧃', '🧉', '🥢', 
            '🍽️', '🍴', '🥄', '🔪', '🫙', '🏺'
        ]
    },
    "activity": {
        "events_and_celebration": [
            '🎃', '🎄', '🎆', '🎇', '🧨', '✨', '🎈', '🎉', '🎊', '🎋',
            '🎍', '🎎', '🎏', '🎐', '🎑', '🧧', '🎁', '🎟️', '🎫', '🏮',
            '🪔'
        ],
        "sports_and_awards": [
            '🎖️', '🏆', '🏅', '🥇', '🥈', '🥉', '⚽', '⚾', '🥎', '🏀',
            '🏐', '🏈', '🏉', '🎾', '🥏', '🎳', '🏏', '🏑', '🏒', '🥍',
            '🏓', '🏸', '🥊', '🥋', '🥅', '⛳', '⛸️', '🎣', '🤿', '🎽',
            '🎿', '🛷', '🥌', '🎯'
        ],
        "games_and_culture": [
            '🪀', '🪁', '🎱', '🔮', '🪄', '🎮', '🕹️', '🎰', '🎲', '🧩',
            '🪅', '🪩', '🪆', '♠️', '♥️', '♦️', '♣️', '♟️', '🃏', '🀄', '🎴', 
            '🎭', '🖼️', '🎨', '🔫'
        ]
    },
    "travel_and_places": {
        "maps_and_geography": [
            '🌍', '🌎', '🌏', '🌐', '🗺️', '🗾', '🧭', '🏔️', '⛰️', '🌋',
            '🗻', '🏕️', '🏖️', '🏜️', '🏝️', '🏞️'
        ],
        "buildings_and_places": [
            '🏟️', '🏛️', '🏗️', '🧱', '🛖', '🏘️', '🏚️', '🏠', '🏡', '🏢',
            '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭',
            '🏯', '🏰', '💒', '🗼', '🗽', '⛪', '🕌', '🛕', '🕍', '⛩️',
            '🕋', '⛲', '⛺', '🌁', '🌃', '🏙️', '🌄', '🌅', '🌆', '🌇',
            '🌉', '♨️', '🎠', '🛝', '🎡', '🎢', '💈', '🎪', '🛎️', '🗿'
        ],
        "land_travel": [
            '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚝',
            '🚞', '🚋', '🚌', '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔',
            '🚕', '🚖', '🚗', '🚘', '🚙', '🛻', '🚚', '🚛', '🚜', '🏎️',
            '🏍️', '🛵', '🦽', '🦼', '🛺', '🚲', '🛴', '🛹', '🛼', '🚏',
            '🛣️', '🛤️', '🛢️', '⛽', '🛞', '🚨', '🚥', '🚦', '🛑', '🚧'
        ],
        "air_and_sea_travel": [
            '⚓', '🛟', '⛵', '🛶', '🚤', '🛳️', '⛴️', '🛥️', '🚢', '✈️',
            '🛩️', '🛫', '🛬', '🪂', '💺', '🚁', '🚟', '🚠', '🚡', '🛰️',
            '🚀', '🛸'
        ]
    },
    "objects": {
        "clothing_and_appearence": [
            '🎀', '🎗️', '👓', '🕶️', '🥽', '🥼', '🦺', '👔', '👕', '👖',
            '🧣', '🧤', '🧥', '🧦', '👗', '👘', '🥻', '🩱', '🩲', '🩳',
            '👙', '👚', '👛', '👜', '👝', '🛍️', '🎒', '🩴', '👞', '👟', 
            '🥾', '🥿', '👠', '👡', '🩰', '👢', '👑', '👒', '🎩', '🎓', 
            '🧢', '🪖', '⛑️', '📿', '💄', '💍', '💎', '🦯'
        ],
        "music_and_sound": [
            '🔇', '🔈', '🔉', '🔊', '📢', '📣', '📯', '🔔', '🔕', '🎼',
            '🎵', '🎶', '🎙️', '🎚️', '🎛️', '🎤', '🎧', '📻', '🎷', '🪗',
            '🎸', '🎹', '🎺', '🎻', '🪕', '🥁', '🪘'
        ],
        "it_and_av": [
            '📱', '📲', '☎️', '📞', '📟', '📠', '🔋', '🪫', '🔌', '💻',
            '🖥️', '🖨️', '⌨️', '🖱️', '🖲️', '💽', '💾', '💿', '📀', '🎥',
            '🎞️', '📽️', '🎬', '📺', '📷', '📸', '📹', '📼'
        ],
        "office_and_stationary": [
            '📔', '📕', '📖', '📗', '📘', '📙', '📚', '📓', '📒', '📃',
            '📜', '📄', '📰', '🗞️', '📑', '🔖', '🏷️', '✉️', '📧', '📨',
            '📩', '📤', '📥', '📦', '📫', '📪', '📬', '📭', '📮', '🗳️',
            '✏️', '✒️', '🖋️', '🖊️', '🖌️', '🖍️', '📝', '💼', '📁', '📂',
            '🗂️', '📅', '📆', '🗒️', '🗓️', '📇', '📈', '📉', '📊', '📋',
            '📌', '📍', '📎', '🖇️', '📏', '📐', '✂️', '🗃️', '🗄️', '🗑️'
        ],
        "money_and_time": [
            '⌛', '⏳', '⌚', '⏰', '⏱️', '⏲️', '🕰️', '🕛', '🕧', '🕐',
            '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕',
            '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚',
            '🕦', '🧮', '💰', '🪙', '💴', '💵', '💶', '💷', '💸', '💳',
            '🧾', '💹'
        ],
        "tools_and_household_items": [
            '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚝',
            '🚞', '🚋', '🚌', '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔', 
            '🚕', '🚖', '🚗', '🚘'
        ]
    },
    "symbols": {
        "hearts_shapes_and_emotions": [
            '💋', '💌', '💘', '💝', '💖', '💗', '💓', '💞', '💕', '💟', 
            '❣️', '💔', '❤️‍🔥', '❤️‍🩹', '❤️', '🧡', '💛', '💚', '💙', '💜',
            '🤎', '🖤', '🤍', '💯', '💢', '💥', '💦', '💨', '🕳️', '💬',
            '👁️‍🗨️', '🗨️', '🗯️', '💭', '💤', '🔴', '🟠', '🟡', '🟢', '🔵',
            '🟣', '🟤', '⚫', '⚪', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪',
            '🟫', '⬜', '◼️', '◻️', '◾', '◽', '▪️', '▫️', '🔶', '🔷',
            '🔸', '🔹', '🔺', '🔻', '💠', '🔘', '🔳', '🔲'
        ],
        "location_and_warning": [
            '🛗', '🏧', '🚮', '🚰', '♿', '🚹', '🚺', '🚻', '🚼', '🚾',
            '🛂', '🛃', '🛄', '🛅', '⚠️', '🚸', '⛔', '🚫', '🚳', '🚭', 
            '🚯', '🚱', '🚷', '📵', '🔞', '☢️', '☣️'
        ],
        "arrows_and_av": [
            '⬆️', '↗️', '➡️', '↘️', '⬇️', '↙️', '⬅️', '↖️', '↕️', '↔️',
            '↩️', '↪️', '⤴️', '⤵️', '🔃', '🔄', '🔙', '🔚', '🔛', '🔜',
            '🔝', '🔀', '🔁', '🔂', '▶️', '⏩', '⏭️', '⏯️', '◀️', '⏪',
            '⏮️', '🔼', '⏫', '🔽', '⏬', '⏸️', '⏹️', '⏺️', '⏏️', '🎦',
            '🔅', '🔆', '📶', '📳', '📴'   
        ],
        "identities_and_beliefs": [
            '🛐', '🕉️', '✡️', '☸️', '☯️', '✝️', '☦️', '☪️', '☮️', '🕎', 
            '🔯', '♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', 
            '♑', '♒', '♓', '⛎', '♀️', '♂️', '⚧️'   
        ],
        "alphanumerics": [
            '✖️', '➕', '➖', '➗', '🟰', '♾️', '‼️', '⁉️', '❓', '❔',
            '❕', '❗', '〰️', '💱', '💲', '#️⃣', '*️⃣', '0️⃣', '1️⃣', '2️⃣',
            '3️⃣', '4️⃣',  '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔠', '🔡',
            '🔢', '🔣', '🔤', '🅰️', '🆎', '🅱️', '🆑', '🆒', '🆓', 'ℹ️',
            '🆔', 'Ⓜ️', '🆕', '🆖', '🅾️', '🆗', '🆘', '🆙', '🆚', '🈁',
            '🈂️', '🈷️', '🈶', '🈯', '🉐', '🈹', '🈚', '🈲', '🉑', '🈸',
            '🈴', '🈳', '㊗️', '㊙️', '🈺', '🈵'
        ],
        "other_symbols": [
            '⚕️', '♻️', '⚜️', '📛', '🔰', '⭕', '✅', '☑️', '✔️', '❌',
            '❎', '➰', '➿', '〽️', '✳️', '✴️', '❇️', '©️', '®️', '™️'
        ]
    },
    "flags": {
        "color_and_identity": [
            '🏁', '🚩', '🎌', '🏴', '🏳️', '🏳️‍🌈', '🏳️‍⚧️', '🏴‍☠️', '🇺🇳'
        ],
        "africa": [
            '🇦🇴', '🇧🇫', '🇧🇮', '🇧🇯', '🇧🇼', '🇨🇩', '🇨🇫', '🇨🇬', '🇨🇮', '🇨🇲',
            '🇨🇻', '🇩🇯', '🇩🇿', '🇪🇬', '🇪🇭', '🇪🇷', '🇪🇹', '🇬🇦', '🇬🇭', '🇬🇲',
            '🇬🇳', '🇬🇶', '🇬🇼', '🇰🇪', '🇰🇲', '🇱🇷', '🇱🇸', '🇱🇾', '🇲🇦', '🇲🇬',
            '🇲🇱', '🇲🇷', '🇲🇺', '🇲🇼', '🇲🇿', '🇳🇦', '🇳🇪', '🇳🇬', '🇷🇼', '🇸🇨',
            '🇸🇩', '🇸🇱', '🇸🇳', '🇸🇴', '🇸🇸', '🇸🇿', '🇹🇩', '🇹🇬', '🇹🇳', '🇹🇿',
            '🇺🇬', '🇿🇦', '🇿🇲', '🇿🇼'
        ],
        "the_americas": [
            '🇦🇬', '🇦🇮', '🇦🇷', '🇦🇼', '🇧🇧', '🇧🇱', '🇧🇲', '🇧🇴', '🇧🇶', '🇧🇷',
            '🇧🇸', '🇧🇿', '🇨🇦', '🇨🇱', '🇨🇴', '🇨🇷', '🇨🇺', '🇨🇼', '🇩🇲', '🇩🇴',
            '🇪🇨', '🇫🇰', '🇬🇩', '🇬🇫', '🇬🇵', '🇬🇹', '🇬🇾', '🇭🇳', '🇭🇹', '🇯🇲',
            '🇰🇳', '🇰🇾', '🇱🇨', '🇲🇫', '🇲🇶', '🇲🇸', '🇲🇽', '🇳🇮', '🇵🇦', '🇵🇪',
            '🇵🇲', '🇵🇷', '🇵🇾', '🇸🇷', '🇸🇻', '🇸🇽', '🇹🇨', '🇹🇹', '🇺🇸', '🇺🇾',
            '🇻🇪', '🇻🇬', '🇻🇮'
        ],
        "asia_and_the_middle_east": [
            '🇦🇪', '🇦🇫', '🇦🇿', '🇧🇩', '🇧🇭', '🇧🇳', '🇧🇹', '🇨🇳', '🇭🇰', '🇮🇩',
            '🇮🇱', '🇮🇳', '🇮🇶', '🇮🇷', '🇯🇴', '🇯🇵', '🇰🇬', '🇰🇭', '🇰🇵', '🇰🇷',
            '🇰🇼', '🇰🇿', '🇱🇦', '🇱🇧', '🇱🇰', '🇲🇲', '🇲🇳', '🇲🇴', '🇲🇻', '🇲🇾',
            '🇳🇵', '🇴🇲', '🇵🇭', '🇵🇰', '🇵🇸', '🇶🇦', '🇷🇺', '🇸🇦', '🇸🇬', '🇸🇾',
            '🇹🇭', '🇹🇯', '🇹🇱', '🇹🇲', '🇹🇷', '🇹🇼', '🇺🇿', '🇻🇳', '🇾🇪'
        ],
        "europe": [
            '🇦🇩', '🇦🇱', '🇦🇲', '🇦🇹', '🇧🇦', '🇧🇪', '🇧🇬', '🇧🇾', '🇨🇭', '🇨🇾',
            '🇨🇿', '🇩🇪', '🇩🇰', '🇪🇦', '🇪🇪', '🇪🇸', '🇪🇺', '🇫🇮', '🇫🇷', '🇬🇧',
            '🇬🇪', '🇬🇬', '🇬🇮', '🇬🇷', '🇭🇷', '🇭🇺', '🇮🇪', '🇮🇲', '🇮🇸', '🇮🇹',
            '🇯🇪', '🇱🇮', '🇱🇹', '🇱🇺', '🇱🇻', '🇲🇨', '🇲🇩', '🇲🇪', '🇲🇰', '🇲🇹',
            '🇳🇱', '🇳🇴', '🇵🇱', '🇵🇹', '🇷🇴', '🇷🇸', '🇷🇺', '🇸🇪', '🇸🇮', '🇸🇰',
            '🇸🇲', '🇺🇦', '🇻🇦', '🇽🇰', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', '🏴󠁧󠁢󠁳󠁣󠁴󠁿', '🏴󠁧󠁢󠁷󠁬󠁳󠁿'
        ],
        "oceania_island_nations_and_territories": [
            '🇦🇨', '🇦🇶', '🇦🇸', '🇦🇺', '🇦🇽', '🇧🇻', '🇨🇨', '🇨🇰', '🇨🇵', '🇨🇽',
            '🇩🇬', '🇫🇯', '🇫🇲', '🇬🇱', '🇬🇸', '🇬🇺', '🇭🇲', '🇮🇨', '🇮🇴', '🇰🇮',
            '🇲🇭', '🇲🇵', '🇳🇨', '🇳🇫', '🇳🇷', '🇳🇺', '🇳🇿', '🇵🇫', '🇵🇬', '🇵🇳',
            '🇵🇼', '🇷🇪', '🇸🇧', '🇸🇭', '🇸🇯', '🇸🇹', '🇹🇦', '🇹🇫', '🇹🇰', '🇹🇴',
            '🇹🇻', '🇺🇲', '🇻🇨', '🇻🇺', '🇼🇫', '🇼🇸', '🇾🇹'
        ]
    }
}

EMOJI_DATA = {
""", output_path)
    
    progress = 0
    
    for data in _extract_emoji_test_data_from_file(emoji_test_file):
        print("Compiling emoji data. Emoji #", progress, ":", data[1][4], "------> EMOJI_DATA{}")
        string_data = data[0]
        _write_data(string_data, output_path)
        progress = progress + 1
    _write_data(
"""    
}
""",
    output_path)

construct_data_file()

def experiment(emoji: str):
    print(adapt_emoji_name("grinning_face", "en", emoji))
#experiment("😀")

