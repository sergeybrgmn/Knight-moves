# Knight-moves

## The project idea
The idea of the project emerged when a friend of mine told me about an interview question: 
To calculate the amount of the Knight moves on the Chess board in order to visit every cell (cover the entire board).

So I couldn't resist to solve the task.
Also some Frontend control was added for the sake of practicing with Flask and working with PostgreSQL/MySQL databases.

## The Knight moves
All the backend logic for calculating the Knight moves is in the knight.py.

Here was my though process on how to code the caclulation of moves.

The entities I have to deal with are:
- board: an array NxN (by_default 8, could be set as a static constant) 
- inititial position: the initial position of the Knight
- move otion: 8 ways to change the position according to the game rules.
- real move: if the Knight stands near the borders - the move options are limited, as we can not go outside the board

- The move logic: there are 2 methods for making the move: 
    - Regular: when we choose a random move each time
    - Otimal: when we choose a random move but "try" not to step twice on the cell (we try to choose a new cell)

## Next steps
Deploy the app on the cloud. 
Maybe practice with AWS/GCP

Try to improve the move algorithm - make the each step not random, but use some common strategy to visit all the cells ASAP.
