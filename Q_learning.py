import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =   20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999



def default_Q_value():
    return 0


if __name__ == "__main__":



    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v0")
    env.seed(1)
    env.action_space.np_random.seed(1)


    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.

    episode_reward_record = deque(maxlen=100)


    for i in range(EPISODES):
        episode_reward = 0

        #TODO PERFORM Q LEARNING
        total_reward = 0
        
        obs = env.reset()
        done = False
        
        while done == False:
            last = obs
            
            if random.uniform(0,1) < EPSILON:
                action = env.action_space.sample()
            else:
                prediction = np.array([Q_table[(obs,i)] for i in range(env.action_space.n)])
                action =  np.argmax(prediction)
                
            obs,reward,done,info = env.step(action)
            total_reward += reward

            
            if done == False:
                nex = np.array([Q_table[(obs,i)] for i in range(env.action_space.n)])                                  
                Q_table[last, action] = Q_table[last, action] + LEARNING_RATE*(reward + DISCOUNT_FACTOR*np.max(nex) - Q_table[last, action])
                            
        episode_reward_record.append(total_reward) 
        EPSILON = EPSILON*EPSILON_DECAY
        if done == True:
            Q_table[last, action] = Q_table[last, action] + LEARNING_RATE*(reward - Q_table[last, action])
        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    ####DO NOT MODIFY######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    #######################