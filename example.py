from qaclassifier import QuestionClassifier

clf = QuestionClassifier()
# Tag question
# print (clf.questionType('Peter plays football, doesn\'t he?'))

# Choice
# print (clf.questionType('Would you prefer coke or iced tea?'))

# is Question
# print (clf.isQuestion('Hello, how are you?'))

# Classify
# print (clf.classify('Peter plays football, doesn\'t he?'))
# print (clf.classify('Who is Terrence Malick ?'))
# print (clf.classify('Would you prefer Coke or iced tea?'))
# print (clf.classify('Give a reason for American Indians oftentimes dropping out of school'))
# print (clf.classify('What fraction of a beaver\'s life is spent swimming ?'))
# print (clf.classify('How many shots can a stock M16 hold ?'))

# clf.addRule('topic', ['topics', 'topic'])
# clf.addRule('company', ['barclays'])

# print (clf.classify('Which are the popular topics in year?'))
# print (clf.classify('Where is the popular topics from?'))
# print (clf.classify('Would you prefer Coke or iced tea?'))
# print (clf.classify('Did Barclays win an award?'))

# print (clf.classify('Where are the gold award winners from?'))
# clf.addRule('topic', ['topics', 'topic'])
# print (clf.classify('What are the popular topics in 2010?'))
# print (clf.classify("What contemptible scoundrel stole the cork from my lunch ?"))
# print (clf.classify("Why do heavier objects travel downhill faster ?"))
# print (clf.classify("Who won gold awards in Australia in 2016 for UX?"))
# print (clf.classify("Who is Terence Malik"))
print (clf.classify("What is tectonic plates?"))

# print (clf.classify('What is the average cost for four years of medical school ?'))
# print (clf.classify('How do you find oxidation numbers ?'))
# print (clf.classify('This\'ll work, won\'t it?'))