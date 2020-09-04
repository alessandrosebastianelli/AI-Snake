# AI-Snake
Python version 3.6.8

Installation:
- create virtual environment
- activate virtual environment
- pip install -r requirements.txt 
- python main.py --display=True --speed=10 --train=False --loadWeights=True

## Game.py


## Snake.py
Class for the Snake object. 

### Init:
The function called when the object is initialized

- The position (expressed by x and y values) is set to a fixed point (based on the gam width and height)
-  The length of the tail is set to 1
- The flag eaten is set to False
- The tiles are loaded: 4 for the head (one for each possible orientation) and 1 for the body
- The x velocity is set to 20
- The y velocity is set to 0

### Render
The function that displays the Snake. If the game is not crashed, firstly the function displays the Snake head using the x and y velocity to select the right tile. Then for each piece of the tail the function displays the body using the same tile. At the end of this process, the update_screen() function is called. If the game is crashed the function waits until a new game start.

### Update
This function is used to update the position of the Snake and of its tail.

### Move
This function is used to move the Snake by modifying the x and y velocity. Firstly this function checks if the Snake have eaten a fruit, if true append the x and y to the positions vector, reset the flag to false and increment the tail size. Secondly based on the input move this function modify the x and y velocity to perform the desired movement. Then the function cheks for possible borders collisions. At the end the eat and the update function are called.

## Food.py
Class for the Food object. 

### Init
The function called when the object is initialized

- The position (expressed by x and y values) is set to a fixed point 
- The food tile is loaded

### Render
This function displays the food and call the update_screen() function.

### Update
This function sets the x and y position randomly and recursively, so during a game there will be only one fruit.

## utils.py
## Agent.py
## main.py
