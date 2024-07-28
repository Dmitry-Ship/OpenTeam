from .agents import image_creator

while True:
  task = input("\n> ")

  result = image_creator.chat(task)

