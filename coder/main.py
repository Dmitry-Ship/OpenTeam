from .agents import engeneer

engeneer.chat("You will need to work on the codebase in the current directory. For now, read all the files, try to understand them and wait for next instructions.")
while True:
  task = input("\n> ")

  engeneer.chat(task)