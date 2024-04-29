# Installing Python
These steps are for installing Python and how to get it to work in Microsoft Visual Studio Code. For documentation, please visit https://www.python.org/about/

1. Go to https://www.python.org/downloads/ and select Download Python 3.12.1. If you do not have a Windows machine, please select the correct download for your computer.
2. Click on the downloaded file and walk through the setup steps.
3. Open Visual Studio Code, and go to the Extensions Tab (It looks like blocks stacking on top of one another).
4. Search for "Python" and install. Install any suggested extensions as well, such as Jupyter Notebook.
5. Afer this, you should be able to create a file with a .py extension

# Installing TensorFlow and music21

## TensorFlow
TensorFlow can be installed directly in Visual Studio Code once Python is installed. Please also make sure pip is up to date by typing into the Terminal python.exe -m pip install  --upgrade pip (you may need to add --users onto the end if you receive an error).

TensorFlow will help with Machine Learning. If you would like more information, you can visit https://www.tensorflow.org/overview which contains examples of TensorFlow running on code.
Keras works alongside TensorFlow as an API that will give the right balance of using your computer's resources to create the best result. TO learn more, please visit https://keras.io/about/#:~:text=Keras%20is%20a%20deep%20learning,the%20problem%20that%20really%20matter.

1. Open Visual Studio Code. Go to View, then Terminal
2. Type in pip install tensorflow. If you get an error, type in pip install tensorflow --user, and it then should work.

 NOTE: Installing TensorFlow this way will also install Keras 3. No need to install seperately.
 
  ## music21
music21 is a package that helps pull information out of MIDI files such as instruments, chords, and notes. This will also create the music we want at the end of the training. For more information, please check https://github.com/cuthbertLab/music21

1. Open Visual Studio Code. Go to View, then Terminal
2. Type in pip install music21. If you get an error, type in pip install music21 --user, and it then should work.

## Mido
1. Open Visual Studio Code. Go to View, then Terminal
2. Type in pip install mido. If you get an error, type in pip install mido --user, and it then should work.

## Other Libraries
There are several libraries that are included in this project that are automatically packaged with Tensorflow or Python. This list includes:
- unittest
- tempfile
- csv
- pickle
- os
- numpy
- PIL
- glob

# Running the Code
Here are the steps for running the code:

1. Open up the main branch using Github Desktop into VSCode
<<<<<<< HEAD
2. In the terminal, enter
   <code>cd BardicInspiration</code>
3. Go to the terminal and type
   <code>python -m main.py</code>
4. Once the code is running, enter admin for username and admin for password.

# Running a PyTest

1. Open Visual Studio Code
2. In the terminal, type python -m pytest name_of_test_file.py
3. All instances of the test should pass, or else it will print out the error.
