# Emojix (Emoji Extended)

## [About](#about)
***Emoji-x*** or ***Emojix*** is built on top of the existing ***[Emoji](https://pypi.org/project/emoji/)*** module for Python. It aims to extend it with new functions and a more robust EMOJI_DATA dictionary.

## [Module Contents](#module-contents)
The following functions and variables are available through the emojix module.

| **Legacy Emoji Functions & Variables**                                                                           |                                                              |
|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [`emojize()`](https://carpedm20.github.io/emoji/docs/#emoji.emojize)                          | Replace emoji shortcodes with the corresponding emojis                    |
| [`demojize()`](https://carpedm20.github.io/emoji/docs/#emoji.demojize)                        | Replace emojis with the corresponding emoji shortcodes                  |
| [`replace_emoji()`](https://carpedm20.github.io/emoji/docs/#emoji.replace_emoji)              | Like str.replace() but only replaces emojis
| [`emoji_list()`](https://carpedm20.github.io/emoji/docs/#emoji.emoji_list)                    | Returns a list of all emojis in a string
| [`distinct_emoji_list()`](https://carpedm20.github.io/emoji/docs/#emoji.distinct_emoji_list)  | Returns a list of unique emojis in a string
| [`emoji_count()`](https://carpedm20.github.io/emoji/docs/#emoji.emoji_count)                  | Returns the number of emojis in a string
| [`is_emoji()`](https://carpedm20.github.io/emoji/docs/#emoji.is_emoji)                        | Returns true if the given char is an emoji and false otherwise
| [`version()`](https://carpedm20.github.io/emoji/docs/#emoji.version)                          | Returns the version of the given emoji

| **Emoji-extended Functions & Variables**                                                                           |                                                              |
|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [`category_exists()`](https://happycod3r.github.io/emojix/docs/#emojix.category_exists)         | Returns true if the given category exists and False otherwise
| [`category()`](https://happycod3r.github.io/emojix/docs/#emojix.category)                      | Returns the category of the given emoji
| [`get_all_categories()`](https://happycod3r.github.io/emojix/docs/#emojix.get_all_categories)  | Returns a dict of all emoji categories and IDs
| [`top_level_categories()`](https://happycod3r.github.io/emojix/docs/#emojix.top_level_categories) | Returns a list of dicts containg all top level categories
| [`sub_level_categories()`](https://happycod3r.github.io/emojix/docs/#emojix.sub_level_categories) | Returns a list of dicts containg all sub level categories
| [`is_top_level_category()`](https://happycod3r.github.io/emojix/docs/#emojix.is_top_level_category) | Returns True if the category is top-level and false otherwise
| [`parent_category()`](https://happycod3r.github.io/emojix/docs/#emojix.parent_category)          | Returns the parent category of the given emoji
| [`child_categories()`](https://happycod3r.github.io/emojix/docs/#emojix.child_categories)        | Returns a list of dicts containg child categries of the given category 
| [`iterate_category()`](https://happycod3r.github.io/emojix/docs/#emojix.iterate_category)        | Iterates over the emojis in a given category
| [`emoji_factory()`](https://happycod3r.github.io/emojix/docs/#emojix.emoji_factory)              | A generator function which iterates over all emojis in EMOJI_DATA and yields each one
| [`get_emojis_in_category()`](https://happycod3r.github.io/emojix/docs/#emojix.get_emojis_in_category)  | Returns a list of dicts of all emojis in a given category
| [`is_emoji_variation()`](https://happycod3r.github.io/emojix/docs/#emojix.is_emoji_variation)        | Returns True if the given emoji is a variation (contains a zwj)
| [`get_all_emoji_variants()`](https://happycod3r.github.io/emojix/docs/#emojix.get_all_emoji_variants) | Returns a list of dicts containg all emoji variants 
| [`emoji_to_unicode()`](https://happycod3r.github.io/emojix/docs/#emojix.emoji_to_unicode)    | Returns the Unicode notation of a given emoji
| [`emoji_name()`](https://happycod3r.github.io/emojix/docs/#emojix.emoji_name)      | Returns the name or shortcode of a given emoji
| [`get_emoji_by_name()`](https://happycod3r.github.io/emojix/docs/#emojix.get_emoji_by_name)        | Returns an the emoji that corresponds to the given name
| [`has_zwj()`](https://happycod3r.github.io/emojix/docs/#emojix.has_zwj)        | Returns True if the given emoji contains a zero-width-joiner character
| [`EMOJI_DATA`](https://happycod3r.github.io/emojix/docs/#emojix.EMOJI_DATA)                      | Dict of just under 5,000 emojis and their corresponding data
| [`STATUS`](https://carpedm20.github.io/emoji/docs/#emoji.STATUS)                               | Dict containing the Unicode status values for emojis
| [`CATEGORIES`](https://happycod3r.github.io/emojix/docs/#emojix.CATEGORIES)                     | Dict containing all emoji categories and an assigned category ID
| [`BASIC_EMOJIS`](https://happycod3r.github.io/emojix/docs/#emojix.BASIC_EMOJIS)                 | Dict containing all basic emojis organized by category
| [`KEYCHAIN`](https://happycod3r.github.io/emojix/docs/#emojix.KEYCHAIN)                        | Holds EMOJI_DATA.keys()
| [`CATS_KEYCHAIN`](https://happycod3r.github.io/emojix/docs/#emojix.CATS_KEYCHAIN)        | Holds CATEGORIES.keys()
| [`compile_emoji_data()`](https://happycod3r.github.io/emojix/docs/#emojix.compile_emoji_data)        | Recompiles data_dict.py which holds EMOJI_DATA
| [`key_chain()`](https://happycod3r.github.io/emojix/docs/#emojix.key_chain)        | Returns EMOJI_DATA.keys(). Use [core.KEYCHAIN](#emojix.KEYCHAIN) instead
| [`categories_key_chain()`](https://happycod3r.github.io/emojix/docs/#emojix.categories_key_chain)        | Returns CATEGORIES.keys(). Use [core.CATS_KEYCHAIN](#emojix.CATS_KEYCHAIN) instead
| [`emoji_data()`](https://happycod3r.github.io/emojix/docs/#emojix.emoji_data)                 | Returns the EMOJI_DATA dictionary
| [`get_emoji_data_for_lang()`](https://happycod3r.github.io/emojix/docs/#emojix.get_emoji_data_for_lang) | Returns and caches emoji data for a specific language
| [`get_emoji_aliases_data()`](https://happycod3r.github.io/emojix/docs/#emojix.get_emoji_aliases_data) | Returns and caches emoji alias data

---

## [Documentation](#documentation) 

Use the following guide to build the documentation with [Sphinx](https://www.sphinx-doc.org/).

```bash
git clone https://github.com/happycod3r/emojix.git
cd emoji/docs
python -m pip install -r requirements.txt
make html
```

Check for warnings:

```bash
make clean
sphinx-build -n -T -b html . _build
```

Test code in code blocks:

```bash
make doctest
```

Test coverage of documentation:

```bash
make coverage
```
