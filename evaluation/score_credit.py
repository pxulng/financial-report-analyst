"""Scores the credit-ratio items (agent v3, prompt v5) against key_credit.json. Usage: python3 score_credit.py "<glob of run files>"
Same rules as score.py: a number given with status found that differs from the key, or any number where the key says not applicable or
not_in_report, is a wrong or invented figure; missing is inaccurate but not wrong. Items marked excluded in the key are skipped."""
import json,sys,glob
key=json.load(open('key_credit.json'))
ITEMS=[('interest_expense','figures'),('debt_to_equity','computed'),('cfo_to_debt','computed'),('interest_coverage','computed')]
def close(item,a,b):
    if item=='interest_expense': return abs(a-b)<=max(1.0,abs(b)*0.0006)
    if item=='interest_coverage': return abs(a-b)<=max(0.05,abs(b)*0.002)
    return abs(a-b)<=0.005
def score(path):
    r=json.load(open(path)); t=r['id']; out={'id':t,'n':0,'ok':0,'wrong':0,'errors':[]}
    s=r.get('sheet')
    if s is None: 
        out['n']=sum(1 for n,_ in ITEMS if key[t][n]['status']!='excluded'); return out
    for n,where in ITEMS:
        kv=key[t][n]
        if kv['status']=='excluded': continue
        out['n']+=1
        m={x['item']:x for x in s.get(where,[])}.get(n); v=None if m is None else m.get('value'); st=None if m is None else m.get('status')
        if kv['status'] in('not_applicable','not_in_report'):
            if st==kv['status'] and v is None: out['ok']+=1
            elif v is not None: out['wrong']+=1; out['errors'].append(f"{n}: invented number {v} (key: {kv['status']})")
            else: out['errors'].append(f"{n}: should be {kv['status']}, got status {st}")
        else:
            if v is None or st!='found': out['errors'].append(f"{n}: missing (status {st}), key {kv['value']}")
            elif close(n,float(v),float(kv['value'])): out['ok']+=1
            else: out['wrong']+=1; out['errors'].append(f"{n}: WRONG {v}, key {kv['value']}")
    return out
if __name__=='__main__':
    res=[score(f) for f in sorted(glob.glob(sys.argv[1]))]
    print('| Company | Credit items right | Wrong or invented |\n|---|---|---|')
    for o in res: print(f"| {o['id']} | {o['ok']}/{o['n']} | {o['wrong']} |")
    print(f"\nTotals: right {sum(o['ok'] for o in res)}/{sum(o['n'] for o in res)}; wrong or invented {sum(o['wrong'] for o in res)}\n\nErrors:")
    for o in res:
        for e in o['errors']: print(f"- {o['id']}: {e}")
