import os

class ListSet ():
  def __init__ (self, words, lists):
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

  def pop (self):
    del self.listSet[:1]
    return self

  def getList (self):
    return self.listSet

  def isNext (self, listName):
    if listName is None:
      return False if len(self.listSet) is 0 else True
    return self.inList(listName, 1)

  def first (self, listName = None):
    if listName is None:
      return False if len(self.listSet) is 0 else True
    return self.inList(listName, 0)