// shredder_seq.js  —  step-sequencer brain for CORPUS SHREDDER (Max, legacy js / ES5)
// inlet 0: messages  bang(=advance one step), generate, clear, numslices N,
//          cell C R V (toggle), rows N, cluster ID LABEL, clearclusters
// outlet 0: slice id  -> "p playback"
// outlet 1: matrixctrl cell message [col,row,val]  (for the grid UI, used later)
// outlet 2: current step index (for a cursor)
autowatch = 1;
inlets = 1;
outlets = 3;

var ROWS = 4, COLS = 16;
var grid = [];
function alloc(){ grid=[]; for(var r=0;r<ROWS;r++){ grid[r]=[]; for(var c=0;c<COLS;c++) grid[r][c]=0; } }
alloc();

var step = 0;
var numSlices = 50;
var clusterMap = null;   // { label: [sliceId,...] }

function numslices(n){ numSlices = Math.max(1, parseInt(n)||1); }
function rows(n){ ROWS = Math.max(1, Math.min(16, parseInt(n)||4)); alloc(); }

function clearclusters(){ clusterMap = null; }
function cluster(id, label){
    if(clusterMap===null) clusterMap = {};
    var L = "c"+label;
    if(!clusterMap[L]) clusterMap[L] = [];
    clusterMap[L].push(parseInt(id));
}

// find the object that maps id -> (array|obj containing a label)
function findIdMap(o){
    if(!o || typeof o!=="object") return null;
    var keys=[]; for(var k in o){ if(o.hasOwnProperty(k)) keys.push(k); }
    if(keys.length){
        var numeric=0, valArr=0;
        for(var i=0;i<keys.length;i++){
            if(/^\d+$/.test(keys[i])) numeric++;
            var v=o[keys[i]];
            if((v instanceof Array) || (v && typeof v==="object")) valArr++;
        }
        if(numeric>=keys.length*0.6 && valArr>=keys.length*0.6) return o;
    }
    for(var kk in o){ if(o.hasOwnProperty(kk)){ var r=findIdMap(o[kk]); if(r) return r; } }
    return null;
}
function labelOf(v){
    if(v instanceof Array) return v[0];
    if(v && v.data) return (v.data instanceof Array)? v.data[0] : v.data;
    return v;
}
function parseDictByName(name){
    try{
        var d = new Dict(name);
        var raw = d.stringify();
        post("shredder RAW("+name+"): "+String(raw).substring(0,400)+"\n");
        var obj = JSON.parse(raw);
        var data = findIdMap(obj);
        if(!data){ post("shredder: no id-map found in dict\n"); clusterMap=null; return; }
        clusterMap = {};
        var nIds=0, maxId=0;
        for(var id in data){
            if(!data.hasOwnProperty(id)) continue;
            var L = "c"+labelOf(data[id]);
            if(!clusterMap[L]) clusterMap[L]=[];
            var iid=parseInt(id); clusterMap[L].push(iid);
            nIds++; if(iid>maxId) maxId=iid;
        }
        if(nIds>0) numSlices=Math.max(numSlices,maxId+1); else clusterMap=null;
        var k=0; for(var key in clusterMap) k++;
        post("shredder: clusters loaded — "+nIds+" slices into "+k+" groups\n");
    }catch(e){ post("shredder dump parse error: "+e+"\n"); clusterMap=null; }
}
// message arrives as "dump dictionary <realname>"  -> the LAST token is the real dict name
function dump(){ var a=arguments; if(a.length) parseDictByName(a[a.length-1]); }
function dictionary(name){ parseDictByName(name); }

function pickForRow(r){
    if(clusterMap){
        var labels = [];
        for(var k in clusterMap) labels.push(k);
        labels.sort();
        if(labels.length){
            var arr = clusterMap[labels[r % labels.length]];
            if(arr && arr.length) return arr[Math.floor(Math.random()*arr.length)];
        }
    }
    return Math.floor(Math.random()*numSlices);
}

function bang(){            // advance one step (driven by metro)
    for(var r=0;r<ROWS;r++){
        if(grid[r][step]) outlet(0, pickForRow(r));
    }
    outlet(2, step);
    step = (step+1) % COLS;
}

function cell(c, r, v){     // toggle one grid cell (from matrixctrl)
    c=parseInt(c); r=parseInt(r);
    if(r>=0 && r<ROWS && c>=0 && c<COLS) grid[r][c] = (parseInt(v)?1:0);
}

function redraw(){
    // use "set" so matrixctrl does NOT echo back (avoids feedback)
    for(var r=0;r<ROWS;r++) for(var c=0;c<COLS;c++) outlet(1, ["set", c, r, grid[r][c]]);
}

function clear(){ alloc(); step=0; redraw(); }

function generate(){       // musical-ish random pattern (kick/snare/hat/perc rows)
    alloc();
    if(ROWS>0){ grid[0][0]=1; grid[0][8]=1; if(Math.random()<0.5) grid[0][14]=1; if(Math.random()<0.3) grid[0][6]=1; }
    if(ROWS>1){ grid[1][4]=1; grid[1][12]=1; if(Math.random()<0.3) grid[1][15]=1; }
    if(ROWS>2){ for(var c=0;c<COLS;c+=2) grid[2][c]=1; for(var c2=1;c2<COLS;c2+=2) if(Math.random()<0.25) grid[2][c2]=1; }
    if(ROWS>3){ for(var c=0;c<COLS;c++) if(Math.random()<0.12) grid[3][c]=1; }
    step=0; redraw();
}

function loadbang(){ generate(); }
