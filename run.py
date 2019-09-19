import commands
import os
import sys

from utils import util


def ls(nothing):
    """ List: shows alias/shortcuts of mongo client connection """
    print "total {}".format(len(util.mongos))
    for index, m in enumerate(util.mongos):
        print "{}\t{}".format(index, m)


def add(args):
    """ Add: add a new shortcut of mongo client connection  """
    name = util.get_value_form_option(args, "-n")
    host = util.get_value_form_option(args, "-h")

    # check if name is already exist
    if name in util.mongos:
        util.exception("name {} exists".format(name))

    mongo_cmd = util.get_mongo_command(host)
    if not mongo_cmd:
        return False

    status, msg = util.connection_test(mongo_cmd)
    if not status:
        util.exception(msg)

    util.handler.append(util.generate_alias_string(name, host))

    print """\n----SUCCESS----
mongo client connection shortcut has been added.
usage:
    mongo_[custom name]       # new terminal needed
    mg [custom name]          # with 'mg' command, new terminal will create automatically
    mg [number from 'mg ls']
"""
    return True


def update(args):
    """ Update: find by name or index, remove and start over by adding a new one """
    # TODO just update name or host
    # FIXME update failed, existing alias disappear
    index_or_name = util.get_value_form_option(args, "-u")

    name = util.get_value_form_option(args, "-n")
    host = util.get_value_form_option(args, "-h")

    # check if name is already exist
    if name in util.mongos:
        util.exception("name {} exists".format(name))

    new_alias_string = util.generate_alias_string(name, host)

    alias_string = util.find_alias_string(index_or_name)
    for s in alias_string:
        util.handler.update(s, new_alias_string)


def delete(args):
    """ Delete: remove alias by name or index """
    index_or_name = util.get_value_form_option(args, "-d")

    alias_string = util.find_alias_string(index_or_name)
    for s in alias_string:
        util.handler.delete(s)

    print "Done"


def help(args):
    """ Help: shows helping information """
    pass


def run(name):
    """ run mongo client shortcuts """
    if name in util.mongos:
        # TODO supporting no one but 'guake' on ubuntu, solve it
        commands.getoutput('guake -n NEW -e "mongo_{}"'.format(name))
        # commands.getoutput('mongo 192.168.4.75')
        # print commands.getoutput('"mongo_{}"'.format(name))

        exit(0)


def _run_local(name="local"):
    """ run mongo client shortcuts for local service """
    cmd = "mongo_{}".format(name)
    ok, msg = util.connection_test(cmd)
    if not ok:
        print msg

    if name in util.mongos:
        # TODO supporting no one but 'guake' on ubuntu, solve it
        util.new_guake(cmd)
        # commands.getoutput('mongo 192.168.4.75')
        # print commands.getoutput('"mongo_{}"'.format(name))

        exit(0)

    # local does not exist
    # try 127.0.0.1 and local ip in LAN
    ip_addresses = ["127.0.0.1", util.local_ip_address]
    for ip in ip_addresses:
        if _try_adding_and_running(name=name, ip_address=ip):
            _run_local()

    util.exception("failed to connect local mongo service")


def _try_adding_and_running(name, ip_address):
    print "\ntrying {}".format(ip_address)

    try:
        if not add(["-n", name, "-h", ip_address]):
            return False
        util.mongos.append(name)
        return True

    except IOError as e:
        if str(e).endswith("Server is not running"):
            print e
            return False


def main():
    if len(sys.argv) == 1:
        print "default option: running local mongod service"
        _run_local()

    name = sys.argv[1]
    run(name)

    try:
        int(sys.argv[1])  # just for triggering the ValueError
        name = util.get_name_or_by_index(sys.argv[1])
        run(name)
    except ValueError:
        pass

    options_map = {
        # TODO make it looks like 'ls/-l'
        # TODO make this choices as a conts instead of string, which may cause so much time on finding and changing it
        "ls": ls,
        "add": add,
        "-l": ls,
        "-a": add,
        "-d": delete,
        "-u": update,
        "--help": help
    }
    option = sys.argv[1]
    fn = options_map.get(option)
    HELP = option == "--help"
    if not fn or HELP:
        msg = "unknown option or shortcut '{}'\n".format(option) if not HELP else "Help\n"
        msg += "  available options:\n"

        option_list = []
        for k in options_map:
            option_list.append("  " + k + "\t" + options_map[k].__doc__)

        option_list.append("\n  [name/index from 'ls/-l']\n\t" + run.__doc__)

        msg += "\n".join(option_list)

        if not HELP:
            util.exception(msg)
        else:
            print msg

    fn(sys.argv[1:])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nKeyboardInterrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
