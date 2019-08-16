"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.

Zahlenspiel is a numbers game in German.

"""
from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import decimal
import lite_call_runtime_top as call
import lite_call_output_manager as output_manager
import lite_call_logging as log

State = {}

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('CALLectorAlexaGames')
# Keep track of the high score per user
highScoresTable = dynamodb.Table('CALLectorAlexaGamesHighScores')
# Keep track of all obtained scores
scoresTable = dynamodb.Table('CALLectorAlexaGamesScores')

highScore = 0

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, visual_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': visual_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" + reprompt_text + "</speak>"
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + output + "</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" + reprompt_text + "</speak>"
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

# Get the user's saved state if any
def get_saved_state_from_db(userId, appId):
   
    try:
        response = table.get_item(
        Key={
            'userId': str(userId),
            'appId': str(appId),
        })
    except ClientError as e:
        return None
    else:
            
        response = replace_decimals(response)
        
        if 'Item' in response and 'laststate' in response['Item']:
            return response['Item']['laststate']
        else:
            return None

# Get 
def get_score_from_db(appId, userId):
   
    try:
       response = highScoresTable.get_item(
       Key={
           'appId': str(appId),
           'userId': str(userId),
       })
    except ClientError as e:
        return 0
    else:
        response = replace_decimals(response)

        if 'Item' in response and 'score' in response['Item']:
            return response['Item']['score']
        else:
            return 0
                
# Get all scores for the application
def get_all_scores_from_db(appId):
   
    scoreList = []
   
    response = scoresTable.query(
        KeyConditionExpression = Key('appId').eq(str(appId)),
        ScanIndexForward=False
    )

    # Store unique scores
    for i in response['Items']:
        if not i in scoreList:
            #print(i['score'])
            scoreList.append(i['score'])

    scoreList = replace_decimals(scoreList)
   
    #return sorted(scoreList, reverse=True)
    return scoreList
        
# Save the user's state
def save_state_in_db(userId, appId, State):
    table.put_item(
    Item={
        'userId': userId,
        'appId': appId,
        'laststate': State
    })   

# Delete the user's state
def delete_state_from_db(userId, appId):
    try:
        table.delete_item(
        Key={
            'userId': userId,
            'appId': appId,
        })   
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        print("Delete State succeeded:")

# Save the user's high score
def save_high_score_in_db(appId, userId, State):
    highScoresTable.put_item(
    Item={
        'appId': appId,
        'userId': userId,
        'score': State
    })   

# Save user's achieved score
def save_score_in_db(appId, State):
    scoresTable.put_item(
    Item={
        'appId': appId,
        'score': State
    })

# Calculate the position of the user in the leaderboard    
def get_score_position(scoreList, currentScore):

    position = 1
    
    for i in scoreList:
        if currentScore >= i:
            break;
        print(i)
        position += 1
    
    print ("Position:")
    print(position)
    
    return position
    
# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(userId):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    global State
    global reprompt_text
    print("UserId = " + str(userId))

    ( NewState, NewInitAct, NewDontUnderstandAct ) = call.init()
    SavedState = get_saved_state_from_db(userId, NewState['namespace']) 
     
    try:
        if SavedState:
            print('Trying to continue state (lambda)')
            ( State, InitAct, DontUnderstandAct ) = call.continue_state(SavedState, userId)
            print(State)
        else:
            print('Not trying to continue state')
            ( State, InitAct, DontUnderstandAct ) = ( NewState, NewInitAct, NewDontUnderstandAct )
            State["userId"] = userId
    except:
        print('Error when trying to continue state')
        ( State, InitAct, DontUnderstandAct ) = ( NewState, NewInitAct, NewDontUnderstandAct )
        State["userId"] = userId
        
    session_attributes = {}
    #card_title = "Welcome"
    card_title = output_manager.realise_generic_message('Welcome', [], State)
    speech_output = InitAct['text']
    visual_output = InitAct['visual_text']
    reprompt_text = DontUnderstandAct['text']
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, visual_output, reprompt_text, should_end_session))

# For one shot requests, we just get the default help text.
def handle_one_shot_request(intent, session):
    global State
    session_attributes = {}
    
    # We need to do an init to load language- and game-specific information.
    ( NewState, NewInitAct, NewDontUnderstandAct ) = call.init()
    action = call.default_help_action(NewState)

    result = action['text']
    visual_result = action['visual_text']
    should_end_session = True
    reprompt_text = 'Hm'

    card_title = output_manager.realise_generic_message('Respond', [], State)
    return build_response(session_attributes, build_speechlet_response(
            card_title, result, visual_result, reprompt_text, should_end_session))

def handle_intent_request(intent, session, standard_intent_or_not):
    global State
    session_attributes = {}

    # If we have a standard intent, the string we pass is the intent name
    if standard_intent_or_not == 'standard_intent':
        String = intent
    # Otherwise, we need to extract the rec string
    else:
        String = intent_to_string(intent)

    # In both cases, we let robust matching and the rest of the backend code
    # figure out what to do
    action = call.string_and_state_to_action(String, State)
    userId = State["userId"]
    save_state_in_db(userId, State['namespace'], State) 
    
    result = action['text']
    visual_result = action['visual_text']
    
    # Get user's high score
    highScore = get_score_from_db(State['namespace'], userId)

    print("Current high score:" + str(highScore))
    
    # Ensure that we are at the end of the lesson
    if 'presented_score' in action:

        save_score_in_db(State['namespace'], action['presented_score'][0])
            
        # Store only the best score
        if highScore < action['presented_score'][0]:
            save_high_score_in_db(State['namespace'], userId, action['presented_score'][0])
       
        scoreList = get_all_scores_from_db(State['namespace'])
    
        if scoreList != None:
            position = []
            #Compare the new high score against all high scores 
            position.append(get_score_position(scoreList, action['presented_score'][0]))
            # Announce leaderboard position only for the 10 best ones
            if position[0] <= 10:
                result += " " + output_manager.realise_generic_message('You have the Nth highest score', position, State)
                
    if 'end' in action and action['end'] == 'yes':
        should_end_session = True
        delete_state_from_db(userId, State['namespace'])
    else:
        should_end_session = False
    #card_title = "Respond"
    card_title = output_manager.realise_generic_message('Respond', [], State)
    return build_response(session_attributes, build_speechlet_response(
            card_title, result, visual_result, reprompt_text, should_end_session))

# Check whether the keys exist
def intent_to_string(intent):
    if 'slots' in intent and 'canonical' in intent['slots']:
        canonical = intent['slots']['canonical']
    else:
        return ''
    if ( 'resolutions' in canonical and
         'resolutionsPerAuthority' in canonical['resolutions'] and
         'values' in canonical['resolutions']['resolutionsPerAuthority'][0]
         ):
        return canonical['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    elif 'value' in canonical:
        return canonical['value'].lower()
    else:
        return ''
    
    
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(get_userId_from_session(session))

def get_userId_from_session(session):
    if "user" in session and "userId" in session["user"]:
        return session["user"]["userId"]
    else:
        return False   

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

##    if intent_name == "AMAZON.HelpIntent":
##        return handle_help_request()
##    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
##        return handle_session_end_request()
    # If we get a standard intent, we just pass the intent name
    if launch_has_not_been_invoked():
        return handle_one_shot_request(intent_name, session)
    elif is_standard_intent(intent_name):
        return handle_intent_request(intent_name, session, 'standard_intent')
    # Otherwise, we pass the whole intent
    else:
        return handle_intent_request(intent, session, 'not_standard_intent')

# If State still has its default value, then we haven't had a launchRequest
def launch_has_not_been_invoked():
    global State
    return State == {}

def is_standard_intent(intent_name):
    return intent_name.startswith('AMAZON.')

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    

