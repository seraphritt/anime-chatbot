import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
# nltk.help.upenn_tagset() get all tags


def is_noun(pos: list) -> bool:
    # function to test if something is a noun
    return pos[:2] == 'NN' or pos[:2] == 'NNP'


lines = 'Tanjirou on Demon Slayer?'

tokenized = nltk.word_tokenize(lines)
print(nltk.pos_tag(tokenized))
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

print(nouns)
