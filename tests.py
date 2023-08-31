import core as emojix

# core.category_exists()
def test_category_exists():
    print(emojix.category_exists(category="people_and_emotions")) # >>> False
    print(emojix.category_exists(category="smileys_and_emotion")) # >>> True
    print(emojix.category_exists(category_id=491123)) # >>> False
    print(emojix.category_exists(category_id=491122)) # >>> True
    
def test_category():
    print(emojix.category("🎃"))
    # Output:
    # >>> {'emoji': '🎃', 'category': 'activities', 'category_id': 335508, 'subcategory': 'event', 'subcategory_id': 325613}

def test_get_all_categories():
    categories = emojix.get_all_categories()
    for item in categories:
        print(categories[item])
    # Output:
    # >>> {'id': 491122, 'face_smiling': 4745, 'face_affection': 9488, 'face_tongue': 14227, 'face_hand': 18967, 'face_neutral_skeptical': 23715, 'face_sleepy': 28453, 'face_unwell': 33198, 'face_hat': 37934, 'face_glasses': 42670, 'face_concerned': 47430, 'face_negative': 52172, 'face_costume': 56913, 'cat_face': 61655, 'monkey_face': 66391, 'heart': 71153, 'emotion': 75906}, ..., ...
    
    for item in categories:
        print(item)
    
    # Output:
    # >>> smileys_and_emotion
    # people_and_body
    # component
    # animals_and_nature
    # food_and_drink
    # travel_and_places
    # activities
    # objects
    # symbols
    # flags 

def test_top_level_categories():
    for item in emojix.top_level_categories():
        print(item)
    # output:
    # >>> {'category': 'smileys_and_emotion', 'id': 491122}
    # {'category': 'people_and_body', 'id': 899911}
    # {'category': 'component', 'id': 113687}
    # {'category': 'animals_and_nature', 'id': 116815}
    # {'category': 'food_and_drink', 'id': 228130}
    # {'category': 'travel_and_places', 'id': 227294}
    # {'category': 'activities', 'id': 335508}
    # {'category': 'objects', 'id': 336837}
    # {'category': 'symbols', 'id': 449583}
    # {'category': 'flags', 'id': 552605}
  
def test_sub_level_categories():
    for item in emojix.sub_level_categories():
        print(item)
    # output:
    # >>> {'subcategory': 'face_smiling', 'id': 4745}
    # {'subcategory': 'face_affection', 'id': 9488}
    # {'subcategory': 'face_tongue', 'id': 14227}
    # {'subcategory': 'face_hand', 'id': 18967}
    # {'subcategory': 'face_neutral_skeptical', 'id': 23715}
    # {'subcategory': 'face_sleepy', 'id': 28453}

def test_is_top_level_category():
    print(emojix.is_top_level_category("people_and_body")) # >>> True
    print(emojix.is_top_level_category("person_role"))     # >>> False
    
def test_parent_category():
    print(emojix.parent_category(category="person_role")) 
    # output:
    # >>> {'category': 'people_and_body', 'id': 899911}

def test_child_categories():
    print(emojix.child_categories(category="people_and_body"))
    # output:
    # >>> [{'subcategory': 'hand_fingers_open', 'id': 85439}, {'subcategory': 'hand_fingers_partial', 'id': 90227}, 
    # {'subcategory': 'hand_single_finger', 'id': 95003}, {'subcategory': 'hand_fingers_closed', 'id': 99772}, 
    # {'subcategory': 'hands', 'id': 104567}, {'subcategory': 'hand_prop', 'id': 109319}, {'subcategory': 'body_parts', 'id': 114101}, 
    # {'subcategory': 'person', 'id': 119026}, {'subcategory': 'person_gesture', 'id': 124059}, {'subcategory': 'person_role', 'id': 129427}, 
    # {'subcategory': 'person_fantasy', 'id': 134405}, {'subcategory': 'person_activity', 'id': 139456}, {'subcategory': 'person_sport', 'id': 144584}, 
    # {'subcategory': 'person_resting', 'id': 149359}, {'subcategory': 'family', 'id': 154626}, {'subcategory': 'person_symbol', 'id': 159365}]
    
    print(emojix.child_categories(category="people_and_body", emojis_in_category=True))
    # output:
    # >>> [{'subcategory': 'hand_fingers_open', 'id': 85439, 'emojis': [{'index': 218, 'category': 'people_and_body', 'category_id': 899911, 'subcategory': 'hand_fingers_open', 'subcategory_id': 85439, 'status': 2, 'emoji': '👋', ..., ...}]

def test_iterate_category():
    emojix.iterate_category(lambda x, *args, **kwargs: print(x, "\n\n"), category="person_symbol")
    # output: 
    # >>> {'index': 3243, 'category': 'people_and_body', 'category_id': 899911, 'subcategory': 'person_symbol', 
    # 'subcategory_id': 159365, 'status': 2, 'emoji': '👥', 'E': 1.0, 'unicode': ['U+1F465'], 'codepoints': ['1F465'], 
    # 'sequences': ['\\U0001F465'], 'variant': False, 'alias': [':speaking_head_in_silhouette:'], 'name': 
    # ':busts_in_silhouette:', 'en': ':busts_in_silhouette:', 'es': ':dos_siluetas_de_bustos:', 'ja': ':2人のシルエット
    # :', 'ko': ':사람들_그림자:', 'pt': ':silhueta_de_bustos:', 'it': ':profilo_di_due_persone:', 'fr': 
    # ':silhouettes_de_bustes:', 'de': ':silhouette_mehrerer_büsten:', 'fa': ':تندیس_های_سایه_نما:', 'id': 
    # ':beberapa_siluet_foto_setengah_badan:', 'zh': ':双人像:'}
    
    emojix.iterate_category(print, category="person_symbol")    
    # output: 
    # >>> {'index': 3243, 'category': 'people_and_body', 'category_id': 899911, 'subcategory': 'person_symbol', 
    # 'subcategory_id': 159365, 'status': 2, 'emoji': '👥', 'E': 1.0, 'unicode': ['U+1F465'], 'codepoints': ['1F465'], 
    # 'sequences': ['\\U0001F465'], 'variant': False, 'alias': [':speaking_head_in_silhouette:'], 'name': 
    # ':busts_in_silhouette:', 'en': ':busts_in_silhouette:', 'es': ':dos_siluetas_de_bustos:', 'ja': ':2人のシルエット
    # :', 'ko': ':사람들_그림자:', 'pt': ':silhueta_de_bustos:', 'it': ':profilo_di_due_persone:', 'fr': 
    # ':silhouettes_de_bustes:', 'de': ':silhouette_mehrerer_büsten:', 'fa': ':تندیس_های_سایه_نما:', 'id': 
    # ':beberapa_siluet_foto_setengah_badan:', 'zh': ':双人像:'}
    
def test_emoji_factory():
    for item in emojix.emoji_factory(category="person_symbol"):
        print(item["emoji"])
    # output:
    # >>>  
    # 🗣️
    # 🗣
    # 👤
    # 👥
    # 🫂
    # 👣

def test_get_emojis_in_category():
    for item in emojix.get_emojis_in_category(category="person_symbol"):  
        print(item["emoji"], item["E"])
    # output:
    # >>>
    # 🗣️ 0.7
    # 🗣 0.7
    # 👤 0.6
    # 👥 1.0
    # 🫂 13.0
    # 👣 0.6

def test_is_emoji_variation():
    print(emojix.is_emoji_variation("💭")) # >>> False
    print(emojix.is_emoji_variation("🕷"))  # >>> True
    
def test_get_all_emoji_variants():
    variants = emojix.get_all_emoji_variants()
    for i, item in enumerate(variants):
        print(variants[i]["emoji"])
    # output:
    # >>>
    # ☺️
    # ☺
    # 😐
    # ☹️
    # ☹
    # ☠️
    # ☠
    # 👽
    # ❣️
    # ❣
    # ❤️
    # ❤
    # ...

def test_emoji_to_unicode():
    print(emojix.emoji_to_unicode("🌊")) # >>> ['U+1F30A']

def test_emoji_name():
    print(emojix.emoji_name("🌊")) # >>> :water_wave:

def test_get_emoji_by_name():
    if emojix.get_emoji_by_name("water_wave") == "🌊":
        return True 
  
  
test_get_emoji_by_name()
    
    