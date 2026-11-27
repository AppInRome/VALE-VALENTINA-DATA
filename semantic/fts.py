"""Local FTS5 retrieval with a safe literal-token query."""
import sqlite3,re
def build(docs):
    db=sqlite3.connect(':memory:')
    db.execute('CREATE VIRTUAL TABLE docs USING fts5(id UNINDEXED, label, body, tokenize="unicode61 remove_diacritics 2")')
    db.executemany('INSERT INTO docs VALUES(?,?,?)',docs)
    return db
def search(db,question,limit=5):
    terms=re.findall(r'[^\W_]+',question.lower(),re.UNICODE)[:32]
    if not terms:return []
    expression=' OR '.join('"'+t+'"' for t in terms)
    return db.execute('SELECT id,label,bm25(docs) FROM docs WHERE docs MATCH ? ORDER BY bm25(docs) LIMIT ?', (expression,max(1,min(20,int(limit))))).fetchall()
