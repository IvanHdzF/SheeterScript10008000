# %%
import re
import easygui
import os
import subprocess
from tkinter import *
from tkinter import ttk
import optrun


bows=['prototypecrescent','rust', 'sacrificialbow', 'skywardharp', 'thestringless', 'thunderingpulse', 'theviridescenthunt', 'windblumeode', 'alleyhunter', 'amosbow', 'blackcliffwarbow', 'elegy', 'favoniuswarbow', 'hamayumi','mitternachtswaltz', 'mouunsmoon', 'polarstar']
catalysts=['frostbearer', 'hakushinring', 'kagura', 'mappamare', 'memoryofdust', 'oathsworneye', 'eyeofperception', 'lostprayertothesacredwinds', 'prototypeamber','skywardatlas', 'solarpearl', 'ttds', 'thewidsith', 'wineandsong','blackcliffagate', 'dodocotales', 'favoniuscodex']
claymores=["songofbrokenpines","prototypearchaic","rainslasher","redhornstonethresher","luxurioussealord","skywardpride","serpentspine","snowtombedstarsilver","theunforged","whiteblind","wolfsgravestone","akuoumaru","blackcliffslasher","favoniusgreatsword","katsuragikirinagamasa"]
polearms=["calamityqueller","thecatch","crescentpike","deathmatch","dragonsbane","dragonspinespear","favoniuslance","engulfinglightning","staffofhoma","kitaincrossspear","lithicspear","primordialjadewingedspear","prototypestarglitter","skywardspine","vortexvanquisher","wavebreakersfin","blackcliffpole"]
swords=["aquilafavonia","theblacksword","blackclifflongsword","favoniussword","festeringdesire","theflute","freedomsworn","haran","harbingerofdawn","ironsting","lionsroar","lithicblade","mistsplitterreforged","jadecutter","prototyperancour","sacrificialsword","skywardblade","summitshaper","thealleyflash","amenomakageuchi"]#Done
refinements=["1","2","3","4","5"]
sands=["hp%=0.466","atk%=0.466","def%=0.466","er=0.518","em=186.5"]
goblets=["hp%=0.466","atk%=0.466","def%=0.466","em=186.5","anemo%=0.466","cryo%=0.466","electro%=0.466","geo%=0.466","hydro%=0.466","pyro%=0.466","phys%=0.466"]
circlets=["hp%=0.466","atk%=0.466","def%=0.466","em=186.5","cr=0.311","cd=0.622","heal=0.359"]

#-----------------Weapon type characters arrays----------------------#
bowusers=[
  'aloy',       'amber',
  'diona',      'fischl',
  'ganyu',      'gorou',
  'sara', 'tartaglia',
  'venti',      'yoimiya'
]

catalystusers=[
  'barbara',
  'klee',
  'lisa',
  'mona',
  'ningguang',
  'kokomi',
  'sucrose',
  'yae',
  'yanfei'
]

claymoreusers=[
  'itto',
  'beidou',
  'chongyun',
  'diluc',
  'eula',
  'noelle',
]

polearmusers=[
  'hutao',
  'raiden',
  'rosaria',
  'shenhe',
  'thoma',
  'xiangling',
  'xiao',
  'yunjin',
  'zhongli'
]

swordsusers=[
  'albedo',
  'bennett',
  'jean',
  'kazuha',
  'kaeya',
  'ayaka',
  'ayato',
  'keqing',
  'qiqi',
  'xingqiu'
]







# %%
configf=easygui.fileopenbox("Please input a file as a base", "Writer", filetypes= "*.txt", multiple=False)

#print(configf)
gcsimpath=os.path.join(os.path.abspath(''))
configpath=(os.path.dirname(configf))


# %%
character=(os.path.basename(configf)).replace(".txt","")
print(character)

# %%
def classifyweapon(character):
    if character in bowusers:weapons=bows
    elif character in catalystusers:weapons=catalysts
    elif character in claymoreusers:weapons=claymores
    elif character in polearmusers:weapons=polearms
    elif character in swordsusers:weapons=swords
    else:
        weapontype = easygui.enterbox("Please input the type of weapon to do the comparison with:\n1 for bows\n2 for catalysts\n3 for claymores\n4 for polearms\n5 for swords" ,"Enter your weapon type (NUMBER ONLY)")
        if weapontype == "1":
            weapons=bows
        if weapontype ==  "2":
            weapons=catalysts
        if weapontype == "3":
            weapons=claymores
        if weapontype== "4":
            weapons=polearms
        if weapontype== "5":
            weapons=swords
        else:
            print("Invalid weapontype, input ONLY the number please")

    return weapons
weapons=classifyweapon(character)
#print(weapons)

# %%
def writeconfig(weapons,refinements,sands,goblets,circlets):

    my_file = open(configf)
    string_list = my_file.readlines()
    #Get file's content as a list

    my_file.close()
    #print(string_list)
    list_contents = "".join(string_list)
    #x=re.search("(?<="+character+" add weapon)", list_contents) #Nayde learning regex dont mind this
    #print(x)
    fileswritten=0
    found=re.findall("("+character+" add weapon)(.*)", list_contents) #try to find if character matches
    if not found:
        print("WARNING: NO FILES WERE WRITTEN, INVALID FILE NAME AS BASE")
        return fileswritten

    #we start the iterations here
    
    for weapon in weapons:
        for refinement in refinements:
            for sand in sands:
                for goblet in goblets:
                    for circlet in circlets:

                        subweapon=re.sub("(?<="+character+" add weapon=\")(.*)(?=\")",weapon, list_contents) #substitute the readed config with the new weapon
                        subrefine=re.sub("(?<="+character+" add weapon=\""+weapon+"\" refine=)(.*)(?= lvl)",refinement, subweapon)#substitute refinements
                        finallist=re.sub("("+character+" add stats hp=4780)(.*)",""+character+" add stats hp=4780 atk=311 "+sand+" "+goblet+" "+circlet+";", subrefine) #substitute the readed config with the new weapon

                        my_file = open(configpath+"//_"+weapon+" R"+refinement+" "+sand.split('=',1)[0]+"-"+goblet.split('=',1)[0]+"-"+circlet.split('=',1)[0]+".txt", "w")

                        my_file.write(finallist)
                        my_file.close()
                        fileswritten+=1
    return fileswritten



# %%
main = Tk()
main.title("Config Writer")
main.geometry("600x300+50+150")

#---------------------------------For weapon---------------------------------#
frame = ttk.Frame(main, padding=(3, 3, 12, 12))
frame.grid(column=0, row=0, sticky=(N, S, E, W))
weaponlabel=ttk.Label(frame,text="Weapons")
weaponlabel.grid(column=0, row=0, sticky=(N, S, E, W))
weaponslist = Listbox(frame, selectmode=MULTIPLE, width=20, height=10,exportselection=0)#List for weapon
weaponslist.grid(column=0, row=1, columnspan=2)
scrollbar1 = Scrollbar(frame,command=weaponslist.yview)#bind
weaponslist.config(yscrollcommand = scrollbar1.set)#bind
scrollbar1.grid(column=2, row=1,sticky=(N, S))

for each_item in range(len(weapons)):  
    weaponslist.insert(END,weapons[each_item])

#---------------------------------For refinements---------------------------------#
frame2 = ttk.Frame(main, padding=(3, 3, 12, 12))
frame2.grid(column=2, row=0, sticky=(N, S, E, W))
refinementlabel=ttk.Label(frame2,text="Refinements")
refinementlabel.grid(column=0, row=0, sticky=(N, S, E, W))
selectedrefinements = []
refinementslist = Listbox(frame2, selectmode=MULTIPLE, width=10, height=10,exportselection=0)#List for refinements
refinementslist.grid(column=0, row=1, columnspan=1)
for each_item in range(len(refinements)):  
    refinementslist.insert(END,refinements[each_item])

#---------------------------------For sands---------------------------------#
frame3 = ttk.Frame(main, padding=(3, 3, 12, 12))
frame3.grid(column=3, row=0, sticky=(N, S, E, W))
sandslabel=ttk.Label(frame3,text="Sands")
sandslabel.grid(column=0, row=0, sticky=(N, S, E, W))
sandslist = Listbox(frame3, selectmode=MULTIPLE, width=10, height=10,exportselection=0)#List for refinements
sandslist.grid(column=0, row=1, columnspan=1)
for each_item in range(len(sands)):  
    sandslist.insert(END,sands[each_item].split('=',1)[0])



#---------------------------------For goblets---------------------------------#
frame4 = ttk.Frame(main, padding=(3, 3, 12, 12))
frame4.grid(column=4, row=0, sticky=(N, S, E, W))
gobletlabel=ttk.Label(frame4,text="Goblets")
gobletlabel.grid(column=0, row=0, sticky=(N, S, E, W))
gobletlist = Listbox(frame4, selectmode=MULTIPLE, width=10, height=10,exportselection=0)#List for refinements
gobletlist.grid(column=0, row=1, columnspan=1)
scrollbar2 = Scrollbar(frame4,command=weaponslist.yview)#bind
gobletlist.config(yscrollcommand = scrollbar2.set)#bind
scrollbar2.grid(column=1, row=1,sticky=(N, S))
for each_item in range(len(goblets)):  
    gobletlist.insert(END,goblets[each_item].split('=',1)[0])




#---------------------------------For circlets---------------------------------#
frame5 = ttk.Frame(main, padding=(3, 3, 12, 12))
frame5.grid(column=5, row=0, sticky=(N, S, E, W))
circletlabel=ttk.Label(frame5,text="Circlets")
circletlabel.grid(column=0, row=0, sticky=(N, S, E, W))
circletlist = Listbox(frame5, selectmode=MULTIPLE, width=10, height=10,exportselection=0)#List for refinements
circletlist.grid(column=0, row=1, columnspan=1)
for each_item in range(len(circlets)):  
    circletlist.insert(END,circlets[each_item].split('=',1)[0])




#---------------------------------GUI functions---------------------------------#
def select_all():
    weaponslist.select_set(0, END)

def deselect_all():
    weaponslist.selection_clear(0, END)

def optimize():
    pathnames=optrun.optimize(configpath)
    if pathnames is None:
        return
    optrun.run(character,pathnames)

def justrun():
    pathnames=easygui.fileopenbox("Please input file(s) to be optimized", "OPTIMIZER", filetypes= "*.txt", multiple=True, default=configpath+"\\*.txt")
    if pathnames is None:
        return

    optrun.run(character,pathnames)

def create():
    selectedweapons = [weaponslist.get(i) for i in weaponslist.curselection()]
    selectedrefinements=[refinementslist.get(i) for i in refinementslist.curselection()]
    selectedsands=[sands[i] for i in sandslist.curselection()]
    selectedgoblets=[goblets[i]  for i in gobletlist.curselection()]
    selectedcirclets=[circlets[i]  for i in circletlist.curselection()]
    # for val in reslist:
    #     print(val)
    if not selectedweapons or (not selectedrefinements)or (not selectedsands)or (not selectedgoblets)or (not selectedcirclets):
        status['text']="At least 1 element empty"
    else:
        numberoffiles=writeconfig(selectedweapons,selectedrefinements,selectedsands,selectedgoblets,selectedcirclets)
        status['text']="Wrote: "+str(numberoffiles)+" file(s)"

#---------------------------------GUI buttons---------------------------------#
btn = ttk.Button(frame, text="Select all", command=select_all)
btn.grid(column=0, row=2)

btn1 = ttk.Button(frame, text="Deselect all", command=deselect_all)
btn1.grid(column=0, row=3)

btn2 = ttk.Button(frame5, text="Create", command=create)
btn2.grid(column=0, row=2, pady=30)

frame6 = ttk.Frame(main, padding=(3, 3, 12, 12))
frame6.grid(column=6, row=0, sticky=(N, S, E, W))

btn3 = ttk.Button(frame6, text="Opt n' run", command=optimize)
btn3.grid(column=0, row=0, pady=30)

btn4 = ttk.Button(frame6, text="Just run", command=justrun)
btn4.grid(column=0, row=1)

status=ttk.Label(frame,text="Status")
status.grid(column=0, row=4, sticky=(N, S, E, W))


main.mainloop()


