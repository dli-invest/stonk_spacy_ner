import spacy
nlp = spacy.load("output/stonk_pipeline")

# see if it catches test case

text = '''Dorel Completes Sale of Sports Segment to Pon Holdings for US $810 Million and Declares Special Dividend of US $12.00 Per Share
'''
doc = nlp(text)

# make sure special dividend is in doc.ents
for entity in doc.ents:
    if entity.label_ == 'DIVIDENDS':
        print(entity)
        assert entity.text == 'Special Dividend'
        print("PASS TEST HERE")
        break
else:
    print('no special dividend found')
    print(doc.ents)
    assert False