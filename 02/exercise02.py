import re

class Node:
  def __init__(self, tagName, text, children, attributeMap, parent):
    self.tagName = tagName
    self.text = text
    self.children = children
    self.attributeMap = attributeMap
    self.parent = parent

whites = set(' \n\r')
numbers = set('0123456789.')
attribute_name = re.compile(r'^[a-z]\w*$', re.I)

class ParsingException(Exception):
  def __init__(self, message, cursor):
    super()
    self.message = message
    self.cursor = cursor

  def __str__(self):
    return '{} on position {}'.format(self.message, self.cursor)

class HTMLParser:
  def __init__(self, doc):
    self.doc = doc
    self.cursor = 0

  def ended(self):
    return self.cursor >= len(self.doc)

  def char(self):
    return self.doc[self.cursor]

  def skip_whites(self):
    while not self.ended() and self.char() in whites:
      self.cursor += 1

  def skip_non_whites(self):
    while not self.ended() and self.char() not in whites:
      self.cursor += 1

  def consume_word(self):
    self.skip_whites()
    start = self.cursor
    self.skip_non_whites()
    end = self.cursor

    return '' if self.ended() else self.doc[start:end]

  def consume_token(self, token):
    self.skip_whites()
    result = not self.ended() and self.doc.find(token, self.cursor, self.cursor + len(token)) >= 0
    if result:
      self.cursor += len(token)
    return bool(result)

  def consume_string(self):
    if self.consume_token('"'):
      opener = '"'
    elif self.consume_token('\''):
      opener = '\''
    else:
      return None

    start = self.cursor
    while not self.ended() and self.char() != opener:
      self.cursor += 1
    end = self.cursor

    if not self.consume_token(opener):
      raise ParsingException('Expected closing {}'.format(opener), self.cursor)

    return self.doc[start:end]

  def consume_number(self):
    self.skip_whites()
    start = self.cursor
    self.consume_token('-')
    dot_found = False
    while not self.ended() and self.char() in numbers:
      if self.char() == '.':
        if dot_found:
          raise ParsingException('Unexpected .', self.cursor)
        dot_found = True
      self.cursor += 1

    if start == self.cursor or self.doc[self.cursor - 1] == '-':
      self.cursor = start
      return None

    end = self.cursor
    return float(self.doc[start:end])

  def consume_attribute(self):
    start = self.cursor
    name = self.consume_word()
    if not attribute_name.match(name):
      self.cursor = start
      return None

    if not self.consume_token('='):
      value = True
    else:
      value = self.consume_string() or self.consume_number()
      if not value:
        raise ParsingException('Expected string or number', self.cursor)

    return (name, value)

parser = HTMLParser(' foo = 23 bar >')
print(parser.consume_attribute())
print(parser.consume_attribute())
print(parser.consume_token('>'))