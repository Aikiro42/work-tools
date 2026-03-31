
def formalize(statement: str) -> str:
  new_statement = statement.lower()
  new_statement.replace("helped")
  return new_statement

if __name__ == "__main__":
  text = ""
  paragraphs = [paragraph.split(".") for paragraph in text.split("\n")]

  for paragraph in paragraphs:
    for statement in paragraphs:
      formalized = formalize(statement)