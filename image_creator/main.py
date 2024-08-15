from .agents import image_creator

while True:
  task = input("> ")

  result = image_creator.chat(task)

