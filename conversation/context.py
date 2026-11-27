"""Explicit transient context; no persistence or personal data upload."""
FIELDS={'indicator','territory','period','scenario','filters','operation'}
def followup(previous,updates):
    if (set(previous)|set(updates))-FIELDS: raise ValueError('Unexpected context field')
    result={**previous,**updates}
    if 'indicator' in updates and updates['indicator']!=previous.get('indicator'):
        for k in ('filters','scenario','operation'):
            if k not in updates: result.pop(k,None)
    return result
