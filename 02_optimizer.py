# %%
import easygui
import os
import subprocess

# %%
configf=[]
pathnames=easygui.fileopenbox("Please input file(s) to be optimized", "OPTIMIZER", filetypes= "*.txt", multiple=True)


# %%
for n, pathname in enumerate(pathnames):
    configf.append(os.path.basename(pathname))
    if n==0:
        configpath=(os.path.dirname(pathname))
    

    
print(configf)
gcsimpath=os.path.join(os.path.abspath(''))

# %%
for f, configs in enumerate(configf):
    print("---------You are optimizing this file: "+configf[f])
    stream = subprocess.run([gcsimpath+"\gcsim.exe", '-c=' + configpath+"\\"+configf[f],"--substatOptim=true","-out="+ configpath+"\_Optimized_"+configf[f]], capture_output=True)

    #print(configpath+"\gcsim.exe", '-c=' + configpath+"\\"+configf[f]+" --substatOptim=true -out="+ configpath+"\Opt"+configf[f]+" --calc")
    
    print(stream.stdout)

    


