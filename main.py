from pydictionary import Dictionary
import time

class Node:
  def __init__(self, value, parent=None):
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
      layer = 1
      p = self.parent
      while p.parent != None:
        p = p.parent
        layer += 1
      if layer > self.root.maxDepth:
        self.root.maxDepth = layer
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
    sortedSynonyms = []
    for word in Dictionary(self.value,100).synonyms():
      sortedSynonyms.append(word)
    sortedSynonyms.sort()
    
    for word in sortedSynonyms:
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
    nodeList.append(self)
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

  def expandSynonymsInLayer(self, targetLayer):
    root = self
    if self.root != None:
      root = self.root
    if targetLayer > root.maxDepth:
      root.maxDepth = targetLayer
    
    nodeList = self.getNodesInLayer(targetLayer)
    for n in nodeList:
      n.getSynonyms()
    
  
  def getNodesInLayer(self, targetLayer,currentLayer=0):
    if currentLayer == targetLayer:
      return [self]
    if len(self.children) == 0:
      return [None]
    root = self
    if self.root != None:
      root = self.root
    nodeList = []
    for c in self.children:
      nextLayerList = c.getNodesInLayer(targetLayer,currentLayer+1)
      if nextLayerList != None:
        for n in c.getNodesInLayer(targetLayer,currentLayer=currentLayer+1):
          if n != None:
            nodeList.append(n)
    return nodeList
  
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

def printMenu(node,depth=0):
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


def writeNodeList(nodeList):
  outStr = ""
  for n in nodeList:
    id = n.id
    value = n.value
    parent = "None"
    if n.parent != None:
      parent= n.parent.value
    outStr += "{},{},{}\n".format(id,value,parent)
  return outStr

def nodesFromFile(path):
  file = open(path,"r")
  lines = file.readlines()
  strippedLines = []
  for l in lines:
    strippedLines.append(l.strip())
  root = getNodeFromLine(strippedLines[0])
  nodeList = [root]
  for i in range(1,len(strippedLines)):
    l = strippedLines[i]
    nodeList.append(getNodeFromLine(l,root=root))
  return nodeList
  
def getNodeFromLine(line,root=None):
  id = line.split(",")[0]
  value = line.split(",")[1]
  parentValue = line.split(",")[2]
  n = None
  if root == None:
    n = Node(value)
    n.id = id
  else:
    parentNode = root.searchNode(root,parentValue)
    n = parentNode.addChild(value)
  return n

startTime = time.time()
nList = nodesFromFile("list.txt")
  


#print("Searching...") 
#root = Node(ROOT_WORD)
#for i in range(0,DEPTH_LIMIT):
#  root.expandSynonymsInLayer(i)

elapsedTime = time.time()-startTime
#nodeList = root.getAllNodes()
#sortedNodeList = sorted(nodeList, key=lambda x: x.id)

printMenu(nList[0])




