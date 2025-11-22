
with open("assets/index-0YGQPArK.js", "r") as f:
    content = f.read()

# Locate the problematic assignment: Pm=fe("User",[...]);Trash=fe("Trash"
# I need to change it to: Pm=fe("User",[...]);const Trash=fe("Trash"
# Or simpler: Pm=fe("User",[...]),Trash=fe("Trash" (replacing semicolon with comma if they are in the same const block, but Pm definition ends with ; in the previous inspection provided by code review? actually looking at file content I see: Pm=fe("User",...);function ... )

# Let's search for the string I inserted.
# The insertion was: 'Trash=fe("Trash",[...])' replacing 'function Sd' with 'Trash=fe("Trash",[...])function Sd'
# But wait, in my previous modification script:
# trash_icon_def = 'Trash=fe("Trash",[...]);'
# content = content.replace('function Sd', trash_icon_def + 'function Sd')

# So the result is likely: ...;Pm=fe("User",...);Trash=fe("Trash",...);function Sd...
# The semi-colon after Pm definition makes Pm independent.
# But Trash is new. "Trash=..." is an assignment. Since it's top level scope of the module (or bundle), and strict mode is on, "Trash" must be declared.

# I will replace "Trash=fe" with "const Trash=fe".

target = 'Trash=fe("Trash"'
replacement = 'const Trash=fe("Trash"'

if target in content:
    # Check if it's already "const Trash" (idempotency)
    if "const " + target not in content:
        print("Fixing Trash declaration...")
        content = content.replace(target, replacement)
        with open("assets/index-0YGQPArK.js", "w") as f:
            f.write(content)
        print("Fixed.")
    else:
        print("Trash is already declared with const.")
else:
    print("Target string 'Trash=fe(\"Trash\"' not found.")
