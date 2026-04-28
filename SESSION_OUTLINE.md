# Class Session Outline: Building the Monty PyDuck Coffee Streamlit App

1. **Create a New Repository**
   - Set up a new GitHub repository for the project.
2. **Put Final Project Code in a Folder in Old Repository**
   - Organize your final project code into a dedicated folder in your existing (old) repository.
3. **Upload That Folder to New GitHub Repository**
   - Copy or upload the project folder from the old repository to the new GitHub repository.
4. **Install GitHub Copilot from Extensions**
   - In VS Code, install the GitHub Copilot extension for AI code suggestions.
5. **Install Copilot Chat from Extensions**
   - Install the Copilot Chat extension for interactive AI chat and paired programming.
6. **Install Cline from Extensions**
   - (If needed) Install the Cline extension for enhanced command-line integration.
7. **Set Up Git User Name and Email**
   - Configure your global Git username and email for commit authorship:
     ```
     git config --global user.name "Your Name"
     git config --global user.email "your@email.com"
     ```
8. **Review and Read Project Code**
   - Use Copilot Chat to read and understand all Python files and data files in the project.
9. **Discuss and Plan Streamlit App Features**
   - Decide on app features (user login, order history, CRUD, menu loading, etc.).
   - Clarify requirements and validation rules.
10. **Implement Streamlit App**
    - Build the app step-by-step:
      - User login/creation (with employee number as unique ID)
      - Load menu from `menu.txt`
      - Display 5 most recent orders for the user
      - Place new orders with verification before saving
      - Force Central Time for all order timestamps
      - Use session state for multi-step forms
11. **Fix Import and Package Issues**
    - Add `__init__.py` to `MontysOOP` folder
    - Use package imports everywhere (e.g., `from MontysOOP.Coffee import Coffee`)
    - Remove sys.path hacks for cloud compatibility
12. **Handle Timezone and Datetime Bugs**
    - Ensure all datetimes are offset-aware and in Central Time for sorting and display
13. **Test and Debug in Local and Cloud Environments**
    - Push changes to GitHub and test in both local VS Code and Streamlit Cloud
    - Fix any import, path, or datetime issues as they arise
14. **Document and Reflect**
    - Save session notes and best practices in a `.md` file for future reference

---
*Prepared by GitHub Copilot, April 21, 2026*
