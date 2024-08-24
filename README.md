# Inventory Management System

## Overview

This repository provides an Inventory Management System built with Python using Tkinter for the GUI and SQLite for the database. The application allows users to manage inventory through functionalities such as querying products by barcode, adding new products, and managing settings.

## Project Structure

- `main.py`: Entry point of the application. Initializes the database and creates the GUI.
- `gui.py`: Contains the GUI code using Tkinter, including the logic for various functionalities such as querying products, adding new products, and toggling themes.
- `database.py`: Handles database operations, including initializing the database, adding barcode information, and retrieving product details.
- `config.py`: Configuration file for database path and theme file.
- `locales` : Contains the translations for languages.
- `images` : Contains the images used in the program.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Alper1718/Inventory-Management-System.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Inventory-Management-System
   ```

3. Ensure you have the required Python packages:
   - `tkinter` (usually included with Python)
   - `sqlite3` (usually included with Python)

4. Run the application:
   ```bash
   python main.py
   ```

## Features

- **Product Query**: Search for a product by scanning or entering its barcode.
- **Sell**: Functionality for selling products (to be implemented).
- **Settings**: Manage application settings including theme (light/dark) and language preferences.
- **Renew Prices**: Functionality for updating product prices.
- **Add Product**: Add new products to the inventory.
- **General Report**: View general reports (e.g., employee sales data) (to be implemented).
- **More To Be Implemented**

## Configuration

- **Database Path**: Configured in `config.py` with the `DATABASE_PATH` variable.
- **Theme File**: Stores the current theme in `theme.txt` (light or dark).

## Usage

1. **Product Query**: 
   - Enter or scan a barcode to view product details.

2. **Sell**: 
   - Access the selling functionality from the main menu.

3. **Settings**: 
   - Toggle between light and dark themes.
   - Change language preferences (currently supports English, Spanish, German, Turkish).

4. **Renew Prices**:
   - Renew a specific product's price.
   - Renew all prices based on a percentage.

6. **Add Product**: 
   - Fill in the product information including barcode, name, price, details, and amount to add them to the database.
   
7. **General Report**: 
   - Access general reports from the main menu.

## Notes

- The application runs in fullscreen mode by default. Modify the code if a windowed mode is preferred.
- Ensure that the `locales` directory contains the necessary JSON files for language translations.
- If you want to add corrections to already existing languages or add a new language please open an issue or submit a pull request with your changes.
