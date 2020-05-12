#!/usr/bin/env python3
#
#  Copyright 2011-2020 Gregory Banks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import sys
import os
import re

ifdef_re = re.compile(r'^@ifdef\s+(\S+)\s*$')
else_re = re.compile(r'^@else\s*$')
endif_re = re.compile(r'^@endif\s*$')
reference_re = re.compile(r'@([a-zA-Z_][a-zA-Z0-9_]*)@')

def filter_file(fin, fout, defines):
    stack = []
    for line in fin:
        line = line.rstrip("\r\n")

        m = ifdef_re.match(line)
        if m is not None:
            stack.append(m.group(1) in defines)
            continue

        m = else_re.match(line)
        if m is not None:
            if len(stack) == 0:
                raise RuntimeError("@else without @ifdef")
            stack[-1] = not stack[-1]
            continue

        m = endif_re.match(line)
        if m is not None:
            if len(stack) == 0:
                raise RuntimeError("@endif without @ifdef")
            stack.pop(-1)
            continue

        if len(stack) == 0 or stack[-1]:
            while True:
                m = reference_re.search(line)
                if not m:
                    break
                name = m.group(1)
                if name not in defines:
                    raise RuntimeError("undefined variable {}".format(name))
                line = line[0:m.start()] + str(defines[name]) + line[m.end():]
            fout.write(line + "\n")

def main():
    # This statement used to be true in Python v2
    # now the only reason we're not using argparse
    # is inertia:
    # Cannot rely on argparse being present
    # so we parse args ourselves.
    defines = {}
    for a in sys.argv[1:]:
        if a.startswith('-D'):
            if "=" in a:
                name, value = a[2:].split("=", 1)
            else:
                name = a[2:]
                value = 1
            defines[name] = value
        else:
            raise RuntimeError("Unknown option \"%s\"" % a)
    filter_file(sys.stdin, sys.stdout, defines)

if __name__ == "__main__":
    main()
