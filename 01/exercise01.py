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
      if self.left_child is None:
        self.left_child = BinaryTreeNode(key, value)
      else:
        self.left_child.insert(key, value)

    if key > self.key:
      if self.right_child is None:
        self.right_child = BinaryTreeNode(key, value)
      else:
        self.right_child.insert(key, value)
    
    if key == self.key:
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

  def successor(self):
    successor = self.right_child
    if successor is not None:
      while successor.left_child is not None:
        successor = successor.left_child

    return successor

class BinaryTree:
  def __init__(self):
    self.root = None

  def search(self, key):
    return None if self.root is None else self.root.search(key)

  def insert(self, key, value):
    if self.root is None:
      self.root = BinaryTreeNode(key, value)
    else:
      self.root.insert(key, value)

  def delete(self, key):
    self.root = None if self.root is None else self.root.delete(key)

  def traverse(self):
    if self.root is not None:
      for node in self.root:
        yield node

  def __iter__(self):
    return self.traverse()

  def sorted_keys(self):
    for node in self:
      yield node.key

### Tests
if __name__ == '__main__':
  # Insertion
  numbers = (
    (4, 'four'),
    (7, 'seven'),
    (6, 'six'),
    (5, 'five'),
    (10, 'ten'),
    (1, 'one'),
    (9, 'nine'),
    (8, 'eight'),
    (3, 'three'),
    (2, 'two'),
  )

  tree = BinaryTree()
  for (key, value) in numbers:
    tree.insert(key, value)

  # Search
  assert tree.search(3) == 'three', 'Search should return correct value if key exists'
  assert tree.search(11) is None, 'Search should return None if key doesn\'t exist'

  # Replace value
  assert tree.search(6) == 'six'
  tree.insert(6, 'half dozen')
  assert tree.search(6) == 'half dozen', 'Insert should replace value if key already exists'

  # Find node successor
  assert tree.root.key == 4
  assert tree.root.successor().key == 5, 'Successor should find the following key'

  lonely_node = BinaryTreeNode(12, 'twelve')
  assert lonely_node.successor() == None, 'Successor should return None if node has no successor'

  # Deletion
  tree.delete(3)
  assert tree.search(3) == None, 'Delete should remove existing key'

  # Print sorted keys
  assert list(tree.sorted_keys()) == [1, 2, 4, 5, 6, 7, 8, 9, 10], 'Should return all keys in sorted order'

  print('All assertions succeeded')
