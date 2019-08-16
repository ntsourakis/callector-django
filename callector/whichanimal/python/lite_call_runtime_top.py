#!/usr/bin/python

import whichanimal.python.lite_call_runtime as call_main
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# NEW INTERFACE

def load_tables(TableFile, MatchingFile):
    return call_main.load_tables(TableFile, MatchingFile)

def get_initial_state(Namespace, Domain, L1):
    return call_main.get_initial_state(Namespace, Domain, L1)

def get_initial_state_basic(Namespace, Domain, L1):
    return call_main.get_initial_state_basic(Namespace, Domain, L1)

def continue_from_saved_state(State):
    return call_main.continue_from_saved_state(State)

def continue_from_saved_state_basic(State):
    return call_main.continue_from_saved_state_basic(State)

# OLD INTERFACE

# Use this to load table file from canonical place in zipfile (speech interface)
def init():
    TableFile = dir_path + '/call_tables.data.gz'
    MatchingFile = dir_path + '/robust_matching_tables.data.gz'
    return call_main.init_state(TableFile, MatchingFile)

# Use this and next function if we're in a session that got interrupted
def can_continue_state(State, userId):
    return call_main.can_continue_state(State, userId)

def continue_state(State, userId):
    return call_main.continue_state(State, userId)

# Use this to load table file from canonical place in zipfile (web-server interface)
def init_basic():
    TableFile = 'call_tables.data.gz'
    MatchingFile = 'robust_matching_tables.data.gz'
    return call_main.init_state_basic(TableFile, MatchingFile)

# For one-shot responses in Alexa
def default_help_action(State):
    return call_main.default_help_action(State)

# Top-level call for Alexa version: string to string
def string_and_state_to_action(String, State):
    return call_main.string_and_state_to_action_main(String, State)

# Top-level call for web-server version: json to json
def message_and_state_to_message(Message, State):
    return call_main.process_call_message(Message, State)

# Top-level call for doing robust matching (either version)
def robust_match(String, State, N):
    return call_main.robust_match_string(String, State, N)

# Convenient for testing on local machine (Alexa apps)
def init_local(Dir0):
    LocalCompiledDir = os.path.abspath(os.path.expandvars('$REGULUSLITECONTENT/alexa_content/compiled/')).replace('\\', '/')
    TableFile = f'{LocalCompiledDir}/{Dir0}/call_tables.data.gz'
    MatchingFile = f'{LocalCompiledDir}/{Dir0}/robust_matching_tables.data.gz'
    return call_main.init_state(TableFile, MatchingFile)

#  Possible values:
#  'quel_animal'
#  'zahlenspiel'
#  'welches_tier'
#  'number_game'
#  'which_language'
#  'which_movie'
#  'jeu_de_chiffres'
#  'quelle_langue'

# import lite_call_runtime_top as call
# (State, Init, Bad) = call.init_local('which_animal')
# call.string_and_state_to_action('help', State)
# call.robust_match('vassili', State, 2)

# Convenient for testing on local machine (web-server apps)

# Dir = 'c:/cygwin64/home/speech/reguluslitecontent-svn/trunk/litecontent/tmp/IAPETUSForServer/dante/python/'
# TableFile = Dir + 'call_tables.data.gz'
# RobustFile = Dir + 'robust_matching_tables.data.gz'
# import lite_call_runtime_top as call
# import lite_call_runtime as call_main
# State = call_main.init_state_basic(TableFile, RobustFile)
# call.message_and_state_to_message(['get_available_lessons'], State)
# call.message_and_state_to_message(['set_lesson_by_name', 'Inferno I 1-30'], State)
# call.message_and_state_to_message(['help_file'], State)
# call.message_and_state_to_message(['spoken_help'], State)
# call.message_and_state_to_message(['match', 'mi ritrovai per una selva oscura'], State)
