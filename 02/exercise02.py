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

  def try_consume_token(self, token):
    checkpoint = self.cursor
    self.skip_whites()
    result = not self.ended() and self.doc.find(token, self.cursor, self.cursor + len(token)) >= 0
    if result:
      self.cursor += len(token)
    else:
      self.cursor = checkpoint
    return bool(result)

  def try_consume_string(self):
    checkpoint = self.cursor
    if self.try_consume_token('"'):
      limiter = '"'
    elif self.try_consume_token('\''):
      limiter = '\''
    else:
      self.cursor = checkpoint
      return None

    start = self.cursor
    end = self.doc.find(limiter, start)

    if end < 0:
      raise ParsingException('Expected closing {}'.format(limiter), self)
    self.cursor = end + 1

    return self.doc[start:end]

  def try_consume_number(self):
    checkpoint = self.cursor
    try:
      value = float(self.consume_word())
    except:
      self.cursor = checkpoint
      return None

    return value

  def try_consume_attribute(self):
    checkpoint = self.cursor
    name = self.consume_word()
    if not NAME.match(name):
      self.cursor = checkpoint
      return None

    if not self.try_consume_token('='):
      value = True
    else:
      value = self.try_consume_string() or self.try_consume_number()
      if not value:
        raise ParsingException('Expected string or number', self)

    return (name, value)

  def consume_open_tag(self):
    if not self.try_consume_token('<'):
      return None

    self.skip_whites()
    start = self.cursor
    name = self.consume_word()
    if not NAME.match(name):
      self.cursor = start
      raise ParsingException('Invalid tag name', self)


parser = HTMLParser(' foo = " Heyyyyy! What\'s up? " bar number = -23.75 >')
print(parser.try_consume_attribute())
print(parser.try_consume_attribute())
print(parser.try_consume_attribute())
print(parser.try_consume_token('>'))