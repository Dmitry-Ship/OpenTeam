from .agents import image_creator_flux

while True:
  task = input("> ")

  result = image_creator_flux.chat(task)

