import traceback
import os
import pexpect


class BuzzTestRunner(object):

    def __init__(self, name):
        self._command_list = []
        self.name = name

    def add_command(self, step_name, command_string,
                    check_result_function, repeat_count=1):
        self._command_list.append((step_name, command_string,
                                   check_result_function, repeat_count))

    def run(self, log_dir, prompt=" $", continue_on_error=False,
            addition_switch=None, switch_after=" "):

        output_dir = os.path.join(log_dir, self.name)
        try:
            os.mkdir(output_dir, 0755)
        except:
            pass
        output_file = os.path.join(output_dir, "commands.log")
        command_file = open(output_file, "w")
        error_file_path = os.path.join(output_dir, "errors.log")
        error_file = open(error_file_path, "w")

        # each test will have its own log file
        var_bag = {}
        failed = False
        for name, cmd, result_func, repeat_count in self._command_list:
            if addition_switch:
                ndx = cmd.find(switch_after)
                if ndx > 0:
                    cmd = cmd[:ndx] + " " + addition_switch + " " + cmd[ndx:]
            saved_ex = None

            # before running write everything to the log file
            if result_func.__doc__:
                doc_lines = result_func.__doc__.split(os.linesep)
                for l in doc_lines:
                    command_file.write("# %s%s" % (l, os.linesep))

            # sub in the var bag and long the command
            cmd = cmd % var_bag
            try:
                rc = 1
                repeat_message = ""
                while rc != 0 and repeat_count > 0:
                    command_file.write(repeat_message)
                    command_file.write("# step %s%s" % (name, os.linesep))
                    command_file.write(prompt + cmd + os.linesep)
                    (output, exit_status) = pexpect.run(cmd, withexitstatus=1)
                    command_file.write(output)

                    (rc, var_bag) = result_func(exit_status, output, var_bag)
                    repeat_count = repeat_count - 1
                    repeat_message = "# repeating the command..." + os.linesep
            except Exception, ex:
                rc = False
                error_file.write("%s failed at step %s with exception: %s" %
                                 (self.name, name, ex))
                command_file.write("Exception: %s" % (self.name, name, ex))
                traceback.print_exc(file=error_file)

            if not rc:
                failed = True
                print "%s failed at step %s" % (self.name, name)
                print "   %s" % (cmd)
                print saved_ex
                print "Check output files in %s" % (output_dir)
                if not continue_on_error:
                    return False

        return not failed


# standard check functions
def simple_exit_status_success_check(rc, output, var_bag):
    return (rc == 0, var_bag)


def simple_exit_status_failed_check(rc, output, var_bag):
    return (rc != 0, var_bag)
