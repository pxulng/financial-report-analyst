"""Add segments / risks / absent answers (shortened) to a hand-saved run file. Usage: add_sheet_extra.py run.json 'extra json'"""
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d["sheet"].update(json.loads(sys.argv[2]))
d["note"]="Free-text fields shortened when saved by hand; figures, statuses, computed values, segments, risk topics and absent answers as returned."
json.dump(d,open(p,'w'),indent=1)
