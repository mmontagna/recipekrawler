import argparse
import json
import pint

unit_registry = pint.UnitRegistry()


def extract_quantity(ingredient):
  quantity = []
  i = 0
  for char in ingredient:
    if char.isnumeric():
      quantity.append(char)
    elif not char.isspace():
      break
    i += 1
  return i, "".join(quantity)

def extract_unit(ingredient):
  i = 0
  for word in ingredient.split(" "):
    i += len(word) + 1
    try:
      if getattr(unit_registry, word) and not getattr(unit_registry, word).dimensionless:
        return i, word
    except Exception:
      pass
  return i, None

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--input-file', type=str, required=True)
  parser.add_argument('--output-file', type=str, required=True)
  args = parser.parse_args()

  recipes = set()



  print(args.input_file)
  with open(args.output_file, 'w') as wf:
    with open(args.input_file) as f:
      for line in f:
        recipe = json.loads(line)
        if recipe['title'] not in recipes:
          recipes.add(recipe['title'])
          instructions = recipe['instructions'].split(" ")
          instructions = [x for x in instructions if x.lower() not in ('advertisement') and x]

          ingredients = recipe['ingredients']
          recipe['ingredients'] = []

          for i in range(len(ingredients)):
            ingredient = ingredients[i]
            x, qnt = extract_quantity(ingredient)
            y, unit = extract_unit(ingredient)

            recipe['ingredients'].append({
              'quantity': qnt,
              'unit': unit,
              'item': ingredient[max(y,x):]
            })

          print recipe
          wf.write(json.dumps(recipe).encode('utf8'))

        else:
          print("dupe", recipe['title'])
        print("\n-----\n")
