import spacy

# Load English tokenizer, POS tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)

    # Extract named entities and noun phrases
    entities = [ent.text for ent in doc.ents]
    noun_phrases = [np.text for np in doc.noun_chunks]

    # Combine the results
    keywords = entities + noun_phrases

    # Deduplicate the list
    keywords = list(set(keywords))

    return keywords
