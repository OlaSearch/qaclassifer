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
print (clf.classify('How much was the minimum wage in 1991 ?'))
# print (clf.classify('What is the average cost for four years of medical school ?'))
# print (clf.classify('How do you find oxidation numbers ?'))
# print (clf.classify('This\'ll work, won\'t it?'))