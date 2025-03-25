# AIDEV-PascalCase Examples

## 1. Function Definition

```python
# File: DataValidation.py
# Path: Core/DataValidation.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  10:16PM
# Description: Provides functions for validating data inputs.

def ValidateUserInput(InputText: str, MaxLength: int = 255) -> str:
    """
    Validates user input to ensure it meets specified criteria.

    Args:
        InputText: The user input string to validate.
        MaxLength: The maximum allowed length of the input string.

    Returns:
        The validated input string, truncated to MaxLength if necessary.

    Raises:
        ValueError: If the input is empty or contains invalid characters.
    """
    if not InputText:
        raise ValueError("Input cannot be empty.")

    # Local variable using PascalCase
    CleanedInput = InputText.strip()

    if len(CleanedInput) > MaxLength:
        CleanedInput = CleanedInput[:MaxLength]

    return CleanedInput
```

This example demonstrates a function definition with parameters (`InputText`, `MaxLength`), a local variable (`CleanedInput`), and a docstring. All custom names follow PascalCase, while Python keywords like `def` and `raise` remain lowercase.

## 2. Class Definition

```python
# File: DataProcessor.py
# Path: Core/DataProcessor.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  10:16PM
# Description: Provides a class for processing data from various sources.

import os
import json

class DataProcessor:
    """
    A class for processing data from various sources, including files and databases.

    Attributes:
        InputDirectory: The directory containing input files.
        OutputDirectory: The directory to store processed files.
    """

    def __init__(self, InputDirectory: str, OutputDirectory: str):
        """
        Initializes the DataProcessor with input and output directories.

        Args:
            InputDirectory: The directory containing input files.
            OutputDirectory: The directory to store processed files.
        """
        self.InputDirectory = InputDirectory
        self.OutputDirectory = OutputDirectory

    def LoadData(self, FileName: str) -> dict:
        """
        Loads data from a JSON file.

        Args:
            FileName: The name of the JSON file to load.

        Returns:
            A dictionary containing the loaded data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        FilePath = os.path.join(self.InputDirectory, FileName)
        try:
            with open(FilePath, 'r') as File:
                Data = json.load(File)
            return Data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {FileName}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Invalid JSON in file: {FileName}")

    def ProcessData(self, Data: dict) -> dict:
        """
        Processes the input data.

        Args:
            Data: A dictionary containing the data to process.

        Returns:
            A dictionary containing the processed data.
        """
        # Example processing: convert keys to uppercase
        ProcessedData = {key.upper(): value for key, value in Data.items()}
        return ProcessedData

    def SaveData(self, Data: dict, FileName: str) -> None:
        """
        Saves the processed data to a JSON file.

        Args:
            Data: A dictionary containing the data to process.
            FileName: The name of the JSON file to save.
        """
        FilePath = os.path.join(self.OutputDirectory, FileName)
        with open(FilePath, 'w') as File:
            json.dump(Data, File, indent=4)

    def GetTimestamp(self): # Example of a standard library method
        """
        Returns the current timestamp.
        """
        return str(datetime.datetime.now())
```

This example demonstrates a class definition (`DataProcessor`) with methods (`LoadData`, `ProcessData`, `SaveData`, `GetTimestamp`), properties (`InputDirectory`, `OutputDirectory`), and both standard library (`os`, `json`, `datetime`) and custom methods. All custom names follow PascalCase, while standard library elements remain lowercase. The `GetTimestamp` method demonstrates interface boundary preservation.

## 3. Special Terms

```python
# Example demonstrating proper handling of special terms

AIModelName = "GPT-4"  # Correct: AI is a special term
DBConnection = "localhost:5432"  # Correct: DB is a special term
GUIWindow = QMainWindow()  # Correct: GUI is a special term

def ProcessAIOutput(AIOutput: str) -> str:
    """Processes the output from an AI model."""
    # Local variable using PascalCase
    FormattedOutput = f"AI Model: {AIOutput}"
    return FormattedOutput

class DatabaseHandler:
    """Handles database connections and operations."""

    def __init__(self, DBConnection: str):
        """Initializes the database handler."""
        self.DBConnection = DBConnection

    def ExecuteQuery(self, Query: str) -> list:
        """Executes a database query."""
        # Placeholder for actual database execution
        return []

class GraphicalUserInterface:
    """Creates and manages the graphical user interface."""

    def __init__(self):
        """Initializes the GUI."""
        self.GUIWindow = QMainWindow()

    def ShowWindow(self):
        """Shows the GUI window."""
        self.GUIWindow.show()
```

This example demonstrates the proper handling of special terms (AI, DB, GUI) within variable names and class names. The special terms are capitalized, and the rest of the name follows PascalCase.

## 4. Complete File

```python
# File: ConfigurationManager.py
# Path: Utils/ConfigurationManager.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  10:18PM
# Description: Manages application configuration settings.

import os
import json
from typing import Optional

# Constants
DEFAULT_CONFIG_FILE = "config.json"

# Global variables
g_ConfigSettings = {}

class ConfigurationManager:
    """
    Manages application configuration settings, loading from and saving to a JSON file.
    """

    def __init__(self, ConfigFile: Optional[str] = None):
        """
        Initializes the ConfigurationManager.

        Args:
            ConfigFile: The path to the configuration file. Defaults to DEFAULT_CONFIG_FILE.
        """
        self.ConfigFile = ConfigFile or DEFAULT_CONFIG_FILE
        self.ConfigData = self.LoadConfig()

    def LoadConfig(self) -> dict:
        """
        Loads configuration data from the specified JSON file.

        Returns:
            A dictionary containing the configuration data.
        """
        try:
            with open(self.ConfigFile, "r") as File:
                ConfigData = json.load(File)
            return ConfigData
        except FileNotFoundError:
            print(f"Configuration file not found: {self.ConfigFile}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in configuration file: {self.ConfigFile}")
            return {}

    def GetSetting(self, SettingName: str, DefaultValue: any = None) -> any:
        """
        Retrieves a configuration setting by name.

        Args:
            SettingName: The name of the setting to retrieve.
            DefaultValue: The value to return if the setting is not found.

        Returns:
            The value of the setting, or the DefaultValue if not found.
        """
        return self.ConfigData.get(SettingName, DefaultValue)

    def SaveConfig(self) -> None:
        """
        Saves the current configuration data to the JSON file.
        """
        try:
            with open(self.ConfigFile, "w") as File:
                json.dump(self.ConfigData, File, indent=4)
        except Exception as e:
            print(f"Error saving configuration: {e}")

# Functions outside classes
def InitializeConfig():
    """Initializes the global configuration settings."""
    global g_ConfigSettings
    g_ConfigSettings = ConfigurationManager().LoadConfig()

# Main entry point (if applicable)
def Main():
    """Main function (if applicable)."""
    pass

if __name__ == "__main__":
    Main()
```

This example demonstrates a complete Python file with a proper header, imports (organized), constants, global variables, a class (`ConfigurationManager`) with methods, and a main entry point. All custom names follow PascalCase, and the file adheres to the specified module organization.

## 5. Refactoring

```python
# Refactoring Example: Converting non-compliant code to compliant code

# Non-compliant code
def process_data(input_value):
    result = input_value.strip()
    return result

class data_handler:
    def __init__(self, db_connection):
        self.db_connection = db_connection

# Compliant code (after refactoring)
def ProcessData(InputValue: str) -> str:
    """Processes the input data."""
    Result = InputValue.strip()
    return Result

class DataHandler:
    """Handles data operations."""
    def __init__(self, DBConnection: str):
        """Initializes the data handler."""
        self.DBConnection = DBConnection
```

This example demonstrates a refactoring scenario where non-compliant code (using snake_case for function and class names) is converted to compliant code (using PascalCase). The variable names are also updated to follow PascalCase.
