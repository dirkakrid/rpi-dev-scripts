#!/usr/bin/env python3

# Copyright (c) 2016 Stephen Warren <swarren@wwwdotorg.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import fnmatch
import os
import shutil
import subprocess
import sys
import tempfile

def push_file(mount_point, local_path, remote_name):
    print('..PUSH FILE: ' + remote_name)
    shutil.copyfile(local_path, os.path.join(mount_point, remote_name))

def op_push_dir(mount_point, local_dir):
    print('PUSH DIR: ' + local_dir)
    for de in os.scandir(local_dir):
        if not de.is_file():
            print('Can\'t handle non-file "%s"' % de.path, file=sys.stderr)
            sys.exit(1)
        push_file(mount_point, de.path, de.name)

def op_rm_list(mount_point, rm_list_file):
    print('RM LIST: ' + rm_list_file)
    existing_files = []
    for de in os.scandir(mount_point):
        if de.is_file():
            existing_files.append(de.name.lower())

    with open(rm_list_file, 'rt') as fh:
        for l in fh:
            l = l.split('#')[0]
            rmspec = l.strip().lower()
            if not rmspec:
                continue
            for remote_filename in existing_files[:]:
                if fnmatch.fnmatch(remote_filename, rmspec):
                    print('..DELETE: ' + remote_filename)
                    os.remove(os.path.join(mount_point, remote_filename))
                    existing_files.remove(remote_filename)

op_map = {
    'push': op_push_dir,
    'rmlist': op_rm_list,
}

def main():
    parser = argparse.ArgumentParser(
        description='Copy files to a mountable disk')
    parser.add_argument('blockdev', help='The block device to copy to')
    parser.add_argument('ops', nargs='+', help='''Operations to perform;
    "dir", "push:dir": push directory, "rmlist:listfile": delete files listed
    in listfile''')
    args = parser.parse_args()

    mount_point = tempfile.mkdtemp()
    # Deliberately not using TemporaryDirectory, so that if the umount fails,
    # the cleanup won't delete the entire content of the mounted blockdev.
    try:
        subprocess.check_call(['mount', args.blockdev, mount_point])
        try:
            for op in args.ops:
                if not ':' in op:
                    func = op_push_dir
                    param = op
                else:
                    (op_name, param) = op.split(':', 1)
                    if op_name not in op_map:
                        print('"%s" is not a valid operation' % op_name,
                            file=sys.stderr)
                        parser.print_help(file=sys.stderr)
                        sys.exit(1)
                    func = op_map[op_name]
                func(mount_point, param)
        finally:
            subprocess.check_call(['umount', mount_point])
    finally:
        os.rmdir(mount_point)

if __name__ == '__main__':
    main()
