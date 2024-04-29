# Design Architecture

## Main Architecture
For this project, there is one main artchitecture that applies to the overall project, with a small sub-architecture for the application itself. The overall architecture will follow a three-tier architecture. Please see below for a diagram for the three layers:

<img width="497" alt="image" src="https://github.com/Duquesne-Spring-2024-COSC-481/Amanda-Shaginaw/assets/68133821/8d6374ee-f1cc-4df6-b8f7-43a187e1bdc1">

### Presentation Tier
The Presentation tier will be the UI that users will use. This is where the cycle starts, as a user logs in and asks for music. For this example, the user wants music for a fight in a chapel.

### Logic Tier
The Logic tier is the code that will be doing the heavy lifting. TensorFlow, a framework that will also be explained in this document, will take the stored music and create the music. This layer will also sort music when new music is added to the data tier.

### Data Tier
THe Data tier is where all music will be stored. This includes the music that is used in the Long Short-Term memory model, as well as the supervised learning model. If any other data is stored, such as the data for a user's account, it will also be stored here.

## Secondary Architecture
The secondary architecture for this model will be the Model-View-Controller architecture. This architecture is for the GUI. The model represents the backend data and code that will interact with the GUI, such as the code for the LSTM model. The view is what the user sees in the application, and the controller is the client interacting with the application.

# Frameworks
The main framework being used in this project is TensorFlow.TensorFlow is an open-source framework that can be used with Python for Machine Learning models. TensorFlow works well with sequential data (music), and allows a user to input their data and train it before creating a final result. TensorFlow also allows you to choose how many layers you want to use for your Machine Learning algorithm, and allows for easy adjustments. For doing a Long Short-Term memory model, we will also need to use the Keras API. Keras API helps you focus on where your model may run into issues and allows you to resolve them easily.
