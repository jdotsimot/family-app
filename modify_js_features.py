
with open("assets/index-v2.js", "r") as f:
    content = f.read()

# 1. Add FAMILY_MEMBERS and Mail icon
# We'll add it before `const Trash=...` or some other clear marker.
# I'll use `const Trash` as a marker.

marker = 'const Trash=fe("Trash"'
if marker not in content:
    print("Marker not found!")
    exit(1)

definitions = """
const FAMILY_MEMBERS = [
  { name: "Mom", email: "lnicholep91@gmail.com" },
  { name: "Dad", email: "jrsimot@gmail.com" },
  { name: "Jaidin", email: "jdkosers112109@gmail.com" },
  { name: "Dausyn", email: "dausynaisley@gmail.com" },
  { name: "Grandma", email: "mbsimot@gmail.com" },
  { name: "Grandpa", email: "earlrsimot@gmail.com" }
];
const Mail = fe("Mail", [
  ["rect", { width: "20", height: "16", x: "2", y: "4", rx: "2", key: "18n3k1" }],
  ["path", { d: "m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7", key: "1ocr93" }]
]);
const sendNotification = async (assigneeName, taskTitle) => {
  const member = FAMILY_MEMBERS.find(m => m.name === assigneeName);
  if (!member) return alert("No email found for user: " + assigneeName);

  try {
      const response = await fetch("/api/notify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: member.email,
          message: `Hey! You've been assigned a new task: ${taskTitle}`
        })
      });

      if (response.ok) alert("Notification sent to " + member.name + "!");
      else alert("Failed to send notification.");
  } catch (e) {
      console.error(e);
      alert("Error sending notification.");
  }
};
"""

content = content.replace(marker, definitions + marker)

# 2. Update Task Options
# Search for the select options.
# Pattern: v.jsxs("select",{className:"p-2 bg-gray-50 rounded-lg text-sm border-none focus:ring-0",value:i,onChange:u=>o(u.target.value),children:[v.jsx("option",{children:"Unassigned"}),v.jsx("option",{children:"Mom"}),v.jsx("option",{children:"Dad"}),v.jsx("option",{children:"Kids"})]})
# I need to replace the children array part.

search_options = 'children:[v.jsx("option",{children:"Unassigned"}),v.jsx("option",{children:"Mom"}),v.jsx("option",{children:"Dad"}),v.jsx("option",{children:"Kids"})]'
replace_options = 'children:[v.jsx("option",{children:"Unassigned"}),...FAMILY_MEMBERS.map(m=>v.jsx("option",{children:m.name},m.name))]'

if search_options in content:
    content = content.replace(search_options, replace_options)
else:
    print("Could not find options block.")
    # Let's dump a context to help debug if it fails.
    idx = content.find('v.jsxs("select"')
    if idx != -1:
        print("DEBUG CONTEXT:", content[idx:idx+300])
    exit(1)

# 3. Add Mail Button
# Search for the trash button in the task list.
# Pattern: v.jsx("button",{onClick:(e)=>{e.stopPropagation();dt(u.id)},className:"ml-2 p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors",children:v.jsx(Trash,{size:18})})
# We want to add the Mail button before it. Note: u is the task object loop variable.

search_trash_btn = 'v.jsx("button",{onClick:(e)=>{e.stopPropagation();dt(u.id)},className:"ml-2 p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors",children:v.jsx(Trash,{size:18})})'

# We need to pass u.assignee and u.title to sendNotification.
mail_btn = 'v.jsx("button",{onClick:(e)=>{e.stopPropagation();sendNotification(u.assignee, u.title)},className:"ml-2 p-2 text-gray-400 hover:text-blue-500 hover:bg-blue-50 rounded-full transition-colors",children:v.jsx(Mail,{size:18})}),'

if search_trash_btn in content:
    content = content.replace(search_trash_btn, mail_btn + search_trash_btn)
else:
    print("Could not find trash button block.")
    exit(1)

with open("assets/index-v2.js", "w") as f:
    f.write(content)

print("Successfully patched assets/index-v2.js")
