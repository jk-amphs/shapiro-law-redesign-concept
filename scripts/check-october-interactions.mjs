import {chromium} from '/Users/aehun/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
const base=process.env.REVIEW_BASE||'http://127.0.0.1:8135/';
const browser=await chromium.launch({executablePath:'/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',headless:true});
const p=await browser.newPage({viewport:{width:390,height:900}}),checks=[];
function check(value,label){if(!value)throw Error(label);checks.push(label);}
await p.goto(base+'?review=off');await p.locator('.nav-toggle').click();check(await p.locator('.nav-toggle').getAttribute('aria-expanded')==='true','Mobile menu opens');await p.keyboard.press('Escape');check(await p.locator('.nav-toggle').getAttribute('aria-expanded')==='false','Escape closes menu');
await p.getByRole('link',{name:'View Jason Shapiro’s Profile',exact:true}).click();await p.waitForURL('**/attorneys/jason-shapiro.html');check(await p.locator('h1').innerText()==='Jason Shapiro, Esq.','Jason button opens individual Jason profile');
await p.goto(base+'?review=off');await p.getByRole('link',{name:'View Ernest Buonocore’s Profile',exact:true}).click();await p.waitForURL('**/attorneys/ernest-buonocore.html');check(await p.locator('h1').innerText()==='Hon. Ernest Buonocore','Ernest button opens individual Ernest profile');
await p.goto(base+'?review=off');await p.getByRole('link',{name:'View More Case Results',exact:true}).click();await p.waitForURL('**/results.html');check(await p.locator('.client-case-result').count()===50,'View more opens complete 50-result page');
await p.goto(base+'?review=off');await p.locator('.client-practice-card').first().click();await p.waitForURL('**/practice-areas/scaffold-accidents.html');check(await p.locator('h1').innerText()==='Scaffold Falls Demand Immediate Investigation','First practice photo card opens scaffold detail');
await p.goto(base+'?review=off');await p.locator('.client-cta .client-btn--light').click();await p.waitForURL('**/contact.html#contact-form');check(await p.locator('#contact-form').isVisible(),'Consultation link reaches form');
check(await p.locator('.client-mobile-contactbar__call').getAttribute('href')==='tel:7182957000','Mobile call destination preserved');
check((await p.locator('.client-mobile-socials .client-social--whatsapp').getAttribute('href')).startsWith('https://wa.me/17182957000'),'Mobile WhatsApp destination preserved');
const touch=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});await touch.goto(base+'?review=off');check(await touch.locator('.client-cta .client-btn--light').getAttribute('href')==='tel:7182957000','Touch-phone consultation button opens the dialer instead of inert preview form');await touch.close();
await p.goto(base+'docs/october-review/');
for(const section of ['index','header','hero','metrics','results','practice','firm','attorneys','book','cta','footer','about','contact'])for(const size of ['390','1440']){
 await p.selectOption('#section',section);await p.selectOption('#size',size);await p.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode()));});
}
check(true,'All 26 desktop/mobile comparison pairs load');
await p.locator('#layout').click();check(await p.locator('#layout').getAttribute('aria-pressed')==='true','Comparison supports stacked view');
await p.setViewportSize({width:1440,height:1000});await p.selectOption('#section','index');await p.selectOption('#size','1440');await p.locator('#layout').click();await p.screenshot({path:'docs/october-review/comparison-desktop.jpg',quality:85});
check(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Comparison has no horizontal overflow');
await browser.close();await fs.writeFile('docs/october-review/interaction-checks.json',JSON.stringify({base,checks},null,2));console.log(checks);
