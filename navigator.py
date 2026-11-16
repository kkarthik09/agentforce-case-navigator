"""Read-only retrieval/routing reference, with explicit document authorization."""
import json, re
from datetime import datetime, timezone

def tokens(text): return set(re.findall(r'[a-z0-9]+',text.lower()))

def navigate(case, articles, allowed_ids, now, min_overlap=2):
    if not isinstance(case.get('subject'),str) or not case['subject'].strip(): raise ValueError('Missing subject')
    if case.get('priority') not in {'Low','Medium','High','Critical'}: raise ValueError('Invalid priority')
    if now.tzinfo is None: raise ValueError('Use timezone-aware now')
    if min_overlap<1: raise ValueError('Positive overlap required')
    query=tokens(case['subject'])
    seen=set(); ranked=[]
    for article in articles:
        key=article['id']
        if key in seen: raise ValueError('Duplicate article id')
        seen.add(key)
        # Never score or return content outside the caller's authorized set.
        if key not in allowed_ids or article.get('status')!='published': continue
        expiry=datetime.fromisoformat(article['expires'])
        if expiry.tzinfo is None: raise ValueError('Article expiry needs timezone')
        if expiry<=now: continue
        if not isinstance(article.get('text'),str): raise ValueError('Missing article text')
        score=len(query & tokens(article['text']))
        if score>=min_overlap: ranked.append((score,key,article['text']))
    ranked.sort(key=lambda x:(-x[0],x[1]))
    escalate=case['priority'] in {'High','Critical'}
    if not ranked:
        return {'route':'human','reason':'no_authorized_current_evidence','citations':[],'draft':None}
    chosen=ranked[:3]
    return {'route':'human' if escalate else 'review_draft',
            'reason':'priority_escalation' if escalate else 'evidence_found',
            'citations':[{'id':i,'quote':text,'overlap':score} for score,i,text in chosen],
            'draft':'\n\n'.join(text for _,_,text in chosen)}

if __name__=='__main__':
    print(json.dumps(navigate({'subject':'VPN connection reset','priority':'Medium'},
      [{'id':'KA-demo','text':'VPN connection reset: check the approved network configuration.',
        'status':'published','expires':'2030-01-01T00:00:00+00:00'}],
      {'KA-demo'},datetime.now(timezone.utc)),indent=2))
