# This should be placed in <nmag-dir>/nsim/interface/nsim/shell.py

# Nmag micromagnetic simulator
# Copyright (C) 2010 University of Southampton
# Hans Fangohr, Thomas Fischbacher, Matteo Franchin and others
#
# WEB:     http://nmag.soton.ac.uk
# CONTACT: nmag@soton.ac.uk
#
# AUTHOR(S) OF THIS FILE: Matteo Franchin
# LICENSE: GNU General Public License 2.0
#          (see <http://www.gnu.org/licenses/>)

'''
Provide means of starting a new Python interactive loop from Python
and provides the main startup code for nsim.
'''

import sys
from code import InteractiveConsole

class Shell(InteractiveConsole):
    def __init__(self, locals=None, filename='<console>'):
        InteractiveConsole.__init__(self, locals=locals, filename=filename)

    def interact(self, banner=''):
        return InteractiveConsole.interact(self, banner=banner)

def ipython(globals=None, locals=None):
    """Interactive python prompt (see :ref:`Example: IPython <example IPython>`)."""
    # We use an embedded ipython session
    # (http://ipython.scipy.org/doc/manual/node9.html)
    # to inspect the current state. The calling_frame magic is necessary
    # to get the context of the place where this ipython() function is called
    # (and not where IPShellEmded([]) is invoked.
    calling_frame = sys._getframe(1)
    if globals == None:
        globals = calling_frame.f_globals
    if locals == None:
        locals = calling_frame.f_locals
    import IPython
    IPython.embed()#(local_ns=locals, global_ns=globals)
    #from IPython.Shell import IPShellEmbed
    #IPShellEmbed([])(local_ns=locals, global_ns=globals)


def traceback_chain(tb):
    """Returns the list of traceback objects chained with tb."""
    chain = []
    while tb is not None:
        chain.append(tb)
        tb = tb.tb_next
    return chain

def partial_traceback(start_tb=0):
    try:
        from traceback import format_exception
        etype, value, tb = sys.exc_info()
        tb = sys.exc_info()[2]
        tb_chain = traceback_chain(tb)
        if start_tb < len(tb_chain):
            my_tb = tb_chain[start_tb]
        else:
            my_tb = tb
        return ''.join(format_exception(etype, value, my_tb))

    finally:
        etype = value = tb = None

def main(args, locals=None, globals=None, use_ipython=True):
    import os.path
    from nsim.setup import setup
    options, arguments = setup(argv=args[1:], warn_about_py_ext=False)
    sys.argv = arguments

    if len(arguments) > 0:
        # Execute a file
        try:
            script_path = os.path.realpath(os.path.split(arguments[0])[0])
            sys.path.insert(0, script_path)
            old__file__ = locals.get("__file__", None)
            locals["__file__"] = arguments[0]
            execfile(arguments[0], globals, locals)
            if old__file__:
              locals["__file__"] = old__file__

        except SystemExit, exit_status:
            import logging
            log = logging.getLogger('')
            log.warn("SystemExit with exit_status=%s" % exit_status)
            sys.exit(exit_status)

        except:
            # We now take the traceback, show it on the screen and also put
            # it into the log file, so that we record the reason for the
            # interruption
            tb_msg = partial_traceback(1)
            import logging
            log = logging.getLogger('')
            log.error("Exit on exception:\n%s" % tb_msg)
            sys.exit(1)

    else:
        # Run the interactive loop

        # We should use ipython, when possible
        try:
            import IPython
            import readline
            # ^^^ It turns out that even if "import IPython" works, readline
            # support may not be installed, leading to a failure subsequently
            # when the shell is launched.

        except:
            use_ipython = False

        if use_ipython:
            # Better to use ipython from nsim.snippets rather than the one
            # in nmag. Indeed, importing nmag, causes a lot of other modules
            # to be imported which can result in slow startup of the shell
            # on older machines.
            ipython(locals=locals, globals=globals)

        else:
            sh = Shell()
            sh.interact()

