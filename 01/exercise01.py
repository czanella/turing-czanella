class BinaryTreeNode:
  def __init__(self, key, value):
    self.key = key
    self.value = value
    self.left_child = None
    self.right_child = None

  def search(self, key):
    if key == self.key:
      return self.value

    next_node = self.left_child if key < self.key else self.right_child

    return None if next_node is None else next_node.search(key)

  def insert(self, key, value):
    if key < self.key:
      self.left_child = BinaryTreeNode(key, value) if self.left_child is None else self.left_child.insert(key, value)
      return self.left_child

    if key > self.key:
      self.right_child = BinaryTreeNode(key, value) if self.right_child is None else self.right_child.insert(key, value)
      return self.right_child

    self.value = value

    return self

  def delete(self, key):
    if key < self.key:
      self.left_child = None if self.left_child is None else self.left_child.delete(key)
      return self

    if key > self.key:
      self.right_child = None if self.right_child is None else self.right_child.delete(key)
      return self

    if self.left_child is None:
      return self.right_child

    if self.right_child is None:
      return self.left_child

    self.key = self.left_child.key
    self.value = self.left_child.value
    self.left_child = self.left_child.delete(self.left_child.key)

  def traverse(self):
    if self.left_child is not None:
      for node in self.left_child:
        yield node

    yield self

    if self.right_child is not None:
      for node in self.right_child:
        yield node

  def __iter__(self):
    return self.traverse()


class BinaryTree:
  def __init__(self):
    self.root = None

  def __iter__(self):
    return () if self.root is None else self.root

  def search(self, key):
    return None if self.root is None else self.root.search(key)

  def insert(self, key, value):
    if self.root is None:
      self.root = BinaryTreeNode(key, value)
    else:
      self.root.insert(key, value)

  def delete(self, key):
    self.root = None if self.root is None else self.root.delete(key)

  def sorted_keys(self):
    for node in self:
      yield node.key

numbers = (
  ('um', 1),
  ('dois', 2),
  ('tres', 3),
  ('quatro', 4),
  ('cinco', 5),
  ('seis', 6),
  ('sete', 7),
  ('oito', 8),
  ('nove', 9),
  ('dez', 10),
)










