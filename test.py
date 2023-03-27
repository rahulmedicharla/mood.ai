import spacy
nlp = spacy.load('en_core_web_sm')

text = "Dallas no good that time, they were unable to convert to that bucket."

doc = nlp(text)

doc.ents