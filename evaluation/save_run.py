"""Helper used to save an n8n agent result by hand with shortened free text.
Usage: python3 save_run.py out.json 'id' 'run_mode' 'tools csv' 'figures json {item:[value,status,note]}' 'computed json {item:[value,status,formula]}' [extra json]"""
import json,sys
out,i,mode,tools,fig,com=sys.argv[1:7]; extra=json.loads(sys.argv[7]) if len(sys.argv)>7 else {}
fig=json.loads(fig); com=json.loads(com); tl=[x for x in tools.split(',') if x]
d={"id":i,"model":"agent","stop_reason":"end","valid_json":True,"valid_after_extraction":True,"tool_calls":len(tl),"tools_used":tl,"run_mode":mode,
"sheet":{"unit":"millions","figures":[{"item":k,"value":v[0],"status":v[1],"source":"as returned (shortened)","note":v[2]} for k,v in fig.items()],
"computed":[{"item":k,"value":v[0],"status":v[1],"formula":v[2],"inputs":"","note":""} for k,v in com.items()]},
"note":"Free-text fields shortened when saved by hand; figures, statuses and computed values as returned. Segments, risks and absent answers were not saved for this run (credit-ratio test)."}
d.update(extra); json.dump(d,open(out,'w'),indent=1)
