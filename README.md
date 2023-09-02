# Emoji-x (Emoji Extended)

## [About](#about)
***Emoji-X*** or ***Emojix*** is built on top of the existing ***[Emoji](https://pypi.org/project/emoji/)*** module for Python. It aims to extend it with new functions and a more robust EMOJI_DATA dictionary.

## [Available Methods](#available_methods)

### [Emoji-X Methods](#emoji_x_methods)

- [category_exists()](#category_exists) - Checks whether or not the specified category exists.
- [category()](#category) - Gets the category of an emoji.
- [get_all_categories()](#get_all_categories) - Returns a dict of all emoji categories.
- [top_level_categories()](#top_level_categories) - Returns a list of top level categories.
- [sub_level_categories()](#sub_level_categories) - Returns a list of sub level categories.
- [is_top_level_category()](#is_top_level_category) - Returns whether or not an emoji category is a top level category.
- [parent_category()](#parent_category) - Returns the parent category of a category.
- [child_categories()](#child_categories) - Returns a list of child categories of a top level category.
- [iterate_category()](#iterate_category) - Iterate through a category of emojis and call func on each item.
- [emoji_factory()](#emoji_factory) - A generator which yields each emoji of a given category.
- [get_emojis_in_category()](#get_emojis_in_category) - Returns a list of emojis in a category.
- [is_emoji_variation()](#is_emoji_variation) - Checks if an emoji is a variation or not.
- [get_all_emoji_variants()](#get_all_emoji_variants) - Returns a list of all emoji variants.
- [emoji_to_unicode()](#emoji_to_unicode) - Returns a Unicode string for the specified emoji.
- [emoji_name()](#emoji_name) - Get the name of an emoji.
- [get_emoji_by_name()](#get_emoji_by_name) - Get an emoji by its name.
- [has_zwj()](#has_zwj) - Returns True if the emoji contains the zero width joiner character.
- [has_alias()](#has_alias) - Returns True if the emoji has an alias, otherwise False.
- [alias()](#alias) - Returns the alias for the given emoji.

### [Legacy Emoji Methods](#legacy_emoji_methods)

- [emojize()](#emojize) - Turns a demojized emoji back into an emoji.
- [demojize()](#demojize) - Turns an emojized emoji back into a form better for storge.
- [replace_emoji()](#replace_emoji) - Replaces an emoji in a string with the given replacement characters.
- [emoji_list()](#emoji_list) - Returns a list of emojis in a given string or text.
- [distinct_emoji_list()](#distinct_emoji_list) - Returns a list of unique emojis in a given string or text.
- [emoji_count()](#emoji_count) - Returns the number of emojis in a given string.
- [is_emoji()](#is_emoji) - Returns true if the given string is an emoji, otherwise false.
- [purely_emoji()](#purely_emoji) - Returns
- [version()](#version) - Returns the version of an emoji.
