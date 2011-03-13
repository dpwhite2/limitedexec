import os
import os.path
import time
from subprocess import Popen, PIPE, STDOUT

ROOT_DIR = os.getcwd()
LTDEXEC_DIR =       'ltdexec'
LTDEXEC_PATH =       os.path.join(ROOT_DIR, LTDEXEC_DIR)
FUNCTESTS_DIR =      'tests_functional'
FUNCTESTS_PATH =     os.path.join(ROOT_DIR, FUNCTESTS_DIR)
EXCLUDE_FILES = set(('__init__.py','_runtest.py'))
PYTHON = 'python'
RUNNER = '_runtest.py'
RUNNER_FILEPATH =   os.path.join(FUNCTESTS_PATH, RUNNER)

MAXWAIT_TIME = 5.0
POLL_INTERVAL = 0.01

def init_tests():
    pypath = os.environ.get('PYTHONPATH','')
    rootpath = ROOT_DIR
    if pypath:
        pypath = pypath + os.pathsep + rootpath
    else:
        pypath = rootpath
    os.environ['PYTHONPATH'] = rootpath

def list_test_filenames():
    names = os.listdir(FUNCTESTS_PATH)
    filtered_names = []
    for name in names:
        if name.endswith('.py') and name not in EXCLUDE_FILES:
            filtered_names.append(name)
    return filtered_names
    
class Test(object):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        ##self.output = None
        ##self.err = None
        self.proc = None
        self.result = None
        self.passed = None
        
    def run(self, timeout):
        self.start = time.time()
        try:
            cwd = FUNCTESTS_PATH
            self.proc = Popen([PYTHON, RUNNER_FILEPATH, self.name], cwd=cwd) #, stdout=PIPE, stderr=STDOUT)
            if not self.wait(timeout):
                self.result = -1
            else:
                self.result = self.proc.returncode
            ##self.output = self.proc.stdout.read()
            ##self.err = self.proc.stderr.read()
        except:
            if self.proc and self.proc.poll() is None:
                self.proc.kill()
            raise
        if self.result==0:
            self.passed = True
        else:
            self.passed = False
        
    def wait(self, timeout):
        start = self.start
        proc = self.proc
        success = True
        while proc.poll() is None:
            if time.time()-start > timeout:
                break
            time.sleep(POLL_INTERVAL)
        if proc.poll() is None:
            print 'terminating test {0}'.format(self.name)
            proc.terminate()
            success = False
        return success

    
def run_test(name, filename):
    print '{0}...'.format(name),
    test = Test(name, filename)
    test.run(MAXWAIT_TIME)
    if test.passed:
        print '...passed.\n'
    else: 
        print '...FAILED!!!\n'
    return test.passed
    
def main():
    init_tests()
    names = list_test_filenames()
    for name in names:
        filename = os.path.join(FUNCTESTS_PATH, name)
        res = run_test(name, filename)
        if not res:
            break
        
main()


