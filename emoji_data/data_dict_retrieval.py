from data_dict import CATEGORIES, EMOJI_DATA, BASIC_EMOJIS, LANGUAGES, STATUS
from typing import Dict, List, Any

__all__ = [
    "get_emoji_data_for_lang", "get_emoji_aliases_data", "get_categories_data",
    "categories_key_chain", "emoji_data", "key_chain", "EMOJI_DATA", "STATUS", 
    "LANGUAGES", "CATEGORIES", "BASIC_EMOJIS"
]

_EMOJI_LANG_CACHE = {lang: None for lang in LANGUAGES}  # Cache for the language dicts

_EMOJI_ALIASES_CACHE = {}  # Cache for the aliases dict

def get_emoji_data_for_lang(lang) -> Dict:
    """Generate dict containing all fully-qualified and component emoji name for a language
    The dict is only generated once per language and then cached in _EMOJI_LANG_CACHE[lang]"""

    if _EMOJI_LANG_CACHE[lang] is None:
        _EMOJI_LANG_CACHE[lang] = {data[lang]: emj for emj, data in EMOJI_DATA.items()
                                if lang in data and data['status'] <= STATUS['fully_qualified']}

    return _EMOJI_LANG_CACHE[lang]

def get_emoji_aliases_data() -> Dict:
    """Generate dict containing all fully-qualified and component aliases
    The dict is only generated once and then cached in _EMOJI_ALIASES_CACHE"""

    if not _EMOJI_ALIASES_CACHE:
        _EMOJI_ALIASES_CACHE.update(get_emoji_data_for_lang('en'))
        for emj, data in EMOJI_DATA.items():
            if 'alias' in data and data['status'] <= STATUS['fully_qualified']:
                for alias in data['alias']:
                    _EMOJI_ALIASES_CACHE[alias] = emj

    return _EMOJI_ALIASES_CACHE

def get_categories_data() -> Dict:
    categories = []
    unique_categories = []
    categories_dict = {}
    for key in EMOJI_DATA.keys():
        categories.append(EMOJI_DATA[key]["category"])
        categories.append(EMOJI_DATA[key]["subcategory"])
    for i in range(len(categories)):
        if len(unique_categories) == 0:
            unique_categories.append(categories[i])
            continue
        if categories[i] not in unique_categories:
            unique_categories.append(categories[i])
    current_category = ""
    current_subcategory = ""
    index = 0
    for i in range(len(unique_categories)):
        for key in EMOJI_DATA.keys():
            if unique_categories[i] == EMOJI_DATA[key]["category"]:
                current_category = unique_categories[i].lower().replace("&", "and").replace(" ", "_")
                categories_dict[current_category] = {}
            if unique_categories[i] == EMOJI_DATA[key]["subcategory"]:
                current_subcategory = unique_categories[i].lower().replace("-", "_")
                categories_dict[current_category][current_subcategory] = {index}
            index = index + 1            
    return categories_dict

def categories_key_chain() -> Dict[Dict[str, int]]:
    return CATEGORIES.keys()

def emoji_data() -> Dict[Dict[str, int, Any]]:
    return EMOJI_DATA

def key_chain() -> Dict[Dict[str, Any]]:
    return EMOJI_DATA.keys()
