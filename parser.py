from glob import glob
import json
from dotdict import DotDict


COLUMNS = ["time", "finesse_p", "piecepersec", "normed_allclear", "normed_doubles", "normed_minitspindoubles", 
            "normed_minitspins", "normed_minitspinsingles", "normed_quads", "normed_realtspins", "normed_singles", 
            "normed_triples", "normed_tspindoubles", "normed_tspinquads", "normed_tspinsingles", "normed_tspintriples",
            "holdspersec", "holdsperpieceplaced", "linesperpiece", "pieceperinput", "inputspersec"]

def genRaw(tjobj):
    tjo = DotDict(tjobj)
    endcontext = tjo.endcontext
    res = []

    # time
    tot_seconds = endcontext.finalTime / 1000
    res.append(tot_seconds) # time in secs

    # non normed stuff
    # res.append(endcontext.piecesplaced) # total pieces placed
    # res.append(endcontext.finesse.perfectpieces) # total perfect pieces

    # all the normed stuff
    res.append(endcontext.finesse.perfectpieces / endcontext.piecesplaced) # normalized finesse percentage
    res.append(endcontext.piecesplaced / tot_seconds) # pps

    total_clears = 0
    total_clears += endcontext.clears.allclear
    total_clears += endcontext.clears.doubles
    total_clears += endcontext.clears.minitspindoubles
    total_clears += endcontext.clears.minitspins
    total_clears += endcontext.clears.minitspinsingles
    total_clears += endcontext.clears.quads
    total_clears += endcontext.clears.realtspins
    total_clears += endcontext.clears.singles
    total_clears += endcontext.clears.triples
    total_clears += endcontext.clears.tspindoubles
    total_clears += endcontext.clears.tspinquads
    total_clears += endcontext.clears.tspinsingles
    total_clears += endcontext.clears.tspintriples

    # normed
    res.append(endcontext.clears.allclear / total_clears)         # allclear
    res.append(endcontext.clears.doubles / total_clears)          # doubles
    res.append(endcontext.clears.minitspindoubles / total_clears) # minitspindoubles
    res.append(endcontext.clears.minitspins / total_clears)       # minitspins
    res.append(endcontext.clears.minitspinsingles / total_clears) # minitspinsingles
    res.append(endcontext.clears.quads / total_clears)            # quads
    res.append(endcontext.clears.realtspins / total_clears)       # realtspins
    res.append(endcontext.clears.singles / total_clears)          # singles
    res.append(endcontext.clears.triples / total_clears)          # triples
    res.append(endcontext.clears.tspindoubles / total_clears)     # tspindoubles
    res.append(endcontext.clears.tspinquads / total_clears)       # tspinquads
    res.append(endcontext.clears.tspinsingles / total_clears)     # tspinsingles
    res.append(endcontext.clears.tspintriples / total_clears)     # tspintriples

    res.append(endcontext.holds / tot_seconds) # holds per sec
    res.append(endcontext.holds / endcontext.piecesplaced) # holds per piece placed

    res.append(endcontext.lines / endcontext.piecesplaced) # lines per piece
    
    res.append(endcontext.piecesplaced / endcontext.inputs) # piece per input
    res.append(endcontext.inputs / tot_seconds) # inputs per sec

    return res

import pandas as pd

rows = []
for file in glob("*.ttr"):
    print(f"{file=}")
    jobj = json.load(open(file))
    rows.append(genRaw(jobj))

df = pd.DataFrame(rows, columns=COLUMNS)
df.to_csv("out.csv")