#!/usr/bin/python

import lite_call_runtime_top as call
import lite_call_runtime as call_main
import requests

def check_uris_in_compiled_alexa_dir(Dir):
    State = call.init_local(Dir)[0]
    check_audio_uris_in_state(State)

def check_audio_uris_in_state(State):
    ( Lessons, NErrors, NOK ) = ( call_main.get_all_current_lessons(State), 0, 0 )
    print(f'--- Lessons found {Lessons}')
    for Lesson in Lessons:
        call_main.set_lesson(State, Lesson)
        print(f'--- Checking prompts for {Lesson}')
        for URI in [ get_uri_from_prompt(State['prompt']) ] + \
            [ get_uri_from_prompt(Item['prompt']) for Item in State['forwardList'] if has_recorded_audio_prompt(Item) ]:
            if not uri_found(URI):
                print(f'*** Error: unable to find {URI}')
                NErrors += 1
            else:
                print(f'--- Found {URI}')
                NOK += 1
    print(f'Score: {NOK}/{NOK + NErrors} URIs found')

def has_recorded_audio_prompt(Item):
    return 'prompt' in Item and get_uri_from_prompt(Item['prompt'])

def get_uri_from_prompt(Prompt):
    Start = Prompt.find('<audio src="')
    if Start < 0:
        return False
    return Prompt[Start + len('<audio src="'):Prompt.find('"/>')]

def uri_found(path):
    try:
        r = requests.head(path)
        return r.status_code == requests.codes.ok
    except:
        return False
