from game import Game
from RL_brain import DeepQNetwork
import numpy as np

if __name__ == "__main__":
    # maze game
    game =Game()
    game.init()
    # number of observation * 2dir
    n_feature=(len(game.enemylist)+1)*2
    # number of action is 4 dir
    n_action=4

    RL = DeepQNetwork(4, n_feature,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )

    while True:
        step = 0
        game.init()
        game.render()
        observation = game.get_infomation()
        for episode in range(int(1e20)):
            # initial observation
            if game.command == 'exit':
                RL.plot_cost()
            game.init()
            game.render()
            observation=game.get_infomation()


            while True:
                # fresh env

                game.render()

                # RL choose action based on observation
                action = RL.choose_action(observation)

                # RL take action and get next observation and reward
                if action is 0:
                    game.player1.set_xy(game.player1.x+1*game.player1.speed,game.player1.y)
                if action is 1:
                    game.player1.set_xy(game.player1.x-1 * game.player1.speed, game.player1.y)
                if action is 2:
                    game.player1.set_xy(game.player1.x, game.player1.y+1 * game.player1.speed)
                if action is 3:
                    game.player1.set_xy(game.player1.x,game.player1.y-1 * game.player1.speed)

                reward, done=game.reward_judgment()
                observation_=Game.get_infomation(game)

                RL.store_transition(observation, action, reward, observation_)

                game.text_box.text_list.clear()
                game.text_box.text_list.append(str(episode)+':episode:')
                game.text_box.text_list.append(str(step)+':step:')
                game.text_box.text_list.append(str(reward)+':reward:')
                if len(RL.cost_his)>100:
                    cost_ave_100=np.average(RL.cost_his[-100:])
                    game.text_box.text_list.append(str(cost_ave_100)+':cost_ave_100')

                if (step > 200) and (step % 20 == 0):
                    RL.learn()
                    # RL.plot_cost()
                # swap observation
                # observation = observation_

                # break while loop when end of this episode
                if done:
                    break
                step += 1

        # end of game
        print('game over')
        game.render()

        RL.plot_cost()