#!/usr/bin/env python
# CORPUS SHREDDER (Max + FluCoMa): slice->kmeans color->2D map/audition
#   + editable grid sequencer + playhead + WAV export + robust spectral MORPH (bufcompose).
import json
SRC="/Users/s29524/Documents/Max 9/Packages/FluidCorpusManipulation/examples/tutorials/corpus-explorer.maxpat"
DST="/Users/s29524/dev/max-corpus/corpus_shredder.maxpat"
EXPORT="/Users/s29524/dev/max-corpus/shred_export.wav"
d=json.load(open(SRC)); p=d["patcher"]; boxes=p["boxes"]; lines=p["lines"]
def B(id_,maxclass,text,x,y,w=150,h=22,nin=2,nout=1,outt=None,extra=None):
    b={"id":id_,"maxclass":maxclass,"numinlets":nin,"numoutlets":nout,"patching_rect":[float(x),float(y),float(w),float(h)]}
    if outt is not None: b["outlettype"]=outt
    if text is not None: b["text"]=text
    if extra: b.update(extra)
    return {"box":b}
def L(s,so,dd,di): lines.append({"patchline":{"source":[s,so],"destination":[dd,di]}})

# ---------- (1) k-means color ----------
boxes += [
 B("obj-tb","newobj","t b",540,195,40,22,nin=1,nout=1,outt=["bang"]),
 B("obj-nc","number",None,720,195,50,22,nin=1,nout=2,outt=["int","bang"]),
 B("obj-ncm","message","numclusters $1",720,230,110,22,nin=2,nout=1,outt=[""]),
 B("obj-fp","message","clear, fitpredict normalised clusters",540,235,210,22,nin=2,nout=1,outt=[""]),
 B("obj-km","newobj","fluid.kmeans~ @numclusters 4",540,275,200,22,nin=1,nout=2,outt=["","dictionary"]),
 B("obj-rf","newobj","route fitpredict",540,315,110,22,nin=1,nout=2,outt=["",""]),
 B("obj-dm","message","dump",540,350,50,22,nin=2,nout=1,outt=[""]),
 B("obj-ls","newobj","fluid.labelset~ clusters",540,390,160,22,nin=1,nout=2,outt=["dictionary",""]),
 B("obj-rd","newobj","route dump",540,430,90,22,nin=1,nout=2,outt=["",""]),
 B("obj-lb","newobj","loadbang",900,160,60,22,nin=1,nout=1,outt=["bang"]),
 B("obj-k4","message","4",900,195,30,22,nin=2,nout=1,outt=[""]),
]
L("obj-20",0,"obj-tb",0); L("obj-tb",0,"obj-fp",0); L("obj-fp",0,"obj-km",0)
L("obj-km",0,"obj-rf",0); L("obj-rf",0,"obj-dm",0); L("obj-dm",0,"obj-ls",0)
L("obj-ls",1,"obj-rd",0); L("obj-rd",0,"obj-43",1)
L("obj-nc",0,"obj-ncm",0); L("obj-ncm",0,"obj-km",0)
L("obj-lb",0,"obj-k4",0); L("obj-k4",0,"obj-nc",0)

# ---------- (2) beat sequencer + editable grid + playhead ----------
boxes += [
 B("obj-seq","newobj","js shredder_seq.js",980,300,150,22,nin=1,nout=3,outt=["","",""]),
 B("obj-play","toggle",None,980,360,24,24,nin=1,nout=1,outt=["int"]),
 B("obj-metro","newobj","metro 125",1020,360,70,22,nin=2,nout=1,outt=["bang"]),
 B("obj-bpm","number",None,980,420,50,22,nin=1,nout=2,outt=["int","bang"]),
 B("obj-bexpr","newobj","expr 60000./$f1/4.",1040,420,130,22,nin=1,nout=1,outt=[""]),
 B("obj-gen","button",None,980,470,24,24,nin=1,nout=1,outt=["bang"]),
 B("obj-genm","message","generate",1020,470,70,22,nin=2,nout=1,outt=[""]),
 B("obj-lb2","newobj","loadbang",1180,360,60,22,nin=1,nout=1,outt=["bang"]),
 B("obj-b120","message","120",1180,395,40,22,nin=2,nout=1,outt=[""]),
 B("obj-grid","matrixctrl",None,980,520,300,90,nin=1,nout=2,outt=["list","list"],
   extra={"rows":4,"columns":16,"range":2,"bgcolor":[0.13,0.15,0.19,1.0],"elementcolor":[0.27,0.3,0.36,1.0],"color":[0.35,0.82,0.78,1.0]}),
 B("obj-gridprep","newobj","prepend cell",980,630,90,22,nin=1,nout=1,outt=[""]),
 B("obj-curt","newobj","t i b",1300,520,50,22,nin=1,nout=2,outt=["int","bang"]),
 B("obj-curclr","message","clear",1380,520,45,22,nin=2,nout=1,outt=[""]),
 B("obj-curpack","newobj","pack 0 0 1",1300,555,80,22,nin=3,nout=1,outt=[""]),
 B("obj-curset","newobj","prepend set",1300,590,80,22,nin=1,nout=1,outt=[""]),
 B("obj-cursor","matrixctrl",None,1300,625,300,20,nin=1,nout=2,outt=["list","list"],
   extra={"rows":1,"columns":16,"range":2,"bgcolor":[0.13,0.15,0.19,1.0],"elementcolor":[0.18,0.2,0.24,1.0],"color":[1.0,0.85,0.3,1.0]}),
]
L("obj-play",0,"obj-metro",0); L("obj-metro",0,"obj-seq",0)
L("obj-bpm",0,"obj-bexpr",0); L("obj-bexpr",0,"obj-metro",1)
L("obj-gen",0,"obj-genm",0); L("obj-genm",0,"obj-seq",0)
L("obj-seq",0,"obj-11",0)
L("obj-lb2",0,"obj-b120",0); L("obj-b120",0,"obj-bpm",0)
L("obj-ls",1,"obj-seq",0)
L("obj-seq",1,"obj-grid",0)
L("obj-grid",0,"obj-gridprep",0); L("obj-gridprep",0,"obj-seq",0)
L("obj-seq",2,"obj-curt",0)
L("obj-curt",1,"obj-curclr",0); L("obj-curclr",0,"obj-cursor",0)
L("obj-curt",0,"obj-curpack",0); L("obj-curpack",0,"obj-curset",0); L("obj-curset",0,"obj-cursor",0)

# ---------- (4) WAV export ----------
boxes += [
 B("obj-sfrec","newobj","sfrecord~ 1",980,690,90,22,nin=2,nout=1,outt=["signal"]),
 B("obj-rectog","toggle",None,1100,690,24,24,nin=1,nout=1,outt=["int"]),
 B("obj-recsel","newobj","sel 1 0",1100,720,60,22,nin=1,nout=3,outt=["bang","bang",""]),
 B("obj-recopen","message","open "+EXPORT+", 1",1100,750,330,22,nin=2,nout=1,outt=[""]),
 B("obj-recstop","message","0",1430,750,30,22,nin=2,nout=1,outt=[""]),
]
L("obj-54",0,"obj-sfrec",0); L("obj-rectog",0,"obj-recsel",0)
L("obj-recsel",0,"obj-recopen",0); L("obj-recopen",0,"obj-sfrec",0)
L("obj-recsel",1,"obj-recstop",0); L("obj-recstop",0,"obj-sfrec",0)

# ---------- (5) MORPH: slice -> dedicated buffer (bufcompose) -> groove loop -> pfft~ ----------
MY=820
def morph_chan(tag, x0):
    pre="obj-m"+tag
    boxes.extend([
     B("buf-"+tag,"newobj","buffer~ morph"+tag,x0,MY-40,120,22,nin=1,nout=2,outt=["signal","bang"]),
     B(pre,"number",None,x0,MY,50,22,nin=1,nout=2,outt=["int","bang"]),
     B(pre+"t","newobj","t i i",x0,MY+30,50,22,nin=1,nout=2,outt=["int","int"]),
     B(pre+"pk1","newobj","peek~ slicepoints",x0,MY+62,130,22,nin=2,nout=1,outt=["float"]),
     B(pre+"p1","newobj","+ 1",x0+150,MY+30,40,22,nin=2,nout=1,outt=["int"]),
     B(pre+"pk2","newobj","peek~ slicepoints",x0+150,MY+62,130,22,nin=2,nout=1,outt=["float"]),
     B(pre+"sub","newobj","- 0.",x0+150,MY+95,50,22,nin=2,nout=1,outt=["float"]),     # end - start (cold=start)
     B(pre+"sf","message","startframe $1",x0,MY+95,100,22,nin=2,nout=1,outt=[""]),
     B(pre+"tb","newobj","t b i",x0+150,MY+128,50,22,nin=1,nout=2,outt=["bang","int"]),
     B(pre+"nf","message","numframes $1",x0+150,MY+160,100,22,nin=2,nout=1,outt=[""]),
     B(pre+"bc","newobj","fluid.bufcompose~ @source sound @destination morph"+tag,x0,MY+195,300,22,nin=1,nout=2,outt=["bang","bang"]),
     B(pre+"gr","newobj","groove~ morph"+tag,x0,MY+230,110,22,nin=3,nout=3,outt=["signal","signal","signal"]),
    ])
    L(pre,0,pre+"t",0)
    # start path (t outlet1 fires first)
    L(pre+"t",1,pre+"pk1",0)
    L(pre+"pk1",0,pre+"sub",1)        # start -> !- cold inlet
    L(pre+"pk1",0,pre+"sf",0)         # start -> startframe message
    L(pre+"sf",0,pre+"bc",0)
    # end path (t outlet0 fires second)
    L(pre+"t",0,pre+"p1",0); L(pre+"p1",0,pre+"pk2",0)
    L(pre+"pk2",0,pre+"sub",0)        # end -> !- hot -> (start - end)?? no: !- 0. computes (right - left). use carefully
    L(pre+"sub",0,pre+"tb",0)
    L(pre+"tb",1,pre+"nf",0); L(pre+"nf",0,pre+"bc",0)   # set numframes
    L(pre+"tb",0,pre+"bc",0)          # then bang bufcompose
    return pre+"gr"
grA=morph_chan("A",980); grB=morph_chan("B",1320)
boxes += [
 B("obj-msig","newobj","sig~ 1.",980,MY+265,55,22,nin=1,nout=1,outt=["signal"]),
 B("obj-mlb","newobj","loadbang",1120,MY+265,60,22,nin=1,nout=1,outt=["bang"]),
 B("obj-mloop","message","loop 1",1120,MY+295,55,22,nin=2,nout=1,outt=[""]),
 B("obj-mstartp","message","0",1185,MY+295,30,22,nin=2,nout=1,outt=[""]),
 B("obj-mA0","message","0",1225,MY+295,30,22,nin=2,nout=1,outt=[""]),
 B("obj-mB0","message","12",1265,MY+295,30,22,nin=2,nout=1,outt=[""]),
 B("obj-pfft","newobj","pfft~ morph~ 2048 4",980,MY+330,170,22,nin=3,nout=1,outt=["signal"]),
 B("obj-msl","slider",None,1170,MY+330,160,18,nin=1,nout=1,outt=[""],extra={"size":128.0,"orientation":1}),
 B("obj-mscale","newobj","scale 0 127 0. 1.",1170,MY+360,120,22,nin=6,nout=1,outt=[""]),
 B("obj-mline","newobj","line~",1170,MY+390,44,22,nin=2,nout=1,outt=["signal","bang"]),
 B("obj-mgain","newobj","*~",980,MY+370,40,22,nin=2,nout=1,outt=["signal"]),
 B("obj-mtog","toggle",None,930,MY+370,24,24,nin=1,nout=1,outt=["int"]),
 # debug monitors
 B("obj-snap","newobj","snapshot~ 80",1340,MY+330,100,22,nin=2,nout=1,outt=["float"]),
 B("obj-snapn","flonum",None,1340,MY+360,60,22,nin=1,nout=2,outt=["float","bang"]),
 B("obj-mtA","newobj","meter~",1340,MY+265,18,40,nin=1,nout=1,outt=["float"]),
 B("obj-mtB","newobj","meter~",1370,MY+265,18,40,nin=1,nout=1,outt=["float"]),
]
L("obj-msig",0,grA,0); L("obj-msig",0,grB,0)
L("obj-mlb",0,"obj-mloop",0); L("obj-mlb",0,"obj-mstartp",0); L("obj-mlb",0,"obj-mA0",0); L("obj-mlb",0,"obj-mB0",0)
L("obj-mloop",0,grA,0); L("obj-mloop",0,grB,0)
L("obj-mstartp",0,grA,0); L("obj-mstartp",0,grB,0)
L("obj-mA0",0,"obj-mA",0); L("obj-mB0",0,"obj-mB",0)
L("obj-tb",0,"obj-mA",0); L("obj-tb",0,"obj-mB",0)   # re-fire after analysis
L(grA,0,"obj-pfft",0); L(grB,0,"obj-pfft",1)
L("obj-msl",0,"obj-mscale",0); L("obj-mscale",0,"obj-mline",0); L("obj-mline",0,"obj-pfft",2)
L("obj-pfft",0,"obj-mgain",0); L("obj-mtog",0,"obj-mgain",1)
L("obj-mgain",0,"obj-7",0); L("obj-mgain",0,"obj-7",1)
L("obj-mline",0,"obj-snap",0); L("obj-snap",0,"obj-snapn",0)
L(grA,0,"obj-mtA",0); L(grB,0,"obj-mtB",0)

# ---------- (3) Presentation ----------
byid={b["box"]["id"]:b["box"] for b in boxes}
def present(id_,x,y,w,h):
    bx=byid.get(id_)
    if bx: bx["presentation"]=1; bx["presentation_rect"]=[float(x),float(y),float(w),float(h)]
if "obj-18" in byid: byid["obj-18"]["text"]="CORPUS SHREDDER (patching title)"
present("obj-7",40,118,46,46); present("obj-47",40,206,40,40)
present("obj-nc",40,290,60,24); present("obj-54",55,358,40,140); present("obj-5",40,536,170,28)
present("obj-43",240,116,640,290)
present("obj-play",240,448,26,26); present("obj-bpm",360,449,50,22)
present("obj-gen",470,448,26,26); present("obj-rectog",600,448,26,26)
present("obj-grid",300,486,560,112); present("obj-cursor",300,602,560,12)
present("obj-mtog",300,660,26,26); present("obj-mA",420,661,50,22); present("obj-mB",500,661,50,22); present("obj-msl",580,663,260,18)
present("obj-snapn",300,712,70,24); present("obj-mtA",420,706,18,36); present("obj-mtB",450,706,18,36)
def label(id_,txt,x,y,w,h,fs=12.0):
    boxes.append(B(id_,"comment",txt,2000,2000,w,h,nin=1,nout=0,extra={"fontsize":fs,"presentation":1,"presentation_rect":[float(x),float(y),float(w),float(h)]}))
label("ui-title","CORPUS SHREDDER",30,16,820,34,24.0)
label("ui-sub","FluCoMa concatenative corpus — slice · cluster · sequence · export · morph",30,56,760,20)
label("ui-1","1 · AUDIO ON",40,96,180,18,12.0); label("ui-2","2 · ANALYZE",40,184,180,18,12.0)
label("ui-3","CLUSTERS (k)",40,268,180,18,12.0); label("ui-4","GAIN",40,338,180,18,12.0)
label("ui-5","drop a folder of WAV/AIFF here",40,516,260,18,11.0)
label("ui-map","SOUND MAP   —   drag to audition · color = k-means cluster",240,96,560,18,12.0)
label("ui-beat","BEAT SEQUENCER   —   click cells to edit · each row = a cluster",240,424,560,18,12.0)
label("ui-play","PLAY",272,450,50,18,12.0); label("ui-bpm","BPM",415,450,50,18,12.0)
label("ui-gen","🎲 NEW BEAT",502,450,110,18,12.0); label("ui-rec","● REC → shred_export.wav",632,450,260,18,11.0)
label("ui-rows","rows 1-4 = clusters",240,486,56,112,9.0)
label("ui-morph","MORPH   —   pick two slices, blend timbre A ◄———► B",240,636,560,18,12.0)
label("ui-mon","ON",334,662,40,18,12.0); label("ui-mA","A",406,662,16,18,11.0); label("ui-mB","B",486,662,16,18,11.0)
label("ui-dbg","DEBUG:  morph value          A-level   B-level",300,694,360,14,10.0)
p["openinpresentation"]=1; p["rect"]=[30.0,50.0,1010.0,820.0]
json.dump(d,open(DST,"w"))
ids={b["box"]["id"] for b in boxes}
bad=[(s,e) for l in lines for s,e in [(l["patchline"]["source"][0],l["patchline"]["destination"][0])] if s not in ids or e not in ids]
print("wrote",DST,"| boxes:",len(boxes),"lines:",len(lines),"| dangling:",bad or "none")
