import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("en")
training_data = [
  ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
]
# the DocBin will store the example documents
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)

# TODO do this later as making test entities would improve the accuracy of my pipeline
# as stonk headlines are different, but my phrase extractor will likely add more value  
db.to_disk("data/dev.spacy")
