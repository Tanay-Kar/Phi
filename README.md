<p align="center"> <image src=docs/Phi_logo_full.png alt=Phi> </p>
<hr>

<h1 align="center">Programmation Heuristique Interface</h1>

Phi is a programming language which aims to build a bridge between classical mathematics and programming. 

Phi is built to provide an intuitive approach to performing mathematical calculations. It is designed to eliminate the need to translate mathematical notations into a programming language, and to allow the user to focus on the mathematical problem at hand.

Salient features of Phi include:
- A simple syntax, which is close to mathematical notations
- Integrated graph plotting system
- Integrated symbolic computation system
- Built to be modified. Written in Python, Phi is designed in a way that it encourages tinkering and modifications.

Currently, Phi is in its early stages of development. The language is still being designed, and the implementation is still in its infancy.

As of now , Phi is able to perform basic mathematical operations, such as:
- Arithmetic operations ,
- Integration calculations ,
- Function operations ,
- Plotting graphs ,
- Evaluating expressions ,
- Equation management ,
- Solving systems of equations ,
- Symbolic computation ,
- Calculating roots of functions and more...

# Installation

- Ensure Git is installed on your system. If not, install it from [here](https://git-scm.com/downloads).

- Clone the repository using the following command:
```
git clone https://github.com/Tanay-Kar/Phi.git

cd Phi
```

- Install the required dependencies using the following command:
```
pip install sympy numpy matplotlib mpl-interactions qbstyles ing_theme_matplotlib colorama
```
You may need to create a virtual environment before installing the dependencies in some debian distros.

- Run the following command to execute the provided file:
```
python compiler.py
```
Ensure that the correct python binary is used . In linux systems python3 is common.

By default , it executes the file named `main.phi` . You can change the file name in the `compiler.py` file.

*Note* : The project is currently in development stage. Later on a dedicated filename-as-argument method will be implemented.

If all steps were followed correctly , the terminal must show :
- Solution of two equations
- Roots of a quadratic function
- Definite integration of a function

A graph of the function and the shaded area under the curve will also be displayed.

Graph                      |  Terminal output
:-------------------------:|:-------------------------:
![Graph](https://github.com/Tanay-Kar/Phi/assets/93914273/15d5ceaa-2138-4343-a735-5d36bebec252)| ![Terminal output](https://github.com/Tanay-Kar/Phi/assets/93914273/a9729fa1-b46c-4bed-bc5b-73a998d54a37)

The code for this output is just :
```python
eq1 : 3x - 4y = 5
eq2 : 4x - 3y = 10

solve (eq1,eq2) for (x,y)

f(x) = x^2 + 2x - 1

solve f(x)

integrate f(x) wrt x from -1 to 3 plot
```

This example shows, just how adaptable the syntax of Phi is from a mathematical point of view. The use of implicit multiplication (```2x```) , inline function declaration (```f(x) = ...```), sentence-like syntax (```integrate f(x) wrt x from -1 to 3 plot```) , etc. 
