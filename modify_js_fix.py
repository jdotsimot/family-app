
with open("assets/index-v2.js", "r") as f:
    content = f.read()

# The problematic code (where l is declared)
# dm=({children:e})=>{const[t,n]=k.useState(cm);const l=k.useRef(!1);k.useEffect(()=>{fetch("/api/data").then(r=>r.json()).then(d=>{if(d){n(d);l.current=!0}else{l.current=!0}}).catch(()=>{l.current=!0})},[]);k.useEffect(()=>{l.current&&fetch("/api/data",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})},[t]);const r=h=>n(g=>({...g,events:[...g.events,{...h,id:zn()}]})),l=h=>n(g=>({...g,tasks:[...g.tasks,{...h,id:zn(),status:"todo"}]})),

# Wait, look at the file content.
# dm=({children:e})=>{const[t,n]=k.useState(cm);const l=k.useRef(!1);...;const r=h=>n(...),l=h=>n(...)
# Aha! `const l=h=>n(...)` is the original `addTask` function, which was minified to `l`.
# I introduced `const l=k.useRef(!1)`. So `l` is declared twice.

# I need to rename my `l` to something else, like `isMounted`.

old_chunk = 'dm=({children:e})=>{const[t,n]=k.useState(cm);const l=k.useRef(!1);k.useEffect(()=>{fetch("/api/data").then(r=>r.json()).then(d=>{if(d){n(d);l.current=!0}else{l.current=!0}}).catch(()=>{l.current=!0})},[]);k.useEffect(()=>{l.current&&fetch("/api/data",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})},[t]);'

# I will rename `l` to `refMounted`.
new_chunk = 'dm=({children:e})=>{const[t,n]=k.useState(cm);const refMounted=k.useRef(!1);k.useEffect(()=>{fetch("/api/data").then(r=>r.json()).then(d=>{if(d){n(d);refMounted.current=!0}else{refMounted.current=!0}}).catch(()=>{refMounted.current=!0})},[]);k.useEffect(()=>{refMounted.current&&fetch("/api/data",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})},[t]);'

if old_chunk in content:
    new_content = content.replace(old_chunk, new_chunk)
    with open("assets/index-v2.js", "w") as f:
        f.write(new_content)
    print("Fixed duplicate declaration of 'l'.")
else:
    print("Could not find the exact code block to replace.")
    # Fallback strategy: regex or manual check if exact string match fails due to spacing or encoding.
    # But since I just wrote it, it should match.
