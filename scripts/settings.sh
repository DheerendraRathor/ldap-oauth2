#!/bin/bash
PORT_PROD=7070
PORT_DEV=7071
KILL=false

if git rev-parse --git-dir > /dev/null 2>&1; then
    : #Valid git repo
else
    >&2 echo "Run this command under git repository"
    exit 1
    : # this is not a git repository
fi

# Get Project root
ROOT="`git rev-parse --show-toplevel`"

while getopts p:s opt; do
  case $opt in
  p)
      PORT_PROD=$OPTARG
      PORT_DEV=$OPTARG
      ;;
  s)
      KILL=true
      ;;
  esac
done