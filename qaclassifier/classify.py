from .listset import ListSet
from pattern.en import tag
import os
import re

tags = {
  'wword': ['WDT', 'WP', 'WP$', 'WRB'],
  'nouns': ['NN', 'NNP', 'NNPS', 'NNS'],
  'verbs': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
  'adjectives': ['JJ', 'JJR', 'JJS'],
}

directory = 'data/list'

def lastPos (pos):
  l = len(pos)
  if pos[l - 1] == '.':
    return pos[l - 2]
  else:
    return pos[l - 1]

def lastWord (words):
  l = len(words)
  if words[l - 1] == '.' or words[l-1] == '?' or words[l-1]=='!':
    return words[l - 2]
  else:
    return words[l - 1]

class QuestionClassifier ():
  def __init__ (self):
    def readLists ():
      lists = {}
      for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), directory)):
        for file in files:
          with open(os.path.join(os.path.dirname(__file__), directory, file)) as f:
            content = f.readlines()
          content = [x.strip() for x in content]
          lists[file.lower()] = content
      return lists

    # Read the lists to cache
    self.lists = readLists()

    # Additional entities added by user
    self.entities = []

  def questionType (self, sentence):
    taggedWords = tag(sentence, tokenize=True)
    words = [word.lower() for word, pos in taggedWords]
    pos = [pos for word, pos in taggedWords]
    hasWWord = any(i in pos for i in tags['wword'])
    listSet = ListSet(words, self.lists)
    code = None
    # print ('Pos tags ', pos)
    # print ('words ', words)
    # print (listSet)

    if hasWWord:
      code = 'WH'

    # Yes/no questions begin with words in the modal/do/have/singleBe/presentBe lists
    if listSet.inWordList('modal', 0) or listSet.inWordList('do', 0) or listSet.inWordList('have', 0) or listSet.inWordList('singleBe', 0) or listSet.inWordList('presentBe', 0):
      code = 'YN'

    # Tag questions always have a comma and end with a personal pronoun
    if ',' in pos and pos.index(',') < len(pos):
      nl = pos.index(',') + 1
      hasVerb = any(i in pos[nl] for i in tags['verbs'])
      if ((lastPos(pos) == 'PRP' or lastWord(words) == 'i') and (pos[nl] == 'MD' or hasVerb)):
        code = 'TG'

    # Choice questions either follow a certain regex or contain the word "or"
    ch_match = re.search(r'NNP? CC(?:\s*DT\s|\s)NNP?', ' '.join(pos))
    if (ch_match or 'or' in words):
      if listSet.inWordList('be', 0) or listSet.inWordList('do', 0) or listSet.inWordList('have', 0) or listSet.inWordList('modal', 0) or code == 'WH' or len(pos) == 3:
        code = 'CH'

    return code

  def addRule (self, type, names):
    self.lists[type] = names
    self.entities.append(type)

  def checkUserNounSet (self, nounSet, sentence):
    for entity in self.entities:
      if nounSet.first(entity):
        return self.questionType(sentence) + ':' + entity
    return False

  def getUserEntityType (self, nounSet):
    for entity in self.entities:
      if nounSet.first(entity):
        return entity
    return 'other'

  def isQuestion (self, sentence):
    taggedWords = tag(sentence, tokenize=True)
    lastWord = taggedWords[-1]
    if lastWord is not None and lastWord[1] == '.' and lastWord[0] == '?':
      return True

    type = self.questionType(sentence)
    if type is not None:
      return True

    return False

  def sentenceToWordsPos (self, sentence):
    taggedWords = tag(sentence, tokenize=True)
    words = [word.lower() for word, pos in taggedWords]
    pos = [pos for word, pos in taggedWords]
    return words, pos

  def classify (self, sentence):
    code = None
    words, pos = self.sentenceToWordsPos(sentence)
    qType = self.questionType(sentence)
    listSet = ListSet(words, self.lists)
    hasWWord = any(i in pos for i in tags['wword'])
    # Get all nouns
    nn = [w for idx, w in enumerate(words) if pos[idx] in tags['nouns']]
    nounSet = ListSet(nn, self.lists)
    sequence = str(words).strip('[]')

    # print (nounSet.getList(), pos)
    # When VB, Date (current or past?)
    if words[0] == 'when':
      code = 'NUM:date'

    # Who: Human, Individual or Group...
    if listSet.inList('who', 0):
      # Who killed Gandhi ?
      code = 'HUM:ind'
      # Who is Terrence Malick ?
      # is => VBZ
      # killed => VBD
      if re.search(r'.*? VBZ (NNP\s?)+$', ' '.join(pos)):
        # Multiple proper nouns and end of sentence
        code = 'HUM:ind'
      elif len(pos) > 1 and pos[1] in ['VBZ'] and pos[2] == 'NNP':
        code = 'HUM:desc'

    # Why VB: Reason "Why do birds sing?"
    # `do` is tagged as JJ (advective)
    if words[0] == 'why' and any(i in pos[1] for i in tags['adjectives'] + tags['verbs']):
      code = 'DESC:reason'

    # Edge Reason - Give a reason...
    # "Give a reason for American Indians oftentimes dropping out of school"
    if str(['give', 'a', 'reason']).strip('[]') in str(words).strip('[]'):
      code = 'DESC:reason'

    # Describe
    if words[0] == 'describe':
      code = 'DESC:desc'

    # Define
    if words[0] == 'define':
      code = 'DESC:def'

    # Time
    if words[0] == 'what' and (listSet.inList('time', 1) or listSet.inList('date', 1)):
      code = 'NUM:time' if listSet.inList('time', 1) else 'NUM:date'

    # How
    if words[0] == 'how' or words[0] == 'what':
      if len(words) > 1 and words[1] == 'often' or listSet.inList('perc'):
        code = 'NUM:perc'
      elif listSet.inList('dimen') or listSet.inList('big'):
        code = 'NUM:volsize'
      elif listSet.inList('weight'):
        code = 'NUM:weight'
      elif listSet.inList('time'):
        code = 'NUM:period'
      elif listSet.inList('dist'):
        code = 'NUM:dist'
      elif listSet.inList('temp'):
        code = 'NUM:temp'
      elif listSet.inList('speed'):
        code = 'NUM:speed'
      elif listSet.inList('num'):
        code = 'NUM:' + self.getUserEntityType(nounSet)

    # How many
    if str(['how', 'many']).strip('[]') in sequence:
      if listSet.inList('weight'):
        code = 'NUM:weight'
      else:
        code = 'NUM:count'

    # How much
    if str(['how', 'much']).strip('[]') in sequence:
      if listSet.inList('weight'):
        code = 'NUM:weight'
      else:
        code = 'NUM:count'

      if listSet.inList('money') or str(['is', 'a']).strip('[]') in sequence or str(['be', 'a']).strip('[]') in sequence:
        code = 'NUM:money'

    # Manner
    # "How do you find oxidation numbers ?"
    if words[0] == 'how' and len(words) > 1 and (words[1] == 'can' or any(i in pos[1] for i in tags['verbs'])):
      code = 'DESC:manner'

    if words[0] == 'what' or words[0] == 'which':
      code = self.findCode(nounSet, listSet, words, sentence, pos)

      # Double check these,
      # What was the name... was slipping though
      if code == 'ENTY:termeq' and 'was' in words:
        code = 'HUM:ind'

    if 'mean' in words or 'meaning' in words:
      code = 'DESC:def'

    # Where, Location - Place
    if words[0] == 'where':
      code = 'LOC:' + self.getUserEntityType(nounSet)

    # Not a leading question
    if not any(i in pos[0] for i in tags['wword']) and (listSet.inList('time') or listSet.inList('date')):
      code = 'NUM:time' if listSet.inList('time') else 'NUM:date'

    if words[0] == 'name':
      if words[1] == 'a' or words[1] == 'something':
        code = self.findCode(nounSet, listSet, words, sentence, pos)
      else:
        code = 'HUM:ind'

    if not any(i in pos[0] for i in tags['wword']) and hasWWord and code == None:
      code = self.findCode(nounSet, listSet, words, sentence, pos)

    if qType == 'YN':
      code = self.findCode(nounSet, listSet, words, sentence, pos)

    return code

  def findCode (self, nounSet, listSet, words, sentence, pos, depth = 0):
    code = None
    sequence = str(words).strip('[]')
    if depth == 5:
      return ''

    if nounSet.first():
      if nounSet.first('num'):
        code = 'NUM:' + self.getUserEntityType(nounSet)
      elif nounSet.first('speed'):
        code = 'NUM:speed'
      elif nounSet.first('dimen'):
        code = 'NUM:volsize'
      elif nounSet.first('date'):
        code = 'NUM:date'
      elif nounSet.first('money'):
        code = 'NUM:money'
      elif nounSet.first('code'):
        code = 'NUM:code'
      elif nounSet.first('peop') or nounSet.first('prof'):
        # Check there is NN + VB
        # What does a person work on?
        wh_ent_other_match = re.search(r'WP VBZ .*? NN VB', ' '.join(pos))
        if wh_ent_other_match:
          code = 'ENTY:' + self.getUserEntityType(nounSet)
        else:
          code = 'HUM:ind'
      elif nounSet.first('group') or nounSet.first('comp'):
        code = 'HUM:gr'
      elif nounSet.first('job'):
        code = 'HUM:title'
      elif nounSet.first('country'):
        code = 'LOC:country'
      elif nounSet.first('state'):
        code = 'LOC:state'
      elif nounSet.first('city'):
        code = 'LOC:city'
      elif nounSet.first('mount'):
        code = 'LOC:mount'
      elif nounSet.first('loca'):
        code = 'LOC:' + self.getUserEntityType(nounSet)
      elif nounSet.first('prod'):
        code = 'ENTY:product'
      elif nounSet.first('art'):
        code = 'ENTY:cremat'
      elif nounSet.first('food'):
        # If the first word is What food, then it has to be food
        if not any(i in pos[0] for i in tags['wword']):
          code2 = self.findCode(nounSet.pop(), listSet, words, pos, sentence)
        else:
          code2 = None
        code = code2 if code2 is not None else 'ENTY:food'
      elif nounSet.first('plant'):
        code = 'ENTY:plant'
      elif nounSet.first('lang'):
        code = 'ENTY:lang'
      elif nounSet.first('substance'):
        code = 'ENTY:substance'
      elif nounSet.first('word'):
        code = 'ENTY:word'
      elif nounSet.first('letter'):
        code = 'ENTY:letter'
      elif nounSet.first('instrument'):
        code = 'ENTY:instru'
      elif nounSet.first('color'):
        code = 'ENTY:color'
      elif nounSet.first('dise'):
        code = 'ENTY:dismed'
      elif nounSet.first('anim'):
        code = 'ENTY:animal'
      elif nounSet.first('religion'):
        code = 'ENTY:religion'
      elif nounSet.first('term'):
        code = 'ENTY:termeq'
      elif nounSet.first('event'):
        code = 'ENTY:event'
      elif nounSet.first('other'):
        code = 'ENTY:' + self.getUserEntityType(nounSet)
      elif nounSet.first('sport'):
        code = 'ENTY:sport'
      elif nounSet.first('def'):
        code = 'DESC:def'
      elif nounSet.first('cause'):
        code = 'DESC:reason'
      elif nounSet.first('desc') or nounSet.first('quot'):
        code = 'DESC:desc'
      elif nounSet.first('abb'):
        if str(['stand', 'for']).strip('[]') in sequence:
          code = 'ABBR:exp'
        else:
          code = 'ABBR:abb'
      elif str(['stand', 'for']).strip('[]') in sequence:
        code = 'ABBR:exp'
      elif nounSet.inList('anim'):
        code = 'ENTY:animal'
      elif self.checkUserNounSet(nounSet, sentence):
        code = self.checkUserNounSet(nounSet, sentence)

      # Fixes "what toy company"
      if code == 'ENTY:product' and nounSet.inList('comp'):
        code = 'HUM:gr'
      elif code == 'ENTY:termeq' and 'name' in words:
        newList = []
        for word, lst, pos in nounSet.listSet:
          if word != 'name':
            newList.append((word, lst, pos))
        nounSet.listSet = newList
        depth = depth + 1
        _code = self.findCode(nounSet, listSet, words, sentence, pos, depth)
        code = _code if _code is not None else 'HUM:ind'

    elif str(['stand', 'for']).strip('[]') in sequence or str(['full', 'form']).strip('[]') in sequence:
      code = 'ABBR:exp'
    elif 'name' in words:
      code = 'HUM:ind'
    elif listSet.inList('def'):
      code = 'DESC:def'
    elif listSet.inList('who'):
      code = 'HUM:ind'
    elif listSet.inList('peop') or listSet.inList('prof') or listSet.inList('sport'):
      code = 'HUM:def'
    else:
      code = 'DESC:def'
    return code

