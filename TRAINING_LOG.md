### 6*6_numeps_100_num_mcts_sims_25_2_input_channel - A
- trained for 2 days. around 40 iterations
- self-competation, the latest 9 iterations, always draw. (40 games in total, 38+ draws)

However, it can stll not win the author:

Turn  26 Player  -1
   0 1 2 3 4 5 
-----------------------
0 |- O - - X - |
1 |- - O O X - |
2 |O X X X O O |
3 |O X O O O - |
4 |X O O - O X |
5 |- X X - X X |
-----------------------
[ 0 0] [ 0 2] [ 0 3] [ 0 5] [ 1 0] [ 1 1] [ 1 5] [ 3 5] [ 4 3] [ 5 0] [ 5 3]  


The AI (0) failed to detect they shall put the stone on [3 5].


Compete the 2 channel model with the 1 channel model, both uses 50 simulations for each step. The outcome is 

channel 1 model wins / loss /draw: 6 / 5 / 9 

performs nearly the same.


Analysis:

Loss_pi=8.34e-01, Loss_v=2.89e-02


### 6*6_numeps_100_num_mcts_sims_100_2_input_channel - B
- trained for one night. 13 iterations
- around 30 / 40 draw rate. Not saturated yet.

When comparing B with A in 10 games, A's win / loss / draw rate is 1 / 4 / 15

Analysis:
 - We did not see a significant improvement in B even after increasing the simulation depths in MCTS. 

Next steps
 - Check if there is any bugs in the code.
 - continue to train B until it saturates (40 draws in each iteration)



 -----------------------
[ 0 0] [ 0 1] [ 0 2] [ 0 3] [ 0 5] [ 1 0] [ 1 1] [ 1 2] [ 1 5] [ 2 0] [ 2 5] [ 3 0] [ 3 5] [ 4 0] [ 4 3] [ 4 4] [ 4 5] [ 5 0] [ 5 1] [ 5 2] [ 5 3] [ 5 4] [ 5 5] 4 5
Turn  15 Player  1
   0 1 2 3 4 5 
-----------------------
0 |- - - - X - |
1 |- - - O O - |
2 |- X X X O - |
3 |- X O O O - |
4 |- O X - - - |
5 |- - - - X - |
-----------------------
   0 1 2 3 4 5 
-----------------------
0 |0.00 0.00 0.00 0.00 0.00 0.00 |
1 |0.00 0.00 0.00 0.00 0.00 0.00 |
2 |0.00 0.00 0.00 0.00 0.00 0.00 |
3 |0.00 0.00 0.00 0.00 0.00 1.00 | # HERE IS A BUG!
4 |0.00 0.00 0.00 0.00 0.00 0.00 |
5 |0.00 0.00 0.00 0.00 0.00 0.00 |
-----------------------
Turn  16 Player  -1
   0 1 2 3 4 5 
-----------------------
0 |- - - - X - |
1 |- - - O O - |
2 |- X X X O - |
3 |- X O O O O |
4 |- O X - - - |
5 |- - - - X - |
-----------------------
[ 0 0] [ 0 1] [ 0 2] [ 0 3] [ 0 5] [ 1 0] [ 1 1] [ 1 2] [ 1 5] [ 2 0] [ 2 5] [ 3 0] [ 4 0] [ 4 3] [ 4 4] [ 4 5] [ 5 0] [ 5 1] [ 5 2] [ 5 3] [ 5 5] 

2 2
3 2
1 2
2 4
1 3
4 0
4 5


Turn  21 Player  1
   0 1 2 3 4 5 
-----------------------
0 |- - - - X - |
1 |- - O O O X |
2 |- X X X O O |
3 |- X O O O O |
4 |- O X - - - |
5 |- X X - X - |
-----------------------
AI must place stone on (5,5), (3, 5) or (0, 5)

-----------------------
0 |0.00 0.00 0.00 0.00 0.00 0.00 | # MCTS visit count
1 |0.00 0.00 0.00 0.00 0.00 0.00 |
2 |26.00 0.00 0.00 0.00 0.00 0.00 |
3 |0.00 0.00 0.00 0.00 0.00 0.00 |
4 |42.00 0.00 0.00 0.00 0.00 0.00 |
5 |0.00 0.00 0.00 31.00 0.00 0.00 |
-----------------------
   0 1 2 3 4 5 
-----------------------
0 |0.00 0.00 0.00 0.00 0.00 0.00 | # move prob reported by MCTS
1 |0.00 0.00 0.00 0.00 0.00 0.00 |
2 |0.26 0.00 0.00 0.00 0.00 0.00 |
3 |0.00 0.00 0.00 0.00 0.00 0.00 |
4 |0.42 0.00 0.00 0.00 0.00 0.00 |
5 |0.00 0.00 0.00 0.31 0.00 0.00 |
-----------------------
   0 1 2 3 4 5 
-----------------------
0 |0.00 0.00 0.00 0.00 0.00 0.00 | # move prob reported by policy network
1 |0.00 0.00 0.00 0.00 0.00 0.00 |
2 |0.27 0.00 0.00 0.00 0.00 0.00 |
3 |0.00 0.00 0.00 0.00 0.00 0.00 |
4 |0.41 0.00 0.00 0.00 0.00 0.00 |
5 |0.00 0.00 0.00 0.31 0.00 0.00 |
-----------------------
Turn  22 Player  -1

However, AI selects to play on (0, 4), which makes it losing the game.
   0 1 2 3 4 5 
-----------------------
0 |- - - - X - |
1 |- - O O O X |
2 |- X X X O O |
3 |- X O O O O |
4 |O O X - - - |
5 |- X X - X - |


## 6*6_numeps_100_num_mcts_sims_100_2_input_channel_128_channels
45 iterations
It beats the old model by 

player 1 wins / loss /draw: 0 / 8 / 12

Player 1 is the old model.
 7708/7708 [01:24<00:00, 91.66it/s, Loss_pi=1.94e+00, Loss_v=1.09e-01]

The previous model's issue is overfitting. After reducing the NN net filters from 512 to 128, 
the model performance dramatically improves.

## 15*15_numeps_100_num_mcts_sims_25_temp_15_input_channels_2_channels_128

Has over fitting issue. The test error is 100% higher than the training error.  

```EPOCH ::: 10
Training Net: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2490/2490 [02:18<00:00, 17.95it/s, Loss_pi=2.69e+00, Loss_v=1.00e-01]
2024-11-22 23:30:28 Bos-Mac-mini.local gomoku.pytorch.NNet[78352] INFO Test Losses - Policy Loss: 5.0656, Value Loss: 0.1131
```

Implemented the early stopping logic.

TODO: The 


Nov 23. GPU prediction , 0.8 ms, for 15*15 , 128 channels. 1 batch size.


GPU optimization stats:

All units are seconds
batch size  ; prediction time (within function); outside of function  ;    seconds per example

1              0.0014                               0.20                      
16             0.0015                               0.28
64             0.0024                               0.29
128            0.0034                               0.41
256            0.0062                               0.66
512            0.0117                               1.23
1024           0.0222                               2.39


(NN forward) Prediction on CPU 
batch size  ; prediction time (within function); outside of function  ;    seconds per example

1              0.0012                               0.12                      
16             0.0200                               2
64             0.048                                4.99

Takeaway: 
  - GPU is good at parallism. The sweet batch size for this case is around 128. 
  - CPU does job sequentially. When batch size increases to 64, multicore starts to work, introducing some sort of parallisation




Seems to be a bug in the 15*15 model.

Likely to be a game rule bug. 

   0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 
-----------------------
0 |- - - - - - - - - - - - - - - |
1 |- - - - - - - - - - - - - - - |
2 |- - - - - - - - - - - - - - - |
3 |- - - - - - - - - - - - - - - |
4 |- - - - O - - - - - - - - - - |
5 |- - - - - - - - - - - - - - - |
6 |- - - - X X X X O - - - - - - |
7 |- - - - - - - O - - - - - - - |
8 |- - - - - - - O - - - - - - - |
9 |- - - - - - - - - O - - - - - |
10 |- - - - - - - - - - - - - - - |
11 |- - - - - - - - - - - - - - - |
12 |- - - - - - - - - - - - - - - |
13 |- - - - - - - - - - - - - - - |
14 |- - - - - - - - - - - - - - - |
-----------------------
[ 3 4] 3 6
Invalid move
3 4

Policy
   0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 
-----------------------
0 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
1 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
2 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
3 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
4 |0.00 0.00 0.00 0.91 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
5 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
6 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.09 0.00 0.00 0.00 0.00 0.00 0.00 |
7 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
8 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
9 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
10 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
11 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
12 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
13 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
14 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
-----------------------

MCTS

   0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 
-----------------------
0 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
1 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
2 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
3 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
4 |0.00 0.00 0.00 0.09 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
5 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
6 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.91 0.00 0.00 0.00 0.00 0.00 0.00 |
7 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
8 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
9 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
10 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
11 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
12 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
13 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
14 |0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 |
-----------------------

Why there is only one valid move, 
why 0.09 becomes 0.91, such a big boost after MCTS

This bug is fixed.

## Jan 5th, 2025

Topic: Message queue for CPU and GPU comunication.

ALL MEASUREMENT IS DONE ON MAC MINI 2020.

args = dotdict({
    'numIters': 1000,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 60,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 100,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 30,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './checkpoints/gomoku/15*15_numeps_100_num_mcts_sims_25_temp_15_input_channels_2_channels_64',
    'load_model': False,
    'load_folder_file': ('checkpoints/gomoku/15*15_numeps_100_num_mcts_sims_25_temp_15_input_channels_2_channels_64','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
    'num_channels': 64,
    'input_channels': 2,
    # parallism params
    'num_workers': 1,
})

No message queue.

Self play with 1 workers: 18s/it. 
From CPU/GPU history.
One CPU performance core is in high usage. 
GPU is in 100% usage.

Self play with 2 workers: 13s/it
2 CPU performance core is in high usage.
GPU is 100% usage.
Python 90% CPU (from monitor)

Self play with 4 workers: 15s/it
2 CPU performance core in high usage.
GPU 100%
Python 100%

Conclusion: Bottleneck is at GPU. CPU is not fully utilized.

Self play with 8 workers: 14s/it (high variance)
2 CPU performance core in high usage.
GPU 100%
Python 100%


Message queue, GPU wait for 1ms per batch.
avg 8 tasks in the queue per batch.
Self play with 16 workers: 5s/it
2 CPU performance core in high usage.
GPU 80% utilization.
Python 90%


Message queue, GPU wait for 1ms per batch.
avg 17 tasks in the queue per batch.

Self play with 32 workers: 6.38s/it
3 CPU performance core in middle usage.
GPU 60% utilization.
Python 90%

Message queue, GPU wait for 0.5ms per batch.
17 tasks per batch.
Self play with 32 workers: 5.5s/it
3 CPU performance core in middle usage.
GPU 60% utilization.
Python 90%


Message queue, GPU wait for 0.1ms per batch.
17 tasks per batch.
Self play with 32 workers: 5s/it
2 CPU performance core in middle usage.
GPU 60% utilization.
Python 90%

Conclusion: seems to be a bug here. the timeout time needs to be evaluated. 

### Jan 6th, 2025

removed the timeout waiting in the task_queue.get() method. 
Now in average, there are multiple tasks waiting in the queue when the GPU looping thread is waken up. 

For 32 workers, 5s/it 
2 CPU performance core is in high usage. 

Sth is wrong. The new model keeps getting rejected. 

args = dotdict({
    'numIters': 1000,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 60,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 100,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 30,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './checkpoints/gomoku/15*15_numeps_100_num_mcts_sims_25_temp_15_input_channels_2_channels_64',
    'load_model': False,
    'load_folder_file': ('checkpoints/gomoku/15*15_numeps_100_num_mcts_sims_25_temp_15_input_channels_2_channels_64','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
    'num_channels': 64,
    'input_channels': 2,
    'verbose': 0,
    # parallism params
    'num_workers': 32,
})

The board is 15*15.

# Feb 17， 2025
So, Let's debug the multithread issue. 
Reduce the board size to 6*6 and retry. 
