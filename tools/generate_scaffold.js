#!/usr/bin/env node
// ═══════════════════════════════════════
// Go Squad Perspective Engine — Scaffold Generator
// Runs the chess analysis + custom character mapping → standalone HTML
// ═══════════════════════════════════════

const fs = require('fs');
const path = require('path');

// ═══════════════════════════════════════
// CHESS ENGINE (from perspective_engine.html)
// ═══════════════════════════════════════
const PIECE_ICONS={K:{white:'♔',black:'♚'},Q:{white:'♕',black:'♛'},R:{white:'♖',black:'♜'},B:{white:'♗',black:'♝'},N:{white:'♘',black:'♞'},P:{white:'♙',black:'♟'}};
const PIECE_NAMES={K:'King',Q:'Queen',R:'Rook',B:'Bishop',N:'Knight',P:'Pawn'};

class Board{
    constructor(){this.board=Array.from({length:8},()=>Array(8).fill(null));const br=['R','N','B','Q','K','B','N','R'];for(let f=0;f<8;f++){this.board[0][f]={type:br[f],color:'white'};this.board[1][f]={type:'P',color:'white'};this.board[6][f]={type:'P',color:'black'};this.board[7][f]={type:br[f],color:'black'};}}
    sq2i(sq){return[sq.charCodeAt(0)-97,parseInt(sq[1])-1]}
    i2sq(f,r){return String.fromCharCode(97+f)+(r+1)}
    get(sq){const[f,r]=this.sq2i(sq);return(r>=0&&r<8&&f>=0&&f<8)?this.board[r][f]:null}
    set(sq,v){const[f,r]=this.sq2i(sq);this.board[r][f]=v}
    snapshot(){return this.board.map(row=>row.map(c=>c?{...c}:null))}
    pathClear(ff,fr,tf,tr){const sf=Math.sign(tf-ff),sr=Math.sign(tr-fr);let f=ff+sf,r=fr+sr;while(f!==tf||r!==tr){if(this.board[r][f])return false;f+=sf;r+=sr}return true}
    canReach(from,to,pt,color,cap){const[ff,fr]=this.sq2i(from),[tf,tr]=this.sq2i(to),df=tf-ff,dr=tr-fr;if(pt==='P'){const dir=color==='white'?1:-1;if(cap)return Math.abs(df)===1&&dr===dir;if(df!==0)return false;if(dr===dir&&!this.board[tr][tf])return true;const sr=color==='white'?1:6;return fr===sr&&dr===2*dir&&!this.board[fr+dir][ff]&&!this.board[tr][tf]}if(pt==='N')return(Math.abs(df)===1&&Math.abs(dr)===2)||(Math.abs(df)===2&&Math.abs(dr)===1);if(pt==='K')return Math.abs(df)<=1&&Math.abs(dr)<=1;if(pt==='B'||pt==='Q'){if(Math.abs(df)===Math.abs(dr)&&df!==0&&this.pathClear(ff,fr,tf,tr))return true;if(pt==='B')return false}if(pt==='R'||pt==='Q'){if((df===0||dr===0)&&(df!==0||dr!==0)&&this.pathClear(ff,fr,tf,tr))return true}return false}
    findSource(move,color){for(let r=0;r<8;r++)for(let f=0;f<8;f++){const p=this.board[r][f];if(!p||p.type!==move.piece||p.color!==color)continue;const sq=this.i2sq(f,r);if(move.srcF&&sq[0]!==move.srcF)continue;if(move.srcR&&sq[1]!==move.srcR)continue;if(this.canReach(sq,move.dest,move.piece,color,move.cap))return sq}return null}
    getAttacked(sq){const p=this.get(sq);if(!p)return[];const[f,r]=this.sq2i(sq),res=[];if(p.type==='P'){const d=p.color==='white'?1:-1;if(f>0&&r+d>=0&&r+d<8)res.push(this.i2sq(f-1,r+d));if(f<7&&r+d>=0&&r+d<8)res.push(this.i2sq(f+1,r+d));return res}const dirs={N:[[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]],K:[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]],B:[[-1,-1],[-1,1],[1,-1],[1,1]],R:[[-1,0],[1,0],[0,-1],[0,1]],Q:[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]};const slider=['B','R','Q'].includes(p.type);for(const[df,dr]of(dirs[p.type]||[])){let nf=f+df,nr=r+dr;if(!slider){if(nf>=0&&nf<8&&nr>=0&&nr<8)res.push(this.i2sq(nf,nr))}else{while(nf>=0&&nf<8&&nr>=0&&nr<8){res.push(this.i2sq(nf,nr));if(this.board[nr][nf])break;nf+=df;nr+=dr}}}return res}
    allAttacked(color){const s=new Set();for(let r=0;r<8;r++)for(let f=0;f<8;f++){const p=this.board[r][f];if(p&&p.color===color)for(const sq of this.getAttacked(this.i2sq(f,r)))s.add(sq)}return s}
    adjacentSquares(sq){const[f,r]=this.sq2i(sq),res=[];for(let df=-1;df<=1;df++)for(let dr=-1;dr<=1;dr++){if(df===0&&dr===0)continue;const nf=f+df,nr=r+dr;if(nf>=0&&nf<8&&nr>=0&&nr<8)res.push(this.i2sq(nf,nr))}return res}
}

function parseMove(s){let m=s.trim().replace(/[!?]/g,'');const r={raw:s,piece:'P',dest:null,srcF:null,srcR:null,cap:false,check:false,mate:false,castle:null,promo:null};if(m.includes('#')){r.mate=true;r.check=true;m=m.replace('#','')}else if(m.includes('+')){r.check=true;m=m.replace(/\+/g,'')}if(m==='O-O'||m==='0-0'){r.castle='K';r.piece='K';return r}if(m==='O-O-O'||m==='0-0-0'){r.castle='Q';r.piece='K';return r}const pm=m.match(/=([QRBN])/);if(pm){r.promo=pm[1];m=m.replace(/=[QRBN]/,'')}if(m.includes('x')){r.cap=true;m=m.replace('x','')}if('KQRBN'.includes(m[0])){r.piece=m[0];m=m.slice(1)}const dm=m.match(/([a-h][1-8])$/);if(dm){r.dest=dm[1];m=m.replace(/[a-h][1-8]$/,'')}if(m.length>0){if(/[a-h]/.test(m))r.srcF=m.match(/[a-h]/)[0];if(/[1-8]/.test(m))r.srcR=m.match(/[1-8]/)[0]}return r}

// ═══════════════════════════════════════
// ANALYSIS
// ═══════════════════════════════════════
function analyzeGame(PGN) {
    const pieces = {};
    const timeline = [];
    const boardSnapshots = [];
    let totalCaptures = 0;

    const files='abcdefgh'; const back=['R','N','B','Q','K','B','N','R'];
    for(let f=0;f<8;f++){const t=back[f],sq=files[f]+'1',suffix=(t==='R'||t==='N'||t==='B')?files[f]:'',id=`w_${t}${suffix}`;
        pieces[id]={id,color:'white',type:t,origType:t,startSq:sq,sq,alive:true,isPawn:false,label:`White ${PIECE_NAMES[t]}`,shortLabel:`${PIECE_NAMES[t]} (${sq})`,moves:[],captures:[],capturedBy:null,capturedOnMove:null,capturedByLabel:'',threats:[],witnesses:[],checksGiven:[],promoted:false,deliversMate:false};}
    for(let f=0;f<8;f++){const sq=files[f]+'2',id=`w_P${files[f]}`;
        pieces[id]={id,color:'white',type:'P',origType:'P',startSq:sq,sq,alive:true,isPawn:true,label:`White Pawn (${files[f]})`,shortLabel:`Pawn ${files[f]}2`,moves:[],captures:[],capturedBy:null,capturedOnMove:null,capturedByLabel:'',threats:[],witnesses:[],checksGiven:[],promoted:false,deliversMate:false};}
    for(let f=0;f<8;f++){const t=back[f],sq=files[f]+'8',suffix=(t==='R'||t==='N'||t==='B')?files[f]:'',id=`b_${t}${suffix}`;
        pieces[id]={id,color:'black',type:t,origType:t,startSq:sq,sq,alive:true,isPawn:false,label:`Black ${PIECE_NAMES[t]}`,shortLabel:`${PIECE_NAMES[t]} (${sq})`,moves:[],captures:[],capturedBy:null,capturedOnMove:null,capturedByLabel:'',threats:[],witnesses:[],checksGiven:[],promoted:false,deliversMate:false};}
    for(let f=0;f<8;f++){const sq=files[f]+'7',id=`b_P${files[f]}`;
        pieces[id]={id,color:'black',type:'P',origType:'P',startSq:sq,sq,alive:true,isPawn:true,label:`Black Pawn (${files[f]})`,shortLabel:`Pawn ${files[f]}7`,moves:[],captures:[],capturedBy:null,capturedOnMove:null,capturedByLabel:'',threats:[],witnesses:[],checksGiven:[],promoted:false,deliversMate:false};}

    function findPieceIdAt(sq){for(const[id,p]of Object.entries(pieces)){if(p.alive&&p.sq===sq)return id}return null}

    const clean=PGN.replace(/\{[^}]*\}/g,'').replace(/\([^)]*\)/g,'').replace(/\[[^\]]*\]/g,'').replace(/\n/g,' ');
    const tokens=clean.split(/\s+/).filter(t=>t&&!t.match(/^\d+\./)&&!['1-0','0-1','1/2-1/2','*'].includes(t));

    let gameResult='';
    if(PGN.includes('1-0'))gameResult='White wins';
    else if(PGN.includes('0-1'))gameResult='Black wins';
    else if(PGN.includes('1/2'))gameResult='Draw';
    if(tokens.length>0&&tokens[tokens.length-1].includes('#')){
        const lastColor=tokens.length%2===1?'White':'Black';
        gameResult=lastColor+' wins by checkmate';
    }

    const board=new Board();
    for(const[id,p]of Object.entries(pieces)){const cell=board.get(p.startSq);if(cell)cell.id=id}
    boardSnapshots.push(board.snapshot());

    const parsedForPlot=[];

    tokens.forEach((str,index)=>{
        const color=index%2===0?'white':'black';const moveNum=Math.floor(index/2)+1;const halfMove=index+1;
        const move=parseMove(str);const events=[];let moverId=null,capturedId=null,fromSq=null,toSq=move.dest;

        if(move.castle){
            const rank=color==='white'?'1':'8';const kSq='e'+rank;moverId=findPieceIdAt(kSq);
            if(move.castle==='K'){const rSq='h'+rank,rId=findPieceIdAt(rSq);board.set('g'+rank,board.get(kSq));board.set('f'+rank,board.get(rSq));board.set(kSq,null);board.set(rSq,null);if(moverId){pieces[moverId].sq='g'+rank;pieces[moverId].moves.push({halfMove,moveNum,from:kSq,to:'g'+rank,raw:str})}if(rId){pieces[rId].sq='f'+rank;pieces[rId].moves.push({halfMove,moveNum,from:rSq,to:'f'+rank,raw:str})}fromSq=kSq;toSq='g'+rank}
            else{const rSq='a'+rank,rId=findPieceIdAt(rSq);board.set('c'+rank,board.get(kSq));board.set('d'+rank,board.get(rSq));board.set(kSq,null);board.set(rSq,null);if(moverId){pieces[moverId].sq='c'+rank;pieces[moverId].moves.push({halfMove,moveNum,from:kSq,to:'c'+rank,raw:str})}if(rId){pieces[rId].sq='d'+rank;pieces[rId].moves.push({halfMove,moveNum,from:rSq,to:'d'+rank,raw:str})}fromSq=kSq;toSq='c'+rank}
        }else{
            fromSq=board.findSource(move,color);
            if(fromSq){moverId=findPieceIdAt(fromSq);
                if(move.cap){capturedId=findPieceIdAt(move.dest);if(!capturedId&&move.piece==='P'){const epSq=move.dest[0]+fromSq[1];capturedId=findPieceIdAt(epSq);if(capturedId)board.set(epSq,null)}}
                const mover=board.get(fromSq);board.set(fromSq,null);
                if(move.promo){board.set(move.dest,{type:move.promo,color,id:moverId});if(moverId){pieces[moverId].promoted=true;pieces[moverId].type=move.promo}}
                else board.set(move.dest,mover);
                if(moverId){pieces[moverId].sq=move.dest;pieces[moverId].moves.push({halfMove,moveNum,from:fromSq,to:move.dest,raw:str})}
            }
        }

        if(capturedId&&moverId){totalCaptures++;
            pieces[moverId].captures.push({halfMove,moveNum,victimId:capturedId,victimLabel:pieces[capturedId].label});
            pieces[capturedId].alive=false;pieces[capturedId].sq=null;pieces[capturedId].capturedBy=moverId;pieces[capturedId].capturedOnMove=moveNum;pieces[capturedId].capturedByLabel=pieces[moverId].label;
            events.push({type:'capture',moveNum,halfMove,raw:str,moverId,capturedId,moverLabel:pieces[moverId].label,victimLabel:pieces[capturedId].label,moverColor:pieces[moverId].color});
        }else if(moverId){events.push({type:'move',moveNum,halfMove,raw:str,moverId,moverLabel:pieces[moverId].label,moverColor:pieces[moverId].color,from:fromSq,to:toSq})}

        if(move.check&&moverId){pieces[moverId].checksGiven.push({halfMove,moveNum});events.push({type:move.mate?'checkmate':'check',moveNum,halfMove,moverId,moverLabel:pieces[moverId].label,moverColor:pieces[moverId].color});if(move.mate)pieces[moverId].deliversMate=true}
        if(move.promo&&moverId)events.push({type:'promotion',moveNum,halfMove,moverId,moverLabel:pieces[moverId].label,moverColor:pieces[moverId].color,promotedTo:move.promo});

        const enemyColor=color==='white'?'black':'white';const attacked=board.allAttacked(color);
        for(const[id,p]of Object.entries(pieces)){if(p.alive&&p.color===enemyColor&&p.sq&&attacked.has(p.sq)&&p.type!=='K')p.threats.push({halfMove,moveNum,byColor:color})}
        if(capturedId){const adjSqs=board.adjacentSquares(toSq||move.dest);for(const[id,p]of Object.entries(pieces)){if(p.alive&&p.sq&&id!==moverId&&id!==capturedId&&adjSqs.includes(p.sq))p.witnesses.push({halfMove,moveNum,event:`${pieces[capturedId].label} captured`})}}

        boardSnapshots.push(board.snapshot());
        timeline.push({moveNum,halfMove,color,raw:str,events});
        parsedForPlot.push({dest:toSq,color,check:move.check,mate:move.mate});
    });

    const totalMoves=Math.ceil(tokens.length/2);

    // Plot structure
    let conflictIdx=0;
    for(let i=0;i<parsedForPlot.length;i++){const m=parsedForPlot[i];if(!m.dest)continue;const rank=parseInt(m.dest[1]);if(m.color==='white'&&rank>=5){conflictIdx=i;break}if(m.color==='black'&&rank<=4){conflictIdx=i;break}}
    const mateIdx=parsedForPlot.findIndex(m=>m.mate);let climaxIdx;
    if(mateIdx>0){climaxIdx=mateIdx-1;for(let i=mateIdx-1;i>=0;i--){if(parsedForPlot[i].check){climaxIdx=i;break}}}
    else{climaxIdx=parsedForPlot.length-2;}
    const conclusionIdx=mateIdx>=0?mateIdx:parsedForPlot.length-1;
    if(climaxIdx<=conflictIdx){if(climaxIdx>=2)conflictIdx=Math.max(1,climaxIdx-Math.floor(climaxIdx/2));else{conflictIdx=0;climaxIdx=Math.max(1,climaxIdx)}}
    const plotStructure={conflictIdx,climaxIdx,conclusionIdx,conflictMove:Math.floor(conflictIdx/2)+1,climaxMove:Math.floor(climaxIdx/2)+1,conclusionMove:Math.floor(conclusionIdx/2)+1};

    return { pieces, timeline, boardSnapshots, plotStructure, gameResult, totalMoves, totalCaptures };
}

// ═══════════════════════════════════════
// BOOK 2 PGN
// ═══════════════════════════════════════
const BOOK2_PGN = '1. e4 e6 2. Bc4 c6 3. Nc3 b5 4. d3 bxc4 5. Nf3 cxd3 6. cxd3 d5 7. Ne5 dxe4 8. d4 Nd7 9. f3 f6 10. Nxc6 Qc7 11. Qa4 e5 12. Nd5 Qd6 13. Qb5 exf3 14. gxf3 a6 15. Qc4 Bb7 16. Ndb4 a5 17. Nd3 Bxc6 18. dxe5 fxe5 19. Qc3 Bxf3 20. Nf2 Bxh1 21. Nxh1 Qd4 22. Be3 Qh4+ 23. Ng3 Qxh2 24. O-O-O Qxg3 25. Qc6 Rb8 26. Qxd7# 1-0';

// ═══════════════════════════════════════
// CHARACTER MAPPING (from user spec)
// ═══════════════════════════════════════
const CHARACTER_MAP = {
    // WHITE SIDE
    'w_Q': {
        names: ['Ahdia Bacchus'],
        faction: 'gosquad',
        factionLabel: 'GO SQUAD',
        role: 'Temporalist / Strategic Coordinator',
        summary: 'Depressed hermit, early 20s. Time manipulation via Hyper Seed. Powers are killing her (18-24 months). TV-saturated voice. Secret power source for Go Squad. Delivers the final blow.',
        arc: 'Watchful restraint → surgical intervention → devastating checkmate',
        themes: ['worthiness', 'sacrifice', 'both/and thinking'],
        notes: 'Ahdia delivers checkmate (Qxd7#). She removes Prime Kain from the field — not kills, but definitively ends his operation. The queen\'s journey: patient positioning through the middle game, then explosive action in the endgame. Maps to Ahdia operating from the shadows until the moment demands she act.',
        removalNote: null,
        pawnCompanions: [],
        powers: 'Selective Time Bubbles, force amplification, selective slowing. Each use = cellular degradation. By endgame, she\'s burning through her remaining baseline.',
        isAhdia: true
    },
    'w_Nb': {
        names: ['Ruth Carter', 'Tess Whitford'],
        faction: 'gosquad',
        factionLabel: 'GO SQUAD',
        role: 'Field Leader + Gloom Girl (Paired Unit)',
        summary: 'Ruth: ER surgeon, Go Squad field leader, co-conspirator with Ahdia, grieving Firas. Tess: Police chief\'s daughter, depression, "teleportation" trigger. Together they\'re the team\'s mobile strike capability.',
        arc: 'Aggressive early engagement → deep penetration into enemy territory → removed from field at M24 (O-O-O)',
        themes: ['grief as fuel', 'systemic complicity', 'depression as shared bond'],
        notes: 'The c3 knight is one of White\'s most active pieces — 7 moves total, deep into Black\'s position. Ruth and Tess operate as a paired unit: Ruth leading, Tess providing the unpredictable edge. Removed at M24 (O-O-O, the castling move rearranges the back rank). NOT killed — incapacitated, captured, displaced. Their removal forces Ahdia to act alone.',
        removalNote: 'Removed M24 — incapacitated/captured during the O-O-O restructuring. Ruth and Tess are taken off the board but survive. Their absence is what makes Ahdia\'s solo checkmate both necessary and devastating.',
        pawnCompanions: [],
        powers: 'Ruth: CR-7 medical expertise, field surgery. Tess: apparent teleportation (Ahdia-powered), Sertraline-managed depression, middle-finger trigger.'
    },
    'w_Ra': {
        names: ['Director Harriet Bourn', 'Dr. Shiba Ryu'],
        faction: 'cadens',
        factionLabel: 'CADENS',
        role: 'CADENS Command (Overseer + FAERIS Specialist)',
        summary: 'Bourn: Late 50s-60s, decades of pragmatic command, potential redemption arc. Ryu: Mid-late 20s, nervous rambler, FAERIS drone operator, Ahdia\'s handler and impossible love interest. Together they represent institutional support.',
        arc: 'Single defensive move (M24 castling) → static institutional presence',
        themes: ['institutional burden', 'love across impossible forms', 'necessary evil'],
        notes: 'The a1 rook only moves once — during O-O-O castling at M24, sliding to d1. This is the institutional machinery repositioning: CADENS restructuring its defenses. Bourn and Ryu are the infrastructure Ahdia relies on but rarely sees move. Their one move enables everything that follows.',
        removalNote: null,
        pawnCompanions: ['w_Pd', 'w_Pc'],
        pawnNotes: 'd-pawn and c-pawn companions: the bureaucratic pawns that get consumed opening lines for others. CADENS resources spent to create operational space.',
        powers: 'Bourn: CADENS institutional authority, intelligence network. Ryu: FAERIS drone operation, AR-Ryu HUD, temporal shear monitoring.'
    },
    'w_Bf': {
        names: ['Leah Turner / Battlea', 'Victor Hernandez (early)'],
        faction: 'gosquad',
        factionLabel: 'GO SQUAD',
        role: 'Emotional Heart + Systems Thinker (Early Pairing)',
        summary: 'Leah: Mid-late 20s, barista/roller derby, anger channeled productively, MMA purple belt. Victor: 30s, community center director, wife murdered, strategic thinker. They begin paired — Leah as the visible fighter, Victor as the analytical backbone.',
        arc: 'Aggressive early deployment (M2 Bc4) → incapacitated M4 (bxc4) → Victor migrates to Ben\'s unit',
        themes: ['earned vs given strength', 'anger as love', 'grief channeled into systems'],
        notes: 'The f1 bishop deploys early (Bc4, move 2) and is captured at move 4 (bxc4). Leah charges in — and gets taken out almost immediately. This is NOT death. Leah is incapacitated, injured, sidelined. Her early removal is devastating because she\'s the team\'s emotional heart. Victor, her analytical partner, survives by migrating to Ben\'s unit after M4.',
        removalNote: 'Leah incapacitated M4 — too early, too fast. She never sees the middle game. The team loses its emotional center and has to reconfigure. Victor carries the grief of watching his partner fall and channels it into the longer fight.',
        pawnCompanions: ['w_Pe'],
        pawnNotes: 'e-pawn companion: the central pawn that opens the game (1. e4). Leah\'s opening salvo — aggressive, center-seeking, ultimately sacrificed to create space.',
        victorMigration: 'Victor leaves Leah\'s unit at M4 and joins Ben (w_Bc) for the remainder of the game. His arc splits: grief for Leah\'s fall → adaptation → quiet survival with Ben\'s unit.'
    },
    'w_Bc': {
        names: ['Ben Bukowski / Night Knight', 'Victor Hernandez (late)'],
        faction: 'gosquad',
        factionLabel: 'GO SQUAD',
        role: 'Discipline Core + Migrated Strategist',
        summary: 'Ben: Late 20s-early 30s, ex-Marine, PTSD, personal trainer. Military discipline keeps him steady. Victor joins after M4, bringing analytical capability to Ben\'s unit. Together they represent the team\'s stable backbone.',
        arc: 'Patient reserve → single critical move M22 (Be3) → survives the endgame',
        themes: ['institutional faith shattered', 'military identity', 'systems thinking applied to survival'],
        notes: 'The c1 bishop waits. And waits. Then makes one move at M22 (Be3) — a critical defensive/offensive repositioning that protects the king and enables the endgame. Ben is the Marine who holds position until the moment demands action. Victor, arriving after M4, provides the analytical framework for knowing WHEN to move. Their single move matters enormously.',
        removalNote: null,
        pawnCompanions: ['w_Pf', 'w_Pg'],
        pawnNotes: 'f-pawn and g-pawn companions: the kingside pawns that advance and get consumed (f3, gxf3). Ben\'s resources — disciplined, deployed methodically, ultimately spent. The g-pawn\'s capture (gxf3) at M14 recaptures material but opens the king position, a calculated risk.',
        victorArrival: 'Victor arrives at M4 after Leah\'s incapacitation. He carries grief but converts it into analytical support for Ben\'s patient defensive posture.'
    },
    // BLACK SIDE
    'b_Q': {
        names: ['Bellatrix / Naima Bacchus'],
        faction: 'cosmic',
        factionLabel: 'COSMIC',
        role: 'Conclave Designate / Rogue Operative',
        summary: 'Type IV civilization being. Ahdia\'s mother AND consciousness source. Locked in higher dimension. 3.7 billion years of accumulated grief across universe cycles. Tragic perfectionist.',
        arc: 'Aggressive accumulation → devastating material advantage → checkmate despite holding everything',
        themes: ['perfection as destruction', 'love as infection', 'cosmic loneliness', 'material advantage means nothing'],
        notes: 'The Black Queen is the most active black piece — multiple moves, captures, deep raids. Bellatrix accumulates +19 material advantage (capturing White pieces, consuming resources). She takes EVERYTHING. And still loses. The checkmate comes while she holds overwhelming material superiority. This IS Bellatrix: she\'s been winning for 3.7 billion years and it never saves her.',
        removalNote: null,
        pawnCompanions: ['b_Pe', 'b_Pc', 'b_Pb', 'b_Pd', 'b_Pf'],
        pawnNotes: 'Seven black pawn companions (e6, c6, b5, bxc4, d5, dxe4, exf3) — Bellatrix\'s expendable resources. Each pawn advance gains material but weakens the position structurally. The pawns ARE the "winning" that creates the losing. Every captured white piece = another brick in a fortress with no roof.',
        powers: 'Omega-level consciousness, clone avatars, dimensional manipulation. Can project through Geneva Windrow avatar.'
    },
    'b_Bc': {
        names: ['Kain Clone'],
        faction: 'triomf',
        factionLabel: 'TRIOMF',
        role: 'Clone Body Operative / Campaign Front',
        summary: 'One of Harding Kain\'s clone bodies. The public-facing version running for president. Clone consciousness transfer makes him effectively immortal — but each body is disposable.',
        arc: '4 moves, 3 kills → removed from field M21 (Nxh1 captures)',
        themes: ['truth vs power', 'disposable identity', 'institutional immunity'],
        notes: 'The c8 bishop (Bb7, Bxc6, Bxf3, Bxh1) is a killing machine — 4 moves, 3 captures. It strips White\'s position of key defenders. This is the Kain Clone\'s political operation: systematic elimination of obstacles. The 3 kills are institutional captures — taking out White\'s infrastructure (pawns, rook). Removed at M21, but it doesn\'t matter. The damage is done. And Prime Kain is still on the board.',
        removalNote: 'Clone body removed M21 — disposed of, replaced. The Kain Clone served its purpose: 3 kills, maximum damage, then discarded. This is how clone immortality works. The body doesn\'t matter. The campaign continues through Prime Kain.',
        pawnCompanions: [],
        powers: 'Clone consciousness transfer, political machinery, TRIOMF resources. Expendable by design.'
    },
    'b_Nb': {
        names: ['Prime Kain'],
        faction: 'triomf',
        factionLabel: 'TRIOMF',
        role: 'The Real Harding Kain / True Consciousness',
        summary: 'The original Kain consciousness. Presidential candidate, crime boss, TRIOMF leader. Unlike the clone, THIS is the one that matters. His removal ends the operation.',
        arc: 'Single move (Nd7) → static presence → removed M26 by Ahdia\'s checkmate (Qxd7#)',
        themes: ['authoritarianism', 'power behind the throne', 'the real target'],
        notes: 'The d7 knight barely moves — 1 move total (Nd7, M8). It sits. It doesn\'t need to act because the Clone and Bellatrix\'s pawns do the work. Prime Kain is the power behind the operation, not the operator. He is the checkmate target: Qxd7# — Ahdia captures the knight on d7. Not the queen, not the active pieces. The quiet one. The one who thought he was safe because others did the fighting.',
        removalNote: 'REMOVED M26 by Ahdia — Qxd7# is checkmate. Ahdia\'s queen captures Prime Kain\'s knight, simultaneously delivering checkmate to the Black King. This is the surgical strike: bypass Bellatrix\'s overwhelming force, ignore the material advantage, and remove the actual power center.',
        pawnCompanions: ['b_Pf'],
        pawnNotes: 'f-pawn companion (f6): Prime Kain\'s single defensive resource, deployed early to shore up the center. The f-pawn\'s advance weakens Black\'s kingside — a structural flaw that enables the eventual checkmate.',
        powers: 'Clone immortality (but THIS body is the real one), political empire, TRIOMF command.'
    },
    'b_Ra': {
        names: ['Eidolon'],
        faction: 'cosmic',
        factionLabel: 'COSMIC',
        role: 'Fear-Amplification Entity / Bellatrix\'s Lieutenant',
        summary: 'Dimensional entity that amplifies and distorts fear responses. Doesn\'t create fear — exploits what\'s already there. Primary function: ensure Kain wins by amplifying voter fears toward authoritarianism.',
        arc: 'Pawn-assisted positioning → fatal overreach at Rb8?? → enables the checkmate',
        themes: ['fear as weapon', 'amplification not creation', 'overreach'],
        notes: 'The a8 rook stays quiet, assisted by the a-pawn advances (a6, a5). Then makes one move: Rb8 — and it\'s the FATAL BLUNDER. Rb8?? is what allows Qc6 followed by Qxd7#. Eidolon\'s single action — its attempt to project force — is what creates the opening for Ahdia\'s checkmate. The fear entity overreaches, and in doing so, exposes Prime Kain.',
        removalNote: 'Not captured — but Rb8?? is the fatal miscalculation. Eidolon survives the game but its action destroys its own side. The fear amplifier creates the exact conditions for its master\'s defeat.',
        pawnCompanions: ['b_Pa'],
        pawnNotes: 'a-pawn companions (a6, a5): Eidolon\'s slow preparation. The fear builds incrementally — small advances that seem defensive but create the conditions for the fatal Rb8.',
        powers: 'Emotion amplification (fear, anger). Exploits existing anxieties. Cannot create from nothing — only distort and amplify.'
    }
};

// Unassigned pieces notation
const UNASSIGNED = {
    'w_Ng': { note: 'White Knight g1 → f3 → e5 → Nxc6 — 3 moves, 1 capture, removed M17 (Bxc6). Active early, penetrates deep, eliminated mid-game. A resource spent opening lines for the main operation.' },
    'w_Rh': { note: 'White Rook h1 — zero moves, captured M20 (Bxh1). Never gets to act. The Kain Clone\'s bishop strips this resource before it can contribute. Infrastructure destroyed before deployment.' },
    'b_Ng': { note: 'Black Knight g8 — zero moves, no character. Inert piece, never enters the game.' },
    'b_Bf': { note: 'Black Bishop f8 — zero moves, no character. Blocked by its own pawns, never deploys.' },
    'b_Rh': { note: 'Black Rook h8 — zero moves, no character. Trapped behind the kingside pawns.' }
};

// ═══════════════════════════════════════
// RUN ANALYSIS
// ═══════════════════════════════════════
const data = analyzeGame(BOOK2_PGN);
const { pieces, timeline, boardSnapshots, plotStructure, gameResult, totalMoves, totalCaptures } = data;

// Log analysis summary
console.log(`\n=== Book 2 Analysis ===`);
console.log(`Moves: ${totalMoves} | Captures: ${totalCaptures} | Result: ${gameResult}`);
console.log(`Plot: Conflict M${plotStructure.conflictMove} | Climax M${plotStructure.climaxMove} | Resolution M${plotStructure.conclusionMove}`);
console.log('');

// Log piece summaries
for (const [id, p] of Object.entries(pieces)) {
    if (p.isPawn) continue;
    const status = p.deliversMate ? 'CHECKMATE' : p.alive ? 'survives' : `removed M${p.capturedOnMove}`;
    const mapped = CHARACTER_MAP[id] ? CHARACTER_MAP[id].names.join(' + ') : (UNASSIGNED[id] ? 'unassigned' : '');
    console.log(`  ${p.label.padEnd(22)} ${p.moves.length}mv ${p.captures.length}k ${p.threats.length}th ${status.padEnd(14)} → ${mapped}`);
}

// Also log pawns briefly
console.log('\nPawns:');
for (const [id, p] of Object.entries(pieces)) {
    if (!p.isPawn) continue;
    const status = p.alive ? 'alive' : `cap M${p.capturedOnMove}`;
    console.log(`  ${p.label.padEnd(22)} ${p.moves.length}mv ${status}`);
}

// ═══════════════════════════════════════
// SVG GENERATORS
// ═══════════════════════════════════════
function renderTrailSVG(p, sz) {
    const sq=sz/8;
    const ac=p.color==='white'?'#58a6ff':'#f0883e';
    const ad=p.color==='white'?'rgba(88,166,255,.3)':'rgba(240,136,62,.3)';
    let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${sz}" height="${sz}" viewBox="0 0 ${sz} ${sz}" style="border-radius:6px;border:1px solid #2a3040">`;
    for(let r=7;r>=0;r--)for(let f=0;f<8;f++){const x=f*sq,y=(7-r)*sq;s+=`<rect x="${x}" y="${y}" width="${sq}" height="${sq}" fill="${(f+r)%2===0?'#1a2230':'#222d3a'}"/>`;}
    const path=[{sq:p.startSq,type:'start'}];
    p.moves.forEach(m=>{if(m.to){const isCap=p.captures.some(c=>c.halfMove===m.halfMove);path.push({sq:m.to,type:isCap?'capture':'move'})}});
    if(!p.alive&&p.moves.length>0)path.push({sq:p.moves[p.moves.length-1].to,type:'death'});
    for(let i=1;i<path.length;i++){const[f1,r1]=[path[i-1].sq.charCodeAt(0)-97,parseInt(path[i-1].sq[1])-1];const[f2,r2]=[path[i].sq.charCodeAt(0)-97,parseInt(path[i].sq[1])-1];s+=`<line x1="${f1*sq+sq/2}" y1="${(7-r1)*sq+sq/2}" x2="${f2*sq+sq/2}" y2="${(7-r2)*sq+sq/2}" stroke="${ad}" stroke-width="2" stroke-dasharray="4,3"/>`;}
    path.forEach((pt,i)=>{const[f,r]=[pt.sq.charCodeAt(0)-97,parseInt(pt.sq[1])-1];const x=f*sq+sq/2,y=(7-r)*sq+sq/2;
        if(pt.type==='start')s+=`<circle cx="${x}" cy="${y}" r="${sq*.3}" fill="${ac}" opacity=".9"/><text x="${x}" y="${y+1}" text-anchor="middle" dominant-baseline="middle" font-size="${sq*.35}" fill="#0e1117" font-weight="bold">S</text>`;
        else if(pt.type==='capture')s+=`<circle cx="${x}" cy="${y}" r="${sq*.25}" fill="#f85149" opacity=".8"/><text x="${x}" y="${y+1}" text-anchor="middle" dominant-baseline="middle" font-size="${sq*.3}" fill="white" font-weight="bold">${i}</text>`;
        else if(pt.type==='death'){s+=`<line x1="${x-sq*.2}" y1="${y-sq*.2}" x2="${x+sq*.2}" y2="${y+sq*.2}" stroke="#f85149" stroke-width="2.5"/>`;s+=`<line x1="${x+sq*.2}" y1="${y-sq*.2}" x2="${x-sq*.2}" y2="${y+sq*.2}" stroke="#f85149" stroke-width="2.5"/>`;}
        else s+=`<circle cx="${x}" cy="${y}" r="${sq*.2}" fill="${ac}" opacity=".6"/><text x="${x}" y="${y+1}" text-anchor="middle" dominant-baseline="middle" font-size="${sq*.28}" fill="white">${i}</text>`;
    });
    for(let f=0;f<8;f++)s+=`<text x="${f*sq+sq/2}" y="${sz-2}" text-anchor="middle" font-size="${sq*.28}" fill="#484f58">${String.fromCharCode(97+f)}</text>`;
    for(let r=0;r<8;r++)s+=`<text x="3" y="${(7-r)*sq+sq/2+sq*.08}" font-size="${sq*.28}" fill="#484f58">${r+1}</text>`;
    s+='</svg>';return s;
}

function renderBoardSVG(bs, highlights, sz) {
    const sq=sz/8;const pc={white:{K:'♔',Q:'♕',R:'♖',B:'♗',N:'♘',P:'♙'},black:{K:'♚',Q:'♛',R:'♜',B:'♝',N:'♞',P:'♟'}};
    let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${sz}" height="${sz}" viewBox="0 0 ${sz} ${sz}" style="border-radius:4px;border:1px solid #2a3040">`;
    for(let r=7;r>=0;r--)for(let f=0;f<8;f++){const x=f*sq,y=(7-r)*sq;const sn=String.fromCharCode(97+f)+(r+1);let fl=(f+r)%2===0?'#1a2230':'#2a3444';if(highlights[sn])fl=highlights[sn];s+=`<rect x="${x}" y="${y}" width="${sq}" height="${sq}" fill="${fl}"/>`;const p=bs[r][f];if(p){const ch=pc[p.color]?.[p.type]||'?';const tc=highlights[sn]?(p.color==='white'?'#fff':'#ffd0a0'):(p.color==='white'?'#e2e6ed':'#a0a8b4');s+=`<text x="${x+sq/2}" y="${y+sq/2+sq*.12}" text-anchor="middle" dominant-baseline="middle" font-size="${sq*.7}" fill="${tc}" style="text-shadow:0 1px 2px rgba(0,0,0,.6)">${ch}</text>`}}
    for(let f=0;f<8;f++)s+=`<text x="${f*sq+sq/2}" y="${sz-2}" text-anchor="middle" font-size="${sq*.3}" fill="#484f58">${String.fromCharCode(97+f)}</text>`;
    for(let r=0;r<8;r++)s+=`<text x="3" y="${(7-r)*sq+sq/2+sq*.1}" font-size="${sq*.3}" fill="#484f58">${r+1}</text>`;
    s+='</svg>';return s;
}

// ═══════════════════════════════════════
// HELPER: resolve character name for piece
// ═══════════════════════════════════════
function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}

function charNameFor(pieceId) {
    const mapping = CHARACTER_MAP[pieceId];
    if (mapping) return mapping.names.join(' + ');
    return pieces[pieceId]?.label || pieceId;
}

function getPhase(halfMoveIdx){
    if(halfMoveIdx<=plotStructure.conflictIdx)return'expo';
    if(halfMoveIdx===plotStructure.conflictIdx+1||halfMoveIdx===plotStructure.conflictIdx+2)return'conflict';
    if(halfMoveIdx<plotStructure.climaxIdx)return'rising';
    if(halfMoveIdx>=plotStructure.climaxIdx&&halfMoveIdx<=plotStructure.climaxIdx+1)return'climax';
    return'conclusion';
}

const PHASE_LABELS = {expo:'Exposition',conflict:'Inciting Incident',rising:'Rising Action',climax:'Climax',conclusion:'Resolution'};

const FACTION_CSS = {
    gosquad: { cls: 'faction-gosquad', label: 'GO SQUAD' },
    triomf: { cls: 'faction-triomf', label: 'TRIOMF' },
    cadens: { cls: 'faction-cadens', label: 'CADENS' },
    cosmic: { cls: 'faction-cosmic', label: 'COSMIC' },
    civilian: { cls: 'faction-civilian', label: 'CIVILIAN' }
};

const SERIES_THEMES = [
    { id: 'worthiness', label: 'You don\'t have to be fixed to be worthy' },
    { id: 'procrastination', label: 'Procrastination as cry for help, not laziness' },
    { id: 'bothand', label: 'Both/And thinking (DBT over CBT)' },
    { id: 'sacrifice', label: 'Sacrifice and what it costs' },
    { id: 'collective', label: 'Collective power over individual heroism' },
    { id: 'truth_vs_power', label: 'Truth doesn\'t defeat power automatically' },
    { id: 'systemic', label: 'Systemic evil vs personal evil' },
    { id: 'love_infection', label: 'Love as infection (Conclave perspective)' },
    { id: 'perfection_destruction', label: 'Perfection as destruction' },
    { id: 'help_strength', label: 'Asking for help is strength' },
    { id: 'progress_nonlinear', label: 'Progress isn\'t linear' }
];

// ═══════════════════════════════════════
// BUILD SCAFFOLD HTML
// ═══════════════════════════════════════
function buildScaffold() {
    let h = '';

    // ── HEADER SECTION ──
    h += `<div class="scaffold-section" style="border-left:3px solid var(--kill)">
<h3>Book 2 — Plot Structure</h3>
<div class="sf"><div class="sf-label">Game</div><div class="sf-val">${esc(BOOK2_PGN)}</div></div>
<div class="sf"><div class="sf-label">Result</div><div class="sf-val">${esc(gameResult)} — ${totalMoves} moves, ${totalCaptures} captures. Black accumulates +19 material advantage. White delivers checkmate anyway.</div></div>
<div class="sf"><div class="sf-label">Core Metaphor</div><div class="sf-val">Bellatrix takes everything. Ahdia takes the one thing that matters. Material advantage ≠ victory. Having more doesn't mean winning. Perfection doesn't mean survival.</div></div>
<div class="sf"><div class="sf-label">Key Rule</div><div class="sf-val" style="color:var(--kill)">CAPTURE = REMOVAL FROM FIELD, NOT DEATH. Could be incapacitation, imprisonment, displacement, forced retreat, political neutralization. Death is reserved for narrative weight, not chess mechanics.</div></div>
<div class="sf"><div class="sf-label">Inciting Incident (Move ${plotStructure.conflictMove})</div>
<div class="sf-prompt"><strong>Auerbach:</strong> What systemic crack first becomes visible? What does Ahdia notice from her rooftop that she can't un-see? The first piece crosses enemy territory — the conflict is no longer abstract.</div></div>
<div class="sf"><div class="sf-label">Climax (Move ${plotStructure.climaxMove})</div>
<div class="sf-prompt"><strong>Auerbach:</strong> Qh4+ — check. The moment Bellatrix's forces directly threaten the White King. Everything before was positioning. Now it's existential. What does each character lose that they can't get back? How does the time bubble degrade Ahdia?</div></div>
<div class="sf"><div class="sf-label">Resolution (Move ${plotStructure.conclusionMove})</div>
<div class="sf-prompt"><strong>Auerbach:</strong> Qxd7# — Ahdia captures Prime Kain, delivers checkmate. But Bellatrix still holds +19 material. The both/and: White wins the game AND is devastated. Victory AND loss simultaneously. Who survived? Who changed? What's left?</div></div>
</div>`;

    // ── THEME RESONANCE ──
    h += `<div class="scaffold-section">
<h3>Series Theme Resonance</h3>
<div class="sf"><div class="sf-label">Active Themes</div><div class="sf-val">`;
    SERIES_THEMES.forEach(t => { h += `• ${t.label}<br>`; });
    h += `</div></div>
<div class="sf"><div class="sf-label">Book 2 Specific</div><div class="sf-val">
• Material advantage = false security (Bellatrix's 3.7 billion years of "winning")<br>
• Capture ≠ death = removal can be worse than killing (displacement, imprisonment, political neutralization)<br>
• Solo checkmate after team removal = the cost of being the one who can't be captured<br>
• Victor's split arc = adaptation as survival, grief as fuel for reconfiguration<br>
• Eidolon's fatal blunder = fear overreaches and creates the opening for courage</div></div>
</div>`;

    // ── MAPPING OVERVIEW ──
    h += `<div class="scaffold-section">
<h3>Character Mapping Overview</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div>
<div class="sf"><div class="sf-label" style="color:var(--gosquad)">White Side</div><div class="sf-val">
♕ <strong>White Queen</strong> → Ahdia Bacchus (checkmate)<br>
♘ <strong>Knight c3</strong> → Ruth + Tess (7mv, removed M24)<br>
♖ <strong>Rook a1</strong> → Bourn + Ryu (1mv, d/c pawn companions)<br>
♗ <strong>Bishop f1</strong> → Leah + Victor-early (removed M4, e-pawn)<br>
♗ <strong>Bishop c1</strong> → Ben + Victor-late (1mv M22, f/g pawns, survives)
</div></div></div>
<div>
<div class="sf"><div class="sf-label" style="color:var(--triomf)">Black Side</div><div class="sf-val">
♛ <strong>Black Queen</strong> → Bellatrix (7 pawn companions)<br>
♝ <strong>Bishop c8</strong> → Kain Clone (4mv, 3 kills, removed M21)<br>
♞ <strong>Knight d7</strong> → Prime Kain (1mv, checkmate target M26)<br>
♜ <strong>Rook a8</strong> → Eidolon (fatal Rb8??, a-pawn companions)<br>
<span style="color:var(--text-dim)">♞ Knight g8, ♝ Bishop f8, ♜ Rook h8 — unassigned (0 moves)</span>
</div></div></div>
</div></div>`;

    // ── PER-CHARACTER SCAFFOLDS ──
    // White Side
    h += buildCharSection('w_Q');
    h += buildCharSection('w_Nb');
    h += buildCharSection('w_Bf');
    h += buildCharSection('w_Bc');
    h += buildCharSection('w_Ra');

    // Black Side
    h += buildCharSection('b_Q');
    h += buildCharSection('b_Bc');
    h += buildCharSection('b_Nb');
    h += buildCharSection('b_Ra');

    // ── UNASSIGNED ──
    h += `<div class="scaffold-section" style="border-left:3px solid var(--death)">
<h3>Unassigned Pieces (Zero Moves)</h3>
<p style="font-size:.85rem;color:var(--text-muted);margin-bottom:12px">These pieces never enter the game. They represent unrealized potential, blocked resources, or forces that simply don't participate.</p>`;
    for (const [id, info] of Object.entries(UNASSIGNED)) {
        const p = pieces[id];
        h += `<div class="sf"><div class="sf-label">${PIECE_ICONS[p.origType]?.[p.color]||'?'} ${p.label}</div><div class="sf-val">${info.note}</div></div>`;
    }
    h += `<div class="sf"><div class="sf-prompt"><strong>Narrative implication:</strong> Black has three major pieces that never move. The entire game is carried by the Queen, one Bishop, and one Knight — with Eidolon's single fatal move. This mirrors Kain's operation: a small core of actual operators, backed by massive inert infrastructure that looks impressive but contributes nothing.</div></div>
</div>`;

    // ── VICTOR'S SPLIT ARC ──
    h += `<div class="scaffold-section" style="border-left:3px solid var(--cadens)">
<h3>Victor Hernandez — Split Arc Scaffold</h3>
<div class="sf"><div class="sf-label">The Migration</div><div class="sf-val">
Victor begins paired with Leah on the f1 Bishop. When Leah is incapacitated at M4 (bxc4), Victor doesn't fall with her — he migrates to Ben's unit (c1 Bishop) and continues the fight from there.</div></div>
<div class="sf"><div class="sf-label">Phase 1: With Leah (M1–M4)</div><div class="sf-val">
• The analytical backbone to Leah's emotional fire<br>
• Deploys early with Leah (Bc4, M2) — aggressive positioning<br>
• Witnesses Leah's incapacitation at M4 — the moment everything changes<br>
• Must choose: fall with her or carry on</div></div>
<div class="sf"><div class="sf-label">Phase 2: With Ben (M4–End)</div><div class="sf-val">
• Arrives carrying grief for Leah's fall<br>
• Channels grief into analytical support for Ben's patient defensive posture<br>
• Helps Ben determine the timing for their single critical move at M22 (Be3)<br>
• Survives the endgame — but carries the weight of watching Leah fall AND watching from the sidelines while Ahdia delivers the final blow alone</div></div>
<div class="sf"><div class="sf-label">Writing Prompt</div>
<div class="sf-prompt"><strong>Victor's migration</strong> is the quiet tragedy of this game. The systems thinker watches his first partner fall, adapts, finds a new unit, contributes to one crucial moment — and then watches from the margins as someone else finishes the fight. He did everything right. He adapted. He survived. And he still feels like he didn't do enough.<br><br>
<strong>The both/and:</strong> Victor is both the person who saved Ben's unit by providing analysis AND the person who couldn't save Leah. Both are true. Neither cancels the other.</div></div>
</div>`;

    // ── PAWN COMPANION MASTER MAP ──
    h += `<div class="scaffold-section" style="border-left:3px solid var(--text-dim)">
<h3>Pawn Companion Map</h3>
<p style="font-size:.85rem;color:var(--text-muted);margin-bottom:12px">Pawn moves fold into parent character story beats. Each pawn advance represents a resource expenditure, an opening, or a sacrifice that serves the parent character's narrative.</p>`;

    const pawnMap = {};
    for (const [pieceId, mapping] of Object.entries(CHARACTER_MAP)) {
        if (mapping.pawnCompanions && mapping.pawnCompanions.length > 0) {
            mapping.pawnCompanions.forEach(pawnId => {
                pawnMap[pawnId] = { parent: mapping.names.join(' + '), parentPiece: pieceId, note: mapping.pawnNotes || '' };
            });
        }
    }

    for (const [pawnId, info] of Object.entries(pawnMap)) {
        const p = pieces[pawnId];
        if (!p) continue;
        const status = p.alive ? 'survives' : `captured M${p.capturedOnMove}`;
        const moveList = p.moves.map(m => `M${m.moveNum}: ${m.raw}`).join(', ');
        h += `<div class="sf"><div class="sf-label">${PIECE_ICONS.P[p.color]} ${p.label} → ${info.parent}</div>
<div class="sf-val">${p.moves.length} moves (${moveList || 'none'}) — ${status}</div></div>`;
    }
    h += `<div class="sf"><div class="sf-label">Pawn Narrative Notes</div><div class="sf-val">`;
    for (const [pieceId, mapping] of Object.entries(CHARACTER_MAP)) {
        if (mapping.pawnNotes) {
            h += `<strong>${mapping.names[0]}:</strong> ${mapping.pawnNotes}<br><br>`;
        }
    }
    h += `</div></div></div>`;

    // ── MOVE-BY-MOVE TIMELINE ──
    h += buildFullTimeline();

    return h;
}

// ═══════════════════════════════════════
// BUILD CHARACTER SECTION
// ═══════════════════════════════════════
function buildCharSection(pieceId) {
    const p = pieces[pieceId];
    const mapping = CHARACTER_MAP[pieceId];
    if (!p || !mapping) return '';

    const icon = PIECE_ICONS[p.origType]?.[p.color] || '?';
    const ac = p.color === 'white' ? 'var(--gosquad)' : 'var(--triomf)';
    const fInfo = FACTION_CSS[mapping.faction] || {};

    const fm = p.moves.length > 0 ? p.moves[0].moveNum : null;
    const lm = p.moves.length > 0 ? p.moves[p.moves.length - 1].moveNum : null;
    const entry = fm ? 'Move ' + fm : 'Never moves';
    const exit = p.deliversMate ? 'Delivers checkmate (Qxd7#)' : p.alive ? 'Survives' : `Removed M${p.capturedOnMove}`;

    const phases = new Set();
    p.moves.forEach(m => phases.add(getPhase(m.halfMove - 1)));
    const phaseLabels = [...phases].map(ph => PHASE_LABELS[ph] || ph);

    // Key moments
    const km = [];
    p.moves.forEach(m => {
        const cap = p.captures.find(c => c.halfMove === m.halfMove);
        if (cap) {
            km.push(`M${m.moveNum} ${m.raw}: Captures ${charNameFor(cap.victimId)} — REMOVAL from field`);
        } else {
            km.push(`M${m.moveNum} ${m.raw}: ${m.from} → ${m.to}`);
        }
    });
    p.checksGiven.forEach(c => km.push(`M${c.moveNum}: Gives CHECK`));
    if (p.deliversMate) km.push(`M${lm}: Delivers CHECKMATE (Qxd7#)`);
    if (!p.alive) km.push(`M${p.capturedOnMove}: REMOVED by ${charNameFor(p.capturedBy)}`);

    // Witnesses
    const witList = p.witnesses.map(w => `M${w.moveNum}: Witnessed ${w.event}`);

    // Pawn companions
    const pawnIds = mapping.pawnCompanions || [];
    const pawnPieces = pawnIds.map(pid => pieces[pid]).filter(Boolean);

    // Trail SVG
    const trail = renderTrailSVG(p, 240);

    // Pawn trails (smaller)
    const pawnTrails = pawnPieces.map(pp => ({
        label: pp.label,
        svg: renderTrailSVG(pp, 120),
        moves: pp.moves.length,
        status: pp.alive ? 'survives' : `captured M${pp.capturedOnMove}`
    }));

    let h = `<div class="scaffold-section" style="border-left:3px solid ${ac}">
<h3>${icon} <span style="color:${ac}">${mapping.names.join(' + ')}</span>
<span class="faction-tag ${fInfo.cls||''}">${fInfo.label||''}</span>
<span style="color:var(--text-dim);font-weight:400;font-size:.85rem;margin-left:8px">${PIECE_NAMES[p.origType]} (${p.startSq})</span></h3>`;

    // Identity
    h += `<div class="sf"><div class="sf-label">Role</div><div class="sf-val">${esc(mapping.role)}</div></div>`;
    h += `<div class="sf"><div class="sf-label">Identity</div><div class="sf-val">${esc(mapping.summary)}</div></div>`;
    h += `<div class="sf"><div class="sf-label">Arc</div><div class="sf-val">${esc(mapping.arc)}</div></div>`;

    // Journey trail
    h += `<div style="text-align:center;margin:12px 0">${trail}
<div style="font-size:.75rem;color:var(--text-dim);margin-top:6px"><span style="color:${ac}">● S</span> = Start &nbsp;<span style="color:${ac}">●</span> = Move &nbsp;<span style="color:var(--kill)">●</span> = Capture &nbsp;<span style="color:var(--kill)">✕</span> = Removed</div></div>`;

    // Chess arc
    h += `<div class="sf"><div class="sf-label">Chess Arc</div>
<div class="sf-val">
Entry: ${entry}<br>
Active: ${p.moves.length} moves ${p.moves.length>0?'(M'+fm+'–M'+lm+')':''}<br>
Exit: ${exit}<br>
Captures: ${p.captures.length}${p.captures.length>0?' — '+p.captures.map(c=>charNameFor(c.victimId)+' (M'+c.moveNum+')').join(', '):''}<br>
Threatened: ${p.threats.length} times<br>
Witnessed: ${p.witnesses.length} events<br>
Phases: ${phaseLabels.join(', ') || 'None'}
</div></div>`;

    // Key moments
    if (km.length) {
        h += `<div class="sf"><div class="sf-label">Move-by-Move</div><div class="sf-val">${km.join('<br>')}</div></div>`;
    }

    // Witnessed events
    if (witList.length) {
        h += `<div class="sf"><div class="sf-label">Witnessed Events</div><div class="sf-val">${witList.join('<br>')}</div></div>`;
    }

    // Removal note
    if (mapping.removalNote) {
        h += `<div class="sf"><div class="sf-label" style="color:var(--kill)">Removal</div><div class="sf-val">${esc(mapping.removalNote)}</div></div>`;
    }

    // Pawn companions
    if (pawnPieces.length > 0) {
        h += `<div class="sf"><div class="sf-label">Pawn Companions</div><div class="sf-val">`;
        pawnPieces.forEach(pp => {
            const status = pp.alive ? 'survives' : `captured M${pp.capturedOnMove}`;
            const moveList = pp.moves.map(m => `M${m.moveNum}: ${m.raw}`).join(', ');
            h += `${PIECE_ICONS.P[pp.color]} ${pp.label}: ${pp.moves.length} moves (${moveList||'none'}) — ${status}<br>`;
        });
        if (mapping.pawnNotes) h += `<br><em>${esc(mapping.pawnNotes)}</em>`;
        h += `</div></div>`;

        // Pawn trails
        if (pawnTrails.length > 0) {
            h += `<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0">`;
            pawnTrails.forEach(pt => {
                h += `<div style="text-align:center">${pt.svg}<div style="font-size:.7rem;color:var(--text-dim)">${pt.label}<br>${pt.moves}mv, ${pt.status}</div></div>`;
            });
            h += `</div>`;
        }
    }

    // Victor migration notes
    if (mapping.victorMigration) {
        h += `<div class="sf"><div class="sf-label" style="color:var(--cadens)">Victor Migration</div><div class="sf-val">${esc(mapping.victorMigration)}</div></div>`;
    }
    if (mapping.victorArrival) {
        h += `<div class="sf"><div class="sf-label" style="color:var(--cadens)">Victor Arrival</div><div class="sf-val">${esc(mapping.victorArrival)}</div></div>`;
    }

    // Powers
    if (mapping.powers) {
        h += `<div class="sf"><div class="sf-label">Powers / Resources</div><div class="sf-val">${esc(mapping.powers)}</div></div>`;
    }

    // Temporal cost (Ahdia only)
    if (mapping.isAhdia) {
        h += `<div class="sf"><div class="sf-label">Temporal Cost Tracking</div>
<div class="sf-val">${p.moves.length} time-bubble activations implied by piece movement. ${p.captures.length} high-intensity temporal event(s) (capture = force amplification).<br><br>
Cellular degradation map:<br>
• <strong>Early moves (Exposition):</strong> Minor nosebleeds. She can hide it. The team doesn't know yet.<br>
• <strong>Mid-game (Rising):</strong> Bleeding ears, muscle weakness, vision blurring. Ruth notices. Ryu's HUD data confirms.<br>
• <strong>Climax (M22–M25):</strong> Operating past safe thresholds. Each bubble costs exponentially more. The math says stop.<br>
• <strong>Checkmate (M26 Qxd7#):</strong> Whatever this costs, she pays it. The cellular baseline drops to near-transcendence levels. She is burning the boundary between human and something else.</div></div>`;
    }

    // Mapping notes
    h += `<div class="sf"><div class="sf-label">Mapping Notes</div><div class="sf-val">${esc(mapping.notes)}</div></div>`;

    // Themes
    if (mapping.themes && mapping.themes.length) {
        h += `<div class="sf"><div class="sf-label">Theme Resonance</div><div class="sf-val">${mapping.themes.map(t=>'• '+t).join('<br>')}</div></div>`;
    }

    // ── WRITING PROMPTS ──
    // Exposition prompt
    h += `<div class="sf"><div class="sf-label">Exposition Prompt</div>`;
    if (fm && fm <= plotStructure.conflictMove) {
        h += `<div class="sf-prompt"><strong>${mapping.names[0]}</strong> is active before the central conflict. Where are they when the first crack appears? What version of their normal life is about to shatter?`;
        if (mapping.isAhdia) h += `<br><br><strong>Voice check:</strong> What show is Ahdia watching when the call comes? What's the TV-reference frame she'd use to describe the situation she's walking into? Remember: she hasn't left the apartment mindset even when she's left the apartment.`;
        h += `</div>`;
    } else if (fm) {
        h += `<div class="sf-prompt"><strong>${mapping.names[0]}</strong> enters at M${fm} — the fight is already underway. What pulled them in? What do they see that the early arrivals have stopped noticing because they're too close?</div>`;
    } else {
        h += `<div class="sf-prompt"><strong>${mapping.names[0]}</strong> never makes a chess move — but that doesn't mean they're inactive. What are they doing off-board? What intelligence are they processing? What decision are they NOT making, and why?</div>`;
    }
    h += `</div>`;

    // Climax prompt
    h += `<div class="sf"><div class="sf-label">Climax Prompt</div>`;
    if (p.capturedOnMove && p.capturedOnMove < plotStructure.climaxMove) {
        h += `<div class="sf-prompt"><strong>${mapping.names[0]}</strong> is removed at M${p.capturedOnMove} — before the climax. They never see how it ends. What do they leave behind that the survivors carry? What would they think of the resolution if they could see it?<br><br>
<strong>Removal ≠ death.</strong> What does their removal actually look like? Incapacitation? Capture? Political neutralization? The form of removal shapes what comes after.</div>`;
    } else if (phases.has('climax')) {
        h += `<div class="sf-prompt"><strong>${mapping.names[0]}</strong> is in the decisive moment. What do they sacrifice? What's the both/and — what do they gain AND lose simultaneously?`;
        if (p.deliversMate) h += `<br><br><strong>Checkmate weight:</strong> This character ends it. Qxd7# — capturing Prime Kain, delivering checkmate. What does it cost? Not just the cellular degradation — what part of Ahdia does she burn to do this? And what does she become on the other side?`;
        h += `</div>`;
    } else {
        h += `<div class="sf-prompt"><strong>${mapping.names[0]}</strong> is alive during the climax but not at the center of the action. How do they experience the shockwave? What do they see from the edges that the central players can't see because they're too close?</div>`;
    }
    h += `</div>`;

    // Capture/violence prompt
    if (p.captures.length) {
        h += `<div class="sf"><div class="sf-label">Violence / Removal Prompt</div>
<div class="sf-prompt"><strong>${mapping.names[0]}</strong> removes ${p.captures.length} ${p.captures.length===1?'opponent':'opponents'} from the field. In this game, capture ≠ death — each removal needs its own narrative form.<br><br>`;
        p.captures.forEach(c => {
            const victimMapping = CHARACTER_MAP[c.victimId];
            const victimName = victimMapping ? victimMapping.names.join(' + ') : pieces[c.victimId]?.label || '?';
            h += `<strong>M${c.moveNum}:</strong> Removes ${victimName}. What form does this removal take? What does ${mapping.names[0]} feel about it?<br>`;
        });
        h += `</div></div>`;
    }

    // Threat prompt
    if (p.threats.length >= 3) {
        h += `<div class="sf"><div class="sf-label">Danger Prompt</div>
<div class="sf-prompt">Threatened ${p.threats.length} times throughout the game — constant danger. For ${mapping.names[0]}: does sustained threat confirm their worldview or shatter it? How does living under threat interact with their arc of "${esc(mapping.arc)}"?</div></div>`;
    }

    h += `</div>`;
    return h;
}

// ═══════════════════════════════════════
// FULL TIMELINE
// ═══════════════════════════════════════
function buildFullTimeline() {
    const mappedPieceIds = new Set(Object.keys(CHARACTER_MAP));
    // Also include pawn companions
    for (const mapping of Object.values(CHARACTER_MAP)) {
        if (mapping.pawnCompanions) mapping.pawnCompanions.forEach(pid => mappedPieceIds.add(pid));
    }

    let h = `<h2 style="font-family:'Playfair Display',serif;margin:30px 0 16px">Move-by-Move Timeline</h2>`;
    h += `<div class="legend">
<div class="legend-item"><div class="legend-dot" style="background:var(--gosquad)"></div> White</div>
<div class="legend-item"><div class="legend-dot" style="background:var(--triomf)"></div> Black</div>
<div class="legend-item"><div class="legend-dot" style="background:var(--kill)"></div> Capture/Removal</div>
<div class="legend-item"><div class="legend-dot" style="background:var(--cosmic)"></div> Overlap</div>
<div class="legend-item"><div class="legend-dot" style="background:var(--death)"></div> Witnessed</div>
</div>`;

    let curPh = '';
    const phLbl = ph => PHASE_LABELS[ph] || '';

    // Group by move number
    const moveGroups = {};
    timeline.forEach(tm => {
        if (!moveGroups[tm.moveNum]) moveGroups[tm.moveNum] = [];
        moveGroups[tm.moveNum].push(tm);
    });

    Object.keys(moveGroups).sort((a,b)=>a-b).forEach(mn => {
        const group = moveGroups[mn];
        const fh = group[0].halfMove;
        const ph = getPhase(fh - 1);

        if (ph !== curPh) {
            curPh = ph;
            const mr = ph==='expo'?'M1–'+plotStructure.conflictMove:ph==='conflict'?'M'+plotStructure.conflictMove:ph==='rising'?'M'+(plotStructure.conflictMove+1)+'–'+(plotStructure.climaxMove-1):ph==='climax'?'M'+plotStructure.climaxMove:'M'+(plotStructure.climaxMove+1)+'–'+plotStructure.conclusionMove;
            h += `<div class="ph-mark ph-${ph}">${phLbl(ph)} <span style="font-weight:400;font-size:.8rem;opacity:.7;margin-left:8px">${mr}</span></div>`;
        }

        // Board snapshot
        const lh = group[group.length-1].halfMove;
        const bs = boardSnapshots[lh];
        const hl = {};
        for (const id of mappedPieceIds) {
            const p = pieces[id];
            if (!p || (p.capturedOnMove && parseInt(mn) > p.capturedOnMove)) continue;
            let psq = p.startSq;
            for (const m of p.moves) { if (m.halfMove <= lh) psq = m.to; else break; }
            if (psq) hl[psq] = p.color==='white' ? 'rgba(88,166,255,.4)' : 'rgba(240,136,62,.4)';
        }
        const bsvg = renderBoardSVG(bs, hl, 200);
        const bid = 'b' + mn;

        h += `<div class="tl-move"><div class="tl-mn">M${mn}</div><div class="tl-mb">`;

        group.forEach(tm => {
            tm.events.forEach(ev => {
                // Determine if this event involves mapped pieces
                const moverMapped = ev.moverId && mappedPieceIds.has(ev.moverId);
                const capMapped = ev.capturedId && mappedPieceIds.has(ev.capturedId);
                if (!moverMapped && !capMapped && ev.type !== 'check' && ev.type !== 'checkmate') return;

                let ec = ev.moverColor==='white' ? 'ev-w' : 'ev-b';
                if (ev.type === 'capture') ec = 'ev-k';
                if (ev.capturedId && capMapped) ec += ' ev-d';
                if (moverMapped && capMapped) ec = 'ev-o';

                let ic = '→', tx = '';
                const moverName = charNameFor(ev.moverId);
                const victimName = ev.capturedId ? charNameFor(ev.capturedId) : '';

                if (ev.type === 'move') {
                    ic = '→'; tx = `<span class="pn">${moverName}</span> moves <span class="nt">${ev.raw}</span>`;
                } else if (ev.type === 'capture') {
                    ic = '⚔️';
                    if (capMapped) {
                        tx = `<span class="pn" style="color:var(--kill)">${victimName}</span> REMOVED by ${moverName} <span class="nt">${ev.raw}</span>`;
                    } else {
                        tx = `<span class="pn">${moverName}</span> removes ${victimName} <span class="nt">${ev.raw}</span>`;
                    }
                } else if (ev.type === 'check') {
                    ic = '⚡'; tx = `<span class="pn" style="color:var(--check)">${moverName}</span> gives CHECK`;
                } else if (ev.type === 'checkmate') {
                    ic = '👑'; tx = `<span class="pn" style="color:var(--promote)">${moverName}</span> delivers <strong>CHECKMATE</strong> — captures ${victimName}`;
                } else if (ev.type === 'promotion') {
                    ic = '⭐'; tx = `<span class="pn" style="color:var(--promote)">${moverName}</span> promotes to <strong>${PIECE_NAMES[ev.promotedTo]}</strong>`;
                }

                h += `<div class="tl-ev ${ec}"><span class="ti">${ic}</span><span>${tx}</span></div>`;
            });

            // Check for witnesses and threats among mapped pieces
            for (const id of mappedPieceIds) {
                const p = pieces[id];
                if (!p) continue;
                const wi = p.witnesses.find(w => w.halfMove === tm.halfMove);
                if (wi) {
                    h += `<div class="tl-ev ev-d"><span class="ti">👁</span><span><span class="pn">${charNameFor(id)}</span> <span class="dt">witnesses: ${wi.event}</span></span></div>`;
                }
            }
        });

        h += `<div class="board-tog" onclick="toggleBoard('${bid}')">▸ Show board</div><div class="board-box" id="${bid}">${bsvg}</div>`;
        h += `</div></div>`;
    });

    return h;
}

// ═══════════════════════════════════════
// ASSEMBLE FINAL HTML
// ═══════════════════════════════════════
const scaffoldContent = buildScaffold();

const finalHTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Go Squad · Book 2 Narrative Scaffold</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0e1117;--surface:#161b22;--surface2:#1c2333;--border:#2a3040;--text:#e2e6ed;--text-muted:#7d8590;--text-dim:#484f58;--gosquad:#58a6ff;--gosquad-light:rgba(88,166,255,0.1);--triomf:#f0883e;--triomf-light:rgba(240,136,62,0.1);--cadens:#d2a8ff;--cadens-light:rgba(210,168,255,0.1);--cosmic:#f0e050;--cosmic-light:rgba(240,224,80,0.12);--kill:#f85149;--kill-light:rgba(248,81,73,0.1);--death:#8b949e;--check:#d2a8ff;--promote:#3fb950;--white-accent:#58a6ff;--white-light:rgba(88,166,255,0.1);--black-accent:#f0883e;--black-light:rgba(240,136,62,0.1)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Source Sans 3',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
header{text-align:center;padding:30px 20px 10px;border-bottom:1px solid var(--border)}
header h1{font-family:'Playfair Display',serif;font-size:clamp(1.4rem,3.5vw,2rem);font-weight:900;background:linear-gradient(135deg,var(--gosquad),var(--triomf));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.container{max-width:1100px;margin:0 auto;padding:0 20px 60px}
.scaffold-section{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin-bottom:16px}
.scaffold-section h3{font-family:'Playfair Display',serif;font-size:1.05rem;margin-bottom:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.sf{margin-bottom:12px;font-size:.9rem}
.sf-label{font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.5px;color:var(--text-muted);margin-bottom:2px}
.sf-val{color:var(--text);line-height:1.6}
.sf-prompt{border:1.5px dashed var(--border);border-radius:6px;padding:12px 16px;margin-top:6px;color:var(--text-dim);font-style:italic;font-size:.85rem;min-height:40px;line-height:1.6}
.sf-prompt strong{color:var(--text-muted);font-style:normal}
.faction-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.faction-gosquad{background:var(--gosquad-light);color:var(--gosquad)}
.faction-triomf{background:var(--triomf-light);color:var(--triomf)}
.faction-cadens{background:var(--cadens-light);color:var(--cadens)}
.faction-cosmic{background:var(--cosmic-light);color:var(--cosmic)}
.faction-civilian{background:rgba(139,148,158,.15);color:var(--death)}
.tl-move{display:flex;gap:14px;padding:12px 0;border-bottom:1px solid rgba(42,48,64,.5)}.tl-move:last-child{border-bottom:none}
.tl-mn{width:50px;flex-shrink:0;font-family:monospace;font-size:.8rem;color:var(--text-dim);padding-top:3px;text-align:right}.tl-mb{flex:1}
.tl-ev{display:flex;align-items:flex-start;gap:10px;padding:6px 10px;border-radius:6px;margin-bottom:4px;font-size:.9rem;line-height:1.5}
.tl-ev .ti{font-size:.85rem;flex-shrink:0;margin-top:2px}.tl-ev .pn{font-weight:700}.tl-ev .nt{font-family:monospace;color:var(--text-dim);font-size:.8rem}.tl-ev .dt{color:var(--text-muted)}
.ev-w{background:var(--white-light)}.ev-w .pn{color:var(--white-accent)}.ev-b{background:var(--black-light)}.ev-b .pn{color:var(--black-accent)}
.ev-k{background:var(--kill-light)}.ev-o{background:var(--cosmic-light);border:1px solid rgba(240,224,80,.25)}.ev-d{background:rgba(139,148,158,.08);border-left:3px solid var(--death)}
.ph-mark{padding:10px 16px;margin:20px 0 10px;font-family:'Playfair Display',serif;font-weight:700;font-size:.95rem;border-radius:6px;border-left:4px solid}
.ph-expo{border-color:var(--white-accent);color:var(--white-accent);background:rgba(88,166,255,.06)}
.ph-conflict{border-color:var(--black-accent);color:var(--black-accent);background:rgba(240,136,62,.06)}
.ph-rising{border-color:var(--check);color:var(--check);background:rgba(210,168,255,.06)}
.ph-climax{border-color:var(--kill);color:var(--kill);background:rgba(248,81,73,.06)}
.ph-conclusion{border-color:var(--promote);color:var(--promote);background:rgba(63,185,80,.06)}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:16px;font-size:.8rem;color:var(--text-muted)}.legend-item{display:flex;align-items:center;gap:5px}.legend-dot{width:10px;height:10px;border-radius:3px}
.board-tog{font-size:.75rem;color:var(--text-dim);cursor:pointer;margin-top:4px;display:inline-block;padding:2px 8px;border-radius:4px;border:1px solid var(--border)}.board-tog:hover{color:var(--text-muted);border-color:var(--text-muted)}
.board-box{margin-top:8px;display:none}.board-box.open{display:block}
@media print{body{background:#fff;color:#222}header{border-color:#ccc}.scaffold-section{border-color:#ccc;background:#fafafa}.tl-ev{background:#f5f5f5!important;border:1px solid #ddd;color:#222}.board-box{display:block!important}.ph-mark{background:#f0f0f0!important;color:#333!important}}
</style>
</head>
<body>
<header>
<h1>Go Squad · Book 2 Narrative Scaffold</h1>
<div style="color:#7d8590;font-size:.9rem;margin-top:4px">Generated ${new Date().toISOString().slice(0,10)} · ${totalMoves} moves · ${gameResult} · Chess is scaffolding, not the building</div>
</header>
<div class="container" style="margin-top:20px">
${scaffoldContent}
</div>
<script>
function toggleBoard(id){const el=document.getElementById(id);if(!el)return;const o=el.classList.toggle('open');el.previousElementSibling.textContent=o?'\\u25BE Hide board':'\\u25B8 Show board'}
</script>
</body>
</html>`;

// ═══════════════════════════════════════
// WRITE OUTPUT
// ═══════════════════════════════════════
const outPath = path.join(__dirname, '..', 'reference', 'book2_scaffold.html');
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, finalHTML, 'utf8');
console.log(`\n✅ Scaffold written to: ${outPath}`);
console.log(`   File size: ${(fs.statSync(outPath).size / 1024).toFixed(1)} KB`);
