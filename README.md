# Errors and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| Mutable default arg | Bug (Pylint) | 8 | `logs=[]` is shared across calls, causing unintended side effects. | Change default to `None` and initialize a new list inside the method. |
| Use of `eval` | Security (Bandit) | 59 | `eval()` is insecure and can run arbitrary code (Medium Severity). | Replace the `eval("print('eval used')")` call with a standard `print('eval used')` call. |
| Bare `except` | Bug (Flake8/Pylint) | 19 | `except:` catches all errors, including system-level ones, hiding bugs. | Replace `except:` with the specific `except KeyError:` to only catch missing items. |
| No input validation | Bug (Runtime) | 11, 51 | Code crashes with a `TypeError` when non-string/int types are passed to `addItem`. | Implement input validation using `isinstance()` at the beginning of `add_item`. |
| No 'with' statement | Refactor (Pylint) | 26, 32 | Files are opened with `open()` but not in a `with` block, risking resource leaks. | Rewrite `loadData` and `saveData` to use the `with open(...) as f:` pattern. |
| Unused import | Cleanup (Flake8/Pylint) | 2 | The `logging` module is imported but never used. | Configure and use the `logging` module for errors and warnings. |




# Reflection on Static Code Analysis

### 1. Easiest and Hardest Issues to Fix

The **easiest fixes** were definitely the simple, one-line changes that the tools pointed out. These included:
* **Fixing the `eval()` call**: Just replacing `eval("print(...)")` with a normal `print(...)` instantly fixed a major security risk.
* **Renaming functions**: Changing names from `addItem` to `add_item` was just a simple find and replace job to follow the `snake_case` style.
* **Formatting**: Cleaning up things like extra spaces or missing newlines at the end of the file was very fast.
* **Adding docstrings**: This was also easy.

The **hardest issue** by far was fixing the **`global-statement` (W0603)** warning. It wasn't a one-line fix; I had to **change the code's whole structure**. I had to update *every* function to accept `stock_data` as a parameter instead of just using a global variable. This also meant I had to change how the `main()` function worked, loading the data into a variable and passing it around.

The **`TypeError` (runtime crash)** was also tough, mostly because **the tools didn't find it**. I had to remember from the first time I ran the code that it crashed with `addItem(123, "ten")`. I fixed it by adding my own `isinstance()` checks to validate the input, which wasn't a fix the tools suggested directly.

### 2. False Positives

Honestly, **I didn't find any false positives**. Every single issue that Pylint, Bandit, and Flake8 reported was a valid problem.
* Bandit was 100% right about `eval()` being a huge security risk.
* Pylint’s warning about the `logs=[]` (mutable default argument) pointed out a really tricky bug that I would have missed.
* Flake8 was right that the `bare-except` was a bad idea.
* Even the `global-statement` warning, which was a pain to fix, was correct. The code is much cleaner and better structured now.

### 3. Integrating Static Analysis Tools into a Software Development Workflow

After this lab, I'd definitely use these tools in any real project. I'd integrate them in two main ways:

1.  **Locally (Pre-commit hooks)**: I'd set them up to run automatically *before* I can even make a commit. This way, I get instant feedback and can fix silly mistakes (like formatting or unused imports) before they ever get into the repository.
2.  **In CI/CD (GitHub Actions)**: I'd add a "Linting" step to the main CI pipeline. This job would run all three tools every time someone makes a pull request. If any serious issues are found, the build would fail, blocking the bad code from being merged.

### 4. Tangible Improvements

The code is **so much better now**. It's not just "cleaner," it's fundamentally improved:

* **It's Way More Robust**: The code is much safer. It no longer has a security hole (`eval`), and it doesn't crash on bad input (like `addItem(123, "ten")`) or if the save file is missing.
* **It's Easier to Read**: With consistent naming, f-strings, and docstrings for every function, anyone can look at the code and understand what it's trying to do.
* **It's Easier to Maintain**: Getting rid of the `global` variable was the biggest win. Now the functions are "pure" (they don't have hidden side effects). This makes them predictable and *way* easier to test on their own.