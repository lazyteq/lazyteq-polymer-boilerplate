#!/usr/bin/env python
import sys
import os


def mywalk(root):   
    for fname in os.listdir(root):
        if not(fname == 'rename.py' or fname.startswith('.')):
            path = os.path.join(root, fname)
            if os.path.isdir(path):
                for p in mywalk(path):
                    yield p
            else:
                yield path
    

def main(element_name="my-element", repo_name=False, user_name=False):
    repo_dir = os.path.dirname(__file__)
    
    old_element_name = 'my-element'
    old_repo_name = 'my-repo'
    old_user_name = 'my-user'
    try:
        with open(os.path.join(repo_dir, '.project_name')) as f:
            a = ''.join(f.read().split()).split(':')
            old_element_name = a[0]
            old_repo_name = a[1]
            old_user_name = a[2]
    except:
        pass
    
    
    if not repo_name:
        repo_name = element_name
    if not user_name:
        try:
            user_name = os.popen('git config user.name').read().strip()
        except:
            user_name = 'my-user'

    element_name = str(element_name)
    repo_name = str(repo_name)
    user_name = str(user_name)
    print("Renaming polymer component project...")
    print("\tElement name " + old_element_name + " -> " + element_name) 
    print("\tRepository name " + old_repo_name + " -> " + repo_name)
    print("\tUser (Github) name " + old_user_name + " -> " + user_name)
    
    print("")
    for path in mywalk(repo_dir):
        print("Renaming in file: " + path)
        t = ''
        with open(path) as f:
            t = f.read().replace(old_element_name, element_name).replace(old_repo_name, repo_name).replace(old_user_name, user_name)
        with open(path, 'w') as f:
            f.write(t)
        if old_element_name in path:
            os.rename(path, path.replace(old_element_name, element_name))
            
    with open(os.path.join(repo_dir, '.project_name'), 'w') as f:
        f.write(':'.join([element_name, repo_name, user_name]))
        
    
    
if __name__ == '__main__':
    main(*sys.argv[1:])