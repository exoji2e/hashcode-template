import glob
S = 0
for f in glob.glob('*.max'):
    S += int(open(f, 'r').read())
print(S)
