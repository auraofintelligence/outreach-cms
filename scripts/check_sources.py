import os
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from cms import load_public

def check(row):
    title=row.get('name',row.get('title','Source'))
    try:
        req=Request(row['url'],method='HEAD',headers={'User-Agent':'OutreachCMS source link review'})
        with urlopen(req,timeout=18) as response:code=response.status
        state='Reachable'
    except HTTPError as err:
        code=err.code
        state='Not found' if code in [404,410] else ('Access restricted or deferred' if code in [401,403,405,429] else 'Needs review')
    except Exception:
        code='';state='Could not verify'
    return f'| {title.replace(chr(124),chr(47))} | {state} | {code} | [Open source]({row["url"]}) |'

if __name__=='__main__':
    data=load_public()
    lines=['# Public source link review','','Link availability does not confirm participation, source accuracy or endorsement.','','| Source | Result | HTTP | Link |','| --- | --- | --- | --- |']
    with ThreadPoolExecutor(max_workers=4) as pool:lines.extend(pool.map(check,data['sources']+data['projects']))
    text='\n'.join(lines)+'\n'
    print(text)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write(text)

