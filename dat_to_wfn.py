import os
def dat2wfn(file,j):
    #transforming a dat file to a multiwfn file
    d={1:'N',2:'N+1',3:'N-1'}
    c=file.split("\\")[-1]
    os.mkdir(fr"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\{c}")
    for j in d:
        with open(file+f'\\{d[j]}.dat', 'r') as f:
            lines = f.readlines()
        begin,end=0,0
        for i in range(len(lines)):
            if lines[i].strip() == "----- TOP OF INPUT FILE FOR BADER'S AIMPAC PROGRAM -----":
                begin = i
            if lines[i].strip() == "----- END OF INPUT FILE FOR BADER'S AIMPAC PROGRAM -----":
                end = i
                break
        #c=file.split("\\")[-1]
        #writing another multiwfn from begiin to end
        #os.mkdir(fr"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\{c}")
        with open(fr"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\{c}\{d[j]}.wfn", 'w') as f:
            for i in range(begin+1,end):
                f.write(lines[i]) 

    return f"{file.replace('.dat','.wfn')} is created. "
for i in range(2,50):
    dat2wfn(fr"C:\Users\Public\gamess-64\restart\4nitroaniline{i}",i)