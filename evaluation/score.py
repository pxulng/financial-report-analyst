"""Scores model sheets against key.json. Usage: python3 score.py <glob of run files> [--out report.md]
Rules (frozen in docs/DESIGN.md): wrong or invented figure = a number given with status 'found' that differs from the key
(or any number where the key says not applicable); tolerance: report rounding. Missing (null / not_in_report) is inaccurate but is not
a 'wrong figure presented as certain'."""
import json,sys,glob,re
key=json.load(open('key.json')); risks=json.load(open('risks_reference.json'))
READ={'revenue':'revenue','operating_income':'operating_income','net_income':'net_income','diluted_eps':'diluted_eps','operating_cash_flow':'operating_cash_flow','capex':'capex','cash':'cash','total_financial_debt':'debt','shareholders_equity':'equity'}
COMP=['revenue_growth','operating_margin','free_cash_flow','net_debt']
def close(item,a,b):
    if item in('revenue_growth','operating_margin'): return abs(a-b)<=0.001
    if item=='diluted_eps': return abs(a-b)<=0.0051
    return abs(a-b)<=max(1.0,abs(b)*0.0006)   # rounding of the report's own unit
def score(path):
    r=json.load(open(path)); t=r['id']; k=key[t]; out={'id':t,'valid_json':r['valid_json'],'in':r['input_tokens'],'out':r['output_tokens'],'errors':[]}
    if not r['valid_json']: return out
    s=r['sheet']; txt=re.sub(r'\s+',' ',open('../data/10k/'+k['file'],encoding='utf-8',errors='ignore').read())
    fig={f['item']:f for f in s.get('figures',[])}; com={f['item']:f for f in s.get('computed',[])}
    n_read=ok_read=n_comp=ok_comp=wrong=0; src_n=src_ok=0
    def check(item,m,kv,kind):
        nonlocal wrong
        kna = kv['status']=='not_applicable'
        v=None if m is None else m.get('value'); st=None if m is None else m.get('status')
        if kna:
            good = (st=='not_applicable' and v is None)
            if not good and v is not None: wrong+=1; out['errors'].append(f"{item}: invented number {v} (key: not applicable)")
            elif not good: out['errors'].append(f"{item}: should be not_applicable, got status {st}")
            return good
        if v is None or st!='found':
            out['errors'].append(f"{item}: missing (status {st}), key {kv['value']}"); return False
        if close(item,float(v),float(kv['value'])): return True
        wrong+=1; out['errors'].append(f"{item}: WRONG {v}, key {kv['value']}"); return False
    for mi,ki in READ.items():
        n_read+=1; ok_read+=check(mi,fig.get(mi),k['items'][ki],'read')
        m=fig.get(mi)
        if m and m.get('status')=='found' and m.get('value') is not None:
            src_n+=1; v=float(m['value']); forms=[f"{abs(v):,.1f}" if abs(v)!=int(abs(v)) else f"{int(abs(v)):,}", f"{abs(v):,.2f}"]
            src_ok+= any(x in txt for x in forms)
    for ci in COMP:
        n_comp+=1; ok_comp+=check(ci,com.get(ci),k['computed'][ci],'comp')
    nir=s.get('not_in_report',[]); n_abs=len(nir); ok_abs=sum(1 for q in nir if q.get('status')=='not_in_report')
    mr=' '.join(x.get('risk','') for x in s.get('major_risks',[])).lower()
    rf=sum(any(kw.lower() in mr for kw in rk['keywords']) for rk in risks[t])
    out.update(read=f"{ok_read}/{n_read}",comp=f"{ok_comp}/{n_comp}",absent=f"{ok_abs}/{n_abs}",wrong=wrong,src=f"{src_ok}/{src_n}",risks_auto=f"{rf}/3",
               n_ok_read=ok_read,n_read=n_read,n_ok_comp=ok_comp,n_comp=n_comp,n_ok_abs=ok_abs,n_abs=n_abs,n_src_ok=src_ok,n_src=src_n)
    return out
if __name__=='__main__':
    files=sorted(glob.glob(sys.argv[1])); res=[score(f) for f in files]
    print('| Company | JSON | Read | Computed | Absent | Wrong/invented | Value found in report | Risks (keyword proxy) |\n|---|---|---|---|---|---|---|---|')
    for o in res: print(f"| {o['id']} | {'ok' if o['valid_json'] else 'INVALID'} | {o.get('read','')} | {o.get('comp','')} | {o.get('absent','')} | {o.get('wrong','')} | {o.get('src','')} | {o.get('risks_auto','')} |")
    for k in ['n_ok_read','n_read','n_ok_comp','n_comp','n_ok_abs','n_abs','n_src_ok','n_src']: globals()[k]=sum(o.get(k,0) for o in res)
    print(f"\nTotals: read {n_ok_read}/{n_read} = {n_ok_read/n_read:.1%}; computed {n_ok_comp}/{n_comp} = {n_ok_comp/n_comp:.1%}; absent {n_ok_abs}/{n_abs}; wrong or invented {sum(o.get('wrong',0) for o in res)}; value-in-report {n_src_ok}/{n_src}")
    print('\nErrors:'); 
    for o in res:
        for e in o['errors']: print(f"- {o['id']}: {e}")
    json.dump(res,open('last_scores.json','w'),indent=1)
