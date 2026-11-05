/* Website-owned renderer. Public upstream JSON is the only research source. */
(() => {
  'use strict';
  const REPO = 'prp-protocol/prp-comparative-analysis';
  const API = 'https://api.github.com/repos/' + REPO + '/commits/main';
  const RAW = 'https://raw.githubusercontent.com/' + REPO + '/';
  const INTERVAL = 300000;
  const retired = new Set(['C08','F25','F35','L02','F38','F19','K02']);
  const labels = {Y:'Yes',N:'No','?':'Pending'};
  const levels = ['assumed','reported','documented','demonstrated'];
  const assert = (v,m) => {if (!v) throw Error(m);};
  const text = v => typeof v === 'string';
  const esc = v => String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeURL = v => {try {const u=new URL(v); return ['https:','http:'].includes(u.protocol)&&!u.username&&!u.password&&!['localhost','127.0.0.1','201.130.81.10'].includes(u.hostname);}catch{return false;}};
  const keys = (v,ks) => v && typeof v==='object' && !Array.isArray(v) && Object.keys(v).sort().join('|')===ks.split(' ').sort().join('|');
  async function digest(bytes) {return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');}
  function validate(d,record,config) {
    assert(keys(d,'schema_version revision date language scope criteria columns cells marks evidence_policy') && d.schema_version===2 && d.language==='en','Unsupported comparison schema');
    assert(text(d.revision)&&d.revision===record.revision&&/^\d{4}-\d\d-\d\d$/.test(d.date)&&text(d.scope),'Invalid revision/date/scope');
    const walk=v=>{if(text(v))assert(!/\/workspace\/|\/opt\/agentmux\/|\/home\/|\/tmp\/|201\.130\.81\.10|\/preview\//.test(v),'Private content rejected');else if(v&&typeof v==='object')Object.values(v).forEach(walk);};walk(d);
    const rows=(name,pattern,fields)=>{assert(Array.isArray(d[name])&&d[name].length>0&&d[name].length<20000,'Invalid '+name);const map=new Map();for(const r of d[name]){assert(r&&pattern.test(r.id)&&!map.has(r.id)&&fields.every(k=>text(r[k])),'Invalid/duplicate '+name+' record');map.set(r.id,r);}return map;};
    const criteria=rows('criteria',/^[A-Z][0-9]+$/,['title','definition','method','research_action']);
    const columns=rows('columns',/^[A-Z][A-Z0-9]*$/,['title','profile','website']);
    const cells=rows('cells',/^[A-Z][0-9]+-[A-Z][A-Z0-9]*$/,['feature','stack','status','reason','method','source_label','qualification']);
    assert([...criteria.keys()].every(id=>!retired.has(id)),'Retired criterion rejected');
    assert(cells.size===criteria.size*columns.size&&cells.size===record.cells,'Incomplete grid');
    const p=d.evidence_policy;
    assert(keys(p,'version levels unclassified interpretation display_rule')&&p.version===1&&keys(p.levels,levels.join(' ')),'Invalid evidence policy');
    for(const l of levels)assert(keys(p.levels[l],'label definition')&&p.levels[l].label===l[0].toUpperCase()+l.slice(1)&&text(p.levels[l].definition)&&p.levels[l].definition.trim(),'Invalid evidence level');
    for(const k of ['unclassified','interpretation','display_rule'])assert(text(p[k])&&p[k].trim(),'Missing evidence policy text');
    for(const c of columns.values())assert(safeURL(c.website)&&(c.logo===null||(text(c.logo)&&Object.hasOwn(config.assets,'logos/'+c.logo))),'Invalid project URL or unavailable logo');
    const counts={Yes:0,No:0,Pending:0};
    for(const c of cells.values()) {
      assert(criteria.has(c.feature)&&columns.has(c.stack)&&c.id===c.feature+'-'+c.stack&&Object.hasOwn(labels,c.status),'Invalid cell identity/verdict');
      assert(Array.isArray(c.sources)&&c.sources.every(safeURL)&&Array.isArray(c.editorial_references)&&c.editorial_references.every(text),'Invalid cell references');
      const e=c.evidence;assert(keys(e,'level basis scope attribution coverage reviewed_at basis_sha256 references')&&levels.includes(e.level),'Invalid evidence annotation');
      for(const k of ['basis','scope','attribution','coverage','reviewed_at','basis_sha256'])assert(text(e[k])&&e[k].trim(),'Missing evidence '+k);
      assert(/^[a-f0-9]{64}$/.test(e.basis_sha256)&&/^\d{4}-\d\d-\d\d$/.test(e.reviewed_at)&&Array.isArray(e.references)&&e.references.every(v=>text(v)&&v.trim()),'Invalid evidence fingerprint/references');
      counts[labels[c.status]]++;
    }
    assert(keys(record.counts,'Yes No Pending')&&Object.keys(counts).every(k=>counts[k]===record.counts[k]),'Count mismatch');
    assert(Array.isArray(d.marks),'Missing credits');
    for(const m of d.marks){const a=config.assets[m.file];assert(a,'Unknown asset');if(m.sha256)assert(m.sha256===a.sha256,'Changed asset hash');if(m.bytes!==undefined)assert(m.bytes===a.bytes,'Changed asset size');for(const k of ['source','license_url'])if(m[k])assert(text(m[k])&&(k==='source'&&!/^[a-z]+:/i.test(m[k])||safeURL(m[k])),'Invalid credit link');}
    return {d,criteria,columns,cells,counts};
  }
  async function acquire(config,request=fetch,previous=null) {
    async function bytes(url,max) {const r=await request(url,{credentials:'omit',cache:'no-cache',referrerPolicy:'no-referrer',signal:AbortSignal.timeout(45000)});assert(r.ok,'Upstream HTTP '+r.status);const b=await r.arrayBuffer();assert(b.byteLength<=max,'Upstream size limit');return new Uint8Array(b);}
    const decode=b=>JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(b));
    const head=decode(await bytes(API,2000000));assert(/^[a-f0-9]{40}$/.test(head.sha),'Invalid source commit');
    if(previous?.commit===head.sha)return {...previous,verifiedAt:new Date().toISOString()};
    const base=RAW+head.sha+'/';
    const provenance=decode(await bytes(base+'provenance.json',1000000));
    assert(provenance.schema_version===1&&Array.isArray(provenance.results)&&provenance.results.length===1,'Provenance must declare one current result');
    const record=provenance.results[0];
    assert(/^results\/[A-Za-z0-9._-]+\.json$/.test(record.path)&&record.schema_version===2&&Number.isInteger(record.bytes)&&record.bytes>0&&record.bytes<=16000000&&/^[a-f0-9]{64}$/.test(record.sha256),'Invalid result declaration');
    const raw=await bytes(base+record.path,16000000);
    assert(raw.byteLength===record.bytes&&await digest(raw)===record.sha256,'Result integrity mismatch');
    const state=validate(decode(raw),record,config);
    return {...state,commit:head.sha,record,url:base+record.path,verifiedAt:new Date().toISOString()};
  }
  // Node tests exercise exactly this acquisition and validation code with fixtures.
  if(typeof module!=='undefined'&&module.exports){module.exports={acquire,validate,esc,INTERVAL};return;}
  const root=new URL('.',document.currentScript.src);
  const local=p=>new URL(p,root).href;
  let current=null,busy=false,config;
  const container=document.querySelector('.comparison-layout');
  const notice=document.createElement('section');notice.className='live-source-status';notice.setAttribute('aria-label','Comparison source status');
  const status=document.createElement('p');status.setAttribute('role','status');status.textContent='Loading and verifying the current research publication…';
  const retry=document.createElement('button');retry.textContent='Check for updates';retry.type='button';retry.addEventListener('click',()=>refresh());
  const source=document.createElement('a');source.href='https://github.com/'+REPO;source.textContent='Research repository';
  notice.append(status,retry,document.createTextNode(' · '),source);container.before(notice);
  // Never present the old static verdicts as if they were the current source.
  container.hidden=true;
  function legend(d,full=false){const p=d.evidence_policy;return '<section class="evidence-legend"><h2 id="evidence-heading">Evidence basis</h2>'+(full?'<dl>'+Object.values(p.levels).map(l=>'<dt>'+esc(l.label)+'</dt><dd>'+esc(l.definition)+'</dd>').join('')+'</dl>':'<p>'+Object.values(p.levels).map(l=>esc(l.label)).join(' · ')+'</p>')+'<p>'+esc(p.interpretation)+'</p>'+(full?'<p>'+esc(p.display_rule)+'</p><p>'+esc(p.unclassified)+'</p>':'<a href="'+local('methodology.html#evidence-heading')+'">Evidence definitions and display rules</a>')+'</section>';}
  function route(kind,id){return local(config[kind].includes(id)?kind+'/'+id+'.html':(kind==='cells'?'cell':'stack')+'.html?id='+encodeURIComponent(id));}
  function render(s){
    const d=s.d;const path=location.pathname;let body='';
    const cellId=path.match(/\/cells\/([^/]+)\.html$/)?.[1]||(path.endsWith('/cell.html')?new URLSearchParams(location.search).get('id'):null);
    const stackId=path.match(/\/stacks\/([^/]+)\.html$/)?.[1]||(path.endsWith('/stack.html')?new URLSearchParams(location.search).get('id'):null);
    const back='<p><a href="'+local('index.html')+'">Back to matrix</a></p>';
    if(cellId){const c=s.cells.get(cellId);assert(c,'This cell is not part of the current published result');const e=c.evidence;body=back+'<h1>'+esc(c.id)+': '+labels[c.status]+'</h1>';for(const [title,key] of [['Rationale','reason'],['Assessment method','method'],['Source context','source_label'],['Outstanding qualification','qualification']])body+='<h2>'+title+'</h2><p>'+esc(c[key])+'</p>';body+='<section class="evidence-detail"><h2>Evidence basis: '+esc(d.evidence_policy.levels[e.level].label)+'</h2><dl>'+['basis','scope','attribution','coverage','reviewed_at'].map(k=>'<dt>'+esc(k.replaceAll('_',' '))+'</dt><dd>'+esc(e[k])+'</dd>').join('')+'</dl><p>Documentary basis fingerprint (SHA-256, not proof of runtime execution): <code>'+esc(e.basis_sha256)+'</code></p><h3>Evidence reference identifiers</h3><p>Research identifiers are retained as text; they are not public links.</p><ul>'+e.references.map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul><p>'+esc(d.evidence_policy.interpretation)+'</p></section><h2>Public sources</h2><ul>'+c.sources.map(u=>'<li><a href="'+esc(u)+'">'+esc(u)+'</a></li>').join('')+'</ul><h2>Editorial evidence references</h2><p>These research identifiers are not downloadable files in the public repository.</p><ul>'+c.editorial_references.map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul>';
    }else if(stackId){const c=s.columns.get(stackId);assert(c,'This stack is not part of the current published result');body=back+'<h1>'+esc(c.title)+' — selected stack</h1><p>'+esc(c.profile)+'</p><p><a href="'+esc(c.website)+'">Official project website</a> · <a href="'+local('logos.html#'+c.id)+'">Logo credits</a></p>';
    }else if(path.endsWith('/methodology.html')){body=back+'<h1>Methodology and limits</h1><p>'+esc(d.scope)+'</p><p>Research is maintained by PRP Comparative Analysis; presentation by PRP Editorial and the website. Read each cell’s rationale, sources and qualifications together. Evidence classifications are not implementation, security, interoperability, performance or global-scale certification. Pending is not absence proof.</p><p>The browser checks the public research main branch on page load and every five minutes while visible. Provenance and result are read from one immutable commit and their digest, schema and complete grid are verified before display. Errors retain the last verified display with a stale notice, or show a load error. No credentials are used. GitHub caching, rate limits and offline periods may delay updates.</p><p>Non-URL references remain unavailable research labels. Publication does not expose the private evidence corpus or grant new licensing rights.</p>'+legend(d,true);
    }else if(path.endsWith('/logos.html')){body=back+'<h1>Marks and credits</h1><p>Marks identify projects and imply no endorsement.</p>'+d.columns.map(c=>'<article id="'+c.id+'"><h2>'+esc(c.title)+'</h2>'+d.marks.filter(m=>c.logo&&m.file==='logos/'+c.logo).map(m=>'<p>'+esc(m.rights||'')+'</p>'+['source','license_url'].filter(k=>m[k]&&safeURL(m[k])).map(k=>'<p><a href="'+esc(m[k])+'">'+k+'</a></p>').join('')).join('')+'</article>').join('');
    }else{body='<h1>Protocol and stack comparison</h1><p>Revision '+esc(d.revision)+' · Updated '+esc(d.date)+'</p><p>'+d.criteria.length+' criteria × '+d.columns.length+' stacks; '+s.counts.Pending+' Pending cells.</p><p><a href="'+local('methodology.html')+'">Methodology and limits</a> · <a href="'+esc(s.url)+'" download>Download verified structured data</a> · <a href="'+local('logos.html')+'">Logo credits</a></p><p class="legend"><span class="Y">Yes</span> <span class="N">No</span> <span class="U">Pending</span></p><p>Click a cell for evidence and qualifications. Expand a criterion for its definition. Results describe selected stacks, not implementation certification. Pending means insufficient evidence, not unsupported.</p>'+legend(d)+'<div class="wrap" tabindex="0" role="region" aria-label="Scrollable protocol comparison"><table class="matrix"><caption>Selected protocol stacks and capabilities</caption><thead><tr><th scope="col">Criterion</th>'+d.columns.map(c=>'<th scope="col" id="col-'+c.id+'"><a class="brand'+(c.id==='TO'?' dark':'')+'" href="'+local('logos.html#'+c.id)+'">'+(c.logo?'<img src="'+local('logos/'+c.logo)+'" alt="'+esc(c.title)+' mark">':esc(c.title))+'</a><div class="stack-heading"><a class="project-title" href="'+esc(c.website)+'">'+esc(c.title)+'</a><a class="stack-info" id="profile-'+c.id+'" href="'+route('stacks',c.id)+'" aria-label="Selected stack: '+esc(c.title)+'"><span aria-hidden="true">i</span></a></div></th>').join('')+'</tr></thead><tbody>';
      for(const r of d.criteria){if(config.groups[r.id])body+='</tbody><tbody><tr class="group-band"><th scope="rowgroup" colspan="'+(d.columns.length+1)+'"><span class="group-label">'+esc(config.groups[r.id])+'</span></th></tr>';body+='<tr><th scope="row" id="row-'+r.id+'">'+r.id+' · '+esc(r.title)+'<details><summary>Definition</summary>'+esc(r.definition)+'</details></th>';for(const col of d.columns){const c=s.cells.get(r.id+'-'+col.id),e=c.evidence;const hidden=c.status==='Y'&&e.level==='demonstrated'||c.status==='N'&&['reported','documented','demonstrated'].includes(e.level);body+='<td class="'+(c.status==='?'?'U':c.status)+' evidence-cell"><a class="cell-evidence-link" href="'+route('cells',c.id)+'" aria-label="'+esc(c.id+': '+labels[c.status]+'; evidence: '+e.level+'; scope: '+e.scope+'; qualification: '+c.qualification)+'"><span class="evidence-verdict">'+labels[c.status]+'</span><span class="evidence-band" aria-hidden="true"'+(hidden?' hidden':'')+'>'+esc(d.evidence_policy.levels[e.level].label)+'</span></a></td>';}body+='</tr>';}body+='</tbody></table></div>';
    }
    const selected=[...container.querySelectorAll('.yes-filter-toggle input:checked')].map(i=>i.id);
    const wrap=container.querySelector('.wrap'),scroll=wrap?[wrap.scrollLeft,wrap.scrollTop]:[0,0];const focus=document.activeElement?.id;
    container.innerHTML='<main'+(cellId||stackId||/\/(methodology|logos)\.html$/.test(path)?' class="content"':'')+'>'+body+'</main>';container.hidden=false;
    document.dispatchEvent(new Event('comparison-rendered'));
    for(const id of selected){const input=document.getElementById(id);if(input)input.checked=true;}container.querySelector('.yes-filter-toggle input')?.dispatchEvent(new Event('change'));
    const next=container.querySelector('.wrap');if(next){next.scrollLeft=scroll[0];next.scrollTop=scroll[1];}if(focus)document.getElementById(focus)?.focus({preventScroll:true});
    if(!current&&location.hash)document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();
  }
  async function refresh(){if(busy)return;busy=true;retry.disabled=true;try{config ||= await (await fetch(local('live-config.json'),{credentials:'omit'})).json();const next=await acquire(config,fetch,current);if(!current||next.commit!==current.commit){render(next);current=next;}status.textContent='Verified revision '+current.d.revision+' · source commit '+current.commit+' · checked '+next.verifiedAt+'. Automatic check every 5 minutes while visible.';notice.dataset.state='verified';notice.dataset.commit=current.commit;notice.dataset.sha256=current.record.sha256;notice.dataset.revision=current.d.revision;source.href='https://github.com/'+REPO+'/tree/'+current.commit;
    }catch(e){notice.dataset.state=current?'stale':'error';status.textContent=(current?'Update failed; showing last verified revision '+current.d.revision+'. ':'Comparison unavailable; no unverified data displayed. ')+e.message+'. Retry or open the research repository.';}finally{busy=false;retry.disabled=false;}}
  refresh();setInterval(()=>{if(!document.hidden)refresh();},INTERVAL);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
})();
