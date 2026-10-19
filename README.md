# DATA 2402 — Assignment 2

## Overview

This project implements a data table for loading and processing CSV data, two prediction approaches (majority-class and nearest-neighbor prediction), and a custom exception for feature values outside the historical data range.

## Project Structure

- `data_representation.py` — CSV data loading and data table operations.
- `predictors.py` — Majority-class and nearest-neighbor predictors.
- `exceptions.py` — Custom `OutOfSampleError` exception.
- `main.py` — Runs the predictors and calculates accuracy.
- `assignment_2_jupyter.ipynb` — Demonstrates normal cases, boundary conditions, and error-handling tests.
- `data/` — Historical data, new cases, and corresponding labels.

## Running the Program

Run this command from the project root:

    python main.py

Open `assignment_2_jupyter.ipynb` in Jupyter Notebook or JupyterLab to run the notebook cells in order.

The program and notebook expect the supplied CSV files to remain in the `data/` directory.

## Testing

The notebook includes tests for data table operations, missing-value handling, historical feature boundaries, out-of-sample exceptions, both predictors, and accuracy calculation.
