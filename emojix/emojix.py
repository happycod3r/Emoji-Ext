# MIT License
import emoji
# Copyright (c) 2023 Paul McCarthy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# **THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.**

import unicodedata

class Emojix:
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
        self._REPLACEMENT_CHARACTER = '�' # "U+FFFD"
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
        
    def iterate_category(self, category: str, func: object) -> (bool | None):
            if self.category_exists(category):
                # If category is a top level category
                for key in self.emojis.keys():
                    if key == category:
                        for item in self.emojis[key]:
                            func(item)
                        return True
                # If category is a sub level category
                for key in self.emojis.keys():
                    for subkey in self.emojis[key]:
                        if subkey == category:
                            for item in self.emojis[key][subkey]:    
                                func(item)
                            return True
                return False
            else:
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
    
    def unicode_to_emoji(self, codepoints: str | list[str]) -> (str | list[str]): 
        pass

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
     
    def version(self, emoji: str) -> float:  
        pass
    
            
