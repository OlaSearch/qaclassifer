from unittest import TestCase
from qaclassifier import QuestionClassifier
import os

class QaTests (TestCase):
  def setUp (self):
    self.clf = QuestionClassifier()
    self.testcases = []
    with open(os.path.join(os.path.dirname(__file__), 'testcases.txt')) as f:
      for line in f:
        (a, q) = line.rstrip('\n').split(' ', 1)
        self.testcases.append((q, a))

  def test_isquestion (self):
    for q, a in self.testcases:
      self.assertEqual(
        self.clf.isQuestion(q),
        True
      )

  def test_classify (self):
    for q, a in self.testcases:
      self.assertEqual(
        self.clf.classify(q),
        a
      )
