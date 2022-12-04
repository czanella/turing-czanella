import re

WHITES = set(' \n\r')
NAME = re.compile(r'[a-z][a-z0-9-]*', re.I)

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
    if self.ended():
      return ''

    start = self.cursor
    self.skip_non_whites()
    end = self.cursor

    return self.doc[start:end]

  def try_consume_token(self, token):
    checkpoint = self.cursor
    self.skip_whites()
    result = not self.ended() and \
      self.doc.find(token, self.cursor, self.cursor + len(token)) >= 0
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

  def try_consume_name(self):
    checkpoint = self.cursor
    self.skip_whites()
    start = self.cursor
    token = self.consume_word()
    match = NAME.match(token)
    if match and match.start() == 0:
      self.cursor = start + match.end()
      return token[:match.end()]
    else:
      self.cursor = checkpoint
      return None

  def try_consume_attribute(self):
    name = self.try_consume_name()
    if name is None:
      return None

    if not self.try_consume_token('='):
      value = True
    else:
      value = self.try_consume_string() or self.try_consume_number()
      if not value:
        raise ParsingException('Expected string or number', self)

    return (name, value)

  def try_consume_open_tag(self):
    if not self.try_consume_token('<'):
      return None

    self.skip_whites()
    tag_name = self.try_consume_name()
    if tag_name == None:
      raise ParsingException('Invalid tag name', self)

    attributes = {}
    attribute = self.try_consume_attribute()
    while attribute is not None:
      name, value = attribute
      attributes[name] = value
      attribute = self.try_consume_attribute()

    if not self.try_consume_token('>'):
      raise ParsingException('> expected', self)

    return Node(tagName=tag_name, attributeMap=attributes)

  def try_consume_close_tag(self):
    checkpoint = self.cursor
    result = self.try_consume_token('<') and \
      self.try_consume_token('/') and \
      ((name := self.try_consume_name()) != None) and \
      self.try_consume_token('>')

    if not result:
      self.cursor = checkpoint
      return None
    return name

  def consume_text_node(self):
    if self.ended():
      return None

    start = self.cursor
    end = self.doc.find('<', start)
    if end <= start:
      return None

    self.cursor = end
    return Node(text=self.doc[start:end])

  def try_consume_node(self):
    node = self.try_consume_open_tag()
    if node is None:
      return None

    node.children = []
    while True:
      close_tag = self.try_consume_close_tag()
      if close_tag != None:
        if close_tag != node.tagName:
          raise ParsingException('Wrong closing tag: {} - expected {}'.format(close_tag, node.tagName), self)
        else:
          break

      child_node = self.try_consume_node()
      if child_node is not None:
        node.children.append(child_node)

      child_text = self.consume_text_node()
      if child_text is not None:
        node.children.append(child_text)

      if child_text is None and child_node is None:
        raise ParsingException('Expected closing tag for {}'.format(node.tagName), self)

    for child in node.children:
      child.parent = node

    return node

# parser = HTMLParser('<span>Hey <p font="helvetica">bro</p>! What\'s up?</span>')
parser = HTMLParser('<p font-family="  helvetica   ">   </p>')
node = parser.try_consume_node()
print(node.tagName)
print(node.attributeMap)