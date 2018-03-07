import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin


    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250

class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        #self._numberLoss = [] #create an empty list where probabilities of loss will be stored
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            #store the number of losses
            #self._numberLoss.append(len(self._gameRewards))??

            # summary statistics on rewards
        self._sumStat_games = \
            Stat.SummaryStat('Outcomes of Games',self._gameRewards)
            # summary statistics on loss
        #self._sumStat_loss = \
            #Stat.SummaryStat('Outcomes of Games', self._numberLoss)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return self._sumStat_games.get_mean()

    def get_CI_reward(self, alpha):
        """
        :param alpha: confidence level
        :return: t-based confidence interval
        """
        return self._sumStat_games.get_t_CI(alpha)

    def get_PI_reward(self, alpha):
        '''

        :param alpha: confidence interval
        :return: returns the prediction interval of the expected reward
        '''
        return self._sumStat_games.get_PI(alpha)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards


    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
        return count_loss / len(self._gameRewards)

   # def get_avg_probability_loss(self):
        #return self._sumStat_loss.get_mean()

    #def get_CI_prob_loss(self, alpha):
        #"""
        #:param alpha: confidence level
        #:return: t-based confidence interval
       # """
        #return self._sumStat_loss.get_t_CI(alpha)

#Problem 1

# Calculate expected reward of 1000 games
trial = SetOfGames(prob_head=0.5, n_games=1000)
print("The average expected reward is:", trial.get_ave_reward())
print('95% CI of expected reward', trial.get_CI_reward(.05))

#Find the probability of a loss
print("The probability of a single game yielding a loss is:", trial.get_probability_loss())
#print('95% CI of probabilty of loss', ?

#Problem 2
#CI Interpretations:

#The expected reward is -25.9. When the game is run many times, the expected reward will be between -31.79 and
#-20 95% of the times.

# The expected loss of a single game is .607. When the game is run many times, the probality of loss will be between X
#and Y 95% of the times.

#Problem 3
#From the perspective of a Casino Owner: They would get to play many times--say, 10,000
# Calculate expected reward of 1000 games
trial = SetOfGames(prob_head=0.5, n_games=10000)
print("The average expected reward for the Casino Owner is:", trial.get_ave_reward())
print('95% CI of expected reward for the Casino Owner', trial.get_CI_reward(.05))

#From the perspective of a gambler who only gets to play 10 times:
trial = SetOfGames(prob_head=0.5, n_games=10)
print("The average expected reward for the Gambler is:", trial.get_ave_reward())
print('95% PI of expected reward for the Gambler', trial.get_PI_reward(.05))
