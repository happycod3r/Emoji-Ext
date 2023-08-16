import tkinter as tk
import customtkinter as ctk
import emoji
from PIL import Image
import io


# Contains duplicate emojis for testing purposes.
test_emoji_str = "🙂😊😀😁😃😄😎😆😂☹️🙁😞😟😣😖😢😭🥲🥹😂😠😡😨😧😦😱😫😩😮😯😲😺😸🐱😼😗😙😚😘😍😉😜😘😛😝😜🤑🤔😕😟😐😑😳😞😖🤐😶😇👼😈😎😪😏😒😵😵‍💫😕🤕🤒😷🤢🤨😬☠️💀🏴‍☠️🐔🐓🌹🎅💔❤️🐟🐠🍻🫡😔🥺😭😢😵☠️😳😣🦀🦞🦈🩹🤕❤️‍🩹🐟🐠💵💸😏😐😑🤨🦇😘🙂🌸😭🐱🐻🧸🐻‍❄️🐼😣😖👶😅😳😓😥😳🚬😴💤😉😜😕😶😵🙄😀😅😆😃😄🙌🙇🖕🤔😭😢😒😩😑😞😔😫😩😪😺😸😹😻😼😽🙀😿😾🐱🙍😔🤭😕😵🤦😃😄😁😀😍👋👽👾😀🙌💃😂✌️😔😒😏😙😚🧐🎧😟😓😬🤓😎✍️📝😀😁😆😅😃😄😁😲😮😯💃🕺😨😱😮😲😬😠🤷🫂😙😴😌😩😫🫧🍵☕️🌠☄️💫🌟🐠🐟🐡🦈🐬🐳🐋🦑🐙🐍💣🧨😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟🙀🙁🙂🙃🙄🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏😰😱😲😳😴😵😶😷😸😹😺😻😼😽😾😿🤐🤑🤒🤓🤔🤕🤖🤗🤘🤙🤚🤛🤜🤝🤞🤟🤠🤡🤢🤣🤤🤥🤦🤧🤨🤩🤪🤫🤬🤭🤮🤯🤰🤱🤲🤳🤴🤵🤶🤷🤸🤺🤻🤼🤽🤾🤿"

# Contains no duplicate emojis
clean_emoji_resource = [
    '🙂', '😊', '😀', '😁', '😃', '😄', '😎', '😆', '😂', '🙁', '😞', 
    '😟', '😣', '😖', '😢', '😭', '🥲', '🥹', '😠', '😡', '😨', '😧', 
    '😦', '😱', '😫', '😩', '😮', '😯', '😲', '😺', '😸', '🐱', '😼', 
    '😗', '😙', '😚', '😘', '😍', '😉', '😜', '😛', '😝', '🤑', '🤔', 
    '😕', '😐', '😑', '😳', '🤐', '😶', '😇', '👼', '😈', '😪', '😏', 
    '😒', '😵', '💫', '🤕', '🤒', '😷', '🤢', '🤨', '😬', '💀', '🏴', 
    '🐔', '🐓', '🌹', '🎅', '💔', '❤', '🐟', '🐠', '🍻', '🫡', '😔', 
    '🥺', '🦀', '🦞', '🦈', '🩹', '💵', '💸', '🦇', '🌸', '🐻', '🧸', 
    '❄', '🐼', '👶', '😅', '😓', '😥', '🚬', '😴', '💤', '🙄', '🙌', 
    '🙇', '🖕', '😹', '😻', '😽', '🙀', '😿', '😾', '🙍', '🤭', '🤦', 
    '👋', '👽', '👾', '💃', '✌', '🧐', '🎧', '🤓', '✍', '📝', '🕺', 
    '🤷', '🫂', '😌', '🫧', '🍵', '☕', '🌠', '☄', '🌟', '🐡', '🐬', 
    '🐳', '🐋', '🦑', '🐙', '🐍', '💣', '🧨', '😋', ' 😐', '🙃', '🙅', 
    '🙆', '🙈', '🙉', '🙊', '🙋', '🙎', '🙏', '😰', '🤖', '🤗', '🤘', 
    '🤙', '🤚', '🤛', '🤜', '🤝', '🤞', '🤟', '🤠', '🤡', '🤣', '🤤', 
    '🤥', '🤧', '🤩', '🤪', '🤫', '🤬', '🤮', '🤯', '🤰', '🤱', '🤲', 
    '🤳', '🤴', '🤵', '🤶', '🤸', '🤺', '🤻', '🤼', '🤽', '🤾', '🤿', # new

    ]


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EmojiPy(ctk.CTk):
    def __init__(self):
        
        self.width = 500
        self.height = 570
        
        self.EMOJIS = []
        self.EMOJI_NAMES = []
        self.EMOJI_UNICODE_VALUES = []

        super().__init__()
        
        self.geometry(f"{self.width}x{self.height}")
        self.title = "EmojiPy"
        self.grid_columnconfigure(0, weight=1)
        
        self.colors = {
            "bg": "#1B0D2C",
            "bg2": "#111111",
            "txt-1": "#FCCB55",
            "txt-2": "#CC0F04"
        }
        
        self.bg_image = ctk.CTkImage(Image.open("./res/bg1.png"), size=(self.width, self.height))
        
        self.bg_image_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        
        self.title_image = ctk.CTkImage(Image.open("./res/EmojiPy_thin.png"), size=(self.width, 60))
        self.app_title = ctk.CTkLabel(self, width=self.width, height=60, image=self.title_image, text="", font=ctk.CTkFont("Segoi UI", 25, weight='bold'), bg_color="transparent", fg_color=self.colors["bg"], text_color=self.colors["txt-1"], corner_radius=0)
        self.app_title.grid(row=0, column=0, padx=(0, 0), pady=(0, 20), ipady=10, sticky="new")
        self.app_title.grid_rowconfigure(0, weight=1)

        self.emoji_frame = ctk.CTkScrollableFrame(self, width=self.width, fg_color=self.colors["bg2"], corner_radius=10)
        self.emoji_frame.grid(row=0, column=0, padx=40, pady=(90, 10), sticky="nsew")
        self.emoji_frame.grid_rowconfigure(1, weight=1)
        
        print(self.convert_emoji_to_unicode("🍇"))
        self.set_emojis()
        self.set_emoji_names()
        self.set_emoji_unicode_values()
        self.populate_gui()
        
    def convert_emoji_to_unicode(self, emojis: str | list[str]) -> (str | list[str]):
        emoji_string = emojis
        unicode_values = []
        for i in range(0, len(emoji_string)):
            unicode_values.append(ord(emoji_string[i].encode('utf-16', 'surrogatepass').decode('utf-16')))
        unicode_strings = []
        for codepoint in unicode_values:
            unicode_strings.append(f"U+{codepoint:04X}")        
        return unicode_strings
    
    def set_emoji_unicode_values(self) -> list[str]:
        self. EMOJI_UNICODE_VALUES = self.convert_emoji_to_unicode(self.EMOJIS)
             
    def get_emojis_from_db(self) -> str:
        """
        Retrieves the short hand emojis from the DEMOJIZED database, emojizes them and 
        returns the emoji string returned by emoji.emojize().
        """
        try:
            with open("DEMOJIZED.db", "r") as db:
                content = db.read()
                db.close()
                emojis = emoji.emojize(content)
                return emojis
        except FileNotFoundError as e:
            print(repr(e))
        except IOError as e:
            print(repr(e))

    def set_emojis(self) -> None:
        """
        Gets the emojis retrieved from the db, checks their validity and 
        appends each one to the EMOJI list.
        """
        emojis = self.get_emojis_from_db()
        for item in emojis:
            if emoji.is_emoji(item):
                self.EMOJIS.append(item)
    
    def get_emoji_names(self) -> list[str]:
        """
        Instead of manually writing out all the names I figured since
        the emoji.demojize() function stores the emojis using the emoji
        name as a shorthand I could just retrieve the stored shorthand 
        version of the emojis from the database to borrow the names from 
        and strip off the leading and trailing colons to leave the name 
        only.
        """
        try:
            with open("DEMOJIZED.db", "r") as db:
                content = db.read()
                db.close()
                names = content.split(":")
                actual_names = []
                for name in names:
                    if name != '':
                        actual_names.append(name)
                return actual_names    
        except FileNotFoundError as e:
            print(repr(e))
        except IOError as e:
            print(repr(e))     

    def set_emoji_names(self):
        self.EMOJI_NAMES = self.get_emoji_names()

    def add_emojis_to_db(self, emojis: list[str]):
        """
        Demojizes the list of emojis and appends them to the 
        database.
        """
        try:
            with open("DEMOJIZED.db", "a") as db:
                for item in emojis:
                    if emoji.is_emoji(item):
                        db.write(emoji.demojize(item))
                db.close()
        except FileNotFoundError as e:
            print(repr(e))
        except IOError as e:
            print(repr(e))
    
    def filter_emojis_from_text(self, text: str) -> list[str]:
        """
        Scans the text for emojis and if found they are appended to 
        the filtered list[] which is then returned.
        """
        filtered = []
        for item in emoji.distinct_emoji_list(text):
            if emoji.is_emoji(item):
                # Filter out unwanted unicode characters
                if item != "\u200d" and item != "️" and item != "☹" and item != "☠":
                    filtered.append(item)
        return filtered
     
    def populate_gui(self) -> None:
        """
        Loads and populates the GUI with the emojis after they have 
        been retrieved from the database. Each emoji is displayed
        on a label in a scrollable list
        """
        del self.EMOJIS[-5:] # temporary
        for i in range(len(self.EMOJIS)):
            if len(self.EMOJIS[i]) != 0:
                emoji_list_item = ctk.CTkButton(self.emoji_frame, fg_color="#1B0D2C", text_color=self.colors["txt-1"], width=40)
                emoji_list_item.configure(   
                    text=f"{self.EMOJIS[i]}", 
                    anchor="center",
                    font=ctk.CTkFont(size=40), 
                    corner_radius=0
                )
                emoji_list_item.grid(
                    row=i, 
                    column=0, 
                    padx=(5, 5), 
                    pady=(0, 2),
                    ipadx=2,
                    ipady=2, 
                    sticky="ew"
                )
                emoji_list_item.grid_rowconfigure(i, weight=0) 
                
                emoji_item_unicode = ctk.CTkLabel(self.emoji_frame, text_color=self.colors["txt-2"])
                emoji_item_unicode.configure(
                    text=f"{self.EMOJI_UNICODE_VALUES[i]}",    
                    font=ctk.CTkFont("Segoi UI", size=16, weight="bold"), 
                    width=40,
                    corner_radius=0,
                    anchor="w",
                    state="normal"
                )
                emoji_item_unicode.grid(
                    row=i, 
                    column=1, 
                    padx=(0, 0), 
                    pady=(0, 2),
                    ipady=2, 
                    sticky="nsew"
                )
                emoji_item_unicode.grid_rowconfigure(i, weight=0)

                emoji_item_name = ctk.CTkLabel(self.emoji_frame)
                emoji_item_name.configure(
                    text=f"{self.EMOJI_NAMES[i]}",    
                    font=ctk.CTkFont("Segoi UI", size=16, weight="bold"), 
                    width=self.width,
                    corner_radius=0,
                    anchor="w",
                    state="normal"
                )
                emoji_item_name.grid(
                    row=i, 
                    column=2, 
                    padx=(0, 0), 
                    pady=(0, 2),
                    ipadx=2,
                    ipady=2, 
                    sticky="nsew"
                )
                emoji_item_name.grid_rowconfigure(i, weight=0) 
    
if __name__ == "__main__":   
    emojipy = EmojiPy()
    emojipy.mainloop()    
