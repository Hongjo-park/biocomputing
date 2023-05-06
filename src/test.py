
arr = [
    "------------M--T-S----P-T--E-------SL-Q-A--T---R-Y--P--G--A-",
    "------------MIAS-S----P-TA-DGRIPARMSISR-AISTQPSR-YATP--G--S-",
    "------------M--T-S----P-I----------SLGNAAP-A---R-Y--T-----A-",
    "------------M---------P------------AI-D----V--------------A-",
    "------------M--R-S----K-L--A-------RG-A-S--V---L-A--I--GIVA-",
    "------------M--VRAVI--PVT--R-------RL-QHA--G---H-Y--P--V--T-",
    "------------M-----------T---------------A------R-Y--A--A--P-",
    "------------M--Q-M----K-G--KL------AL-G-A--S---A-L--TI-G--L-",
    "------------MH-N-A----N-V--Q-------AR-T-L--K---KWFA-P--A--C-",
    "------------M----R----P-A--D-------RC-R-SP-T---G-R--PATG--RH",
    "------------M--SASMFRCV-S--K-------SL-A-A--G---L-L--L--M--A-",
    "------------M----------------------N----A------R-Y-----A--A-",
    "------------M-----------------------------------------------",
    "------------M--T-S----P-T--E-------SL-Q-A--T---R-Y--P--G--A-",
    "------------M--R-G----RLAFGA-------AL-A-A--I---A-L--T--H--C-",
    "------------M--R-T----K-L----------AL-G-A--S---A-M--AL-GLLA-",
    "MSGLARVDNVRFM--T-S----P-T--E-------SL-Q-A--T---R-Y--P--G--A-"
    ]

arr = [list(row) for row in arr]

arr = list(map(list, zip(*arr)))


print(''.join("*" if len(set(row)) == 1 else " " for row in arr))
