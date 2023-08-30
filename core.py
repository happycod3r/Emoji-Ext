"""
emojix.core
~~~~~~~~~~

Core components for emojix derived from https://www.github.com/carpedm20/emoji.

"""

import re
import unicodedata
from typing import Any, Text, Dict, Tuple, List, Iterator
from tokenizer import Token, EmojiMatch, EmojiMatchZWJ, EmojiMatchZWJNonRGI, tokenize, filter_tokens
from emoji_data.data_dict_retrieval import _EMOJI_ALIASES_CACHE, _EMOJI_LANG_CACHE, get_categories_dict, get_emoji_aliases_data, get_emoji_data_for_lang
from emoji_data.data_dict import EMOJI_DATA, CATEGORIES, LANGUAGES, STATUS

__all__ = [
    "category_exists", "category", 
    "Token", "EmojiMatch", "EmojiMatchZWJ", "EmojiMatchZWJNonRGI",
]

_DEFAULT_DELIMITER = ':'
_EMOJI_NAME_PATTERN = '\\w\\-&.’”“()!#*+,/«»\u0300\u0301\u0302\u0303\u0308\u030a\u0327\u064b\u064e\u064f\u0650\u0653\u0654\u3099\u30fb\u309a'

class BasicEmojis: 
    def __init__(self):
        
        self.emojis = {
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
        
        self.emoji_categories = {
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
        
        self._VARIATION_SELECTOR_16 = '️' # Used to specify a particular glyph variation for a base character
        self._REPLACEMENT_CHARACTER = 'U+FFFD' # '�'  
        self._ZWJ_CODEPOINT='U+200D' # Unicode code point for the Zero Width Joiner.
        self._ZWJ_ESCAPE_SEQUENCE='\u200d'
    
    def category_exists(self, category: str) -> bool:
        """
        Returns True if the category exists otherwise returns False.
        """
        exists = False
        for ctgry in self.emoji_categories.keys():
            if category == ctgry:
                return True
        for ctgry in self.emoji_categories.keys():
            for sub_ctgry in self.emoji_categories[ctgry]:
                if category == sub_ctgry:
                    return True
        return False
    
    def category(self, emoji: str) -> (str| None):
        """
        Returns a tuple containing the category and sub category 
        for the given emoji. Returns None if no category or non emoji was given.
        """
        if self.is_emoji(emoji):
            for key in self.emojis.keys():
                for subkey in self.emojis[key]:
                    for _emoji in self.emojis[key][subkey]:
                        if _emoji == emoji:
                            return (key, subkey)
    
    def get_all_categories(self) -> list[str]:
        categories = []
        for key in self.emojis.keys():
            categories.append(key)
            for item in self.emojis[key]:
                categories.append(item)
        return categories
        
    def get_top_level_categories(self) -> list[str]:
        categories = []
        for key in self.emojis.keys():
            categories.append(key)
        return categories
    
    def get_sub_level_categories(self) -> list[str]:
        sub_categories = []
        for key in self.emojis.keys():
            for item in self.emojis[key]:
                sub_categories.append(item)
        return sub_categories

    def is_top_level_category(self, category: str) -> (bool | None):
        if self.category_exists(category):
            for ctgry in self.emojis.keys():
                if ctgry == category:
                    return True
            return False
        else:
            return None
    
    def get_parent_category(self, sub_category: str) -> (str | None):
        for key in self.emojis.keys():
            for item in self.emojis[key]:
                if item == sub_category:
                    return key
        return None

    def get_child_categories(self, category: str) -> (list[str] | None):
        if self.category_exists(category):
            if self.is_top_level_category(category):
                child_categories = []
                for key in self.emojis[category]:
                    child_categories.append(key)
                return child_categories
            return None
        return None

    def emoji_factory(self, category: str) -> (str | None):
        if self.category_exists(category):
            # If category is a top level category
            for key in self.emojis.keys():
                if key == category:
                    for item in self.emojis[key]:
                        yield item
                    return True
            # If category is a sub level category
            for key in self.emojis.keys():
                for subkey in self.emojis[key]:
                    if subkey == category:
                        for item in self.emojis[key][subkey]:    
                            yield item
                        return True
            return False
        else:
            return None
        
    def get_emojis_in_category(self, category: str) -> list[str]:
        if self.category_exists(category):
            if self.is_top_level_category(category):
                emojis = {}
                for subkey in self.emojis[category]:
                    emojis[f"{subkey}"] = self.emojis[category][subkey]
                return emojis
            emojis = []
            for item in self.emojis[self.get_parent_category(category)][category]:
                emojis.append(item)
            return emojis
        return None

    def is_emoji_variation(self, emoji: str) -> bool:
        """
        Checks for the existence of a variation selector which signifies a
        variation then returns True if found. Returns False otherwise.
        
        The character "️" is a variation selector, specifically Variation Selector-16 (VS16). 
        A variation selector is a Unicode character used to specify a particular glyph 
        variation for a base character. Variation selectors are used in conjunction with 
        characters that have multiple possible glyph forms. 

        In the case of VS16, it is used to select an emoji-style presentation for a preceding 
        character. When combined with certain characters, it can change their appearance to an 
        emoji-like representation. However, when it's used alone without a preceding character, 
        it might not have a visible representation by itself. It is intended to modify the 
        presentation of the preceding character and doesn't carry a specific visual appearance 
        on its own.

        The appearance of VS16 might vary depending on the font and rendering engine being used.
        """
        is_variation = False
        for char in emoji:
            if char == self._VARIATION_SELECTOR_16:
                return True
        return False

    def is_emoji(self, char: str) -> bool:
        """
        """
        char_len = len(char)
        try:
            if char_len == 1:
                if unicodedata.category(char) == "So":
                    return True
                return False
            elif char_len > 1:
                if self.is_emoji_variation(char):
                    return True
                return False
        except TypeError as e:
            print(repr(e))

    def emoji_to_unicode(self, emojis: str | list[str]) -> (str | list[str]):
        emoji_string = emojis
        unicode_values = []
        for i in range(0, len(emoji_string)):
            unicode_values.append(ord(emoji_string[i].encode('utf-16', 'surrogatepass').decode('utf-16')))
        unicode_strings = []
        for codepoint in unicode_values:
            unicode_strings.append(f"U+{codepoint:04X}")        
        return unicode_strings
    
    def get_emoji_name(self, emoji: str) -> (str | None):
        if self.is_emoji(emoji):
            return unicodedata.name(emoji)
        return None    
    
    def get_emoji_by_name(self, name: str) -> (str | None):
        try:
            emoji = unicodedata.lookup(name)
            return unicodedata.lookup(name)
        except KeyError as e:
            return None
    
    def demojize(self, emoji: str) -> (str | None):
        if self.is_emoji(emoji):
            if self.is_emoji_variation(emoji):
                for char in emoji:
                    if char == self._VARIATION_SELECTOR_16:
                        continue
                    name = self.get_emoji_name(char).replace(" ", "_").lower()
                    name = f":_{name}_:"
                    return name                 
            name = self.get_emoji_name(emoji).replace(" ", "_").lower()
            name = f":_{name}_:"
            return name
        return None
    
    def emojize(self, demojized_emoji: str, delimeter: str=None) -> (str | None):
        try:
            emojized = unicodedata.lookup(demojized_emoji.lstrip(":_").rstrip("_:").replace("_", " ").upper())
            return emojized
        except KeyError as e:
            print(repr(e))

    def emoji_list(self, text: str) -> (list[str] | None):
        emojis = []
        index = 0
        prev_index = 0
        for char in text:
            if self.is_emoji(char):
                emojis.append(char)
            if char == self._VARIATION_SELECTOR_16:
                # Append the vs16 to the last emoji.
                emojis[-1] += self._VARIATION_SELECTOR_16
            index = index + 1
        return emojis

    def distinct_emoji_list(self, text: str) -> (list[str] | None):
        emojis = []
        for char in text:
            if self.is_emoji(char):
                if len(emojis) == 0:
                    emojis.append(char)
                    continue
                duplicate = False
                for i in range(0, len(emojis)):
                    if char == emojis[i]:
                        duplicate = True
                if not duplicate:
                    emojis.append(char)
        return emojis
    
    def emoji_count(self, text: str, unique: bool=False) -> int:
        count = 0
        emojis = []
        if not unique:
            for char in text:
                if self.is_emoji(char):
                    emojis.append(char)
            return len(emojis)
        for char in text:
            if self.is_emoji(char):
                if len(emojis) == 0:
                    emojis.append(char)
                    continue
                duplicate = False
                for i in range(0, len(emojis)):
                    if char == emojis[i]:
                        duplicate = True
                if not duplicate:
                    emojis.append(char)
        return len(emojis)

    def analyze(self, text: str, non_emoji: bool=False):
        """
        A generator function that loops through the characters of a 
        string represented by 'text'. If the character is an emoji it
        yields a tuple containing the emoji and its position in the 
        string.
        
        Optionally you can choose to also yield at non emoji characters
        by changing 'non_emoji' to True. 
        """
        position = 0
        for char in text:
            if non_emoji:
                if self.is_emoji_variation(char):
                    positions = (position - 1, position)
                    data = (char, positions)
                else:
                    data = (char, position)
                position += 1
                yield data
            else:
                data = None
                if self.is_emoji_variation(char):
                    positions = (position - 1, position)
                    data = (char, positions)
                if self.is_emoji(char):
                    data = (char, position)
                position += 1
                if data is not None:
                    yield data

    def emoji_position(self, text: str):
        position = 0
        for char in text:
            data = None
            if self.is_emoji_variation(char):
                positions = (position - 1, position)
                data = (positions)
            if self.is_emoji(char):
                data = (position)
            position += 1
            if data is not None:
                yield data

    def replace_emojis(self, string: str, replacement: str):
        done = False
        emojis = self.distinct_emoji_list(string)
        while not done:
            for item in emojis:
                string = string.replace(item, replacement)
                present = True
                for char in string:
                    if char == item:
                        present = True
                    present = False
                if not present:
                    done = True
        return string
        
    def has_replacement_character(self, text: str) -> (bool | None):
        for char in text:
            if char == self._REPLACEMENT_CHARACTER:
                return True
        return False
     
    def version(self, _emoji: str) -> float:  
        import emoji
        return emoji.version(_emoji)

class config():
    """Module-wide configuration"""

    demojize_keep_zwj = True
    """Change the behavior of :func:`emoji.demojize()` regarding
    zero-width-joiners (ZWJ/``\\u200D``) in emoji that are not
    "recommended for general interchange" (non-RGI).
    It has no effect on RGI emoji.

    For example this family emoji with different skin tones "👨‍👩🏿‍👧🏻‍👦🏾" contains four
    person emoji that are joined together by three ZWJ characters:
    ``👨\\u200D👩🏿\\u200D👧🏻\\u200D👦🏾``

    If ``True``, the zero-width-joiners will be kept and :func:`emoji.emojize()` can
    reverse the :func:`emoji.demojize()` operation:
    ``emoji.emojize(emoji.demojize(s)) == s``

    The example emoji would be converted to
    ``:man:\\u200d:woman_dark_skin_tone:\\u200d:girl_light_skin_tone:\\u200d:boy_medium-dark_skin_tone:``

    If ``False``, the zero-width-joiners will be removed and :func:`emoji.emojize()`
    can only reverse the individual emoji: ``emoji.emojize(emoji.demojize(s)) != s``

    The example emoji would be converted to
    ``:man::woman_dark_skin_tone::girl_light_skin_tone::boy_medium-dark_skin_tone:``
    """

    replace_emoji_keep_zwj = False
    """Change the behavior of :func:`emoji.replace_emoji()` regarding
    zero-width-joiners (ZWJ/``\\u200D``) in emoji that are not
    "recommended for general interchange" (non-RGI).
    It has no effect on RGI emoji.

    See :attr:`config.demojize_keep_zwj` for more information.
    """

def category_exists(category: str=None, category_id: int=None) -> bool:
    if category_id is not None:
        for key in CATEGORIES.keys():
            if CATEGORIES[key]["id"] == category_id:
                return True
            for subkey in CATEGORIES[key].keys():
                if CATEGORIES[key][subkey] == category_id:
                    return True
    for key in EMOJI_DATA.keys():
        if category == EMOJI_DATA[key]["category"]:
            return True
        if category == EMOJI_DATA[key]["subcategory"]:
            return True
    return False
    
def category(emoji: (list[str] | str)) -> (dict | List[Dict] | None):
    categories = []
    for i in range(len(emoji)):
        if is_emoji(emoji[i]):                    
            for key in EMOJI_DATA.keys():
                if key == emoji[i]:
                    data = {}
                    data["emoji"] = key
                    data["category"] = EMOJI_DATA[key]["category"]
                    data["category_id"] = EMOJI_DATA[key]["category_id"]
                    data["subcategory"] = EMOJI_DATA[key]["subcategory"]
                    data["subcategory_id"] = EMOJI_DATA[key]["subcategory_id"]
                    if data not in categories:
                        categories.append(data)
    if len(categories) > 1:
        return categories
    return data

def get_all_categories(only_names: bool=False) -> List[str]:
    categories = []
    if only_names:
        for key in CATEGORIES.keys():
            categories.append(key)
            for subkey in CATEGORIES[key].keys():
                if subkey == "id":
                    continue
                categories.append(subkey)
        return categories
    return CATEGORIES

def top_level_categories() -> List[Dict[str, int]]:
    top_lvl_categories = []
    for key in CATEGORIES.keys():
        data = {"category": key, "id": CATEGORIES[key]["id"]}
        top_lvl_categories.append(data)
    return top_lvl_categories

def sub_level_categories() -> List[Dict[str, int]]:
    sub_lvl_categories = []
    for key in CATEGORIES.keys():
        for subkey in CATEGORIES[key]:
            if subkey != "id":
                data = {"subcategory": subkey, "id": CATEGORIES[key][subkey]}
                sub_lvl_categories.append(data)
    return sub_lvl_categories

def is_top_level_category(category: str=None, category_id: int=None) -> (bool | None):
    if category_id is not None and category_exists(category_id=category_id):
        for key in CATEGORIES.keys():
            if CATEGORIES[key]["id"] == category_id:
                return True
        return False
    if category_id is None and category is not None and category_exists(category):
        for key in CATEGORIES.keys():
            if key == category:
                return True
        return False
    return None
 
def parent_category(category: str=None, category_id: int=None, emojis_in_category: bool=False) -> (str | None):
    if category_id is not None and category_exists(category_id=category_id):
        for key in CATEGORIES.keys():
            for subkey in CATEGORIES[key].keys():
                if CATEGORIES[key][subkey] == category_id:
                    if not emojis_in_category:
                        data = {"category": key, "id":CATEGORIES[key]["id"]}
                        return data
                    emojis = []
                    for edkey in EMOJI_DATA.keys():
                        if EMOJI_DATA[edkey]["category"] == key:
                            emojis.append(EMOJI_DATA[edkey])
                    return emojis
    if category_id is None and category is not None and category_exists(category):
        for key in CATEGORIES.keys():
            for subkey in CATEGORIES[key].keys():
                if subkey == category:
                    if not emojis_in_category:
                        return {"category": key, "id": CATEGORIES[key]["id"]}
                    emojis = []
                    for edkey in EMOJI_DATA.keys():
                        if EMOJI_DATA[edkey]["category"] == key:
                            emojis.append(EMOJI_DATA[edkey])
                    return emojis

def child_categories(category: str=None, category_id: int=None, emojis_in_category: bool=False) -> (List[str] | None):
    child_categories = []
    if category_id is not None and category_exists(category_id=category_id):
        for key in CATEGORIES.keys():
            if CATEGORIES[key]["id"] == category_id:
                for subkey in CATEGORIES[key].keys():
                    if subkey == "id":
                        continue
                    if not emojis_in_category:
                        data = {"subcategory": subkey, "id": CATEGORIES[key][subkey]}
                    emojis = []
                    for edkey in EMOJI_DATA.keys():
                        if EMOJI_DATA[edkey]["subcategory"] == subkey:
                            emojis.append(EMOJI_DATA[edkey])
                    data = {"subcategory": subkey, "id": CATEGORIES[key][subkey], "emojis": emojis}
                    child_categories.append(data)
        return child_categories
    if category is not None and category_exists(category):
        for key in CATEGORIES.keys():
            if key == category:
                for subkey in CATEGORIES[key].keys():
                    if subkey == "id":
                        continue
                    if not emojis_in_category:
                        data = {"subcategory": subkey, "id": CATEGORIES[key][subkey]}
                    emojis = []
                    for edkey in EMOJI_DATA.keys():
                        if EMOJI_DATA[edkey]["subcategory"] == subkey:
                            emojis.append(EMOJI_DATA[edkey])
                    data = {"subcategory": subkey, "id": CATEGORIES[key][subkey], "emojis": emojis}
                    child_categories.append(data)
    return child_categories

def iterate_category(func: object, func_args: list=None, category: str=None, category_id: int=None) -> None:
    category_items = []
    if category_id is not None and category_exists(category_id=category_id): 
        for key in EMOJI_DATA.keys():
            if EMOJI_DATA[key]["category_id"] == category_id:
                category_items.append(EMOJI_DATA[key])
            if EMOJI_DATA[key]["subcategory_id"] == category_id:
                category_items.append(EMOJI_DATA[key])
    if category_id is None and category is not None and category_exists(category):
        for key in EMOJI_DATA.keys():
            if EMOJI_DATA[key]["category"] == category:
                category_items.append(EMOJI_DATA[key])
            if EMOJI_DATA[key]["subcategory"] == category:
                category_items.append(EMOJI_DATA[key])
    for i in range(len(category_items)):
        func(category_items[i], func_args)

def emoji_factory(category: str=None, category_id: int=None) -> (str | None):
    if category_id is not None and category_exists(category_id=category_id):
        for key in EMOJI_DATA.keys():
            if EMOJI_DATA[key]["category_id"] == category_id:
                yield EMOJI_DATA[key]
            if EMOJI_DATA[key]["subcategory_id"] == category_id:
                yield EMOJI_DATA[key]
    if category_id is None and category is not None and category_exists(category):
        for key in EMOJI_DATA.keys():
            if EMOJI_DATA[key]["category"] == category:
                yield EMOJI_DATA[key]
            if EMOJI_DATA[key]["subcategory"] == category:
                yield EMOJI_DATA[key]
    return None

def get_emojis_in_category(category: str=None, category_id: int=None) -> List[str]:
    emojis = []
    if category_id is not None:
        if category_exists(category_id=category_id):
            for key in EMOJI_DATA.keys():
                if EMOJI_DATA[key]["category_id"] == category_id:
                    emojis.append(EMOJI_DATA[key])
    if category_id is None and category is not None:
        if category_exists(category):
            for key in EMOJI_DATA.keys():
                if EMOJI_DATA[key]["category"] == category:
                    emojis.append(EMOJI_DATA[key])
                if EMOJI_DATA[key]["subcategory"] == category:
                    emojis.append(EMOJI_DATA[key])
    return emojis

def is_emoji_variation(emoji: str) -> (bool | None):
    if is_emoji(emoji):
        for key in EMOJI_DATA.keys():
            if key == emoji:
                return EMOJI_DATA[key]["variant"]
    return None

def get_all_emoji_variants() -> List[Dict[str, Any]]:
    variants = []
    for key in EMOJI_DATA.keys():
        if EMOJI_DATA[key]["variant"] is True:
            variants.append(EMOJI_DATA[key])
    return variants    
    
def emoji_to_unicode(emoji: str | List[str]) -> (str | List[str]):
    unicode_values = []
    for i in range(0, len(emoji)):
        unicode_values.append(ord(emoji[i].encode("utf-16", "surrogatepass").decode("utf-16")))
    unicode_strings = []
    for codepoint in unicode_values:
        unicode_strings.append(f"U+{codepoint:04X}")        
    return unicode_strings

def emoji_name(emoji: str) -> (str | None):
    if is_emoji(emoji):
        for key in EMOJI_DATA.keys():
            if key == emoji:
                return EMOJI_DATA[key]["name"]
    return None

def get_emoji_by_name(name: str) -> (str | None):
    for key in EMOJI_DATA.keys():
        _name = EMOJI_DATA[key]["name"]
        if _name == f":{name}:":
            return key

def has_zwj(text: str) -> (bool | None):
    for i in range(len(text)):
        if text[i] == '️':
            return True
    return False

def emojize(
        string,
        delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
        variant=None,
        language='en',
        version=None,
        handle_version=None
) -> str:
    """
    Replace emoji names in a string with Unicode codes.
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbsup:", language='alias'))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun {thumbs_up}", delimiters = ("{", "}")))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :red_heart:", variant="text_type"))
        Python is fun ❤
        >>> print(emoji.emojize("Python is fun :red_heart:", variant="emoji_type"))
        Python is fun ❤️ # red heart, not black heart

    :param string: String contains emoji names.
    :param delimiters: (optional) Use delimiters other than _DEFAULT_DELIMITER. Each delimiter
        should contain at least one character that is not part of a-zA-Z0-9 and ``_-&.()!?#*+,``.
        See ``emoji.core._EMOJI_NAME_PATTERN`` for the regular expression of unsafe characters.
    :param variant: (optional) Choose variation selector between "base"(None), VS-15 ("text_type") and VS-16 ("emoji_type")
    :param language: Choose language of emoji name: language code 'es', 'de', etc. or 'alias'
        to use English aliases
    :param version: (optional) Max version. If set to an Emoji Version,
        all emoji above this version will be ignored.
    :param handle_version: (optional) Replace the emoji above ``version``
        instead of ignoring it. handle_version can be either a string or a
        callable; If it is a callable, it's passed the Unicode emoji and the
        data dict from :data:`EMOJI_DATA` and must return a replacement string
        to be used::

            handle_version('\\U0001F6EB', {
                'en' : ':airplane_departure:',
                'status' : fully_qualified,
                'e' : 1,
                'alias' : [':flight_departure:'],
                'de': ':abflug:',
                'es': ':avión_despegando:',
                ...
            })

    :raises ValueError: if ``variant`` is neither None, 'text_type' or 'emoji_type'

    """

    if language == 'alias':
        language_pack = get_emoji_aliases_data()
    else:
        language_pack = get_emoji_data_for_lang(language)

    pattern = re.compile('(%s[%s]+%s)' %
                         (re.escape(delimiters[0]), _EMOJI_NAME_PATTERN, re.escape(delimiters[1])))

    def replace(match):
        name = match.group(1)[len(delimiters[0]):-len(delimiters[1])]
        emj = language_pack.get(
            _DEFAULT_DELIMITER +
            unicodedata.normalize('NFKC', name) +
            _DEFAULT_DELIMITER)
        if emj is None:
            return match.group(1)

        if version is not None and EMOJI_DATA[emj]['E'] > version:
            if callable(handle_version):
                emj_data = EMOJI_DATA[emj].copy()
                emj_data['match_start'] = match.start()
                emj_data['match_end'] = match.end()
                return handle_version(emj, emj_data)

            elif handle_version is not None:
                return str(handle_version)
            else:
                return ''

        if variant is None or 'variant' not in EMOJI_DATA[emj]:
            return emj

        if emj[-1] == '\uFE0E' or emj[-1] == '\uFE0F':
            # Remove an existing variant
            emj = emj[0:-1]
        if variant == "text_type":
            return emj + '\uFE0E'
        elif variant == "emoji_type":
            return emj + '\uFE0F'
        else:
            raise ValueError(
                "Parameter 'variant' must be either None, 'text_type' or 'emoji_type'")

    return pattern.sub(replace, string)

def analyze(string: str, non_emoji: bool = False, join_emoji: bool = True) -> Iterator[Token]:
    """
    Find unicode emoji in a string. Yield each emoji as a named tuple
    :class:`Token` ``(chars, EmojiMatch)`` or `:class:`Token` ``(chars, EmojiMatchZWJNonRGI)``.
    If ``non_emoji`` is True, also yield all other characters as
    :class:`Token` ``(char, char)`` .

    :param string: String to analyze
    :param non_emoji: If True also yield all non-emoji characters as Token(char, char)
    :param join_emoji: If True, multiple EmojiMatch are merged into a single
        EmojiMatchZWJNonRGI if they are separated only by a ZWJ.
    """

    return filter_tokens(
        tokenize(string, keep_zwj=True), emoji_only=not non_emoji, join_emoji=join_emoji)

def demojize(
        string,
        delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
        language='en',
        version=None,
        handle_version=None
):
    """
    Replace Unicode emoji in a string with emoji shortcodes. Useful for storage.
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.demojize("Python is fun 👍"))
        Python is fun :thumbs_up:
        >>> print(emoji.demojize("icode is tricky 😯", delimiters=("__", "__")))
        Unicode is tricky __hushed_face__

    :param string: String contains Unicode characters. MUST BE UNICODE.
    :param delimiters: (optional) User delimiters other than ``_DEFAULT_DELIMITER``
    :param language: Choose language of emoji name: language code 'es', 'de', etc. or 'alias'
        to use English aliases
    :param version: (optional) Max version. If set to an Emoji Version,
        all emoji above this version will be removed.
    :param handle_version: (optional) Replace the emoji above ``version``
        instead of removing it. handle_version can be either a string or a
        callable ``handle_version(emj: str, data: dict) -> str``; If it is
        a callable, it's passed the Unicode emoji and the data dict from
        :data:`EMOJI_DATA` and must return a replacement string  to be used.
        The passed data is in the form of::

            handle_version('\\U0001F6EB', {
                'en' : ':airplane_departure:',
                'status' : fully_qualified,
                'E' : 1,
                'alias' : [':flight_departure:'],
                'de': ':abflug:',
                'es': ':avión_despegando:',
                ...
            })

    """

    if language == 'alias':
        language = 'en'
        _use_aliases = True
    else:
        _use_aliases = False

    def handle(emoji_match):
        if version is not None and emoji_match.data['E'] > version:
            if callable(handle_version):
                return handle_version(emoji_match.emoji, emoji_match.data_copy())
            elif handle_version is not None:
                return handle_version
            else:
                return ''
        elif language in emoji_match.data:
            if _use_aliases and 'alias' in emoji_match.data:
                return delimiters[0] + emoji_match.data['alias'][0][1:-1] + delimiters[1]
            else:
                return delimiters[0] + emoji_match.data[language][1:-1] + delimiters[1]
        else:
            # The emoji exists, but it is not translated, so we keep the emoji
            return emoji_match.emoji

    matches = tokenize(string, keep_zwj=config.demojize_keep_zwj)
    return "".join(str(handle(token.value)) if isinstance(
        token.value, EmojiMatch) else token.value for token in matches)

def replace_emoji(string, replace='', version=-1):
    """
    Replace Unicode emoji in a customizable string.

    :param string: String contains Unicode characters. MUST BE UNICODE.
    :param replace: (optional) replace can be either a string or a callable;
        If it is a callable, it's passed the Unicode emoji and the data dict from
        :data:`EMOJI_DATA` and must return a replacement string to be used.
        replace(str, dict) -> str
    :param version: (optional) Max version. If set to an Emoji Version,
        only emoji above this version will be replaced.
    """

    def handle(emoji_match):
        if version > -1:
            if emoji_match.data['E'] > version:
                if callable(replace):
                    return replace(emoji_match.emoji, emoji_match.data_copy())
                else:
                    return str(replace)
        elif callable(replace):
            return replace(emoji_match.emoji, emoji_match.data_copy())
        elif replace is not None:
            return replace
        return emoji_match.emoji

    matches = tokenize(string, keep_zwj=config.replace_emoji_keep_zwj)
    if config.replace_emoji_keep_zwj:
        matches = filter_tokens(
            matches, emoji_only=False, join_emoji=True)
    return "".join(str(handle(m.value)) if isinstance(
        m.value, EmojiMatch) else m.value for m in matches)

def emoji_list(string):
    """
    Returns the location and emoji in list of dict format.
        >>> emoji.emoji_list("Hi, I am fine. 😁")
        [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
    """

    return [{
        'match_start': m.value.start,
        'match_end': m.value.end,
        'emoji': m.value.emoji,
    } for m in tokenize(string, keep_zwj=False) if isinstance(m.value, EmojiMatch)]

def distinct_emoji_list(string):
    """Returns distinct list of emojis from the string."""
    distinct_list = list(
        {e['emoji'] for e in emoji_list(string)}
    )
    return distinct_list

def emoji_count(string, unique=False):
    """
    Returns the count of emojis in a string.

    :param unique: (optional) True if count only unique emojis
    """
    if unique:
        return len(distinct_emoji_list(string))
    return len(emoji_list(string))

def is_emoji(string):
    """
    Returns True if the string is a single emoji, and it is "recommended for
    general interchange" by Unicode.org.
    """
    return string in EMOJI_DATA

def purely_emoji(string: str) -> bool:
    """
    Returns True if the string contains only emojis.
    This might not imply that `is_emoji` for all the characters, for example,
    if the string contains variation selectors.
    """
    return all(isinstance(m.value, EmojiMatch) for m in analyze(string, non_emoji=True))

def version(string):
    """
    Returns the Emoji Version of the emoji.

    See https://www.unicode.org/reports/tr51/#Versioning for more information.
        >>> emoji.version("😁")
        0.6
        >>> emoji.version(":butterfly:")
        3

    :param string: An emoji or a text containing an emoji
    :raises ValueError: if ``string`` does not contain an emoji
    """
    # Try dictionary lookup
    if string in EMOJI_DATA:
        return EMOJI_DATA[string]['E']

    language_pack = get_emoji_data_for_lang('en')
    if string in language_pack:
        emj_code = language_pack[string]
        if emj_code in EMOJI_DATA:
            return EMOJI_DATA[emj_code]['E']

    # Try to find first emoji in string
    version = []

    def f(e, emoji_data):
        version.append(emoji_data['R'])
        return ''
    replace_emoji(string, replace=f, version=-1)
    if version:
        return version[0]
    emojize(string, language='alias', version=-1, handle_version=f)
    if version:
        return version[0]
    for lang_code in _EMOJI_LANG_CACHE:
        emojize(string, language=lang_code, version=-1, handle_version=f)
        if version:
            return version[0]

    raise ValueError("No emoji found in string")

