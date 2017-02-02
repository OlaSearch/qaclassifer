import os
directory = 'qaclassifier/data/list'

def readLists ():
  lists = {}
  for root, dirs, files in os.walk(directory):
    for file in files:
      with open(os.path.join(directory, file)) as f:
        content = f.readlines()
      content = [x.strip() for x in content]
      lists[file.lower()] = content
  return lists

# Read the lists to cache
lists = readLists()

class ListSet ():
  def __init__ (self, words):
    self.listSet = []
    words = [w.lower() for w in words]
    for idx, word in enumerate(words):
      _listset = []
      for l in lists:
        if word in lists[l]:
          _listset.append(l)
      if len(_listset) > 0:
        self.listSet.append((word, _listset, idx))
    # print (self.listSet)

  def inWordList (self, listName, pos):
    listName = listName.lower()
    for word, lst, position in self.listSet:
      if position == pos and listName in lst:
        return True
    return False

  def inList (self, listName, pos = None):
    listName = listName.lower()
    for idx, (word, lst, position) in enumerate(self.listSet):
      if pos is not None:
        if idx == pos and listName in lst:
          return True
      else:
        if listName in lst:
          return True

    return False

  def getList (self):
    return self.listSet

  def first (self, listName = None):
    if listName is None:
      return False if len(self.listSet) is 0 else True
    return self.inList(listName, 0)