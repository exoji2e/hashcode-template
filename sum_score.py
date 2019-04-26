import glob
S = 0
for f in glob.glob('*.max'):
    v = int(open(f, 'r').read())
    print('{}: {}'.format(f.replace('.max', ''), v))
    S += v
print('Total: {}'.format(S))
