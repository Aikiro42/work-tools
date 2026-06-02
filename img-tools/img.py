
import os, sys, re, io
from typing import Callable
from math import floor, sqrt

# import fitz
# from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image, ImageFile

def core_parseCmd():
  argv = sys.argv[1:]  # skip script name

  vars = {}
  args = []
  flags = []

  for arg in argv:
    if "=" in arg:
      var, val = arg.split("=", 1)
      var = var.removeprefix("--").removeprefix("-")
      vars[var] = val
    elif arg.startswith("-"):
      flags.append(arg)
    else:
      args.append(arg)

  return args, flags, vars

def cmd_compress(): ...
def cmd_convert(): ...

FUNCTIONS = {
  "compress": cmd_compress,
  "convert": cmd_convert,
}
DOCS = {}

DEBUG = True

def mainHelp():
  print(f"Usage:\n")
  print(f"  python img.py <function> <pdf/folder path> <function args>\n")
  print(f"Functions:\n")
  for f in FUNCTIONS.keys():
    print(f"  {f}")
  print()

if __name__ == "__main__":
  if DEBUG:
    args, flags, vars = core_parseCmd()
    fn = args[0]
    path = args[1]
    args = args[2:]
    # print(fn, path, args, flags, vars)
    FUNCTIONS[fn](path, flags, vars, *args)
  else:
    if len(sys.argv) < 2:
      mainHelp()
    else:
      try:
        args, flags, vars = core_parseCmd()
        fn = args[0]
        try:
          path = args[1]
          args = args[2:]
          # print(fn, path, args, flags, vars)
          FUNCTIONS[fn](path, flags, vars, *args)
        except Exception:
          DOCS.get(fn, mainHelp)()
      except Exception:
        mainHelp()
