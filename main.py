from pydictionary import Dictionary
import time

class Node:
  def __init__(self, value, parent=None,id=0):
    self.value = value
    self.parent = parent
    self.children = []
    self.root = None
    self.maxDepth = 0
    self.totalChildren = 0
    self.id = 0
    if self.parent != None:
      p = self.parent
      while p.parent != None:
        p = p.parent
      self.root = p

  def addChild(self,value):
    child = Node(value,parent=self)
    self.children.append(child)
    if self.root != None:
      self.root.totalChildren += 1
      child.id = self.root.totalChildren
      if self.root.totalChildren % 10 == 0:
        print("{} children of root.".format(self.root.totalChildren))
    else:
      self.totalChildren += 1
      child.id = self.totalChildren
      if self.totalChildren % 10 == 0:
        print("{} children of root.".format(self.totalChildren))
    return child
  
  def getSynonyms(self):
    for word in Dictionary(self.value,100).synonyms():
      if " " in word:
        continue
      if self.root == None:
        self.addChild(word)
      elif self.root.value != word and self.root.searchNode(self.root,word) == None:
        self.addChild(word)

  def getAllNodes(self):
    if len(self.children) == 0:
      return [self]
    nodeList = []
    for c in self.children:
      for n in c.getAllNodes():
        nodeList.append(n)
    return nodeList
    
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

  def expandSynonyms(self, node, level, limit):
    if level == limit:
      return
    if node.root != None and level > node.root.maxDepth:
      node.root.maxDepth = level
      #print("Max depth: {}".format(level))
    node.getSynonyms()
    if len(node.children) == 0:
      return
    for n in node.children:
      self.expandSynonyms(n, level+1,limit)

  def saveNodeToText(self):
    #id,value,children
    retStr = "id={},val={},children=".format(self.id,self.value)
    for c in self.children:
      retStr+= c.id
    return retStr
    
  def __str__(self):
    retStr = "--- {}\n".format(self.value.upper())
    index = 0
    for n in self.children:
      retStr+="{}. {}, """.format(index, n.value)
      index += 1
    return retStr

ROOT_WORD = "aluminum"
DEPTH_LIMIT = 3
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
  print("Root: {}\t\tCurrent depth: {}/{}\t\tCurrent width: {}\t\t{:.2f} seconds elapsed.\n\n".format(ROOT_WORD.upper(),depth,maxDepth,width,elapsedTime))
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

startTime = time.time()

print("Searching...") 
root = Node(ROOT_WORD)
root.expandSynonyms(root,0,DEPTH_LIMIT)

elapsedTime = time.time()-startTime
nodeList = root.getAllNodes()

for n in nodeList:
  print(n.id,n.value)

printMenu(root)
# id, value, children




