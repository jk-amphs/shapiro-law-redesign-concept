"""Specification checks independent of the September baseline assertions."""
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

root=Path(__file__).resolve().parents[1]
home=BeautifulSoup((root/'index.html').read_text(),'html.parser')
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
def text(selector):return home.select_one(selector).get_text(' ',strip=True)
check(text('.client-hero__led')=='LED BY','Small LED BY label')
check(text('.client-hero__copy h2')=='Jason Shapiro','Name separate from LED BY')
check(text('.client-hero__credential')=='Ivy League-Educated Trial Attorney','Concise trial credential')
check(text('.client-hero__author')=='Author of The Lawyers’ Guide to Personal Injury Law','Concise author credential')
check(text('.client-proof__item:nth-child(4) strong')=='AV Preeminent','AV label')
check(text('.client-proof__item:nth-child(4) span')=='Martindale-Hubbell’s highest peer-review rating.','Exact AV caption')
check(text('.client-proof__item:nth-child(5) span')=='10-time Super Lawyers selectee.','Exact Super Lawyers caption')
check(text('.client-results h2')=='Proven Results for Injured New Yorkers','Results heading')
check(text('.client-results .client-intro')=='Shapiro Law Offices, PLLC has secured over $300 million in verdicts and settlements, including over 50 recoveries of $1 million or more. The firm has obtained multi-million dollar recoveries in construction and scaffold accidents, motor vehicle crashes, premises liability \u2014 including trip, slip, and fall accidents \u2014 and medical malpractice, including birth injuries.','Exact results replacement copy, including source punctuation')
check(len(home.select('.client-result-card'))==3,'Three featured cases')
check('jury verdict' not in ' '.join(c.get_text().lower() for c in home.select('.client-result-card')),'Jury Verdict removed only from homepage cards')
check(home.select_one('.client-results__grid').find_next_sibling('a').get('href')=='results.html','View more link below cards')
check(text('.client-results .client-legal-note')=='Prior results do not guarantee a similar outcome.','Results disclaimer retained without advertising label')
check(text('.client-practice h2')=='OUR PRACTICE AREAS','Practice section heading')
check(text('.client-practice .client-intro')=='We investigate early, develop the evidence, and prepare serious cases for trial from the start.','Exact practice replacement copy')
check(len(home.select('.client-practice-card'))==5 and len(home.select('.client-practice-card img'))==5,'Five practice areas with photos')
check(not home.select('.client-practice-card p'),'Practice card descriptions removed')
check(text('.client-practice-card h3')=='Scaffold Accidents','Scaffold first')
firm=home.select_one('.client-firm').get_text(' ',strip=True)
check('Founder Jason Shapiro' in firm and 'over 60 years of combined experience' in firm,'Founder and combined experience restored')
check('former' not in firm and 'No Fee' not in firm and 'Spanish' not in firm,'Redundant firm content removed')
check([n.get_text() for n in home.select('.october-benefits li')]==['Trial-tested','Appellate Experience','Substantial Results'],'Three exact benefit bullets')
check(home.select('.client-firm .client-shell > p')[-1].get_text()=='Jason Shapiro and Hon. Ernest Buonocore personally oversee every case from investigation through resolution or trial.','Exact final firm sentence')
check(text('.client-attorneys h2')=='Our Attorneys' and not home.select('.client-attorneys .client-intro'),'Attorney heading and no redundant subtitle')
for slug,name in [('jason-shapiro','Jason Shapiro'),('ernest-buonocore','Ernest Buonocore')]:
    a=home.select_one(f'.client-attorneys a[href="attorneys/{slug}.html"]')
    check(a and a.get_text()==f'View {name}’s Profile',f'{name} dedicated profile button')
    profile=BeautifulSoup((root/'attorneys'/f'{slug}.html').read_text(),'html.parser')
    check(profile.select_one('#'+slug) is not None,f'{name} profile destination exists')
check('state and federal court' not in text('.client-attorneys'),'Outdated Jason description removed')
check('He wrote the textbook The Lawyers’ Guide to Personal Injury Law.' in text('.client-attorneys'),'Jason textbook sentence')
check('His time on the bench gives him firsthand insight into how judges assess evidence, credibility, and damages \u2014 perspectives he brings to the firm’s injury cases.' in text('.client-attorneys'),'Exact Ernest replacement sentence')
check(text('.client-book__copy .client-eyebrow')=='AUTHOR & TRIAL ATTORNEY','Book section label')
check(text('.client-book__copy p:not(.client-eyebrow)')=='Written by Jason Shapiro, The Lawyers’ Guide to Personal Injury Law gives plaintiffs’ attorneys practical guidance on investigating, developing, litigating, and trying cases involving scaffold and construction accidents, motor vehicle crashes, premises liability, and other areas of personal injury law.','Exact book replacement copy')
check(not home.select('main > .client-contact') and 'Tell Us What Happened' not in home.main.get_text(),'Redundant Tell Us section deleted')
check(text('.client-cta h2')=='Speak With a Personal Injury Trial Attorney','CTA headline')
check(text('.client-cta h5')=='No Fee Unless We Win','Secondary fee statement')
check(text('.client-cta .client-shell > p')=='Call or request a free consultation to discuss your case. Se habla Español.','Exact CTA replacement copy')
check(text('.client-cta strong')=='Se habla Español.','Spanish statement bold')
paths=list(root.glob('*.html'))+list((root/'practice-areas').glob('*.html'))+list((root/'es').rglob('*.html'))+list((root/'attorneys').glob('*.html'))
count=0
for path in paths:
    soup=BeautifulSoup(path.read_text(),'html.parser')
    if not soup.select_one('.october-revised'):continue
    count+=1
    header=soup.select_one('.client-logo .brand-wordmark');footer=soup.select_one('.client-footer__logo .brand-wordmark')
    check(header.decode_contents()==footer.decode_contents(),f'{path.relative_to(root)} matching header/footer logo')
    check(header.small.get_text()==', PLLC',f'{path.relative_to(root)} comma and PLLC')
    check(not soup.select('.client-header .client-text-us'),f'{path.relative_to(root)} Text Us removed')
    check(all(a.get_text()=='WhatsApp' for a in soup.select('.client-header .client-social--whatsapp')),f'{path.relative_to(root)} WhatsApp label')
    check('Suffolk' in soup.select_one('.client-footer__serving').get_text(),f'{path.relative_to(root)} Suffolk County')
    check('Suite 1, Bronx' in soup.select_one('.client-footer__contact').get_text(),f'{path.relative_to(root)} address comma')
    check(not any(p.get_text(strip=True) in ['New York','Nueva York'] for p in soup.select('.client-footer__brand > p')),f'{path.relative_to(root)} redundant location line removed')
    if soup.html.get('lang')=='en':
        check(soup.select_one('.client-footer__nav h2').get_text()=='Quick Links',f'{path.relative_to(root)} Quick Links')
        check('does not create an attorney-client relationship.' in soup.select_one('.client-footer__legal').get_text(),f'{path.relative_to(root)} corrected legal notice')
        check('Attorney Advertising.' in soup.select_one('.client-footer__legal').get_text(),f'{path.relative_to(root)} advertising label retained')
    for a in soup.select('a[href]'):
        href=a['href']
        if not href or re.match(r'\w+:|//',href):continue
        target,_,anchor=href.partition('#');target=target.split('?')[0]
        dest=path.parent/target if target else path
        check(dest.exists(),f'{path.relative_to(root)} link {href}')
        if anchor and dest.suffix=='.html':check(BeautifulSoup(dest.read_text(),'html.parser').find(id=anchor) is not None,f'Anchor {href}')
report={'pages':count,'checks':len(checks),'passed':True,'pending':['Actual back-cover photograph with spine, required from Jason; current front-cover mockup retained.','Jason’s revised wording for the three featured case cards.'],'notes':['Exact client-supplied punctuation is retained in replacement passages.','Spanish main content is not rewritten without approved translation. Shared header/footer styling applies to both languages.','Preview contact form is not connected to production intake.','No meeting was scheduled or cancelled.']}
(root/'docs/october-review/static-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
