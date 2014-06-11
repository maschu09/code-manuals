import os
import shutil
import glob

def clean():
    for f in glob.glob('ttl/*.ttl'):
        os.remove(f)
    for d in os.listdir('ttl/'):
        if not d.startswith('.'):
            shutil.rmtree(os.path.join('ttl', d))

