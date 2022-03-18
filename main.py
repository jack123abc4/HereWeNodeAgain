from pydictionary import Dictionary

class Node:
  def __init__(self, value, parent=None):
    self.value = value
    self.parent = parent
    self.children = []
    self.root = None
    self.maxDepth = 0
    if self.parent != None:
      p = self.parent
      while p.parent != None:
        p = p.parent
      self.root = p

  def addChild(self,value):
    child = Node(value,parent=self)
    self.children.append(child)
    return child

  def getSynonyms(self):
    for word in Dictionary(self.value,100).synonyms():
      if " " in word:
        continue
      if self.root == None:
        self.addChild(word)
      elif self.root.value != word and self.root.searchNode(self.root,word) == None:
        self.addChild(word)
    
  def searchNode(self, node, value):
    if node.value == value:
      return node
    if len(node.children) == 0:
      return None
  
    nodeFound = None
    for n in node.children:
      searchVal = self.searchNode(n,value)
      if searchVal != None:
        nodeFound = searchVal
    return nodeFound

  def expandSynonyms(self, node, level):
    print("{}\t{}".format(level,node.value))
    if node.root != None and level > node.root.maxDepth:
      node.root.maxDepth = level
      print("Max depth: {}".format(level))
    numSynonyms = node.getSynonyms()
    if len(node.children) == 0:
      return
    for n in node.children:
      self.expandSynonyms(n, level+1)
    
  def __str__(self):
    retStr = "--- {}\n".format(self.value.upper())
    index = 0
    for n in self.children:
      retStr+="{}. {}, ".format(index, n.value)
      index += 1
    return retStr

ROOT_WORD = "homonym"

def clearScreen():
  print("\033[H\033[J", end="")

def printMenu(node,depth):
  clearScreen()
  width = len(node.children)
  maxDepth = 0
  if node.root == None:
    maxDepth = node.maxDepth
  else:
    maxDepth = node.root.maxDepth
  print("Root: {}\t\tCurrent depth: {}/{}\t\tCurrent width: {}\n\n".format(ROOT_WORD.upper(),depth,maxDepth,width))
  print("{}\n\n".format(node))
  try:
    choice = int(input("Choice: ").strip())
    if choice < 0:
      if depth > 0:
        printMenu(node.parent,depth-1)
      else:
        print("Already at top of tree.")
    elif choice >= width:
      print("Option exceeds width.")
    elif depth==maxDepth:
      print("Already at bottom of tree.")
    else:
      printMenu(node.children[choice],depth+1)
  except ValueError:
    print("Error")
  input()
  printMenu(node,depth)
  

print("Searching...") 
root = Node(ROOT_WORD)
root.expandSynonyms(root,0)
printMenu(root,0)






