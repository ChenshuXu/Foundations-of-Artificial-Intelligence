# Fundations of Artificial Intelligence

### 1. solve sophisticated 3D Mazes

In this project, I need to apply AI search techniques to solve some sophisticated 3D Mazes. Each 3D maze is a grid of points (not cells) with (x, y, z) locations in which your agent may use one of the 18 elementary actions to move to one of the 18 neighboring grid point locations. At each grid point, my agent is given a list of actions that are available for the current point your agent is at. My agent will select and execute one of these available actions to move inside the 3D maze.

![**3D Maze Configuration: grids world that contains travelable actions**](./solve\ sophisticated\ 3D\ Mazes/maze2.jpg)

To find the solution, I used the following algorithms:
- Breadth-first search algorithm
- Uniform-cost search algorithm
- A* search (A*) algorithm

### 2. little go game

In this project, you developed my own AI agents based on some of the AI techniques for Search, Game Playing, and Reinforcement Learning that I have learnt in class to play a small version of the Go game, that has a reduced board size of 5x5. My agent played this Little-Go game against some basic as well as more advanced AI agents. 

To beat other players, I build three algorithms:

- Greedy algorithm
- Min-Max with alpha-beta pruning algorithm
- Q-Learning algorithm

The finally I achieved 90% + win rate against all three kinds of players from grader.

### 3. classify hand-written digits

In this project, I implemented a multi-layer perceptron (MLP) neural network and use it to classify hand-written digits without using any machine learning libraries. I implemented feedforward/backpropagation as well as training process by myself. The hand-written data set we use is [MNIST](http://yann.lecun.com/exdb/mnist/) dataset.

![Figure1](./classify\ hand-written digits/Figure1.jpg)

The neural network is setup like this:

![Figure2](./classify\ hand-written digits/Figure2.png)

