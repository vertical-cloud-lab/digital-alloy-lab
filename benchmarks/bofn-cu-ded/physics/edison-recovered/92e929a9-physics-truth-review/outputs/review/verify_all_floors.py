import json
from audit_reproduce import *
models=json.loads((OUT/'refits.json').read_text())
for m in models:
    m['p']=np.array(m['p'])
    print(m['label'],flush=True)
    for alloy in refx:
        print(alloy,robust_floor(m,alloy),flush=True)
