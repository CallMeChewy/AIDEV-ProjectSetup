# File: DirectoryParser.py
# Path: AIDEV-ProjectSetup/Utils/DirectoryParser.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  5:10PM
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
        
        # Process lines
        IndentStack = [-1]
        DictStack = [Structure]
        
        for Line in ProcessedLines:
            # Try to match standard tree format
            Match = self.IndentPattern.match(Line)
            if not Match:
                # Try direct format (just indentation)
                Match = self.DirectPattern.match(Line)
                if not Match:
                    continue
                
                Indent = len(Match.group(1))
                Name = Match.group(2).strip()
            else:
                Indent = len(Match.group(1))
                Name = Match.group(3).strip()
            
            # Skip files (containing periods, except directories starting with '.')
            if '.' in Name and not Name.startswith('.') and Name != '..':
                # Special files like README.md and LICENSE
                if Name in ['README.md', 'LICENSE', 'requirements.txt', '.gitignore']:
                    # Handle special files
                    CurrentDict = DictStack[-1]
                    CurrentDict[Name] = {}
                continue
            
            # Process indentation
            while len(IndentStack) > 0 and Indent <= IndentStack[-1]:
                IndentStack.pop()
                DictStack.pop()
            
            # Get current dictionary
            if not DictStack:
                # This is a safety check in case the stack became empty
                DictStack = [Structure]
                IndentStack = [-1]
            
            CurrentDict = DictStack[-1]
            
            # Add new directory
            CurrentDict[Name] = {}
            
            # Update stacks
            IndentStack.append(Indent)
            DictStack.append(CurrentDict[Name])
        
        return Structure
    
    def FormatStructureToText(self, Structure, Prefix=""):
        """
        Format directory structure to text representation.
        
        Args:
            Structure: Dictionary representing directory structure
            Prefix: Prefix for indentation (used in recursion)
            
        Returns:
            list: Lines of text representation of structure
        """
        Result = []
        
        # Handle empty structure
        if not Structure:
            return Result
            
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
