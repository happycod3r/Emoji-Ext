
from core import *
from emoji_data import *
from emoji_data.data_dict_retrieval import *
__all__ = [
    # emojix.core
    "KEYCHAIN", "CATS_KEYCHAIN",
    "category_exists", "category", "get_all_categories", 
    "top_level_categories", "sub_level_categories", "is_top_level_category", "parent_category", "child_categories", "iterate_category", "emoji_factory", "get_emojis_in_category", "is_emoji_variation", "get_all_emoji_variants", "emoji_to_unicode", "emoji_name", "get_emoji_by_name",
    "has_zwj", "emojize", "demojize", "analyze", "config",
    "emoji_list", "distinct_emoji_list", "emoji_count",
    "replace_emoji", "is_emoji", "purely_emoji", "version",
    # emojix.tokenize
    "Token", "EmojiMatch", "EmojiMatchZWJ", "EmojiMatchZWJNonRGI",
    "EMOJI_DATA", "STATUS", "LANGUAGES", "CATEGORIES", "BASIC_EMOJIS"
    # emojix.emoji_data.data_dict_retrieval
    "key_chain", "categories_key_chain", "emoji_data", "get_emoji_data_for_lang",
    "get_categories_data", "get_emoji_aliases_for_lang"
]

__version__ = '1.0.0'
__author__ = 'Paul McCarthy'
__email__ = 'paulmccarthy676@gmail.com'
__source__ = 'https://github.com/happycod3r/emojix'
__license__ = '''
New BSD License

Copyright (c) 2223, Paul McCarthy
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* The names of its contributors may not be used to endorse or promote products
  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
