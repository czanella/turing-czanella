import re

WHITES = set(' \n\r')
NAME = re.compile(r'[a-z][a-z0-9-]*', re.I)


class Node:
  '''Represents each node in a parsed HTML document.'''
  def __init__(self, tagName = None, text = None, children = None, attributeMap = None, parent = None):
    self.tagName = tagName
    self.text = text
    self.children = children
    self.attributeMap = attributeMap
    self.parent = parent


class ParsingException(Exception):
  '''Exception thrown when HTMLParser is trying to parse a malformed HTML document.'''
  def __init__(self, message, parser):
    super()
    self.message = message
    self.parser = parser

  def __str__(self):
    return '{} on position {}'.format(self.message, self.parser.cursor)


class HTMLParser:
  '''Parses an HTML document.

  * Constructor: HTMLParser(doc)
  - doc: a String containing the HTML information to be parsed
  '''
  def __init__(self, doc):
    self.doc = doc
    self.cursor = 0

  def ended(self):
    '''Checks if the entire document has been consumed'''
    return self.cursor >= len(self.doc)

  def char(self):
    '''Returns the document character at the current parsing cursor position'''
    return self.doc[self.cursor]

  def skip_whites(self):
    '''Moves the cursor forward until a non-space character is found'''
    while not self.ended() and self.char() in WHITES:
      self.cursor += 1

  def skip_non_whites(self):
    '''Moves the cursor forward until a space character is found'''
    while not self.ended() and self.char() not in WHITES:
      self.cursor += 1

  def consume_word(self):
    '''Consumes a sequence of non-space characters
    
    Returns: a string contining the consumed sequence of characters
    '''
    self.skip_whites()
    if self.ended():
      return ''

    start = self.cursor
    self.skip_non_whites()
    end = self.cursor

    return self.doc[start:end]

  def try_consume_token(self, token):
    '''Given a string token, tries to consume it at the current cursor position.

    - token: a string containing the token that will attempt to be consumed.

    Returns: True if the token was present at the current position, False
    otherwise. The cursor position remains unchanged if the token could not
    be consumed.
    '''
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
    '''Tries to consume a string (a sequence of characters bookended by " or ').

    Returns: The contents of the string, if there was a valid string at the current
    cursor position, or None otherwise. If no string could be consumed, the cursor
    position remains unchanged.
    '''
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
    '''Tries to consume a number at the current cursor position.

    Returns: The parsed number, if there was a valid one at the current
    cursor position, or None otherwise. If no number could be consumed,
    the cursor position remains unchanged.
    '''
    checkpoint = self.cursor
    try:
      value = float(self.consume_word())
    except:
      self.cursor = checkpoint
      return None

    return value

  def try_consume_name(self):
    '''Tries to consume a sequence of characters that can form a valid name
    (a character followed by any sequence of characters, numbers and dashes).

    Returns: The parsed name, if there was a valid one at the current
    cursor position, or None otherwise. If no name could be consumed,
    the cursor position remains unchanged.
    '''
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
    '''Tries to consume a node attribute - a name, optionally followed by a '='
    and a string or a number, which comprises the attribute's value.
    If only a name could be parsed, the attribute's value defaults to True.

    Returns: A tuple containing the attribute's name and value, if there was
    a valid attribute at the current cursor position, or None otherwise.
    If no attribute could be consumed, the cursor position remains unchanged.
    '''
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
    '''Tries to consume an opening HTML tag.

    Returns: A tuple containing a new Node object, containing the tag's name
    and attributes, if there was a valid opening tag at the current cursor position,
    or None otherwise.
    If it's a self-closing tag (e.g.: <img src="image.gif"/>), then the returned
    Node's children attribute is None; otherwise, it's an empty list that will hold
    the node's children.
    If no opening tag could be consumed, the cursor position remains unchanged.
    '''
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

    if self.try_consume_token('/'):
      children = None
    else:
      children = []

    if not self.try_consume_token('>'):
      raise ParsingException('> expected', self)

    return Node(tagName=tag_name, attributeMap=attributes, children=children)

  def try_consume_close_tag(self):
    '''Tries to consume a closing HTML tag.

    Returns: The name of the closing tag, if there was a valid one at the current
    cursor position, or None otherwise.
    If no closing tag could be consumed, the cursor position remains unchanged.
    '''
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
    '''Tries to consume a text HTML tag.

    Returns: A Node containing all the text between the current cursor position
    and the following '<' character or the end of the document, whichever comes
    first. If the result is a Node with an empty string as a text, the None is
    returned instead.
    '''
    if self.ended():
      return None

    start = self.cursor
    end = self.doc.find('<', start)
    if end < 0:
      end = len(self.doc)

    self.cursor = end
    if start == end:
      return None
    return Node(text=self.doc[start:end])

  def try_consume_node(self):
    '''Tries to consume a full HTML node - an opening tag, followed by child nodes
    and a closing tag.

    Returns: A Node containing all the parsed contents, or None if no node could
    be consumed at the current cursor position. In this case, the cursor position
    remains unchanged.
    '''
    node = self.try_consume_open_tag()
    if node is None:
      return None

    # If the parsed tag is not a self-closing tag, we must consume its children
    if node.children == []:
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

  def parse(self):
    '''Resets the cursor position and parses the document.

    Returns: a list containing all the top-level HTML nodes that could be parsed.
    '''
    self.cursor = 0
    nodes = []
    while not self.ended():
      child_text = self.consume_text_node()
      if child_text is not None:
        nodes.append(child_text)

      child_node = self.try_consume_node()
      if child_node is not None:
        nodes.append(child_node)

    return nodes

### Tests
if __name__ == '__main__':
  parser = HTMLParser('<img src=\'photo.jpg\' /><span>Hey <p font="helvetica">bro</p>! What\'s up? <img src="hey.gif"/> </span> End of document! ')
  nodes = parser.parse()
