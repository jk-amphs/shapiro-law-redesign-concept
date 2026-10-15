import {chromium} from '/Users/aehun/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
const stage=process.argv[2]||'after';
const base=process.env.REVIEW_BASE||(stage==='before'?'https://codex-implement-approved-cop.shapiro-law-redesign-concept.pages.dev/':'http://127.0.0.1:8135/');
const out='docs/october-review';await fs.mkdir(`${out}/screenshots`,{recursive:true});
const browser=await chromium.launch({executablePath:'/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',headless:true});
const widths=stage==='before'?[390,1440]:[320,390,768,1024,1440];
const english=JSON.parse(await fs.readFile('docs/september-update/source-audit.json','utf8')).pages.map(p=>p.file);
const spanish=['index.html','about.html','practice-areas.html','results.html','contact.html','practice-areas/construction-scaffold.html','practice-areas/motor-vehicle.html','practice-areas/premises.html','practice-areas/medical-malpractice.html'].map(f=>'es/'+f);
const pages=stage==='before'?['index.html','about.html','contact.html']:[...english,...spanish,'attorneys/jason-shapiro.html','attorneys/ernest-buonocore.html'];
const checks=[];const errors=[];
for(const width of widths){
 const page=await browser.newPage({viewport:{width,height:1000}});
 for(const file of pages){
  await page.goto(base+file+'?review=off',{waitUntil:'domcontentloaded'});
  await page.evaluate(async()=>{await document.fonts.ready;for(const i of document.images)i.loading='eager';await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
  const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),h1:document.querySelectorAll('h1').length}));
  checks.push({file,width,...state});if(state.overflow||state.broken.length||state.h1!==1)errors.push({file,width,...state});
  if(stage==='after'){
   const logo=await page.evaluate(()=>{const header=document.querySelector('.client-header').getBoundingClientRect(),h1=document.querySelector('h1').getBoundingClientRect();const name=document.querySelector('.client-logo .brand-wordmark__name');const range=document.createRange();range.setStart(name.firstChild,6);range.setEnd(name.firstChild,7);const o=range.getBoundingClientRect();const s=document.querySelector('.client-logo .brand-wordmark__offices > :last-child').getBoundingClientRect();return{headlineClear:h1.top>=header.bottom,alignment:Math.abs(o.right-parseFloat(getComputedStyle(name).letterSpacing)-s.right)};});
   if(!logo.headlineClear||logo.alignment>0.5)errors.push({file,width,...logo});
  }
  if(stage==='after'&&file==='index.html'){
   const metrics=await page.evaluate(()=>{const cards=[...document.querySelectorAll('.client-result-card')].map(e=>e.getBoundingClientRect());const imgs=[...document.querySelectorAll('.client-practice-card img')];return{equalCards:Math.max(...cards.map(b=>b.width))-Math.min(...cards.map(b=>b.width))<1&&Math.max(...cards.map(b=>b.height))-Math.min(...cards.map(b=>b.height))<1,fivePhotos:imgs.length===5&&imgs.every(i=>i.naturalWidth>0),cta:document.querySelectorAll('.client-cta').length===1,duplicate:!!document.querySelector('main > .client-contact'),proofFont:Math.min(...[...document.querySelectorAll('.client-proof__item span')].map(e=>parseFloat(getComputedStyle(e).fontSize)))};});
   if(!metrics.equalCards||!metrics.fivePhotos||!metrics.cta||metrics.duplicate||metrics.proofFont<13)errors.push({file,width,...metrics});
  }
  if([390,1440].includes(width)&&['index.html','about.html','contact.html','attorneys/jason-shapiro.html','attorneys/ernest-buonocore.html'].includes(file)){
   const key=file.replaceAll('/','-').replace('.html','');
   await page.screenshot({path:`${out}/screenshots/${key}-${width}-${stage}.jpg`,fullPage:true,quality:82});
   if(file==='index.html')for(const [key,selector] of Object.entries({header:'.client-header',hero:'.client-hero',metrics:'.client-proof',results:'.client-results',practice:'.client-practice',firm:'.client-firm',attorneys:'.client-attorneys',book:'.client-book',cta:'.client-cta',footer:'.client-footer'}))await page.locator(selector).screenshot({path:`${out}/screenshots/${key}-${width}-${stage}.jpg`,quality:88});
  }
 }
 await page.close();
}
await browser.close();await fs.writeFile(`${out}/${stage}-checks.json`,JSON.stringify({base,checks,errors},null,2));console.log(JSON.stringify({checks:checks.length,errors}));if(stage==='after'&&errors.length)process.exitCode=1;
