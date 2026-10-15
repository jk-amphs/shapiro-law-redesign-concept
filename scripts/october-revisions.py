"""Idempotent implementation of Jason's October 13 homepage specification.

The back-cover photograph and revised featured-case copy remain client inputs.
Run after the September source and design generators, not in place of them.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import copy
import json
import re

ROOT=Path(__file__).resolve().parents[1]
RESULTS='Shapiro Law Offices, PLLC has secured over $300 million in verdicts and settlements, including over 50 recoveries of $1 million or more. The firm has obtained multi-million dollar recoveries in construction and scaffold accidents, motor vehicle crashes, premises liability \u2014 including trip, slip, and fall accidents \u2014 and medical malpractice, including birth injuries.'
PRACTICE='We investigate early, develop the evidence, and prepare serious cases for trial from the start.'
OVERSIGHT='Jason Shapiro and Hon. Ernest Buonocore personally oversee every case from investigation through resolution or trial.'
ERNEST='His time on the bench gives him firsthand insight into how judges assess evidence, credibility, and damages \u2014 perspectives he brings to the firm’s injury cases.'
BOOK='Written by Jason Shapiro, The Lawyers’ Guide to Personal Injury Law gives plaintiffs’ attorneys practical guidance on investigating, developing, litigating, and trying cases involving scaffold and construction accidents, motor vehicle crashes, premises liability, and other areas of personal injury law.'
JASON='Jason Shapiro is an Ivy League-educated trial attorney with more than 30 years of experience representing injured New Yorkers. He handles substantial construction, motor-vehicle, premises-liability, and medical-malpractice matters. He wrote the textbook The Lawyers’ Guide to Personal Injury Law.'
ERNEST_INTRO='Hon. Ernest Buonocore brings the perspective of an experienced trial lawyer, judge, and mediator to the firm’s serious personal injury cases.'

def fragment(html):return BeautifulSoup(html,'html.parser')
def replace_contents(node,html):
    node.clear()
    for child in list(fragment(html).contents):node.append(child)

files=list(ROOT.glob('*.html'))+list((ROOT/'practice-areas').glob('*.html'))+list((ROOT/'es').rglob('*.html'))
for path in files:
    soup=BeautifulSoup(path.read_text(),'html.parser')
    if not soup.body or not set(soup.body.get('class',[]))&{'client-home','client-site'}:continue
    soup.body['class']=list(dict.fromkeys(soup.body.get('class',[])+['october-revised']))
    prefix='../'*len(path.relative_to(ROOT).parts[:-1])
    is_es=soup.html.get('lang')=='es'
    link=soup.select_one('link[href*="october-revisions.css"]')
    if not link:link=soup.new_tag('link',rel='stylesheet');soup.head.append(link)
    link['href']=prefix+'css/october-revisions.css?v=20261015-1'
    # The suffix uses the same baseline, with punctuation outside S/O alignment.
    for line in soup.select('.brand-wordmark__line'):
        small=line.find('small');small.string=', PLLC'
    for a in soup.select('.client-header .client-text-us'):a.decompose()
    for a in soup.select('.client-header .client-social--whatsapp'):
        replace_contents(a,'<span>WhatsApp</span>')
    footer=soup.select_one('.client-footer')
    if footer:
        for p in footer.select('.client-footer__brand > p'):
            if p.get_text(strip=True) in ['New York','Nueva York']:p.decompose()
        serving=footer.select_one('.client-footer__serving')
        if serving and 'Suffolk' not in serving.get_text():
            serving.string=serving.get_text().replace('Nassau County,','Nassau County, Suffolk County,').replace('Nassau,','Nassau, Suffolk,')
        footer.select_one('.client-footer__nav h2').string='Enlaces rápidos' if is_es else 'Quick Links'
        for p in footer.select('.client-footer__contact p'):
            if 'Suite 1 Bronx' in p.get_text():p.string=p.get_text().replace('Suite 1 Bronx','Suite 1, Bronx')
        if not is_es:
            footer.select('.client-footer__legal p')[-1].string='Attorney Advertising. Prior results do not guarantee a similar outcome. The information presented at this site should not be construed to be formal legal advice and does not create an attorney-client relationship. Photo credits.'
    if not is_es:
        for cta in soup.select('.client-cta'):
            cta.select_one('h2').string='Speak With a Personal Injury Trial Attorney'
            cta.select_one('h5').string='No Fee Unless We Win'
            replace_contents(cta.select_one('.client-shell > p'),'Call or request a free consultation to discuss your case. <strong>Se habla Español.</strong>')
    if path.name=='about.html' and not is_es:
        j=soup.select_one('#jason-shapiro .client-attorney-profile__content > p:not(.client-attorney-role)');j.string=JASON
        e=soup.select_one('#ernest-buonocore .client-attorney-profile__content > p:not(.client-attorney-role)');e.string=ERNEST_INTRO+' '+ERNEST
        b=soup.select_one('.client-book-feature__copy')
        if b:
            b.select_one('p:not(.client-eyebrow)').string=BOOK
            if not b.select_one('.client-eyebrow'):b.insert(0,fragment('<p class="client-eyebrow">AUTHOR &amp; TRIAL ATTORNEY</p>').p)
    if path==ROOT/'index.html':
        soup.body['class']=list(dict.fromkeys(soup.body['class']+['october-home']))
        hero=soup.select_one('.client-hero__copy')
        hero.select_one('h2').string='Jason Shapiro'
        if not hero.select_one('.client-hero__led'):hero.select_one('h2').insert_before(fragment('<p class="client-hero__led">LED BY</p>').p)
        for p in hero.select('.client-hero__biography,.client-hero__credential,.client-hero__author'):p.decompose()
        hero.select_one('h2').insert_after(fragment('<p class="client-hero__author">Author of <em>The Lawyers’ Guide to Personal Injury Law</em></p>').p)
        hero.select_one('h2').insert_after(fragment('<p class="client-hero__credential">Ivy League-Educated Trial Attorney</p>').p)
        proof=soup.select('.client-proof__item')
        proof[3].strong.string='AV Preeminent'
        proof[3].span.string='Martindale-Hubbell’s highest peer-review rating.'
        proof[4].span.string='10-time Super Lawyers selectee.'
        result=soup.select_one('.client-results')
        result.h2.string='Proven Results for Injured New Yorkers'
        result.select_one('.client-intro').string=RESULTS
        more=result.select_one('.client-text-link').extract()
        result.select_one('.client-results__grid').insert_after(more)
        for card in result.select('.client-result-card'):
            card['class']=['client-result-card']
            for n in card.select('.client-result-card__matter,p'):
                if 'jury verdict' in n.get_text().lower():
                    n.string='Motor-Vehicle Recovery' if n.name=='span' else 'Recovery for a passenger ejected in a motor-vehicle crash.'
        result.select_one('.client-legal-note').string='Prior results do not guarantee a similar outcome.'
        practice=soup.select_one('.client-practice');practice.h2.string='OUR PRACTICE AREAS'
        practice.select_one('.client-intro').string=PRACTICE
        practice.select_one('.client-eyebrow').decompose() if practice.select_one('.client-eyebrow') else None
        cards=[('Scaffold Accidents','scaffold-accidents','pa-scaffold.jpg','Scaffolding surrounding a building under construction'),('Scaffold and Construction Accidents','construction-scaffold','pa-construction.jpg','Construction crane at a job site'),('Motor-Vehicle Accidents','motor-vehicle','pa-car.jpg','New York City taxis on the road'),('Premises and Sidewalk Accidents','premises','pa-premises.jpg','A Bronx apartment building and sidewalk'),('Medical Malpractice and Birth Injuries','medical-malpractice','pa-medical.jpg','Hospital corridor')]
        replace_contents(practice.select_one('.client-practice__grid'),''.join(f'<a class="client-practice-card" href="practice-areas/{slug}.html"><img src="images/{img}" alt="{alt}" loading="lazy"/><h3>{title}</h3></a>' for title,slug,img,alt in cards))
        replace_contents(soup.select_one('.client-firm > .client-shell'),'<h2>Why Choose Our Firm</h2><p>Founder Jason Shapiro and Senior Trial Attorney Hon. Ernest Buonocore bring over 60 years of combined experience. Judge Buonocore also brings the perspective of a judge and mediator.</p><ul class="october-benefits"><li>Trial-tested</li><li>Appellate Experience</li><li>Substantial Results</li></ul><p>'+OVERSIGHT+'</p>')
        attorneys=soup.select_one('.client-attorneys')
        attorneys.select_one('.client-eyebrow').decompose() if attorneys.select_one('.client-eyebrow') else None
        attorneys.h2.string='Our Attorneys'
        intro=attorneys.select_one('.client-intro')
        if intro:intro.decompose()
        for card,name,slug,description in zip(attorneys.select('.client-attorney-card'),['Jason Shapiro','Ernest Buonocore'],['jason-shapiro','ernest-buonocore'],[JASON,ERNEST_INTRO+' '+ERNEST]):
            card.select('p')[1].string=description
            card.a.string=f'View {name}’s Profile';card.a['href']=f'attorneys/{slug}.html'
        book=soup.select_one('.client-book__copy');book.select_one('p:not(.client-eyebrow)').string=BOOK
        if book.select_one('.client-eyebrow'):book.select_one('.client-eyebrow').string='AUTHOR & TRIAL ATTORNEY'
        if not book.select_one('.client-eyebrow'):book.insert(0,fragment('<p class="client-eyebrow">AUTHOR &amp; TRIAL ATTORNEY</p>').p)
        # Keep the supplied front cover until Jason supplies the real back cover.
        for block in soup.select('main > .client-contact'):block.decompose()
    path.write_text(str(soup).rstrip()+'\n')

# Dedicated profile URLs, based solely on existing approved profile material.
about=BeautifulSoup((ROOT/'about.html').read_text(),'html.parser')
for slug,name in [('jason-shapiro','Jason Shapiro, Esq.'),('ernest-buonocore','Hon. Ernest Buonocore')]:
    profile=copy.deepcopy(about)
    profile.title.string=f'{name} | Shapiro Law Offices, PLLC'
    profile.select_one('meta[name="description"]')['content']=JASON if slug=='jason-shapiro' else ERNEST_INTRO
    for alt in profile.select('link[hreflang]'):alt.decompose()
    main=profile.main;main.clear()
    main.append(fragment(f'<section class="client-inner-hero"><div class="client-shell"><p class="client-inner-hero__eyebrow">OUR ATTORNEYS</p><h1>{name}</h1><nav class="client-breadcrumbs" aria-label="Breadcrumb"><a href="about.html">Our Attorneys</a></nav></div></section>').section)
    main.append(copy.deepcopy(about.select_one('#'+slug)))
    if slug=='jason-shapiro':main.append(copy.deepcopy(about.select_one('.client-book-feature')))
    main.append(copy.deepcopy(about.select_one('.client-cta')))
    for tag in profile.select('[href],[src]'):
        for attr in ['href','src']:
            url=tag.get(attr)
            if url and not re.match(r'\w+:|//|#',url):tag[attr]='../'+url
    for a in profile.select('a[lang="es"]'):a['href']='../es/about.html#'+slug
    dest=ROOT/'attorneys'/f'{slug}.html';dest.parent.mkdir(exist_ok=True);dest.write_text(str(profile).rstrip()+'\n')

print('October specifications applied: 38 existing pages, 2 dedicated profiles. Back cover and featured-case wording remain pending.')
