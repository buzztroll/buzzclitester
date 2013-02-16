import optparse
import tempfile
import os
import sys


def run_directory(path, logdir, prompt, continue_on_error=False):

    print "Logs will be place under the directory %s" % (logdir)
    if not os.path.isdir(path):
        raise Exception("Pass in a directory")

    init_file_path = os.path.join(path, "__init__.py")
    if not os.path.exists(init_file_path):
        raise Exception(('the directory must be a submodule. '
                         'Create __init__.py'))

    # remove trailing / for dirname
    while path.endswith("/"):
        path = path[:-1]

    # add the higher level dir to the path
    mod_path = os.path.dirname(path)
    mod_base_name = os.path.basename(path)
    sys.path.append(mod_path)

    # get the submodules in the directory
    used_names = []
    runner_list = []
    for sub_mod_name in os.listdir(path):
        if sub_mod_name.endswith("test.py"):
            full_mod_name = "%s.%s" % (mod_base_name, sub_mod_name[:-3])
            base_mod = __import__(full_mod_name)
            sub_mod = getattr(base_mod, sub_mod_name[:-3])
            if getattr(sub_mod, "load_test_object", None):
                print "loading %s" % sub_mod_name
                runner = sub_mod.load_test_object()
                if runner.name in used_names:
                    raise Exception(("The name %s is aleady used.  "
                                     "%s is trying to reuse it"
                                     % (runner.name, sub_mod_name)))
                runner_list.append(runner)
                used_names.append(runner.name)

    for runner in runner_list:
        print "Running %s" % (runner.name)
        rc = runner.run(logdir, prompt=prompt)
        if not rc:
            print "... failed"
            if not continue_on_error:
                return False
        else:
            print "... passed"


def main():
    parser = optparse.OptionParser(usage="hello")
    parser.add_option("-l", "--logdir", dest="logdir",
                      help="The directory where the logs will be stored",
                      default=None)
    parser.add_option("-c", "--continue", dest="c_on_error",
                      help="Continue to run tests when an error occurs.",
                      default=True)
    parser.add_option("-p", "--prompt", dest="prompt",
                      help="The command prompt to place in the output logs.",
                      default="$ ")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        print "You must provide a path to your test modules"
        sys.exit(1)

    if options.logdir is None:
        options.logdir = tempfile.mkdtemp()
    rc = run_directory(args[0],
                       options.logdir,
                       options.prompt,
                       continue_on_error=options.c_on_error)
    return rc
