import ncs

import _ncs
import sys
import argparse

debug = False

def test1(t):
    root = ncs.maagic.get_root(t)
    at = root.template.apply_config_template
    args = at.get_input()
    args.name = 'frobnicator-foo'
    # Why isn't this working?
    # args.variable.create('DEVICE').value = 'frob0'
    d = args.variable.create()
    d.name = 'DEVICE'
    d.value = 'frob0'
    at(args)

def test2(t, kv):
    root = ncs.maagic.get_root(t)
    at = root.template.apply_config_template
    args = at.get_input()
    args.name = 'frobnicator-rule'
    for k, v in kv.iteritems():
        d = args.variable.create()
        d.name = k
        d.value = v
    at(args)

def dry(m, t):
    r = t.apply_with_result(False, m.COMMIT_NCS_DRY_RUN_NATIVE)
    print r


def main(args):
    if args.debug:
        _ncs.set_debug(ncs.TRACE, sys.stdout)

    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'admin'):
            with m.start_read_trans() as t:
                root = ncs.maagic.get_root(t)
                root.devices.sync_from()
                version = root.ncs_state.version
                print ("Version: %s" % version)
            with m.start_write_trans() as t:
                test2(t, dict(DEVICE='frob0', NAME='rule1',
                              NUMBER=99, ALLOW='true'))
                test2(t, dict(DEVICE='frob0', NAME='rule2',
                              NUMBER=5, ALLOW='false'))
                # dry(m, t)
                t.apply()
    print "DONE"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    main(args)
