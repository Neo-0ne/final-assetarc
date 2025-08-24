import json, os, sys
with open('eng-drafting/templates/templates.json') as f:
    items=json.load(f)
missing=[i for i in items if i.get('target') and not os.path.exists(i['target'])]
if missing:
    print('Missing targets:')
    for m in missing:
        print('-', m['id'], '->', m['target'])
    sys.exit(1)
print('All template targets present.')
