#SS AIDEV-ProjectSetup

<div align="center">
  <img src="Resources/Icons/BowersWorld Icon  (Ttrans).png" alt="AIDEV-ProjectSetup Logo" width="200"/>
  <br><br>
  <p><strong>A powerful, user-friendly tool for initializing new projects in the Project Himalaya ecosystem</strong></p>
  <br>
  <p>
    <img src="https://img.shields.io/badge/Status-Development-blue?style=for-the-badge" alt="Status: Development"/>
    <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python 3.8+"/>
    <img src="https://img.shields.io/badge/PySide6-6.5.0+-blue?style=for-the-badge" alt="PySide6 6.5.0+"/>
    <img src="https://img.shields.io/badge/License-MIT-gold?style=for-the-badge" alt="License: MIT"/>
  </p>
</div>

## Overview

AIDEV-ProjectSetup streamlines the creation of new projects that conform to the Project Himalaya ecosystem standards. With a clean, intuitive interface, it automates setting up proper directory structures, database connections, GitHub integration, and initial files.

### Features

- 🌟 **Intuitive Wizard Interface** - Step-by-step project setup
- 🌳 **Flexible Directory Structure** - Use defaults or customize to your needs
- 🔄 **GitHub Integration** - Seamless repository creation and management
- 🗄️ **Dual-Database Architecture** - Automatic setup of Himalaya.db and project-specific databases
- 📝 **Template Generation** - Creates README, LICENSE, and .gitignore with proper formatting
- 🧩 **Modular Design** - Following Project Himalaya's architectural principles
- 🎨 **Silver/Blue/Gold/Red Theme** - Consistent with Project Himalaya ecosystem

## Installation

```bash
# Clone the repository
git clone https://github.com/CallMeChewy/AIDEV-ProjectSetup.git
cd AIDEV-ProjectSetup

# Install dependencies
pip install -r requirements.txt

# Run the application
python Main.py
```

## Quick Start

1. Launch the application with `python Main.py`
2. Enter your project information (name, description, location)
3. Configure GitHub settings
4. Customize directory structure or use defaults
5. Click "Create Project"
6. Your new project is ready with all necessary files and GitHub integration!

## Project Structure

```
AIDEV-ProjectSetup/
├── Core/                 # Core application functionality
│   ├── DatabaseIntegration.py
│   ├── GitHubManager.py
│   └── ProjectInitializer.py
├── GUI/                  # User interface components
│   ├── AppStyles.py
│   ├── DirectoryEditor.py
│   ├── MainWindow.py
│   └── ProjectConfigPanel.py
├── Utils/                # Utility functions
│   ├── ConfigManager.py
│   └── DirectoryParser.py
├── Resources/            # Application resources
│   ├── Icons/
│   └── Templates/
├── Tests/                # Test suites
│   ├── UnitTests/
│   └── IntegrationTests/
├── Main.py               # Application entry point
└── requirements.txt      # Project dependencies
```

## Creating a New Project

AIDEV-ProjectSetup will initialize new projects with:

- Standard directory structure based on Project Himalaya guidelines
- README.md and LICENSE files from custom templates 
- .gitignore with special handling for `..*` directories
- Initial git repository with proper configuration
- Connection to GitHub repository (if credentials provided)
- Project-specific database in the Directories folder
- Registration in the Himalaya.db master database
- Update script for easy repository management

## Project Himalaya Integration

This application is part of the Project Himalaya ecosystem, a comprehensive framework demonstrating optimal AI-human collaboration. Project Himalaya establishes a new paradigm where quality, transparency, and continuity are inherent to the process rather than aspirational goals.

## Requirements

- Python 3.8 or higher
- PySide6 6.5.0 or higher
- Git
- GitHub account (for repository integration)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- **Herbert J. Bowers**: Project creator and principal architect
- **Claude AI (Anthropic)**: Implementation assistance and development collaboration
- **Project Himalaya Team**: Framework and standards development

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <br>
  <p><em>"Project Himalaya redefines software development by elevating AI to the role of primary implementer while positioning humans as strategic architects. Through rigorous standards, comprehensive testing, and database-driven accountability, we establish a new paradigm where quality, transparency, and continuity are inherent to the process rather than aspirational goals."</em></p>
  <p>— Herbert J. Bowers</p>
</div>
