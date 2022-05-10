# %%
# %%
import pandas as pd
import easygui
import os
import subprocess
import re
# %%

pathnames=easygui.fileopenbox("Please input file(s) to be run", "Multiple executer", filetypes= "*.txt", multiple=True)



# %%


# %%
gz=easygui.buttonbox("Do you want to output the .gz file(s)?", choices=["Yes","No"])
character = easygui.enterbox("Please input the character you want to do the comparison with \n IMPORTANT: Type it exactly as the config file","Enter your character")
if character is None:
    exit()
print(gz)

# %%
configf=[]
for n, pathname in enumerate(pathnames):
    configf.append(os.path.basename(pathname))
    if n==0:
        configpath=(os.path.dirname(pathname))
    

    
print(configf)
gcsimpath=os.path.join(os.path.abspath(''))

# %%


# %%
def parsedps(config, gz, character):
    if gz:
        stream = subprocess.run([gcsimpath+"\gcsim.exe", '-c=' + configpath+"\\"+config,
        "-gz","-out="+configpath+"\\"+str(config).replace(".txt","")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    else:
        stream = subprocess.run([gcsimpath+"\gcsim.exe", '-c=' + configpath+"\\"+config],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    gcsimoutput = str(stream.stdout).split("\\n")
    #print(gcsimoutput)

    # in ST sims the dps line is the second to last line (in gcsimoutput there's 3 elements before it so it's index -4)
    stdps = round(float(re.findall("(?<=resulting in )(.*)(?= dps)", gcsimoutput[-4])[0]))

    for ind, token in enumerate (gcsimoutput):
        try:
            IndDPS=float(re.findall("(?<="+character+" total avg dps: )(.*)(?=; total percentage: )", gcsimoutput[ind])[0])
            break
        except IndexError:
            if ind==len(gcsimoutput)-1:
                print("Character not found!")
                exit()
    DPSlist.append(stdps)
    IndDPSlist.append(IndDPS)
    #IndDPSlist.append(IndDPS)
    print(f'{config}\n\tsingle target dps: {stdps}\n')


# %%
DPSlist=[]
IndDPSlist=[]
if (gz=="Yes"):
    for config in configf:
        parsedps(config, True, character)
    print(".gz file(s)")

else:
    print(".gz output disabled\n")
    for config in configf:
        parsedps(config, False, character)

# %%
if len(DPSlist)==len(IndDPSlist):
    df = pd.DataFrame({'Name' : configf, 'Total DPS' : DPSlist, character+' DPS' : IndDPSlist})    
    df['Name']=df['Name'].str.replace('.txt','',regex=True)#Delete .txt 
    df['Name']=df['Name'].str.replace('_','')#Replace _s with nothing 
    df['Total DPS']=pd.to_numeric(df['Total DPS'])#convert to numbers
    df=df.sort_values(by='Total DPS',ascending=False)#sort
    median=df['Total DPS'].median()
    df_sort_median=df.iloc[(df['Total DPS']-median).abs().argsort()[:1]]
    df_close_median=df_sort_median['Total DPS'].tolist()
    df['% Team DPS']=df['Total DPS']/df_close_median*100#create a new column with % of the median
    df.index=df['Name']
    del df['Name']

    print(df)

    print(df)

    exportExcel=easygui.buttonbox("Do you want to export the results to Excel?", choices=["Yes","No"])
    if exportExcel=="Yes":
        df.to_excel(""+character+".xlsx")
        print("Exported to "+character+".xlsx")



