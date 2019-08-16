#!/usr/bin/python

# Abstract strings to French strings

def french_strings():
    return {# Normal responses
            'yes': '<audio src="SYSTEM_AUDIO_DIR/success.mp3"/>',
            'yes {string}': '{string} <audio src="SYSTEM_AUDIO_DIR/success.mp3"/>',
            'no {string}': 'J\'ai entendu {string}. <audio src="SYSTEM_AUDIO_DIR/failure.mp3"/>',
            'no {string} {prompt}': 'J\'ai entendu {string}. <audio src="SYSTEM_AUDIO_DIR/failure.mp3"/> {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Next: {prompt}': 'Suivant: {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            '{prompt}': '{prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Exit': 'Arrêtez. Merci et au revoir.',
            'Repeat. {text}': 'Répétez. {text} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Back: {prompt}': 'Arrière: {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Waiting. {prompt}': 'J\'attends. {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Help: is it {text}. {prompt}': 'Aide: Est-ce que c\'est {text}? <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Help: the answer is {text}. {prompt} (then continue)': 'Aide: la réponse est {text}. <break time="0.5s"/> ',
            'Lessons: {lessons}': 'Leçons: {lessons} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Lesson: {lesson}. {prompt}': 'Leçon: {lesson}. {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            # Conjunctions
            '{t1}, {t2}': '{t1}, {t2}',
            '{t1} or {t2}': '{t1} ou {t2}',
            # Errors
            'Unknown lesson': 'Leçon inconnue <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At end of lesson': 'Fin de la leçon. <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At end of lesson {score} {max_possible_score}':
               'Fin de la leçon. Note: {score} sur {max_possible_score} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At beginning of lesson': 'Début de la leçcon <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'No help is available': 'Désolé, je ne peux pas vous aider <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Nothing to repeat': 'Il n\'y a rien à répéter <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'I don\'t understand': 'Désolé, je ne comprends pas. Répétez s\'il vous plaît <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'No more lessons': 'Fin du jeu.',
            'Something went wrong': 'Désolé, erreur <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            # Names of cards
            ( 'Welcome', ): 'Bienvenue',
            ( 'Respond', ): 'Répondre',
            # High score phrases
            ( 'You have the Nth highest score', 1): 'Vous êtes au premier rang',
            ( 'You have the Nth highest score', 2): 'Vous êtes au deuxième rang',
            ( 'You have the Nth highest score', 3): 'Vous êtes au troisième rang',
            ( 'You have the Nth highest score', 4): 'Vous êtes au quatrième rang',
            ( 'You have the Nth highest score', 5): 'Vous êtes au cinquième rang',
            ( 'You have the Nth highest score', 6): 'Vous êtes au sixième rang',
            ( 'You have the Nth highest score', 7): 'Vous êtes au septième rang',
            ( 'You have the Nth highest score', 8): 'Vous êtes au huitième rang',
            ( 'You have the Nth highest score', 9): 'Vous êtes au neuvième rang',
            ( 'You have the Nth highest score', 10): 'Vous êtes au dixième rang'
            }
