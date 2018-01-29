import yaml
document = """
  a: 1
  b:
    c: 3
    d: 4
"""
print(yaml.dump(yaml.load(document)))


"""
 - Language: Julia
 - Language: Go
 - Language: Python
 - Language: Java
 - Language: c
 - Language: vhdl
 - Language: Haskell
"""
