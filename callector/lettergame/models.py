from django.db import models

# Keep track of the last State
class CALLectorGames(models.Model):
    userId=models.CharField(max_length=100, primary_key=True)
    laststate=models.TextField(max_length=10000)
	
    def __str__(self):
        return self.laststate	    
   
# Keep track of the high scores
class CALLectorGamesHighScores(models.Model):
    userId=models.CharField(max_length=100, primary_key=True)
    score=models.IntegerField()
	
    def __str__(self):
        return self.score
		
# Keep track of the scores
class CALLectorGamesScores(models.Model):
    #namespace=models.CharField(max_length=100, primary_key=True)
    score=models.IntegerField(primary_key=True)
	
    def __str__(self):
        return self.score