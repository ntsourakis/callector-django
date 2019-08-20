from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from .models import CALLectorGames
from .models import CALLectorGamesHighScores
from .models import CALLectorGamesScores
from ast import literal_eval
import json
import uuid
import sys
#sys.path.append('./dante/python/')
#sys.path.append('/app/poetry/python/')
import numbergame.python.lite_call_runtime_top as call
import numbergame.python.lite_call_output_manager as output_manager
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

States = {};

def NumberGamePageView(request):
    return HttpResponse('Hello, NumberGame!')

# Class for initialization
class NumberGameInitView(APIView):
    permission_classes = (IsAuthenticated,)
			
	# Handle the GET request
    def get(self, request): 
    
        model = CALLectorGames
        
        userId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        print("UserId = " + userId)
      
        # Initialize the state
        ( State, InitAct, DontUnderstandAct ) = NumberGameInitView.init(userId)
		
        #speech_output = InitAct['text']
        #speech_output = InitAct['text']
        visual_output = InitAct['visual_text']
        #l_result = {'stateId':userId, 'state':State.__str__()}
		
        #return Response(speech_output)
        return Response(visual_output)
	
	# Initialize the state
    def init(userId): 
		 
        ( NewState, NewInitAct, NewDontUnderstandAct ) = call.init()
       
        try:
            SavedState = CALLectorGames.objects.get(userId=userId)
        except CALLectorGames.DoesNotExist:
            SavedState = None

        try:
            if SavedState:
                print('Trying to continue state')
                #StateDict = json.loads((SavedState.__str__()).replace("\"", "\\\"").replace("True", "true").replace("False", "false").replace("\'", "\""))
                StateDict = json.loads(SavedState.__str__())
                ( State, InitAct, DontUnderstandAct ) = call.continue_state(StateDict, userId)
            else:
                print('Not trying to continue state')
                ( State, InitAct, DontUnderstandAct ) = ( NewState, NewInitAct, NewDontUnderstandAct )
                State["userId"] = userId
                #CALLectorGames.objects.create(userId=userId, laststate=State.__str__())
                CALLectorGames.objects.create(userId=userId, laststate=json.dumps(State))
        except:
            print('Error when trying to continue state')
            ( State, InitAct, DontUnderstandAct ) = ( NewState, NewInitAct, NewDontUnderstandAct )
            State["userId"] = userId
         
        print("Current state:" + State.__str__())
		
        return ( State, InitAct, DontUnderstandAct )
        
class NumberGameInitViewOLD(APIView):
    permission_classes = (IsAuthenticated,)
			
    def get(self, request): 

        global State
        model = State
        
        #l_newState = call.init_basic()
        
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        #l_stateId = uuid.uuid4().hex # generate unique Id for state
        
        ##State.objects.create(userId=request.META.get('HTTP_AUTHORIZATION').split(' ')[1], current=l_newState)
        ##State.objects.userId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        ##State.objects.current = l_newState
        ##State.objects.save()
		
        #state, created = State.objects.get_or_create(userId=request.META.get('HTTP_AUTHORIZATION').split(' ')[1], current=l_newState)

        #if created:
        #    print ("--- INIT | New user: %s #" % l_stateId)
        #else:
        #    print ("--- INIT | Existing user: %s #" % l_stateId)
   
        try:
            currentState = State.objects.get(userId=l_stateId)
			
            if 'Item' in currentState and 'laststate' in currentState['Item']:
                currentState = currentState['Item']['laststate']
            else:
                currentState = None
				
        except State.DoesNotExist:
            currentState = None
        
        if currentState:
            print("--- INIT | Existing user: %s #" % l_stateId)
            #currentState["userId"] = l_stateId
            call.continue_state(currentState, l_stateId)
            #( State, InitAct, DontUnderstandAct ) = call.continue_state(currentState, l_stateId)
            print("1111111")
            #State["userId"] = userId			
            l_result = {'stateId':l_stateId, 'state':currentState.__str__()}
            print("2222222")
        else:
            print("--- INIT | New user: %s #" % l_stateId)
            l_newState = call.init_basic()
            #print("--- INIT | type(l_newState): %s #" % type(l_newState))	
            State.objects.create(userId=l_stateId, current=l_newState)
            l_result = {'stateId':l_stateId, 'state':l_newState}
			
		##model.(l_newState)
		
		##setattr(f, l_newState)
		##f.save()

        ##l_newState = call.init_state('C:/Projects/django/callector/api/python/call_tables.data.gz', 'C:/Projects/django/callector/api/python/robust_matching_tables.data.gz')
        ##l_newState = call.init_state('C:/Projects/django/callector/api/lite_call_python/call_tables.data.gz', 'C:/Projects/django/callector/api/lite_call_python/robust_matching_tables.data.gz')
        
        #States[l_stateId] = l_newState
        #TODO
        #print (">>>>>>> INIT >>>>>>> States[l_stateId] : %s" % States[l_stateId])
        #print (">>>>>>> INIT >>>>>>> States : %s" % States)
		
		##request.session['l_stateId'] = l_newState
        ##fav_color = request.session.get('fav_color')
        ##print(fav_color)
        ##request.session['fav_color'] = 'blue'
        ##fav_color = request.session.get('fav_color')
        ##print(fav_color)
        ##for key, value in request.session.items():
        ##    print('{} => {}'.format(key, value))
        #l_result = {'stateId':l_stateId, 'state':l_newState}
        
        ##if 'fav_color' in request.session:
        ##   print(request.session['fav_color'])
        ##request.session['fav_color'] = 'blue'        
        
        return Response(l_result)

# Class for getting messages 
class NumberGameMessageView(APIView):
    permission_classes = (IsAuthenticated,)
	
    # Handle the POST request
    def post(self, request): 

        model = CALLectorGames
        
        #l_newState = call.init_basic()
        
        req = json.loads(request.body)
        userId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        String = req['message']
        print ("--- MESSAGE | Received message: %s #" % String)
        
        StateDict = None
		
        # Get the saved state
        try:
            SavedState = CALLectorGames.objects.get(userId=userId)
            # Create a dictionary from the json string
		    #StateDict = json.loads((SavedState.__str__()).replace("\"", "\\\"").replace("True", "true").replace("False", "false").replace("\'", "\""))
            StateDict = json.loads(SavedState.__str__())
        except CALLectorGames.DoesNotExist:
            ( State, InitAct, DontUnderstandAct ) = NumberGameInitView.init(userId)
            StateDict = State
        
        print("Current state:" + StateDict.__str__())
		
		# In both cases, we let robust matching and the rest of the backend code
        # figure out what to do
        action = call.string_and_state_to_action(String, StateDict)
        userId = StateDict["userId"]
        print(action)	
        
        CALLectorGames.objects.filter(userId=userId).update(laststate=json.dumps(StateDict))
		
        #result = action['text']
        visual_result = action['visual_text']
        result = visual_result
		
        # Get user's high score
        highScore = NumberGameMessageView.getUserHighScore(userId)
        #print("Current high score:" + highScore.__str__())
		
	    
		
        #NumberGameMessageView.saveUserHighScore(userId, 100)
        #NumberGameMessageView.saveScore(30)
        
        #position = []
        #scoreList = NumberGameMessageView.getAllUserScores()
        #position.append(NumberGameMessageView.getScorePosition(scoreList, 29))
        #print(type(scoreList))
		
        #print(output_manager.realise_generic_message('You have the Nth highest score', position, StateDict))
        #NumberGameMessageView.deleteState(userId=userId)
		
		
		
        # Ensure that we are at the end of the lesson
        if 'presented_score' in action:
            NumberGameMessageView.saveScore(action['presented_score'][0])
        
            # Store only the best score
            if highScore.__str__() < action['presented_score'][0]:
                NumberGameMessageView.saveUserHighScore(userId, action['presented_score'][0])
            
            scoreList = NumberGameMessageView.getAllUserScores()
            print(type(scoreList))
			
            if scoreList != None:
                position = []
                #Compare the new high score against all high scores 
                position.append(NumberGameMessageView.getScorePosition(scoreList, action['presented_score'][0]))
                # Announce leaderboard position only for the 10 best ones
                if position[0] <= 10:
                    result += " " + output_manager.realise_generic_message('You have the Nth highest score', position, StateDict)
                
        if 'end' in action and action['end'] == 'yes':
            NumberGameMessageView.deleteState(userId)
        
        return Response(result)		
     
    # Get the score from the database for the specific user 
    def getUserHighScore(userId):
            
        model = CALLectorGamesHighScores
            
        try:
            return CALLectorGamesHighScores.objects.get(userId=userId)
        except CALLectorGamesHighScores.DoesNotExist:
            return 0;

    # Get all scores for the application 
    def getAllUserScores():
            
        model = CALLectorGamesScores
            
        try:
            return sorted(CALLectorGamesScores.objects.values_list(), reverse=True)
        except CALLectorGamesScores.DoesNotExist:
            return None;
			
    # Save user's achieved score
    def saveScore(score):
			
        model = CALLectorGamesScores
        
        try:
            CALLectorGamesScores.objects.update_or_create(score=score)
            return 1
        except:
            return 0
			
    # Save user's highest score
    def saveUserHighScore(userId, score):
			
        model = CALLectorGamesHighScores
			
        try:
            CALLectorGamesHighScores.objects.update_or_create(userId=userId, score=score)
            return 1
        except:
            return 0

    # Delete the user's state
    def deleteState(userId):
        
        model = CALLectorGames
	    
        try:
            CALLectorGames.objects.filter(userId=userId).delete()
            print("Delete State succeeded")
            return 1		
        except:
            print("Delete State failed")
            return 0
			
    # Calculate the position of the user in the leaderboard    
    def getScorePosition(scoreList, currentScore):

        position = 1
    
        for i in scoreList:
            if currentScore >= i[0]:
                break;
            print(i)
            position += 1
    
        print ("Position:")
        print(position)
    
        return position
		
class NumberGameMessageViewNew(APIView):
    permission_classes = (IsAuthenticated,)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
			
    def post(self, request):
        
        model = CALLectorGames
		
        req = json.loads(request.body)
        userId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        print ("--- MESSAGE | Received message: %s #" % l_message)
        print("userId:")
        print(userId)

        # In both cases, we let robust matching and the rest of the backend code
        # figure out what to do
        action = call.string_and_state_to_action(String, State)
        userId = State["userId"]
        #save_state_in_db(userId, State['namespace'], State) 
        CALLectorGames.objects.create(userId=userId, current=State.__str__())
    
        try:
            l_state = CALLectorGames.objects.get(userId=userId)
        except CALLectorGames.DoesNotExist:
            l_state = None
        
        python_dict = literal_eval(l_state.__str__())
        l_newState = call.init_basic()
        l_result = call.message_and_state_to_message(l_message, python_dict)
        print ("--- MESSAGE | Result : %s #" % l_result)
        CALLectorGames.objects.filter(userId=userId).update(current=python_dict)
        
        return Response(l_result)
		
class NumberGameMessageViewOLD(APIView):
    permission_classes = (IsAuthenticated,)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
			
    def post(self, request):

        model = State
		
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        #l_stateId = req['state']
        l_message = req['message']
        print ("--- MESSAGE | Received message: %s #" % l_message)
        print("l_stateId:")
        print(l_stateId)
        #print("l_state")
        #l_state = request.session['l_stateId']

        ##for key, value in request.session.items():
        ##    print('{} => {}'.format(key, value))
        ##fav_color = request.session.get('fav_color')
        ##print(fav_color)
        ##print ("len(States) : %d" % len (States))
        ##print (">>>>>>> MESSAGE >>>>>>> States : %s" % States)
        
		#l_state = States[l_stateId]
        try:
            l_state = State.objects.get(userId=l_stateId)
        except State.DoesNotExist:
            l_state = None
        
        #print("--- MESSAGE | Current state: %s #" % l_state)
        ##st = request.session['States']
        
        ##print ("len(States) : %d" % len (States))
		##print(l_state);
        ##if 'fav_color' in request.session:
        ##   print(request.session['fav_color'])
		
        ##l_state=State.objects.get()
        ##print("l_state")
        ##print ("l_state : %s" % l_state)
        #print("--------------------")
        #print(json.loads(l_state.__str__()))
        python_dict = literal_eval(l_state.__str__())
        #print("--- MESSAGE | type(python_dict): %s #" % type(python_dict))	
        #print(python_dict)
        l_newState = call.init_basic()
        l_result = call.message_and_state_to_message(l_message, python_dict)
        #print("--- Message | New state: %s #" % python_dict)
        print ("--- MESSAGE | Result : %s #" % l_result)
        ##print ("l_state : %s" % l_state)
        #States[l_stateId] = l_state
        State.objects.filter(userId=l_stateId).update(current=python_dict)
        ##print (">>>>>>> MESSAGE >>>>>>> States[l_stateId] : %s" % States[l_stateId])
        
        return Response(l_result)

class NumberGameRobustView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        req = json.loads(request.body)
        l_stateId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        l_message = req['message']
        ##print("l_state")
        #l_state = States[l_stateId]
        try:
            l_state = State.objects.get(userId=l_stateId)
        except State.DoesNotExist:
            l_state = None
			
        python_dict = literal_eval(l_state.__str__())
        ##print("l_state")
        ##print(l_state);
        #l_result = call.robust_match(l_message, l_state, 1)
        l_result = call.robust_match(l_message, python_dict, 1)
        #States[l_stateId] = l_state 
        State.objects.filter(userId=l_stateId).update(current=python_dict)
		
        #print (">>>>>>> ROBUST >>>>>>> States[l_stateId] : %s" % States[l_stateId])
        		
        return Response(l_result)