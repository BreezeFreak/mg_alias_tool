import os
import sys

from utils.FileHandler import TextHandler
from utils import util

shell_rc_path = util.backup()
current_script_path = os.getcwd() + "/run.py"

handler = TextHandler(shell_rc_path)

alias_name = "mg" if len(sys.argv) < 2 else sys.argv[1]

alias_string = 'alias {}="python {}"'.format(alias_name, current_script_path)

if handler.find('\nalias {}="python {}"'.format(alias_name, current_script_path)):
    print "This mongo tool has been installed."
    exit(1)

handler.append(alias_string)

print "Successfully installed. Start a new terminal tab and try command '{}'!".format(alias_name)
