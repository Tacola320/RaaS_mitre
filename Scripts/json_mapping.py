import json
import pandas as pd

with open('<path>\\layer.json', 'r') as f:
    data = json.load(f)

column_names = ["t_id", "tactics", "technique", "subtechnique", "score", "X", "Y", "Z", "comment"]
df = pd.read_excel("<ttps>.xls", names=column_names)

techniques = df['t_id'].tolist()
tactics = df['tactics'].tolist()
score = df['score'].tolist()
comment = df['comment'].tolist()

for t, ta, s, c in zip(techniques, tactics, score, comment):
    phrase = {'techniqueID': 'T_X', 'tactic': 'execution', 'score': 1, 'color': '', 'comment': 'Conti', 'enabled': True, 'metadata': [], 'links': [], 'showSubtechniques': False}
    phrase['techniqueID'] = t
    phrase['tactic'] = ta
    phrase['score'] = s
    phrase['comment'] = c
    data['techniques'].append(phrase)

result = json.dumps(data, sort_keys=True, indent=4)
print(result)

with open("all.json", "w") as outfile:
    outfile.write(result)