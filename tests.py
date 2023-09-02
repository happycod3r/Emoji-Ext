import core as emojix

def test_category_exists():
    print("test_category_exists()")
    if not emojix.category_exists(category="people_and_emotions"): 
        return True
    else:
        return False
    
def test_category():
    print("test_category()")
    if emojix.category("🎃")["category"] == "activities":
        return True
    return False

def test_get_all_categories():
    print("test_get_all_categories()")
    if isinstance(emojix.get_all_categories(), dict):
        return True
    return False
        
def test_top_level_categories():
    print("test_top_level_categories()")
    if isinstance(emojix.top_level_categories(), list):
        return True
    return False

def test_sub_level_categories():
    print("test_sub_level_categories()")
    if isinstance(emojix.sub_level_categories(), list):
        return True
    return False

def test_is_top_level_category():
    print("test_is_top_level_category()")
    if emojix.is_top_level_category("people_and_body") == True and emojix.is_top_level_category("person_role") == False:
        return True
    return False
        
def test_parent_category():
    print("test_parent_category()")
    if isinstance(emojix.parent_category(category="person_role"), dict):
        return True
    return False

def test_child_categories():
    print("test_child_categories()")
    if isinstance(emojix.child_categories(category="people_and_body"), dict):
        return True
    return False

def test_iterate_category():
    print("test_iterate_category()")
    try:
        emojix.iterate_category(lambda x, *args, **kwargs: True, category="person_symbol")
        return True
    except Exception as e:
        return False
        
def test_emoji_factory():
    print("test_emoji_factory()")
    try:
        for (i, item) in enumerate(emojix.emoji_factory(category="person_symbol")):
            if isinstance(item, dict) is not True:
                return False
        return True
    except Exception as e:
        return False

def test_get_emojis_in_category():
    print("test_get_emojis_in_category()")
    try:
        for (i, item) in enumerate(emojix.get_emojis_in_category(category="person_symbol")):  
            if isinstance(item, dict) is not True:
                return False
        return True
    except Exception as e:
        return False

def test_is_emoji_variation():
    print("test_is_emoji_variation()")
    if emojix.is_emoji_variation("💭") == False and emojix.is_emoji_variation("🕷") == True:
        return True
    return False
    
def test_get_all_emoji_variants():
    print("test_get_all_emoji_variants()")
    variants = emojix.get_all_emoji_variants()
    if isinstance(variants, list):
        return True
    return False
    
def test_emoji_to_unicode():
    print("test_emoji_to_unicode()")
    if emojix.emoji_to_unicode("🌊") == ['U+1F30A']:
        return True
    return False

def test_emoji_name():
    print("test_emoji_name()")
    if emojix.emoji_name("🌊") == ":water_wave:":
        return True
    return False

def test_get_emoji_by_name():
    print("test_get_emoji_by_name()")
    if emojix.get_emoji_by_name("water_wave") == "🌊":
        return True
    return False
  
def begin_tests():
    if test_category_exists():
        print("Passed")
    else:
        print("Failed")
    if test_category():
        print("Passed")
    else:
        print("Failed")
    if test_get_all_categories():
        print("Passed")
    else:
        print("Failed")
    if test_top_level_categories():
        print("Passed")
    else:
        print("Failed")
    if test_sub_level_categories():
        print("Passed")
    else:
        print("Failed")
    if test_is_top_level_category():
        print("Passed")
    else:
        print("Failed")
    if test_parent_category():
        print("Passed")
    else:
        print("Failed")
    if test_child_categories():
        print("Passed")
    else:
        print("Failed")
    if test_iterate_category():
        print("Passed")
    else:
        print("Failed")
    if test_emoji_factory():
        print("Passed")
    else:
        print("Failed")
    if test_get_emojis_in_category():
        print("Passed")
    else:
        print("Failed")
    if test_is_emoji_variation():
        print("Passed")
    else:
        print("Failed")
    if test_get_all_emoji_variants():
        print("Passed")
    else:
        print("Failed")
    if test_emoji_to_unicode():
        print("Passed")
    else:
        print("Failed")
    if test_emoji_name():
        print("Passed")
    else:
        print("Failed")
    if test_get_emoji_by_name():
        print("Passed")
    else:
        print("Failed")
if __name__ == "__main__":
    begin_tests()
    