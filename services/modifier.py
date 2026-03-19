import spacy
import pyinflect

class Modifier:
    def __init__(self):
        # Load the small English model
        self.nlp = spacy.load("en_core_web_sm")

    def modify(self, sentence: str, pirates_count: int):
        try:
            doc = self.nlp(sentence)
            new_sentence = ""
            
            #Find the subject 
            subj_token = None
            new_subj_text = ""
            is_singular = False
            
            for token in doc:
                if "subj" in token.dep_:
                    subj_token = token
                    # If the user says "I", they become the "Pirate King"
                    if token.text.lower() == "i":
                        new_subj_text = "Pirate King"
                        is_singular = True
                    else:
                        # Otherwise, replace the subject with the count of pirates
                        new_subj_text = f"{pirates_count} Pirates" 
                        is_singular = False
                    break # Handle the first subject for simplicity

            if not subj_token:
                return None, "Where am I?"

            #Rebuild the sentence and conjugate verbs 
            for token in doc:
                word = token.text
                
                # Replace the original subject with new pirate subject
                if token == subj_token:
                    word = new_subj_text
                
                # Check if this token is a verb/auxiliary connected to the subject
                elif token.pos_ in ["AUX", "VERB"] and (token == subj_token.head or token.head == subj_token.head):
                    
                    # Conjugate for "Pirate King" (Singular)
                    if is_singular:
                        if token.tag_ == "VBP":
                            inflected = token._.inflect("VBZ") 
                            if inflected: word = inflected
                            
                    # Conjugate for "Pirates" (Plural)
                    else:
                        if token.lemma_ == "be":
                            if token.tag_ in ["VBP", "VBZ"]: # handles "am" and "is"
                                word = "are"
                            elif token.tag_ == "VBD": # handles "was"
                                word = "were"
                        
                        # Handle other general verbs
                        elif token.tag_ == "VBZ":  
                            inflected = token._.inflect("VBP") 
                            if inflected: word = inflected

                if token.is_title and token != subj_token:
                    word = word.capitalize()

                new_sentence += word + token.whitespace_

            return new_sentence.strip(), None
            
        except Exception as e:
            return None, str(e)