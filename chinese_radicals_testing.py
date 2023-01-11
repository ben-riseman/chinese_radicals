import sys, math, pandas
from ben_lib import *



#cn_font = pygame.font.SysFont("lisu", 20)

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 20)
pandas.set_option('display.width', 1000)

""" GLOBALS """

d = {
    "a1" : "ā",
    "a2" : "á",
    "a3" : "ǎ",
    "a4" : "à",
    "a5"  : "a",
    
    "e1" : "ē",
    "e2" : "é",
    "e3" : "ě",
    "e4" : "è",
    "e5"  : "e",
    
    "i1" : "ī",
    "i2" : "í",
    "i3" : "ǐ",
    "i4" : "ì",
    "i5"  : "i",
    
    "o1" : "ō",
    "o2" : "ó",
    "o3" : "ǒ",
    "o4" : "ò",
    "o5"  : "o",
    
    "u1" : "ū",
    "u2" : "ú",
    "u3" : "ǔ",
    "u4" : "ù",
    "u5"  : "u"
    }




class Character():
    def __init__(self, char, pinyin, english, components = [], compounds = [], words = [], memory = "", stroke_count = 0):
        self.char = char
        self.pinyin = pinyin
        self.english = english
        self.stroke_count = stroke_count

        self.components = components
        self.compounds = compounds
        self.words = words

        self.memory = memory

        self.pl = lambda: print(self.char, "~", self.pinyin, ":", self.english)

    def add_component(self, component):
        self.components.append(component)

    def add_compound(self, compound):
        self.compounds.append(compound)

    def add_word(self, word):
        self.words.append(word)

    def print(self):
        self.pl()
        if len(self.components):
            print("components:")
            #print(self.components)
            [m[ct].pl() for ct in self.components]
        if len(self.compounds):
            print("compounds:")
            [m[cd].pl() for cd in self.compounds]
        if len(self.words):
            print("words:")
            [m[w].pl() for w in self.words]
        if type(self.memory) == str and self.memory != "":
            print("memory sentence:")
            print(self.memory)
        print("----------------------------------------------")
        

def add_component(sub, obj):
    m[sub].add_component(obj)
    m[obj].add_compound(sub)

def add_compound(sub, obj):
    m[sub].add_compound(obj)
    m[obj].add_component(sub)

def get_c_from_e(eng):
    for char in list(m.values()):
        e = char.english.split(" ")
        if eng in e:
            char.print()

def get_c_from_p(pin):
    #print(pin)
    for char in list(m.values()):
        p = char.pinyin
        #print(p)
        if type(p) == str and pin in p:
            char.print()

            

def process_tone(pin):
    """
        Methodology:

        1.) Get pinyin, sort in alphabetical order
        2.) Sort through and look for numbers
        3.) If no numbers in entire word, get first alphabetical 


    """

    
    vowels = ["a","e","i","o","u"]
    nums = ["1", "2", "3", "4", "5"]
    #print("pin", pin)
    
    if any([z in pin for z in nums]):
        
        for letter in pin:
            
            if letter in vowels:
                try:
                    num = pin[pin.find(letter)+1]
                    #print("this letter & following char:", letter+str(num))
                    if num in nums:
                        new_vowel = d[letter+str(num)]
                        new_pin = pin.replace(letter+str(num), new_vowel)
                        #print("fixed & old:", new_pin, pin)
                    else:
                        new_vowel = letter
                        num = ""
                        new_pin = pin
                        continue
                    break
                except Exception as e:
                    #print(e)
                    new_vowel = letter
                    num = ""
                    new_pin = pin
                    break

        get_c_from_p(new_pin)
        

        return new_pin

    else:
        v = [a in pin for a in vowels]
        #print("v:", v)
        if any(v):
            g = list(zip(v, vowels))
            p = []
            for t in g:
                if t[0]:
                   p.append(t)
            for letter in p:
                for x in range(1, 6):
                    process_tone(pin.replace(letter[1], letter[1]+str(x)))

def build_csv():
    data = [[1, "一", "yī", "one", "", "", ""]]
    columns = ["Number", "Character", "Pinyin", "English",
               "Components", "Compounds", "Words", "Stroke Count"]
    indexes = [1]
    df = pandas.DataFrame(data = data, index = indexes, columns = columns)
    df.to_csv("master.csv", index = False, encoding='utf_8_sig')

def read_csv():
    df = pandas.read_csv("master.csv", encoding='utf-8')
    m = {}
    df["Memory"] = df["Memory"].astype("string")
    for index, row in df.iterrows():
        char = row["Character"]
        pinyin = row["Pinyin"]
        english = row["English"]
        if type(row["Components"]) != float:
            components = [int(x) for x in str_to_list(row["Components"])]
        else:
            components = []
        if type(row["Compounds"]) != float:
            compounds = [int(x) for x in str_to_list(row["Compounds"])]
        else:
            compounds = []
        if type(row["Words"]) != float:
            words = [int(x) for x in str_to_list(row["Words"])]
        else:
            words = []
        if type(row["Memory"]) != float:
            memory = row["Memory"]
        else:
            memory = ""
        stroke_count = row["Stroke Count"]
        #print(str(char),pinyin,english)
        m.update({int(row["Number"]): Character(char, pinyin, english, components, compounds, words, memory, stroke_count)})
    return df, m

def save_to_csv(df):
    df.to_csv("master.csv", index = False, encoding='utf_8_sig')
    

def add_row(df, char, pin, eng, components = [], stroke_count = 0):
    #if len(components) == 1:
    #    new_comp = int(components[0])
    #else:
    new_comp = list_to_str(components)
    d = {"Number": len(df)+1,
         "Character": char,
         "Pinyin": pin,
         "English": eng,
         "Components": new_comp,
         "Compounds": "",
         "Words": "",
         "Stroke Count": int(stroke_count)}

    #print(components)

    df2 = df.sort_values(by = ["Stroke Count", "Number"])
    df2["Components"] = df2["Components"].astype("string")

    df2 = df2.append(d, ignore_index = True)
    return df2

# l = [1,2,3]
# s = str(l[1:-1])
# l2 = list(s.replace(" ","").replace(",",""))

def list_to_str(l):
    return str(l)[1:-1]
def str_to_list(s):
    return list(s.replace(" ","").split(","))

def edit(df, col, index, l):
    s = list_to_str(l)
    df2 = df
    print(s)
    #df2["Number"] = df2["Number"].astype("int")
    df2[col] = df2[col].astype("string")
    df2.at[index, col] = str(s)
    return df2

def fwik(s, comp):
    l = s.split()
    print(l)
    char = l[0]
    stroke_count = int(l[1])
    eng = l[2]
    pin = l[3]

    df2 = add_row(df, char, pin, eng, comp, stroke_count)
    return df2
    

edit_components = lambda df, index, l : edit(df, "Components", index, l)
edit_compounds = lambda df, index, l : edit(df, "Compounds", index, l)
edit_words = lambda df, index, l : edit(df, "Words", index, l)

    
        

"""m = {1: Character("一", "yī", "one", 1),
     2: Character("丨", "gǔn", "line", 1),
     3: Character("丶", "zhǔ", "dot", 1),
     4: Character("丿", "piě", "slash", 1),
     5: Character("乀", "piě", "slash", 1),
     6: Character("⺄", "piě", "slash", 1),
     7: Character("乙", "yǐ", "second", 1),
     8: Character("乚", "yǐ", "second", 1),
     9: Character("乛", "yǐ", "second", 1),
     10: Character("亅", "jué", "hook", 1),
     
     11: Character("二", "èr", "two", 2),
     12: Character("亠", "tóu", "lid", 2), 
     13: Character("⺊", "bo", "prophesy, fortune telling", 2),
     14: Character("人", "rén", "man", 2),
     15: Character("亻", "rén", "man", 2),
     16: Character("儿", "ér", "son, legs", 2),
     17: Character("入", "rù", "enter", 2),
     18: Character("八", "bā", "eight", 2),
     19: Character("丷", "bā", "eight", 2),
     20: Character("冂", "jiōng", "wide", 2),

     
     21: Character("上", "shàng", "on top, above, to attend", 3)

     }"""

""" Components """

"""add_component(13, 1)
add_component(13, 2)

add_component(11, 1)

add_component(12, 1)
add_component(12, 3)

add_component(16, 4)
add_component(16, 7)

add_component(18, 4)
add_component(18, 5)

add_component(20, 2)
add_component(20, 10)



add_component(21, 1)
add_component(21, 13)"""


df, m = read_csv()

if __name__ == "__main__":
    
    while True:
        search = input("Search here:")
        l = search.split(" ")

        if search == "exit":
            break
        if search == "save":
            save_to_csv(df)
            print("Saved!")
            
        if len(l) > 1:
            if "eng" == l[0]:
                print("----------------------------------------------")
                try:
                    get_c_from_e(l[1])
                except Exception as e:
                    print("Not recognized, try again")
            elif "pin" == l[0]:
                print("----------------------------------------------")
                
                process_tone(l[1])

            elif "show" == l[0]:
                if "all" == l[1]:
                    print(df)
                else:
                    try:
                        s = l[1].split(",")
                        #temp = pandas.DataFrame()
                        #print(s)
                        first = df.iloc[int(s[0])]
                        s.pop(0)
                        for num in s:
                            #first = first.append(df.iloc[int(num)])
                            first = pandas.concat([first, df.iloc[int(num)]], axis = 1)
                            #temp.append(df.iloc[int(l[1])], ignore_index = True, )
                            #print(df.iloc[int(num)])
                        print(first.T)
                    except Exception as e:
                        print("Indexing failed, try again", e)

            elif "del" == l[0]:
                index = int(l[1])
                if index >= len(df):
                    print("Index out of bounds, try again")
                    continue
                sure = input("Are you sure? Confirm with Y/N:")
                if sure == "Y":
                    df = df.drop(index = index, axis = 0)

        if len(l) > 3:
            if "edit" == l[0]:
                # input to change is Index, components are Number (reference)
                if "component" == l[1]:
                    index = int(l[2])
                    """components = []
                    for x in l[3].split(","):
                        char = str(df["Character"][int(x)])
                        components.append(char)
                    """
                    components = [int(x) for x in l[3].split(",")]
                    print(components)
                    df = edit_components(df, index, components)
                    print(df.iloc[int(index)].to_frame().T)
            elif "add" == l[0]:
                #print(len(l))
                char = l[1]
                pin = l[2]
                eng = l[3]
                stroke_count = l[4] if len(l) >= 5 else 0
                components = [int(x) for x in l[5].split(',')] if len(l) == 6 else []
                
                df = add_row(df, char, pin, eng, components, stroke_count)
                print(df.iloc[len(df)-1].to_frame().T)
                    


        #else:
        #    print("Not found, try again")


    
