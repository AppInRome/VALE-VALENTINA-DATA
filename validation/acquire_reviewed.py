"""Fetch pinned, explicitly reviewed original public assets without publishing them."""
import argparse,hashlib,pathlib,urllib.request,urllib.parse,tempfile,os
HOSTS={'huggingface.co','raw.githubusercontent.com','publications.europa.eu','op.europa.eu','population.un.org','www.istat.it','esploradati.istat.it','data.europa.eu'}
def acquire(url,expected,output,max_bytes):
    u=urllib.parse.urlparse(url)
    if u.scheme!='https' or u.hostname not in HOSTS or u.username or u.password:raise ValueError('Unapproved origin')
    if len(expected)!=64 or any(c not in '0123456789abcdef' for c in expected):raise ValueError('Pinned SHA256 required')
    out=pathlib.Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise FileExistsError(out)
    digest=hashlib.sha256();size=0
    fd,tmp=tempfile.mkstemp(dir=out.parent)
    try:
        with os.fdopen(fd,'wb') as f, urllib.request.urlopen(url,timeout=60) as r:
            if urllib.parse.urlparse(r.geturl()).scheme!='https':raise ValueError('Unsafe redirect')
            while True:
                chunk=r.read(1024*1024)
                if not chunk:break
                size+=len(chunk)
                if size>max_bytes:raise ValueError('Size limit exceeded')
                digest.update(chunk);f.write(chunk)
        if digest.hexdigest()!=expected:raise ValueError('Hash mismatch')
        os.replace(tmp,out)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return size
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('sha256');p.add_argument('output');p.add_argument('--license-reviewed',action='store_true');p.add_argument('--max-bytes',type=int,default=500_000_000);a=p.parse_args()
    if not a.license_reviewed:raise SystemExit('Review exact license and attribution first')
    print(acquire(a.url,a.sha256,a.output,a.max_bytes))
