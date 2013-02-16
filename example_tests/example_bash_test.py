import buzzclitester

def make_temp_check(rc, output, var_bag):
    if rc != 0:
        return (False, var_bag)

    # add the file name to the var bag
    var_bag['filename'] = output.strip()
    return (True, var_bag)

def load_test_object():
    runner = buzzclitester.BuzzTestRunner("BashExample")
    runner.add_command("Create a temp file",
                       "mktemp",
                       make_temp_check)
    runner.add_command("Take a look at the newly made file",
                       "stat %(filename)s",
                       buzzclitester.simple_exit_status_success_check)
    runner.add_command("Copy a known file to the file name",
                       "cp /etc/group %(filename)s",
                       buzzclitester.simple_exit_status_success_check)
    runner.add_command("Verify that the files are the same",
                       "cmp /etc/group %(filename)s",
                       buzzclitester.simple_exit_status_success_check)
    runner.add_command("Delete the file",
                       "rm %(filename)s",
                       buzzclitester.simple_exit_status_success_check)

    return runner
