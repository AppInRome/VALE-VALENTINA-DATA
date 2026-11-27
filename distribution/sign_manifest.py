"""Offline Ed25519 signing using OpenSSL; private key is never packaged."""
import subprocess,pathlib
def sign(manifest,key,signature):
    m,k,s=map(pathlib.Path,(manifest,key,signature))
    if k.resolve().is_relative_to(m.parent.resolve()):raise ValueError('Private key must be outside pack')
    subprocess.run(['openssl','pkeyutl','-sign','-rawin','-inkey',str(k),'-in',str(m),'-out',str(s)],check=True)
def verify(manifest,public_key,signature):
    subprocess.run(['openssl','pkeyutl','-verify','-rawin','-pubin','-inkey',str(public_key),'-in',str(manifest),'-sigfile',str(signature)],check=True)
