# File: DirectoryEditor.py
# Path: AIDEV-ProjectSetup/GUI/DirectoryEditor.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  12:35PM
# Description: Directory structure editor for AIDEV-ProjectSetup

"""
Directory structure editor component.

This module provides the interface for viewing and modifying
the project directory structure.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QTreeView, QToolBar, QAction, QPushButton,
                             QFileDialog, QLabel, QMenu, QInputDialog,
                             QMessageBox)
from PySide6.QtCore import Qt, QStandardItemModel, QStandardItem
from PySide6.QtGui import QIcon

from Utils.DirectoryParser import DirectoryParser

class DirectoryEditor(QWidget):
    """Directory structure editor component."""
    
    def __init__(self, Initializer):
        """Initialize the directory editor."""
        super().__init__()
        
        self.Initializer = Initializer
        self.DirectoryParser = DirectoryParser()
        
        self.SetupUI()
        self.LoadDefaultStructure()
    
    def SetupUI(self):
        """Set up the user interface components."""
        # Create main layout
        self.MainLayout = QVBoxLayout(self)
        
        # Create header label
        self.HeaderLabel = QLabel("Project Directory Structure")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)
        self.MainLayout.addWidget(self.HeaderLabel)
        
        # Create toolbar
        self.ToolBar = QToolBar()
        self.MainLayout.addWidget(self.ToolBar)
        
        # Add actions to toolbar
        self.LoadDefaultAction = QAction("Load Default", self)
        self.LoadFromFileAction = QAction("Load from File", self)
        self.AddFolderAction = QAction("Add Folder", self)
        self.RemoveFolderAction = QAction("Remove Folder", self)
        
        self.ToolBar.addAction(self.LoadDefaultAction)
        self.ToolBar.addAction(self.LoadFromFileAction)
        self.ToolBar.addAction(self.AddFolderAction)
        self.ToolBar.addAction(self.RemoveFolderAction)
        
        # Connect actions
        self.LoadDefaultAction.triggered.connect(self.LoadDefaultStructure)
        self.LoadFromFileAction.triggered.connect(self.LoadFromFile)
        self.AddFolderAction.triggered.connect(self.AddFolder)
        self.RemoveFolderAction.triggered.connect(self.RemoveFolder)
        
        # Create tree view
        self.DirectoryTree = QTreeView()
        self.DirectoryModel = QStandardItemModel()
        self.DirectoryModel.setHorizontalHeaderLabels(["Directory Structure"])
        self.DirectoryTree.setModel(self.DirectoryModel)
        self.DirectoryTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.DirectoryTree.customContextMenuRequested.connect(self.ShowContextMenu)
        
        self.MainLayout.addWidget(self.DirectoryTree)
        
        # Add description label
        self.DescriptionLabel = QLabel(
            "Define the directory structure for your project. "
            "You can use the default structure, load from a file, "
            "or manually edit the structure."
        )
        self.DescriptionLabel.setWordWrap(True)
        self.MainLayout.addWidget(self.DescriptionLabel)
        
        # Add error label
        self.ErrorLabel = QLabel("")
        self.ErrorLabel.setObjectName("error")
        self.ErrorLabel.setAlignment(Qt.AlignCenter)
        self.ErrorLabel.setVisible(False)
        self.MainLayout.addWidget(self.ErrorLabel)
    
    def GetDefaultStructure(self):
        """Get the default directory structure."""
        return """
.
├── AddThese
├── AddTheseNow
├── Core
├── Docs
│   └── API
├── GUI
├── KnowledgeDatabase
├── LICENSE
├── Models
├── Notes
├── README.md
├── requirements.txt
├── Scripts
├── SysUtils
├── Tests
└── Utils
"""
    
    def LoadDefaultStructure(self):
        """Load the default directory structure."""
        # Clear existing model
        self.DirectoryModel.clear()
        self.DirectoryModel.setHorizontalHeaderLabels(["Directory Structure"])
        
        # Parse default structure
        Structure = self.DirectoryParser.ParseStructure(self.GetDefaultStructure())
        
        # Build the tree
        self.BuildDirectoryTree(Structure, self.DirectoryModel.invisibleRootItem())
        
        # Expand all items
        self.DirectoryTree.expandAll()
    
    def LoadFromFile(self):
        """Load directory structure from a text file."""
        FilePath, _ = QFileDialog.getOpenFileName(
            self, "Load Directory Structure", "", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not FilePath:
            return
        
        try:
            with open(FilePath, 'r') as File:
                Content = File.read()
                
            # Parse structure
            Structure = self.DirectoryParser.ParseStructure(Content)
            
            # Clear existing model
            self.DirectoryModel.clear()
            self.DirectoryModel.setHorizontalHeaderLabels(["Directory Structure"])
            
            # Build the tree
            self.BuildDirectoryTree(Structure, self.DirectoryModel.invisibleRootItem())
            
            # Expand all items
            self.DirectoryTree.expandAll()
            
        except Exception as E:
            self.ShowError(f"Failed to load structure: {str(E)}")
    
    def BuildDirectoryTree(self, Structure, ParentItem):
        """Build tree structure from parsed directory structure."""
        for Name, Children in Structure.items():
            Item = QStandardItem(Name)
            ParentItem.appendRow(Item)
            
            if Children:
                self.BuildDirectoryTree(Children, Item)
    
    def AddFolder(self):
        """Add a new folder to the structure."""
        # Get selected item or use root if none selected
        SelectedIndexes = self.DirectoryTree.selectedIndexes()
        if SelectedIndexes:
            ParentItem = self.DirectoryModel.itemFromIndex(SelectedIndexes[0])
        else:
            ParentItem = self.DirectoryModel.invisibleRootItem()
        
        # Get folder name
        FolderName, Ok = QInputDialog.getText(
            self, "Add Folder", "Folder Name:", QLineEdit.Normal, ""
        )
        
        if Ok and FolderName:
            # Check if folder already exists
            for Row in range(ParentItem.rowCount()):
                if ParentItem.child(Row).text() == FolderName:
                    self.ShowError(f"Folder '{FolderName}' already exists.")
                    return
            
            # Add new folder
            NewItem = QStandardItem(FolderName)
            ParentItem.appendRow(NewItem)
            
            # Expand parent item
            if ParentItem != self.DirectoryModel.invisibleRootItem():
                ParentIndex = ParentItem.index()
                self.DirectoryTree.expand(ParentIndex)
    
    def RemoveFolder(self):
        """Remove selected folder from the structure."""
        SelectedIndexes = self.DirectoryTree.selectedIndexes()
        if not SelectedIndexes:
            self.ShowError("Please select a folder to remove.")
            return
        
        # Get selected item
        SelectedItem = self.DirectoryModel.itemFromIndex(SelectedIndexes[0])
        
        # Confirm deletion
        Reply = QMessageBox.question(
            self, "Remove Folder", 
            f"Are you sure you want to remove '{SelectedItem.text()}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if Reply == QMessageBox.Yes:
            # Remove item from model
            ParentItem = SelectedItem.parent()
            if ParentItem:
                ParentItem.removeRow(SelectedItem.row())
            else:
                self.DirectoryModel.removeRow(SelectedItem.row())
    
    def ShowContextMenu(self, Position):
        """Show context menu for tree view."""
        ContextMenu = QMenu(self)
        
        AddAction = ContextMenu.addAction("Add Folder")
        RemoveAction = ContextMenu.addAction("Remove Folder")
        RenameAction = ContextMenu.addAction("Rename Folder")
        
        # Get selected item
        SelectedIndexes = self.DirectoryTree.selectedIndexes()
        if not SelectedIndexes:
            RemoveAction.setEnabled(False)
            RenameAction.setEnabled(False)
        
        # Show context menu
        Action = ContextMenu.exec_(self.DirectoryTree.viewport().mapToGlobal(Position))
        
        if Action == AddAction:
            self.AddFolder()
        elif Action == RemoveAction:
            self.RemoveFolder()
        elif Action == RenameAction:
            self.RenameFolder()
    
    def RenameFolder(self):
        """Rename selected folder."""
        SelectedIndexes = self.DirectoryTree.selectedIndexes()
        if not SelectedIndexes:
            return
        
        # Get selected item
        SelectedItem = self.DirectoryModel.itemFromIndex(SelectedIndexes[0])
        
        # Get new name
        NewName, Ok = QInputDialog.getText(
            self, "Rename Folder", "New Name:", 
            QLineEdit.Normal, SelectedItem.text()
        )
        
        if Ok and NewName:
            # Check if name already exists in parent
            ParentItem = SelectedItem.parent()
            if not ParentItem:
                ParentItem = self.DirectoryModel.invisibleRootItem()
                
            for Row in range(ParentItem.rowCount()):
                ChildItem = ParentItem.child(Row)
                if ChildItem != SelectedItem and ChildItem.text() == NewName:
                    self.ShowError(f"Folder '{NewName}' already exists.")
                    return
            
            # Update name
            SelectedItem.setText(NewName)
    
    def ShowError(self, Message):
        """Display an error message."""
        self.ErrorLabel.setText(Message)
        self.ErrorLabel.setStyleSheet("color: red; font-weight: bold;")
        self.ErrorLabel.setVisible(True)
        
        # Hide after 5 seconds
        QTimer.singleShot(5000, lambda: self.ErrorLabel.setVisible(False))
    
    def ValidateStep(self):
        """Validate the current step before proceeding."""
        # Check if structure is not empty
        if self.DirectoryModel.rowCount() == 0:
            self.ShowError("Directory structure cannot be empty.")
            return False
        
        return True
    
    def GetConfiguration(self):
        """Get the directory structure configuration."""
        # Extract structure from model
        Structure = {}
        self.ExtractStructure(self.DirectoryModel.invisibleRootItem(), Structure)
        
        return {
            "DirectoryStructure": Structure
        }
    
    def ExtractStructure(self, ParentItem, Structure):
        """Recursively extract directory structure from model."""
        for Row in range(ParentItem.rowCount()):
            Item = ParentItem.child(Row)
            ChildStructure = {}
            Structure[Item.text()] = ChildStructure
            self.ExtractStructure(Item, ChildStructure)
