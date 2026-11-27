"""Deterministic calculations. Never infer intersections from marginal data."""
from decimal import Decimal
def number(x):
    if isinstance(x,bool) or not isinstance(x,(int,float,Decimal)): raise ValueError('Numeric input required')
    d=Decimal(str(x))
    if not d.is_finite(): raise ValueError('Nonfinite input')
    return d
def percentage(part,total):
    p,t=number(part),number(total)
    if not 0<=p<=t or t<=0: raise ValueError('Invalid universe')
    return p*100/t
def change(old,new):
    a,b=number(old),number(new)
    if a==0: raise ValueError('Undefined relative change')
    return (b-a)*100/a
def compare(a,b,operation='difference'):
    keys=('indicator','unit','universe','period','scenario','method')
    if any(k not in a or k not in b or a[k]!=b[k] for k in keys): raise ValueError('Noncomparable observations')
    if operation=='difference': return number(a['value'])-number(b['value'])
    if operation=='relative_change': return change(b['value'],a['value'])
    raise ValueError('Unknown operation')
