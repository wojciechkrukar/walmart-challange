import json

nb = json.load(open('analysis.ipynb'))
cells = nb['cells']

old_frag = (
    "   What would change our minds:\n"
    "   - If, on a fresh 8-quarter held-out window (2022\u20132023), the delta MAPE falls below 0 pp,\n"
    "     we would downgrade the signal to \"inconclusive\"."
)
new_frag = (
    "   What would change our minds:\n"
    "   - If a fresh held-out window of at least eight quarters beginning no earlier than 2026 Q2\n"
    "     produces an M1 OOS MAPE improvement of less than 0.25 pp over SN-A, we would conclude\n"
    "     the signal has degraded and recommend withdrawing the product."
)

changed = 0
for i, cell in enumerate(cells):
    src = ''.join(cell['source'])
    if old_frag in src:
        new_src = src.replace(old_frag, new_frag, 1)
        lines = new_src.splitlines(keepends=True)
        cells[i]['source'] = lines
        changed += 1
        print(f'Patched cell index {i} (cell number {i+1})')

if changed == 0:
    print('ERROR: fragment not found')
else:
    with open('analysis.ipynb', 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print('Saved successfully.')
