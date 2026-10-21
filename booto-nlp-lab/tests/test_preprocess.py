from booto_nlp.preprocess import normalize, tokenize

def test_accents_retained():
    assert 'école' in tokenize('Une école accueille les élèves.', 'fr')

def test_stopwords():
    assert 'the' not in tokenize('The teachers study language.', 'en')

def test_whitespace_normalize():
    assert normalize(' Bonjour  le  monde ') == 'Bonjour le monde'
