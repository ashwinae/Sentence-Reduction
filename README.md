# Sentence-Reduction

The goal is to convert a verbose statement into a simple understandable statement, without losing the essence of the statement. The essence in this case is understood to be main intention of the statement. While these functions were developed to handle real-world customer complaints like "Pulley put grove into the tub. The washer need to be replaced. Not worth doing" to "washer need to be replaced", it also handles regular english statements.

For example, the goal is to reduce "I need to go to New York right now and there is no other way out" to "go to New York" and we achieve that by making use of both refining the punctuations and reducing the sentence. 

The sentence reduction and convert_puntcutation_to_dots functions make use of numerous grammatical functions like get_main_verbs (which identifies the main verb or high-level intent of a statement), get_root (which uses spacy.io to derive the root form of a word) and more.

## Examples:

1. Original: "Would you please be able to get me a ticket to Los Angeles whenever you can?"

   Reduced: "get me a ticket to los angeles"

2. Original: "Please help me order some pizza as soon as possible" 

   Reduced: "order some pizza"

   
- Real Complaints:

3. Original: "Replaced Control panel in door and checked...delay was due to both customers had limited availability because they are                   teachers."

   Reduced:  "Replaced control panel in door. Had limited availability"

4. Original: "Burners too high adjusted burner valves"

   Reduced: "Adjusted burner valves"

# What does each file contain?

- Preprocessing-Functions: Basic grammatical functions like clean_data, get_root, get_main_verbs

- Functions: Functons that build upon the grammatical functions in Preprocessing-Functions file to achieve the required output

- API-Functions: Functions required to create an API including error-handling and function calling

- API: Main API file which is run on a local server to activate the API
