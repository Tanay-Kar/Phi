![Phi](docs/Phi_logo_full.png)
<hr>

# Programmation Heuristique Interface

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
By default , it executes the file named `main.phi` . You can change the file name in the `compiler.py` file.

*Note* : The project is currently in development stage. Later on a dedicated filename-as-argument method will be implemented.

If all steps were followed correctly , the terminal must show :
- Solution of two equations
- Roots of a quadratic function
- Definite integration of a function

A graph of the function and the shaded area under the curve will be displayed.


