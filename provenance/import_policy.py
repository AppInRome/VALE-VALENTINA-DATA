"""Require pinned hashes and explicit license review before accepting downloaded resources."""
import hashlib,pathlib
def reviewed_bytes(path,sha256,license_id,attribution,approved=False,max_bytes=100_000_000):
    if approved is not True or not license_id.strip() or not attribution.strip():raise ValueError('License review required')
    p=pathlib.Path(path)
    if p.stat().st_size>max_bytes:raise ValueError('Resource too large')
    raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha256.lower():raise ValueError('Checksum mismatch')
    return raw
