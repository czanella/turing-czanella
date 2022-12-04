import re

WHITES = set(' \n\r')
NAME = re.compile(r'^[a-z]\w*$', re.I)

class Node:
  def __init__(self, tagName = None, text = None, children = None, attributeMap = None, parent = None):
    self.tagName = tagName
    self.text = text
    self.children = children
    self.attributeMap = attributeMap
    self.parent = parent

class ParsingException(Exception):
  def __init__(self, message, parser):
    super()
    self.message = message
    self.parser = parser

  def __str__(self):
    return '{} on position {}'.format(self.message, self.parser.cursor)


class HTMLParser:
  def __init__(self, doc):
    self.doc = doc
    self.cursor = 0

  def ended(self):
    return self.cursor >= len(self.doc)

  def char(self):
    return self.doc[self.cursor]

  def skip_whites(self):
    while not self.ended() and self.char() in WHITES:
      self.cursor += 1

  def skip_non_whites(self):
    while not self.ended() and self.char() not in WHITES:
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
      raise ParsingException('Expected closing {}'.format(opener), self)

    return self.doc[start:end]

  def consume_number(self):
    start = self.cursor
    try:
      value = float(self.consume_word())
    except:
      self.cursor = start
      return None

    return value

  def consume_attribute(self):
    start = self.cursor
    name = self.consume_word()
    if not NAME.match(name):
      self.cursor = start
      return None

    if not self.consume_token('='):
      value = True
    else:
      value = self.consume_string() or self.consume_number()
      if not value:
        raise ParsingException('Expected string or number', self)

    return (name, value)

  def consume_open_tag(self):
    if not self.consume_token('<'):
      return None

    self.skip_whites()
    start = self.cursor
    name = self.consume_word()
    if not NAME.match(name):
      self.cursor = start
      raise ParsingException('Invalid tag name', self)

    
parser = HTMLParser(' foo = +-.23 bar >')
print(parser.consume_attribute())
print(parser.consume_attribute())
print(parser.consume_token('>'))