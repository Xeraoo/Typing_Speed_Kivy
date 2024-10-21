# Typing Speed App

## Overview

The **Typing Speed App** is a Kivy-based application designed to help users measure their typing speed and accuracy. It provides a user-friendly interface where participants can type randomly generated texts, track their performance in real time, and visualize their results through graphs. This application is a fun and effective way to improve typing skills.

## Features

- **Random Text Generation**: Users are presented with various texts to type, enhancing the practice experience.
- **Typing Speed and Accuracy Calculation**: The app calculates typing speed in words per minute (WPM) and accuracy percentage.
- **History Tracking**: Users can view their past typing attempts, including speed and accuracy metrics.
- **Graph Visualization**: Performance data can be visualized using graphs for better insights into typing improvement over time.
- **Theme Support**: The application supports both dark and light themes.

## Screens

The application consists of the following screens:

- **Welcome Screen**: Introduction to the app and navigation to the main typing interface.
- **Main Screen**: The primary screen where users type the given text and see their speed and accuracy.
- **History Screen**: A log of previous typing attempts with speed and accuracy details.
- **Graph Screen**: Visual representation of typing speed and accuracy over time.

## Usage

1. Open the application.
2. Navigate through the screens using the buttons provided.
3. Start typing the text displayed on the main screen.
4. Your typing speed and accuracy will be displayed once you stop typing.
5. View your history and graph to track your progress.

## Code Structure

The main application code is contained within the `main.py` file. The Kivy layout is defined in the `kv_strings.kv` file.

### Main Classes

- **TypingSpeedApp**: The main application class that initializes the app, manages the screens, and handles typing speed calculations.

### Key Methods

- `start()`: Starts the typing test and initializes the timer.
- `stop()`: Stops the typing test, calculates speed and accuracy, and updates the UI.
- `new_text()`: Randomly selects a new text for the user to type.
- `save_result()`: Saves the typing results to a JSON file for history tracking.
- `update_graph()`: Generates a graph based on the user's typing history.

## Acknowledgments

This application was developed by Tymoteusz Maja. You can find my projects on GitHub.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
