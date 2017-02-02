# Question and Answer type classification

## Usage

````
pip install -e git+ssh://git@gitlab.com/olasearch/qaclassifier.git#egg=qaclassifier
````

### Requirements

1. Python 2.7
2. Pattern


````
from qaclassifier import QuestionClassifier
clf = QuestionClassifier()

# Check if a sentence is a question
clf.isQuestion('Hello how are you')

# Check question type
# YN => Yes/No questions
# WH => What/When/How
# TG => This'll work, won't it?
# CH => Would you prefer Coke or iced tea?
clf.questionType('Would you prefer Coke or iced tea?')

# Detect answer type to output
clf.classify('How much was the minimum wage in 1991 ?')
=> NUM:money
````