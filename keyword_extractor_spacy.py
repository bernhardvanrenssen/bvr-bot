# import spacy

# # Load English tokenizer, POS tagger, parser, NER, and word vectors
# nlp = spacy.load("en_core_web_sm")

# def extract_keywords(text):
#     doc = nlp(text)

#     # Extract named entities, nouns, and adjectives
#     entities = [ent.text for ent in doc.ents]
#     nouns = [token.text for token in doc if token.pos_ == "NOUN"]
#     adjectives = [token.text for token in doc if token.pos_ == "ADJ"]

#     # Combine the results
#     keywords = entities + nouns + adjectives

#     # Deduplicate the list
#     keywords = list(set(keywords))

#     # Convert list to comma-separated string
#     keyword_string = ", ".join(keywords)

#     return keyword_string


