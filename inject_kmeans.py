#!/usr/bin/env python
# Inject k-means color grouping into FluCoMa corpus-explorer, following the EXACT
# canonical wiring from fluid.plotter.maxhelp:
#   trigger -> [clear, fitpredict normalised clusters] -> fluid.kmeans~ @numclusters 4
#   kmeans[0] -> [route fitpredict] -> [dump] -> fluid.labelset~ clusters
#   labelset[1] -> [route dump] -> plotter(obj-43) inlet 1   (auto colors per cluster)
import json
SRC="/Users/s29524/Documents/Max 9/Packages/FluidCorpusManipulation/examples/tutorials/corpus-explorer.maxpat"
DST="/Users/s29524/dev/max-corpus/corpus_shredder.maxpat"
d=json.load(open(SRC)); p=d["patcher"]; boxes=p["boxes"]; lines=p["lines"]

def B(id_,maxclass,text,x,y,w=150,h=22,nin=2,nout=1,outt=None):
    b={"id":id_,"maxclass":maxclass,"numinlets":nin,"numoutlets":nout,"patching_rect":[float(x),float(y),float(w),float(h)]}
    if outt is not None: b["outlettype"]=outt
    if text is not None: b["text"]=text
    return {"box":b}
def L(s,so,dd,di): return {"patchline":{"source":[s,so],"destination":[dd,di]}}

new=[
 B("obj-ksh","comment","+ k-means color grouping  (auto-colored clusters in the plotter)",540,150,420,20,nin=1,nout=0),
 B("obj-tb","newobj","t b",540,195,40,22,nin=1,nout=1,outt=["bang"]),
 B("obj-nc","number",None,720,195,50,22,nin=1,nout=2,outt=["int","bang"]),
 B("obj-ncm","message","numclusters $1",720,230,110,22,nin=2,nout=1,outt=[""]),
 B("obj-fp","message","clear, fitpredict normalised clusters",540,235,210,22,nin=2,nout=1,outt=[""]),
 B("obj-km","newobj","fluid.kmeans~ @numclusters 4",540,275,200,22,nin=1,nout=2,outt=["","dictionary"]),
 B("obj-rf","newobj","route fitpredict",540,315,110,22,nin=1,nout=2,outt=["",""]),
 B("obj-dm","message","dump",540,350,50,22,nin=2,nout=1,outt=[""]),
 B("obj-ls","newobj","fluid.labelset~ clusters",540,390,160,22,nin=1,nout=2,outt=["dictionary",""]),
 B("obj-rd","newobj","route dump",540,430,90,22,nin=1,nout=2,outt=["",""]),
 B("obj-cc","comment","clusters -> plotter 2nd inlet",640,433,180,20,nin=1,nout=0),
]
boxes.extend(new)
lines.extend([
 L("obj-20",0,"obj-tb",0),   # after points are dumped to plotter -> trigger coloring
 L("obj-tb",0,"obj-fp",0),
 L("obj-fp",0,"obj-km",0),
 L("obj-km",0,"obj-rf",0),
 L("obj-rf",0,"obj-dm",0),
 L("obj-dm",0,"obj-ls",0),
 L("obj-ls",1,"obj-rd",0),   # labelset SECOND outlet
 L("obj-rd",0,"obj-43",1),   # -> plotter second inlet
 L("obj-nc",0,"obj-ncm",0),
 L("obj-ncm",0,"obj-km",0),
])
for b in boxes:
    if b["box"].get("id")=="obj-18": b["box"]["text"]="CORPUS SHREDDER (FluCoMa)"
json.dump(d,open(DST,"w"))
print("wrote",DST,"| boxes:",len(boxes),"lines:",len(lines))
