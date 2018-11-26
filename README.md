# Sentence-Reduction

The goal is to convert a verbsoe statement into a simple understandable statement. While these functions were developed to handle real-world customer complaints like " " which will be reduced to " ", it also handles regular english statements.

For example, the goal is to reduce " " to " " and we achieve that by making use of both refining the punctuations and reducing the sentence. 

The sentence reduction and convert_puntcutation_to_dots functions make use of numerous grammatical functions like get_main_verbs (which identifies the main verb or high-level intent of a statement), get_root (which uses spacy.io to derive the root form of a word) and more.

# What does each file contain?

- Preprocessing-Functions: Basic grammatical functions like clean_data, get_root, get_main_verbs

- Functions: Functons that build upon the grammatical functions in Preprocessing-Functions file to achieve the required output

- API-Functions: Functions required to create an API including error-handling and function calling

- API: Main API file which is run on a local server to activate the API
