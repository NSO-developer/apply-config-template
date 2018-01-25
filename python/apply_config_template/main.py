# -*- mode: python; python-indent: 4 -*-
#
# Copyright 2017 Sebastian Strollo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import ncs
from ncs import maapi
from ncs.application import Service
from ncs.dp import Action

import _ncs.error

class ApplyTemplate(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info('invoke action %s with template %s' % (name, input.name))

        def apply_template(t, i):
            template = ncs.template.Template(t, i.context_node)
            vars = ncs.template.Variables()
            for v in i.variable:
                vars.add(v.name, v.value)
            template.apply(i.name, vars)

        do_apply = False
        m = maapi.Maapi()
        if uinfo.actx_thandle != -1:
            # When invoked from the CLI we get a transaction
            # Note: unless we are in configure mode it will be read-only
            m.attach2(0, 0, uinfo.actx_thandle)
            trans = maapi.Transaction(m, uinfo.actx_thandle)
        else:
            # Start write transaction and apply it at end
            trans = m.start_write_trans(usid=uinfo.usid)
            do_apply = True

        try:
            apply_template(trans, input)
        except _ncs.error.Error as e:
            if e.confd_errno == ncs.ERR_NOT_WRITABLE:
                # Happens when invoked from the CLI and not in configure mode,
                # assume user wants us to start a separate transaction and
                # apply the template there.
                m.detach(uinfo.actx_thandle)
                trans = m.start_write_trans(usid=uinfo.usid)
                do_apply = True
                apply_template(trans, input)
            else:
                raise e

        if do_apply:
            trans.apply()


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        self.register_action('apply-config-template-action', ApplyTemplate)

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
