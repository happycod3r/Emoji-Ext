# file_parsers.py
from emoji_data.data_dict import EMOJI_DATA, CATEGORIES, LANGUAGES
from emoji_data.data_dict_legacy import LEGACY_EMOJI_DATA
from core import is_emoji
import xml.etree.ElementTree as ET
import unicodedata
import requests
import bs4
import os
import re

def _get_text_from_url(url: str) -> str:
    """Get text from url"""
    return requests.get(url).text

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

def get_emojiterra_from_url(url: str) -> dict:
    html = _get_text_from_url(url)

    soup = bs4.BeautifulSoup(html, "html.parser")
    emojis = {}

    data = soup.find_all('li')
    data = [i for i in data if 'href' not in i.attrs and 'data-e' in i.attrs and i['data-e'].strip()]

    for i in data:
        code = i['data-e']
        emojis[code] = i['title'].strip()

    assert len(data) > 100, f"emojiterra data from {url} has only {len(data)} entries"

    return emojis

def get_cheat_sheet(url: str) -> dict:
    """
    Returns a dict of emoji to short-names:
    E.g. {'👴': ':old_man:', '👵': ':old_woman:', ... }
    """

    html = _get_text_from_url(url)

    soup = bs4.BeautifulSoup(html, "html.parser")
    emojis = {}

    items = soup.find(class_='ecs-list').find_all(class_='_item')

    pattern = re.compile(r'U\+([0-9A-F]+)')

    for i in items:
        unicode_text = i.find(class_='unicode').text

        code_points = pattern.findall(unicode_text)
        code = ''.join(chr(int(x,16)) for x in code_points)

        emojis[code] = i.find(class_='shortcode').text

    # Remove some unwanted and some weird entries from the cheat sheet
    filtered = {}
    for emj, short_code in emojis.items():

        if short_code.startswith(':flag_'):
            # Skip flags from cheat-sheet, because we already have very similar aliases for the flags
            continue

        if '⊛' in short_code:
            # Strange emoji with ⊛ in the short-code
            continue

        if emj == '\U0001F93E\U0000200D\U00002640\U0000FE0F':
            # The short-code for this emoji is wrong
            continue

        if emj == '\U0001F468\U0000200D\U0001F468\U0000200D\U0001F467':
            # The short-code for this emoji is wrong
            continue

        if short_code.startswith('::'):
            # Do not allow short-codes to have double :: at the start
            short_code = short_code[1:]

        if short_code.endswith('::'):
            # Do not allow short-codes to have double :: at the end
            short_code = short_code[:-1]

        filtered[emj] = short_code

    assert len(filtered) > 100, f"emoji-cheat-sheet data from {url} has only {len(filtered)} entries"

    return filtered

def get_emoji_from_youtube(url: str) -> dict:
    """Get emoji alias from Youtube
    Returns a dict of emoji to list of short-names:
    E.g. {'💁': [':person_tipping_hand:', ':information_desk_person:'], '😉': [':winking_face:', ':wink:']}
    """

    data = requests.get(url).json()

    output = {}
    for obj in data:
        if 'shortcuts' not in obj or 'emojiId' not in obj:
            continue

        shortcuts = [x for x in obj['shortcuts'] if x.startswith(':') and x.endswith(':')]

        if shortcuts:
            output[obj['emojiId']] = shortcuts

    assert len(output) > 100, f"youtube data from {url} has only {len(output)} entries"

    return output

def extract_emojis(emojis_lines: list, sequences_lines: list) -> dict:
    """Extract emojis line by line to dict"""

    output = {}
    for line in emojis_lines:
        if not line == "" and not line.startswith("#"):
            emoji_status = line.split(";")[1].strip().split(" ")[0]

            codes = line.split(";")[0].strip().split(" ")
            separated_line = line.split(" # ")[-1].strip().split(" ")
            separated_name = separated_line[2:]
            version_str = separated_line[1]
            emoji_name = (
                "_".join(separated_name)
                .removeprefix("flag:_")
                .replace(":", "")
                .replace(",", "")
                .replace("\u201c", "")
                .replace("\u201d", "")
                .replace("\u229b", "")
                .strip()
                .replace(" ", "_")
                .replace("_-_", "-")
            )

            emoji_code = "".join(
                [
                    "\\U0000" + code if len(code) == 4 else "\\U000" + code
                    for code in codes
                ]
            )

            version = float(version_str.replace("E", "").strip())

            if emoji_code in output:
                raise Exception("Duplicate emoji: " +
                                emoji_name + " " + emoji_code)

            output[emoji_code] = {
                "en": emoji_name,
                "status": emoji_status.replace("-", "_"),
                "version": version
            }

    # Walk through the emoji-variation-sequences.txt
    for line in sequences_lines:
        if not line == "" and not line.startswith("#"):
            # No variant
            normal_codes = line.split(";")[0].strip().split(" ")
            normal_code = "".join(
                [
                    "\\U0000" + code if len(code) == 4 else "\\U000" + code
                    for code in normal_codes
                ]
            )
            if normal_code in output:
                output[normal_code]["variant"] = True

            # Text variant U+FE0E
            text_codes = re.sub(r'\s*FE0E\s*$', '',
                                line.split(";")[0]).strip().split(" ")
            text_code = "".join(
                [
                    "\\U0000" + code if len(code) == 4 else "\\U000" + code
                    for code in text_codes
                ]
            )
            if text_code in output:
                output[text_code]["variant"] = True

            # Emoji variant U+FE0F
            emoji_codes = re.sub(r'\s*FE0F\s*$', '', line.split(";")[0]).strip().split(" ")
            emoji_code = "".join(
                [
                    "\\U0000" + code if len(code) == 4 else "\\U000" + code
                    for code in emoji_codes
                ]
            )
            if emoji_code in output:
                output[emoji_code]["variant"] = True

    return output

def add_unicode_annotations(data, lang, url):
    xml = _get_text_from_url(url)

    tree = ET.fromstring(xml)
    annotations = tree.find('annotations')
    for annotation in annotations:
        if annotation.get('type') == 'tts':
            emj = annotation.get('cp')
            text = annotation.text.strip()

            emoji_name = adapt_emoji_name(text, lang, emj)

            if emj in data and data[emj] != emoji_name:
                print(
                    f"# {lang}: CHANGED {data[emj]} TO {emoji_name} \t\t(Original: {text})")
            data[emj] = emoji_name

def extract_names(github_tag, github_lang, lang, emoji_terra={}):
    """Copies emoji.EMOJI_DATA[emj][lang] and adds the names from the Unicode CLDR xml

    Find latest tag at https://cldr.unicode.org/index/downloads or
    https://github.com/unicode-org/cldr/tree/main/common/annotations
    """

    data = _translate_emoji_name(lang)
    add_unicode_annotations(data, lang, f"https://github.com/unicode-org/cldr/raw/{github_tag}/common/annotations/{github_lang}.xml")
    add_unicode_annotations(data, lang, f"https://github.com/unicode-org/cldr/raw/{github_tag}/common/annotationsDerived/{github_lang}.xml")

    # Add names from emojiterra if there is no unicode annotation
    for emj, name in emoji_terra.items():
        if emj in EMOJI_DATA and emj not in data:
            emoji_name = adapt_emoji_name(name, lang, emj)
            data[emj] = emoji_name

    # There are some emoji with two code sequences for the same emoji, one that ends with \uFE0F and one that does not.
    # The one that ends with \uFE0F is the "new" emoji, that is RGI.
    # The Unicode translation data sometimes only has one of the two code sequences and is missing the other one.
    # In that case we want to use the existing translation for both code sequences.
    missing_translation = {}
    for emj in data:
        if emj.endswith('\uFE0F') and emj[0:-1] not in data and emj[0:-1] in EMOJI_DATA:
            # the emoji NOT ending in \uFE0F exists in EMOJI_DATA but is has no translation
            # e.g. ':pirate_flag:' -> '\U0001F3F4\u200D\u2620\uFE0F' or '\U0001F3F4\u200D\u2620'
            missing_translation[emj[0:-1]] = data[emj]

        with_emoji_type = f"{emj}\uFE0F"
        if not emj.endswith('\uFE0F') and with_emoji_type not in data and with_emoji_type in EMOJI_DATA:
            # the emoji ending in \uFE0F exists in EMOJI_DATA but is has no translation
            # e.g. ':face_in_clouds:' -> '\U0001F636\u200D\U0001F32B\uFE0F' or '\U0001F636\u200D\U0001F32B'
            missing_translation[with_emoji_type] = data[emj]

    # Find emoji that contain \uFE0F inside the sequence (not just as a suffix)
    # e.g. ':eye_in_speech_bubble:' -> '\U0001F441\uFE0F\u200D\U0001F5E8\uFE0F'
    for emj in EMOJI_DATA:
        if emj in data:
            continue
        emj_no_variant = emj.replace('\uFE0F', '')
        if emj_no_variant != emj and emj_no_variant in data:
            # the emoji with \uFE0F has no translation, but the emoji without all \uFE0F has a translation
            data[emj] = data[emj_no_variant]

    data.update(missing_translation)

    return data

def get_emoji_from_github_api(url: str) -> dict:
    """Get emoji alias from GitHub API
    """

    data = requests.get(url).json()
    pattern = re.compile(r"unicode/([0-9a-fA-F-]+)\.[a-z]+")

    output = {}
    for name, img in data.items():
        m = pattern.search(img)
        if m:
            emj = "".join(chr(int(h, 16)) for h in m.group(1).split('-'))
            output[name] = emj
        else:
            pass  # Special GitHub emoji that is not part of Unicode

    assert len(output) > 100, f"data from github API has only {len(output)} entries"

    return output

def find_github_aliases(emj, github_dict, v, emj_no_variant=None):
    aliases = set()

    # Strip ZWJ \u200D, text_type \uFE0E and emoji_type \uFE0F
    # because the GitHub API does not include these
    emj_clean = GITHUB_REMOVED_CHARS.sub("", emj)

    for gh_alias in github_dict:
        if emj == github_dict[gh_alias]:
            aliases.add(gh_alias)
        elif 'variant' in v and emj_no_variant == github_dict[gh_alias]:
            aliases.add(gh_alias)
        elif emj_clean == github_dict[gh_alias]:
            aliases.add(gh_alias)

    return aliases

##############################################################

_CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
GITHUB_REMOVED_CHARS = re.compile("\u200D|\uFE0F|\uFE0E", re.IGNORECASE)
github_alias_dict = get_emoji_from_github_api('https://api.github.com/emojis')
cheat_sheet_dict = get_cheat_sheet('https://www.webfx.com/tools/emoji-cheat-sheet/')
youtube_dict = get_emoji_from_youtube('https://www.gstatic.com/youtube/img/emojis/emojis-png-7.json')

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

def _ascii(s):
    # return escaped Code points \U000AB123
    return s.encode("unicode-escape").decode()

def _translate_emoji_name(lang):
    data = {emj: EMOJI_DATA[emj][lang] for emj in EMOJI_DATA if lang in EMOJI_DATA[emj]}
    return data
    
def _get_text_from_url(url: str) -> str:
    """Get text from url"""
    return requests.get(url).text

def _in_emoji_data(emoji):
    return emoji in EMOJI_DATA

def get_unicode_emoji_variation_sequence_file(version: str) -> list:
    """Get splitlines of emoji variation sequences from unicode.org"""

    url = f"https://www.unicode.org/Public/{version}/ucd/emoji/emoji-variation-sequences.txt"
    return _get_text_from_url(url).splitlines()

def get_unicode_emoji_test_file(version: float) -> list:
    """Get splitlines of emojis list from unicode.org"""
    url = f"https://unicode.org/Public/emoji/{version}/emoji-test.txt"
    return _get_text_from_url(url).splitlines()

def extract_unused_github_emojis() -> dict:
    ghemojis = {}
    for key in github_alias_dict.keys():
        emoji = github_alias_dict[key]
        emoji_name = key
        if not _in_emoji_data(emoji):
            ghemojis[emoji] = emoji_name   
    return ghemojis

def extract_emoji_data():
    
    """
    Extracts emoji data line by line to dict
    
    This function parses the emoji-test.txt file found on Unicode.org at
    https://unicode.org/Public/emoji/latest/emoji-test.txt
    
    This function generates a string representation of a dictionary containing 
    the data from the emoji-test.txt file for each emoji and yields the dict 
    representation string to be printed or written to file. Each yield is used 
    to construct the EMOJI_DATA dictionary in data_dict.py 
    
    Each emoji is stored in a dictionary with the following keys and value
    types:
    
    "\U0001F600": {  # 😀
        "index": 1,                        int
        "category": "Smileys & Emotion",      str
        "subcategory": "face-smiling",        str
        "status": fully_qualified,         int
        "emoji": "😀",                     str
        "E": 1.0,                          float
        "unicodes": ['U+1F600'],           list
        "codepoints": ['1F600'],           list
        "sequences": ['\\U0001F600'],      list
        "category": "So",                  str
        "name": ":grinning_face:",         str
        "en": ":grinning_face:",           str
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
   
    current_category = None
    current_subcategory = None
    current_category_id = None
    current_subcategory_id = None
    current_status = None
    current_codepoints = None
    current_emoji = None
    current_version = None
    current_emoji_name = None
    current_emoji_alias = None
    is_emoji_variant = False
    real_index = 0
    
    #//////////// UNICODE EMOJI-TEST.TXT //////
    for current_line, line in enumerate(get_unicode_emoji_test_file(15.0)):
        line = line.strip()
        
        #//////////// EMOJI CATEGORY //////
        if line.startswith("# group:"):
            current_category = line.split("# group:")[1].strip().lower()
            current_category = current_category.replace(" ", "_")
            for i in range(len(current_category)):
                if current_category[i].startswith("&"):
                    current_category = current_category.replace("&", "and")
                    
        #//////////// EMOJI SUBCATEGORY //////
        elif line.startswith("# subgroup:"):
            current_subcategory = line.split("# subgroup:")[1].strip().lower()
            current_subcategory = current_subcategory.replace("-", "_")
        
        #//////////// EMOJI CODEPOINTS //////
        elif line.startswith(("0", "1", "2", "3", "4")):
            line_parts = line.split(";")
            current_codepoints = line_parts[0].strip()
            current_codepoints = f"{current_codepoints.split(' ')}"
            line_data = line_parts[1].strip().split(" ")

            #//////////// EMOJI STATUS //////
            current_status = line_data[0].strip().replace("-", "_")            
            emj_name = ""
            for item in line_data:
                
                #//////////// EMOJI //////
                if is_emoji(item):
                    current_emoji = item
                    
                #//////////// EMOJI VERSION //////
                elif item.startswith("E") and item[1].isdigit():
                    item_parts = item.strip().split("E")
                    for part in item_parts:
                        if part == "":
                            continue
                        if part[0].isdigit():
                            current_version = part
                elif item == "component" or item == "fully-qualified" or item == "minimally-qualified" or item == "unqualified":
                    continue
                elif item == '' or item == "#":
                    continue
                #//////////// EMOJI NAME //////
                # elif item == "keycap:":
                #     emj_name += item.replace(":", " ").strip()
                # elif item == "(blood":
                #     item = item.lstrip("(")
                #     new_txt = ""
                #     new_txt += "_"
                #     for i in range(len(item)):
                #         new_txt += item[i]
                #     new_txt += "_"
                #     item = new_txt
                #     emj_name += item
                # elif item == "type)":
                #     emj_name += item.rstrip(")")
                # elif item.startswith("(") and item.endswith(")"):
                #     emj_name += item.lstrip("(").rstrip(")")
                #     print(real_index, item)
                # elif ":" in item:
                #     emj_name += item.replace(":", "_")
                # elif "“" in item or "”" in item:
                #     emj_name += item.replace("“", "_").replace("”", "_")
                # else:
                #     emj_name += f"_{item}"

            #current_emoji_name = emj_name.replace("-", "_")
            
            if current_emoji in LEGACY_EMOJI_DATA:
                current_emoji_name = LEGACY_EMOJI_DATA[current_emoji]["en"]
                
            if current_emoji_name.startswith("_"):
                current_emoji_name = current_emoji_name.lstrip("_")     
            current_emoji_name = adapt_emoji_name(current_emoji_name, "en", current_emoji)
           
        #////// FILTERS //////

        # Filter out the file header text
        if current_line < 35: # Table data starts on line #35.
            continue

        real_index = real_index + 1
            
        if current_emoji is not None: 
            
            #//////////// ALIASES //////
            if current_emoji in LEGACY_EMOJI_DATA:
                if "alias" in LEGACY_EMOJI_DATA[current_emoji]:
                    current_emoji_alias = []
                    for i in range(len(LEGACY_EMOJI_DATA[current_emoji]["alias"])):
                        current_emoji_alias.append(LEGACY_EMOJI_DATA[current_emoji]["alias"][i].lower())

            #//////////// VARIANT //////
            if current_emoji in LEGACY_EMOJI_DATA:
                if "variant" in LEGACY_EMOJI_DATA[current_emoji]:
                    is_emoji_variant = LEGACY_EMOJI_DATA[current_emoji]["variant"]
                else:
                    is_emoji_variant = False
                    
            #//////////// LANGUAGES //////
            LANG_STRING = ""
            for lang in LANGUAGES:
                emoji_in_langs = _translate_emoji_name(lang)
                if current_emoji in emoji_in_langs:
                    emoji_name_in_lang = (emoji_in_langs[current_emoji])
                    if lang == "zh":
                        LANG_STRING += f"""        "{lang}": "{emoji_name_in_lang.lower()}" """
                        continue
                    LANG_STRING += f"""        "{lang}": "{emoji_name_in_lang.lower()}",\n"""

            #//////////// SEQUENCES //////
            emoji_sequence = _escape_sequence(current_emoji)
            sequence_string = ""
            for sequence in emoji_sequence.strip().split(" "):
                sequence_string += sequence
            emoji_sequence = sequence_string
            sequences = emoji_sequence.split("\\")
            escaped_sequences = []
            _new_str = ""
            for item in sequences:
                if item == '':
                    continue
                _new_str += f"\\{item}"
                escaped_sequences.append(_new_str)
                _new_str = ""
                
            #//////////// CATEGORY ID //////
            for key in CATEGORIES.keys():
                if key == current_category:
                    current_category_id = CATEGORIES[key]["id"]
                    for subkey in CATEGORIES[key].keys():
                        if subkey == current_subcategory:
                            current_subcategory_id = CATEGORIES[key][subkey]

            DATA = f"""    "{emoji_sequence}": {{  # {current_emoji}
        "index": {int(real_index)},
        "category": "{current_category}",
        "category_id": {current_category_id},
        "subcategory": "{current_subcategory}",
        "subcategory_id": {current_subcategory_id},
        "status": {current_status},
        "emoji": "{current_emoji}",
        "E": {float(current_version)},
        "unicode": {_unicode(current_emoji)},
        "codepoints": {current_codepoints},
        "sequences": {escaped_sequences},
        "variant": {is_emoji_variant},
        "alias": {current_emoji_alias},
        "name": "{current_emoji_name}",
{LANG_STRING}
    }},\n"""

            yield [DATA, [real_index, current_category, current_subcategory, current_status,
                            current_emoji, current_version, current_emoji_name,
                            _unicode(current_emoji), current_codepoints.split(" "),
                            emoji_sequence.split(" ")]]

def compile_data_dict():
    emoji_test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "emoji_data")
    emoji_test_file = os.path.join(emoji_test_file, "emoji-v15-data")
    emoji_test_file = os.path.join(emoji_test_file, "emoji-test.txt")
    output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "emoji_data")
    output_path = os.path.join(output_path, "data_dict.py")

    _create_data_file(output_path)

    _write_data(
"""
\"\"\"
emoji-v15-data-dict.py

!!! ⚠️ DO NOT EDIT THIS FILE ⚠️ !!!
Don't edit this file or things will 💥 and this module will be 💤💤💤 ...
unless you know what you're doing! This file is used by other parts of the 
module and you may and probably will encounter errors when trying to update 
or regenerate it later. You wil also encounter errors with the modules
core functions.

This file is automatically generated by running emoji_data_compiler.py
It builds on the original EMOJI_DATA dict which can be found in the 
emoji module http://github.com/carpedm20/emoji and contains a dictionary 
holding all current emoji data and properties.

This data was extracted from the following files which can be found on 
Unicode.org at:
  🔹https://unicode.org/Public/emoji/latest/emoji-test.txt
  🔹https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt

The emoji-test.txt file 
https://unicode.org/Public/emoji/latest/emoji-test.txt or you can run 
the download_emoji_test_data function in utils/download_emoji_data.py to
download the latest files. 

Once you download the latest data from Unicode.org you can run 
emoji_data_comiler.py to recompile this file and regenerate the EMOJIS dict
with updated information.
                          
Emoji Version Info: http://www.unicode.org/reports/tr51/#Versioning
 +----------------+-------------+------------------+-------------------+
 | Emoji Version  |    Date     | Unicode Version  | Data File Comment |
 +----------------+-------------+------------------+-------------------+
 | N/A            | 2010-10-11  | Unicode 6.0      | E0.6              |
 | N/A            | 2014-06-16  | Unicode 7.0      | E0.7              |
 | Emoji 1.0      | 2015-06-09  | Unicode 8.0      | E1.0              |
 | Emoji 2.0      | 2015-11-12  | Unicode 8.0      | E2.0              |
 | Emoji 3.0      | 2016-06-03  | Unicode 9.0      | E3.0              |
 | Emoji 4.0      | 2016-11-22  | Unicode 9.0      | E4.0              |
 | Emoji 5.0      | 2017-06-20  | Unicode 10.0     | E5.0              |
 | Emoji 11.0     | 2018-05-21  | Unicode 11.0     | E11.0             |
 | Emoji 12.0     | 2019-03-05  | Unicode 12.0     | E12.0             |
 | Emoji 12.1     | 2019-10-21  | Unicode 12.1     | E12.1             |
 | Emoji 13.0     | 2020-03-10  | Unicode 13.0     | E13.0             |
 | Emoji 13.1     | 2020-09-15  | Unicode 13.0     | E13.1             |
 | Emoji 14.0     | 2021-09-14  | Unicode 14.0     | E14.0             |
 | Emoji 15.0     | 2022-09-13  | Unicode 15.0     | E15.0 <-- current |
#  +---------------------------------------------------------------------+

Emoji versions refer to the different iterations of the Unicode Standard, 
each of which introduces new emojis, updates to existing ones, and sometimes 
changes in design or representation. These updates basically ensure that 
emojis stay relevant to the ever evolving communication trends and cultural 
contexts.

New emoji versions are typically released annually, and each version is 
associated with a specific Unicode version number. Emoji version numbers do 
not always match the Unicode version numbers exactly; they might be slightly 
different due to the release schedules and updates. 

Heres a few examples of some big updates from over the past 10 years or so
that I could find:

    🔹Unicode 6.0  (2010) introduced emoji symbols like 😀, 🌍, 🍕.
    🔹Unicode 8.0  (2015) brought in diverse skin tones for certain emojis.
    🔹Unicode 11.0 (2018) added emojis such as 🦄, 🧜‍♀️, 🧸.
    🔹Unicode 13.0 (2020) included emojis like 🥲, 🤌, 🪐.
    
As time goes on, new emoji versions will continue to be released to keep up 
with the evolving ways people communicate and express themselves. It's important 
to note that while Unicode defines the characters and their meanings, how these 
emojis are displayed can vary depending on the operating system, device, or 
platform you're using. Different platforms might have their own interpretations 
of specific emoji designs, even though they share the same underlying Unicode code 
points.
    
\"\"\"

__all__ = [
    'STATUS' , 'LANGUAGES', 'EMOJI_DATA', 'BASIC_EMOJIS'
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

CATEGORIES = {
    "smileys_and_emotion": {
        'id': 491122,
        'face_smiling': 4745, 
        'face_affection': 9488, 
        'face_tongue': 14227, 
        'face_hand': 18967,
        'face_neutral_skeptical': 23715, 
        'face_sleepy': 28453,
        'face_unwell': 33198, 
        'face_hat': 37934,
        'face_glasses': 42670, 
        'face_concerned': 47430, 
        'face_negative': 52172, 
        'face_costume': 56913, 
        'cat_face': 61655,
        'monkey_face': 66391, 
        'heart': 71153, 
        'emotion': 75906
    },
    "people_and_body": {
        'id': 899911,
        'hand_fingers_open': 85439, 
        'hand_fingers_partial': 90227, 
        'hand_single_finger': 95003, 
        'hand_fingers_closed': 99772, 
        'hands': 104567, 
        'hand_prop': 109319, 
        'body_parts': 114101, 
        'person': 119026, 
        'person_gesture': 124059, 
        'person_role': 129427, 
        'person_fantasy': 134405, 
        'person_activity': 139456, 
        'person_sport': 144584, 
        'person_resting': 149359, 
        'family': 154626, 
        'person_symbol': 159365
    },
    "component": {
        'id': 113687,
        'skin_tone': 168836, 
        'hair_style': 173573
    },
    "animals_and_nature": {
        'id': 116815,
        'animal_mammal': 183107, 
        'animal_bird': 187862, 
        'animal_amphibian': 192596, 
        'animal_reptile': 197337, 
        'animal_marine': 202082, 
        'animal_bug': 206833, 
        'plant_flower': 211579, 
        'plant_other': 216329
    },
    "food_and_drink": {
        'id': 228130,
        'food_fruit': 225814, 
        'food_vegetable': 230565, 
        'food_prepared': 235332, 
        'food_asian': 240082, 
        'food_marine': 244820, 
        'food_sweet': 249567, 
        'drink': 254320, 
        'dishware': 259061
    },
    "travel_and_places": {
        'id': 227294,
        'place_map': 268535, 
        'place_geographic': 273284, 
        'place_building': 278049, 
        'place_religious': 282789, 
        'place_other': 287541, 
        'transport_ground': 292329, 
        'transport_water': 297074, 
        'transport_air': 301823, 
        'hotel': 306559, 
        'time': 311326,
        'sky_and_weather': 316124
    },
    "activities": {
        'id': 335508,
        'event': 325613, 
        'award_medal': 330353, 
        'sport': 335114, 
        'game': 339877, 
        'arts_and_crafts': 344618
    },
    "objects": {
        'id': 336837,
        'clothing': 354134, 
        'sound': 358876, 
        'music': 363621, 
        'musical_instrument': 368365, 
        'phone': 373105, 
        'computer': 377857, 
        'light_and_video': 382609, 
        'book_paper': 387361, 
        'money': 392104, 
        'mail': 396852, 
        'writing': 401598, 
        'office': 406362, 
        'lock': 411102, 
        'tool': 415870, 
        'science': 420611, 
        'medical': 425351, 
        'household': 430111, 
        'other_object': 434855
    },
    "symbols": {
        'id': 449583,
        'transport_sign': 444334, 
        'warning': 449083, 
        'arrow': 453851, 
        'religion': 458606, 
        'zodiac': 463352, 
        'av_symbol': 468119, 
        'gender': 472858, 
        'math': 477599, 
        'punctuation': 482342, 
        'currency': 487077, 
        'other_symbol': 491843, 
        'keycap': 496601, 
        'alphanum': 501383, 
        'geometric': 506154
    },
    "flags": {
        'id': 552605,
        'flag': 515634, 
        'country_flag': 520625,
        'subdivision_flag': 525362
    }
}

EMOJI_DATA = {
""", output_path)

    extracted_data = extract_emoji_data()

    current_emoji = None
    previous_emoji = None

    progress = 0
    clocks = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕡']
    clock_index = 0
    for data in extracted_data:
        string_data = data[0]
        current_emoji = data[1][4]
        
        for i in enumerate(clocks):
            if clock_index == 12:
                clock_index = 0
            print(f"{clocks[clock_index]}: {progress} [", data[1][4], "] ------> EMOJI_DATA{}")
            clock_index = clock_index + 1
            break
        
        if current_emoji == previous_emoji:
            continue        
        
        _write_data(string_data, output_path)
        
        previous_emoji = current_emoji
        progress = progress + 1

    ###############################


    ###############################

    _write_data(
"""
}
""",
    output_path)
    print("Finished extracting & compiling emoji data successfully.")

def generate_data():
    # Find the latest version at https://www.unicode.org/reports/tr51/#emoji_data
    emoji_source = get_unicode_emoji_test_file(15.0)
    emoji_sequences_source = get_unicode_emoji_variation_sequence_file('15.0.0')
    emojis = extract_emojis(emoji_source, emoji_sequences_source)
    # Find latest release tag at https://cldr.unicode.org/index/downloads
    github_tag = 'release-43-1'

    languages = {
        # Update names in other languages:
        'de': extract_names(github_tag, 'de', 'de', get_emojiterra_from_url('https://emojiterra.com/de/kopieren/')),
        'es': extract_names(github_tag, 'es', 'es', get_emojiterra_from_url('https://emojiterra.com/es/copiar/')),
        'fr': extract_names(github_tag, 'fr', 'fr', get_emojiterra_from_url('https://emojiterra.com/fr/copier/')),
        'ja': extract_names(github_tag, 'ja', 'ja', get_emojiterra_from_url('https://emojiterra.com/copypaste/ja/')),
        'ko': extract_names(github_tag, 'ko', 'ko', get_emojiterra_from_url('https://emojiterra.com/copypaste/ko/')),
        'pt': extract_names(github_tag, 'pt', 'pt', get_emojiterra_from_url('https://emojiterra.com/pt/copiar/')),
        'it': extract_names(github_tag, 'it', 'it', get_emojiterra_from_url('https://emojiterra.com/it/copiare/')),
        'fa': extract_names(github_tag, 'fa', 'fa', get_emojiterra_from_url('https://emojiterra.com/copypaste/fa/')),
        'id': extract_names(github_tag, 'id', 'id', get_emojiterra_from_url('https://emojiterra.com/copypaste/id/')),
        'zh': extract_names(github_tag, 'zh', 'zh', get_emojiterra_from_url('https://emojiterra.com/copypaste/zh/')),
    }

    github_alias_dict = get_emoji_from_github_api('https://api.github.com/emojis')
    cheat_sheet_dict = get_cheat_sheet('https://www.webfx.com/tools/emoji-cheat-sheet/')
    youtube_dict = get_emoji_from_youtube('https://www.gstatic.com/youtube/img/emojis/emojis-png-7.json')

    used_github_aliases = set()

    escapedToUnicodeMap = {escaped: escaped.encode().decode('unicode-escape') for escaped in emojis}  # maps: "\\U0001F4A4" to "\U0001F4A4"

    all_existing_aliases_and_en = set(item for emj_data in EMOJI_DATA.values() for item in emj_data.get('alias', []))
    all_existing_aliases_and_en.update(emj_data['en'] for emj_data in EMOJI_DATA.values())

    f = 0
    c = 0
    new_aliases = []
    for code, v in sorted(emojis.items(), key=lambda item: item[1]["en"]):
        language_str = ''
        emj = escapedToUnicodeMap[code]

        alternative = re.sub(r"\\U0000FE0[EF]$", "", code)
        emj_no_variant = escapedToUnicodeMap[alternative]

        # add names in other languages
        for lang in languages:
            if emj in languages[lang]:
                language_str += ",\n        '%s': '%s'" % (
                    lang, languages[lang][emj])
            elif 'variant' in v:
                # the language annotation uses the normal emoji (no variant), while the emoji-test.txt uses the emoji or text variant
                if emj_no_variant in languages[lang]:
                    language_str += ",\n        '%s': '%s'" % (
                        lang, languages[lang][emj_no_variant])

        # Add existing alias from EMOJI_DATA
        aliases = set()
        if emj in EMOJI_DATA and 'alias' in EMOJI_DATA[emj]:
            aliases.update(a[1:-1] for a in EMOJI_DATA[emj]['alias'])
        old_aliases = set(aliases)

        if emj_no_variant in EMOJI_DATA and 'alias' in EMOJI_DATA[emj_no_variant]:
            aliases.update(a[1:-1] for a in EMOJI_DATA[emj_no_variant]['alias'])

        # Add alias from GitHub API
        github_aliases = find_github_aliases(emj, github_alias_dict, v, emj_no_variant)
        aliases.update(shortcut for shortcut in github_aliases if shortcut not in all_existing_aliases_and_en)
        used_github_aliases.update(github_aliases)

        # Add alias from cheat sheet
        if emj in cheat_sheet_dict and cheat_sheet_dict[emj] not in all_existing_aliases_and_en:
            aliases.add(cheat_sheet_dict[emj][1:-1])
        if emj_no_variant in cheat_sheet_dict and cheat_sheet_dict[emj_no_variant] not in all_existing_aliases_and_en:
            aliases.add(cheat_sheet_dict[emj_no_variant][1:-1])

        # Add alias from youtube
        if emj in youtube_dict:
            aliases.update(shortcut[1:-1] for shortcut in youtube_dict[emj] if shortcut not in all_existing_aliases_and_en)
        if emj_no_variant in youtube_dict:
            aliases.update(shortcut[1:-1] for shortcut in youtube_dict[emj_no_variant] if shortcut not in all_existing_aliases_and_en)

        # Remove if alias is same as 'en'-name
        if v["en"] in aliases:
            aliases.remove(v["en"])

        # Store new aliases to print them at the end after the dict of dicts
        if emj in EMOJI_DATA:
            if 'alias' in EMOJI_DATA[emj]:
                diff = aliases.difference(a[1:-1] for a in EMOJI_DATA[emj]['alias'])
            else:
                diff = aliases
            for a in diff:
                new_aliases.append(f"# alias NEW {a} FOR {emj} CODE {code}")

        # Keep the order of existing aliases intact
        if emj in EMOJI_DATA and 'alias' in EMOJI_DATA[emj]:
            aliases = [a[1:-1] for a in EMOJI_DATA[emj]['alias']] + [a for a in aliases if f":{a}:" not in EMOJI_DATA[emj]['alias']]

        if any("flag_for_" in a for a in aliases):
            # Put the :flag_for_COUNTRY: alias as the first entry so that it gets picked by demojize()
            # This ensures compatibility because in the past there was only the :flag_for_COUNTRY: alias
            aliases = [a for a in aliases if "flag_for_" in a] + [a for a in aliases if "flag_for_" not in a]

        # Print dict of dicts
        alias = ''
        if len(aliases) > 0:
            alias_list_str = ", ".join([f"':{a}:'" for a in aliases])
            alias = ",\n        'alias': [%s]" % (alias_list_str, )
        variant = ",\n        'variant': True" if 'variant' in v else ''
        print(f"""    '{code}': {{  # {emj}
        'en': ':{v['en']}:',
        'status': {v["status"]},
        'E': {v["version"]:g}{alias}{variant}{language_str}
    }}""", end=",\n")
        if v["status"] == "fully_qualified":
            f += 1
        elif v["status"] == "component":
            c += 1



