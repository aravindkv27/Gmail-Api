import json

predicate = json.load(open('rules.json'))

value = predicate["4"]['value']
print(value)