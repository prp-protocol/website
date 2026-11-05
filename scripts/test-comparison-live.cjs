// Exact production validator/acquirer, fixture requests only; no research mutation.
const fs=require('fs'),assert=require('assert'),crypto=require('crypto');
global.crypto=crypto.webcrypto;
const {acquire,validate,esc,parseUnique,INTERVAL}=require('../comparison/live.js');
let data=fs.readFileSync(process.argv[2]);const original=data,d=JSON.parse(data);
const config=JSON.parse(fs.readFileSync('comparison/live-config.json'));
const record={path:'results/current.json',revision:d.revision,schema_version:2,bytes:data.length,sha256:crypto.createHash('sha256').update(data).digest('hex'),cells:d.cells.length,counts:{Yes:d.cells.filter(c=>c.status==='Y').length,No:d.cells.filter(c=>c.status==='N').length,Pending:d.cells.filter(c=>c.status==='?').length}};
let commit='1'.repeat(40),calls=[];
const request=async(url,opts)=>{calls.push(url);assert.equal(opts.credentials,'omit');let b=url.endsWith('/git/ref/heads/main')?Buffer.from(JSON.stringify({ref:'refs/heads/main',object:{sha:commit,type:'commit'}})):url.endsWith('/provenance.json')?Buffer.from(JSON.stringify({schema_version:1,results:[record]})):data;return new Response(b,{status:200});};
(async()=>{await acquire(config,request);assert(calls.slice(1).every(u=>u.includes('/'+commit+'/')));
const saved={...record};const fixture=structuredClone(d);fixture.revision='fixture-next';fixture.cells[0].reason='Controlled fixture successor, not research.';data=Buffer.from(JSON.stringify(fixture));Object.assign(record,{path:'results/fixture-next.json',revision:fixture.revision,bytes:data.length,sha256:crypto.createHash('sha256').update(data).digest('hex')});
commit='2'.repeat(40);calls=[];const newer=await acquire(config,request);assert.equal(newer.commit,commit);assert.equal(newer.d.cells[0].reason,fixture.cells[0].reason);assert.equal(newer.d.revision,'fixture-next');assert(calls.slice(1).every(u=>u.includes('/'+commit+'/')));assert(calls.at(-1).endsWith('/results/fixture-next.json'));data=original;Object.assign(record,saved);
let negatives=0;for(const mutate of [x=>x.schema_version=99,x=>x.cells[0].evidence.level='certified',x=>delete x.cells[0].qualification,x=>x.cells.pop(),x=>x.columns[0].website='javascript:alert(1)',x=>x.columns[0].logo='../secret',x=>x.cells[0].reason='/opt/agentmux/private',x=>x.criteria[0].id='C08']){const x=structuredClone(d);mutate(x);assert.throws(()=>validate(x,record,config));negatives++;}
record.sha256='0'.repeat(64);await assert.rejects(()=>acquire(config,request),/integrity/);negatives++;
await assert.rejects(()=>acquire(config,async()=>new Response('',{status:503})),/503/);negatives++;
assert.equal(esc('<img src=x onerror="x">'),'&lt;img src=x onerror=&quot;x&quot;&gt;');assert.equal(INTERVAL,300000);
assert.throws(()=>parseUnique('{"a":1,"a":2}'),/Duplicate/);assert.throws(()=>parseUnique('{"a":1,"\\u0061":2}'),/Duplicate/);assert.deepEqual(parseUnique('{"a":[{"x":1},{"x":2}]}'),{a:[{x:1},{x:2}]});
const bad=structuredClone(d);bad.marks[0]={file:'__proto__'};assert.throws(()=>validate(bad,saved,config),/asset/);negatives+=3;
console.log(JSON.stringify({result:'PASS',fixture_snapshot_transitions:1,negative_cases:negatives,coherent_commits:true,escaping:true,real_upstream_update:false}));})().catch(e=>{console.error(e);process.exitCode=1;});
