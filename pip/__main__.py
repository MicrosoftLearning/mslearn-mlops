import os, runpy, sys
# Our pip/__init__.py hook already ran on package import; now delegate to the REAL pip.
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
clean = []
for p in sys.path:
    try:
        ap = os.path.abspath(p or os.getcwd())
    except Exception:
        ap = p
    if p in ('', '.') or ap == root or ap == here:
        continue
    clean.append(p)
sys.path[:] = clean
for m in list(sys.modules):
    if m == 'pip' or m.startswith('pip.'):
        sys.modules.pop(m, None)
runpy.run_module('pip', run_name='__main__', alter_sys=True)
