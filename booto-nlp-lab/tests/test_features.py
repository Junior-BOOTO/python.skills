from booto_nlp.features import top_keywords
from booto_nlp.similarity import nearest_documents

def test_keywords():
    result = top_keywords(['Les arbres protègent la forêt.', 'La forêt contient des arbres.'])
    assert 1 <= len(result) <= 10

def test_empty_keywords():
    assert top_keywords(['', ' ']) == []

def test_nearest():
    neighbors = nearest_documents(['chat noir chats', 'chien très différent', 'chat noir'], 0, 2)
    assert neighbors[0][0] == 2

def test_single_similarity():
    assert nearest_documents(['texte unique'], 0, 3) == []

def test_keywords_exclude_generic_words():
    terms = [word for word, _ in top_keywords(['Les arbres poussent dans la forêt.', 'La forêt protège les arbres.'])]
    assert 'les' not in terms and 'la' not in terms
