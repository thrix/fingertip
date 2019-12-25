import subprocess

import fingertip
from fingertip.util import log


@fingertip.transient
def main(m, cmd=None):
    assert not m._up_counter

    m = m.apply('unseal')

    with m.transient() as m:
        log.info(f'waiting for the SSH server to be up...')
        if cmd is None:
            m.ssh('true')
            log.info(f'starting interactive SSH session, {m.ssh.port}')
            subprocess.run(['ssh',
                            '-o', 'StrictHostKeyChecking=no',
                            '-o', 'GSSAPIAuthentication=no',
                            '-o', 'GSSAPIKeyExchange=no',
                            '-i', m.ssh.key_file,
                            '-p', str(m.ssh.port),
                            '-t',
                            'root@127.0.0.1'])
        else:
            m.ssh(cmd)