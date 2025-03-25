#!/bin/bash

# Script to set up templates for AIDEV-ProjectSetup

# Create the Resources/Templates directory
mkdir -p Resources/Templates

# Create README.md.template
cat > Resources/Templates/README.md.template << 'EOL'
# ${ProjectName}

## Overview

${Description}

## Project Structure

This project follows the Project Himalaya organization standards.

```
${ProjectName}/
├── Core/
├── Docs/
│   └── API/
├── Utils/
└── Tests/
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/${GitHubAccount}/${RepositoryName}.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

[Provide usage instructions here]

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

${Author}

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
EOL

# Create LICENSE.template
cat > Resources/Templates/LICENSE.template << 'EOL'
MIT License

Copyright (c) ${Year} ${Author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOL

# Create gitignore.template
cat > Resources/Templates/gitignore.template << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.manifest
*.spec

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# OS specific files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
Directories/
**/local_settings.py
db.sqlite3
*.db
EOL

echo "Template setup script created successfully."
