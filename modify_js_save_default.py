
with open("assets/index-v2.js", "r") as f:
    content = f.read()

# Old chunk (with refMounted)
old_chunk = 'dm=({children:e})=>{const[t,n]=k.useState(cm);const refMounted=k.useRef(!1);k.useEffect(()=>{fetch("/api/data").then(r=>r.json()).then(d=>{if(d){n(d);refMounted.current=!0}else{refMounted.current=!0}}).catch(()=>{refMounted.current=!0})},[]);k.useEffect(()=>{refMounted.current&&fetch("/api/data",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})},[t]);'

# New chunk
# If data is null (d is falsy), we want to save the current default state (t/cm).
# We can do this by calling the save fetch immediately in the else block.
# However, 't' might not be accessible or stable in that closure easily without warning, but 'cm' is constant.
# Actually 't' is in scope.
# But wait, simply setting refMounted.current = true is not enough to trigger the effect if 't' doesn't change.
# The effect runs on [t].
# If I want to force a save of default data, I can do it in the fetch callback.

new_chunk = 'dm=({children:e})=>{const[t,n]=k.useState(cm);const refMounted=k.useRef(!1);k.useEffect(()=>{fetch("/api/data").then(r=>r.json()).then(d=>{if(d){n(d);refMounted.current=!0}else{refMounted.current=!0;fetch("/api/data",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(cm)})}}).catch(()=>{refMounted.current=!0})},[]);k.useEffect(()=>{refMounted.current&&fetch("/api/data",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})},[t]);'

if old_chunk in content:
    new_content = content.replace(old_chunk, new_chunk)
    with open("assets/index-v2.js", "w") as f:
        f.write(new_content)
    print("Updated JS to save default data on initialization.")
else:
    print("Could not find the code block.")
