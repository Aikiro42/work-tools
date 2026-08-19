# https://stackoverflow.com/questions/66672150/how-to-generate-qr-code-with-python-and-when-scanned-make-it-open-a-url-defined

import sys
from pathlib import Path
from typing import Union
from datetime import datetime, time


def parse_date_string(date_str: str):
    """Parses a date string formatted as 'DD/MM/YYYY'."""
    # strptime returns a full datetime object
    dt = datetime.strptime(date_str, "%d/%m/%Y")
    
    # Return just the date portion
    return dt.date()

def parse_time_string(time_str: str) -> time:
    """Parses a time string formatted as 'HH:MM:SS am/pm' into a datetime.time object.

    Example inputs: '08:30:15 am', '08:30:15 AM', '11:45:00 pm'
    """
    # Clean up leading/trailing whitespaces and parse
    # %I = 12-hour hour (01-12)
    # %M = Minute (00-59)
    # %S = Second (00-59)
    # %p = AM/PM indicator
    dt = datetime.strptime(time_str.strip(), "%I:%M:%S %p")

    # Extract just the time part (hours, minutes, seconds)
    return dt.time()

def read_lines_to_list(filepath: Union[str, Path]) -> list[str]:
    """Reads a text file and returns a list of its lines.

    Strips trailing newlines (\\n) from each line.
    """
    path = Path(filepath)

    with open(path, "r", encoding="utf-8") as file:
        # .rstrip('\r\n') removes trailing newlines while preserving inner line spaces
        return [line.rstrip("\r\n") for line in file]

def write_to_file(filepath: str, text: str, mode: str = "w") -> None:
  """Writes or appends text to a file.

  Modes:
    'w' - Write mode (overwrites existing content)
    'a' - Append mode (adds text to the end of existing content)
  """
  try:
    path = Path(filepath)

    # Create parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode=mode, encoding="utf-8") as file:
      file.write(text)

    print(f"Successfully wrote to: {path.resolve()}")

  except PermissionError:
    print(f"Error: Permission denied for '{filepath}'.", file=sys.stderr)
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":

  path = ""
  if len(sys.argv) > 1:
    path = sys.argv[1]
  else:
    print("Usage: python al_parser.py path/to/file.txt")
    sys.exit(0)
  path = "test.txt"

  outname = "parsed.csv"
  if len(sys.argv) > 2:
    outname = sys.argv[2]

  entries = read_lines_to_list(path)
  entried = {}
  minDate = 0
  maxDate = 0
  for entry in entries:
    sEntryDate, sEntryTime, dayHalf = entry.split(" ")
    sEntryTime += " " + dayHalf.split("/")[0][:2]
    entryDate = parse_date_string(sEntryDate)
    entryTime = parse_time_string(sEntryTime)

    dateKey = entryDate.day

    if minDate == 0 or minDate > dateKey:
      minDate = dateKey
    if maxDate == 0 or maxDate < dateKey:
      maxDate = dateKey
    
    if entried.get(dateKey) is None:
      entried[dateKey] = {}

    def reformatHour(h):
      return h % 12 if h > 12 else h

    if entryTime.hour <= 9:
      entried[dateKey]["amIn"] = f"{reformatHour(entryTime.hour)}:{entryTime.minute:02}"
    
    if 9 < entryTime.hour <= 13 and entried[dateKey].get("amOut") is None:
      entried[dateKey]["amOut"] = f"{reformatHour(entryTime.hour)}:{entryTime.minute:02}"
    
    if 12 <= entryTime.hour <= 15:
      entried[dateKey]["pmIn"] = f"{reformatHour(entryTime.hour)}:{entryTime.minute:02}"
    
    if 15 < entryTime.hour: 
      entried[dateKey]["pmOut"] = f"{reformatHour(entryTime.hour)}:{entryTime.minute:02}"
  
  for k in entried.keys():
    entried[k]["amIn"] = entried[k].get("amIn", '')
    entried[k]["amOut"] = entried[k].get("amOut", '')
    entried[k]["pmIn"] = entried[k].get("pmIn", '')
    entried[k]["pmOut"] = entried[k].get("pmOut", '')

  outmsg = ""
  for i in range(minDate, maxDate+1):
    k = i
    v = entried.get(k)
    if v is None:
      outmsg += f"{k},,,,\n"
    else:
      outmsg += f'{k},{",".join(v.values())}\n'
  
  write_to_file(outname, outmsg)