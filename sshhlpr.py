#!/usr/bin/env python3

import os
import re
import sys
import argparse
import subprocess

#
# Variables and constants
#

sshconfig="~/.ssh/config"

DEBUGMODE=False

#
# Stand ins
#

def Msg(msg, output=sys.stdout):
	"""Msg Stand in"""

	print(msg, file=output)

def DbgMsg(msg, output=sys.stdout):
	"""Dbg Msg Stand in"""

	global DEBUGMODE

	if DEBUGMODE:
		Msg(msg,output)

def DebugMode(flag=None):
	"""DebugMode Stand in"""

	global DEBUGMODE

	if flag:
		DEBUGMODE = flag

	return DEBUGMODE

#
# Functions
#

def PrintAlias(alias, lines, print_config=False):
	"""Print Alias"""

	Msg(f">>> {alias}")

	if print_config:
		for line in lines:
			line = line.strip()

			if line != "":
				Msg(f"\t{line}")

def SearchAlias(args):
	"""Search Aliases"""

	global sshconfig

	pattern = ".+"

	if args.options:
		pattern = args.options

	exp = re.compile(pattern)
	comment = re.compile(r"^\s*#")
	info_comment = re.compile(r"^\s*#\s+info\s+(?P<aliasinfo>.+)")
	host_exp = re.compile(r"^\s*host\s+(?P<aliases>.+)", re.IGNORECASE)

	filename = os.path.expanduser(sshconfig)

	with open(filename,"rt") as config:
		alias = None
		lines = None

		for line in config:
			line = line.strip()

			match = host_exp.search(line)

			if match:
				if alias and exp.search(alias) and len(lines) > 0:
					PrintAlias(alias, lines, args.details)

				alias = match.group("aliases")
				lines = list()
			elif alias:
				match = info_comment.search(line)

				if match:
					lines.append(f"Description : {match.group('aliasinfo')}")
				elif not comment.search(line):
					lines.append(line)

def SearchAll(args):
	"""Search entire Config"""

	pass

#
# Main Loop
#

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("-c", "--config", help="Alternate SSH Config")
	parser.add_argument("-d", "--debug", action="store_true", help="Enter Debug Mode")
	parser.add_argument("--details", action="store_true", help="Show config definition/details")
	parser.add_argument("operation", choices=[ "alias", "search" ], help="Operation to carry out")
	parser.add_argument("options", nargs="?", default=None, help="Options for operation")

	args = parser.parse_args()

	DebugMode(args.debug)

	if args.operation == "alias":
		SearchAlias(args)
	elif args.operation == "search":
		SearchAll(args)
