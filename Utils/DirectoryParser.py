# File: DirectoryParser.py
# Path: AIDEV-ProjectSetup/Utils/DirectoryParser.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-24  3:30PM
# Description: Parser for directory structure text files

"""
Directory structure parser utility.

This module provides functionality for parsing directory structure
from text files or string input in tree-like format.
"""

import re

class DirectoryParser:
    """Parser for directory structure text files."""
    
    def __init__(self):
        """Initialize DirectoryParser."""
        # Patterns for line parsing
        self.IndentPattern = re.compile(r'^(\s*)(├── |└── |│   |\s\s\s)(.+)$')
        self.DirectPattern = re.compile(r'^(\s*)(.+)$')
    
    def ParseStructure(self, Content):
        """
        Parse directory structure from string content.
        
        Args:
            Content: String containing directory structure in tree format
            
        Returns:
            Dict: Hierarchical representation of directory structure
        """
        if not Content or not isinstance(Content, str):
            return {}
            
        Lines = Content.strip().split('\n')
        Structure = {}
        
        # Skip empty lines and the root '.' line
        ProcessedLines = []
        for Line in Lines:
            Line = Line.rstrip()
            if Line and not Line.strip() == '.':
                ProcessedLines.append(Line)
        
        if not ProcessedLines:
            return Structure
        
        # Process lines with a simpler approach using just indent tracking
        PrevIndent = -1
        Path = []
        
        for Line in ProcessedLines:
            # Try to match standard tree format first
            Match = self.IndentPattern.match(Line)
            if Match:
                Indent = len(Match.group(1))
                Name = Match.group(3).strip()
            else:
                # Try direct format (just indentation)
                Match = self.DirectPattern.match(Line)
                if not Match:
                    continue
                
                Indent = len(Match.group(1))
                Name = Match.group(2).strip()
            
            # Skip files (excluding special files)
            if '.' in Name and not Name.startswith('.') and Name not in ['..', 'README.md', 'LICENSE', 'requirements.txt', '.gitignore']:
                continue
                
            # Adjust path based on indentation level
            if Indent > PrevIndent:
                # Going deeper
                Path.append(Name)
            elif Indent < PrevIndent:
                # Going back up
                LevelDiff = (PrevIndent - Indent) // 2  # Assuming standard indentation of 2 spaces
                for _ in range(LevelDiff + 1):
                    if Path:
                        Path.pop()
                Path.append(Name)
            else:
                # Same level, replace last item
                if Path:
                    Path.pop()
                Path.append(Name)
            
            # Remember current indent for next iteration
            PrevIndent = Indent
            
            # Create path in structure
            Current = Structure
            for i, PathItem in enumerate(Path[:-1]):
                if PathItem not in Current:
                    Current[PathItem] = {}
                Current = Current[PathItem]
            
            # Add current item if not already there
            if Path and Path[-1] not in Current:
                Current[Path[-1]] = {}
        
        return Structure
    
    def FormatStructureToText(self, Structure, Prefix=""):
        """
        Format directory structure to text representation.
        
        Args:
            Structure: Dictionary representing directory structure
            Prefix: Prefix for indentation (used in recursion)
            
        Returns:
            list: List of lines representing the structure
        """
        if not Structure or not isinstance(Structure, dict):
            return []
            
        Result = []
        
        # Get sorted keys
        Keys = sorted(Structure.keys())
        
        for i, Name in enumerate(Keys):
            IsLast = (i == len(Keys) - 1)
            
            # Determine prefix and connector
            if IsLast:
                Connector = "└── "
                ChildPrefix = Prefix + "    "
            else:
                Connector = "├── "
                ChildPrefix = Prefix + "│   "
            
            # Add line for current directory
            Line = Prefix + Connector + Name
            Result.append(Line)
            
            # Process children recursively
            if Structure[Name]:
                ChildLines = self.FormatStructureToText(
                    Structure[Name], ChildPrefix
                )
                Result.extend(ChildLines)
        
        return Result
