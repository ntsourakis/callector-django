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
import whichanimal.python.lite_call_runtime_top as call
import whichanimal.python.lite_call_output_manager as output_manager
import os 

States = {};

def WhichAnimalPageView(request):
    return HttpResponse('Hello, WhichAnimal!')

# Class for initialization
class WhichAnimalInitView(APIView):
    permission_classes = (IsAuthenticated,)
			
	# Handle the GET request
    def get(self, request): 
    
        model = CALLectorGames
        
        userId = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        print("UserId = " + userId)
      
        # Initialize the state
        ( State, InitAct, DontUnderstandAct ) = WhichAnimalInitView.init(userId)
		
        #speech_output = InitAct['text']
        visual_output = InitAct['visual_text']
        
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
                StateDict = json.loads(SavedState.__str__())
                ( State, InitAct, DontUnderstandAct ) = call.continue_state(StateDict, userId)
            else:
                print('Not trying to continue state')
                ( State, InitAct, DontUnderstandAct ) = ( NewState, NewInitAct, NewDontUnderstandAct )
                State["userId"] = userId
                CALLectorGames.objects.create(userId=userId, laststate=json.dumps(State))
        except:
            print('Error when trying to continue state')
            ( State, InitAct, DontUnderstandAct ) = ( NewState, NewInitAct, NewDontUnderstandAct )
            State["userId"] = userId
        
        return ( State, InitAct, DontUnderstandAct )

# Class for getting messages        
class WhichAnimalMessageView(APIView):
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
            StateDict = json.loads(SavedState.__str__())
        except CALLectorGames.DoesNotExist:
            ( State, InitAct, DontUnderstandAct ) = WhichAnimalInitView.init(userId)
            StateDict = State
        
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
        highScore = WhichAnimalMessageView.getUserHighScore(userId)
		
        # Ensure that we are at the end of the lesson
        if 'presented_score' in action:
            WhichAnimalMessageView.saveScore(action['presented_score'][0])
        
            # Store only the best score
            if highScore.__str__() < action['presented_score'][0]:
                WhichAnimalMessageView.saveUserHighScore(userId, action['presented_score'][0])
            
            scoreList = WhichAnimalMessageView.getAllUserScores()
            print(type(scoreList))
			
            if scoreList != None:
                position = []
                #Compare the new high score against all high scores 
                position.append(WhichAnimalMessageView.getScorePosition(scoreList, action['presented_score'][0]))
                # Announce leaderboard position only for the 10 best ones
                if position[0] <= 10:
                    result += " " + output_manager.realise_generic_message('You have the Nth highest score', position, StateDict)
                
        if 'end' in action and action['end'] == 'yes':
            WhichAnimalMessageView.deleteState(userId)
        
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
		