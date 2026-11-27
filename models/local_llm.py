"""Optional local llama.cpp test harness. Not connected to VALE data."""
import argparse,pathlib,hashlib,subprocess
def run(binary,model,sha,question):
    binary=pathlib.Path(binary).resolve(strict=True);model=pathlib.Path(model).resolve(strict=True)
    if model.suffix.lower()!='.gguf' or not model.is_file():raise ValueError('Expected local GGUF')
    with model.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    if actual!=sha.lower():raise ValueError('Model checksum mismatch')
    if len(question)>700:raise ValueError('Question too long')
    prompt='Sei Valentina, assistente locale. Spiega in italiano con cortesia e sintesi. Non hai accesso ai dati VALE: non inventare statistiche, cifre o fonti.\nDomanda: '+question+'\nRisposta:'
    r=subprocess.run([str(binary),'-m',str(model),'-p',prompt,'-n','256','-c','2048','--no-display-prompt','--temp','0.2'],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120,check=True)
    return r.stdout.strip()[:4000]
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('llama_cli');p.add_argument('gguf');p.add_argument('--sha256',required=True);p.add_argument('question');a=p.parse_args()
    print('RISPOSTA GENERATIVA LOCALE NON VERIFICATA\n'+run(a.llama_cli,a.gguf,a.sha256,a.question))
