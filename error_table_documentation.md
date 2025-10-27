| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| Mutable default arg | Bug (Pylint) | 8 | `logs=[]` is shared across calls, causing unintended side effects. | Change default to `None` and initialize a new list inside the method. |
| Use of `eval` | Security (Bandit) | 59 | `eval()` is insecure and can run arbitrary code (Medium Severity). | Replace the `eval("print('eval used')")` call with a standard `print('eval used')` call. |
| Bare `except` | Bug (Flake8/Pylint) | 19 | `except:` catches all errors, including system-level ones, hiding bugs. | Replace `except:` with the specific `except KeyError:` to only catch missing items. |
| No input validation | Bug (Runtime) | 11, 51 | Code crashes with a `TypeError` when non-string/int types are passed to `addItem`. | Implement input validation using `isinstance()` at the beginning of `add_item`. |
| No 'with' statement | Refactor (Pylint) | 26, 32 | Files are opened with `open()` but not in a `with` block, risking resource leaks. | Rewrite `loadData` and `saveData` to use the `with open(...) as f:` pattern. |
| Unused import | Cleanup (Flake8/Pylint) | 2 | The `logging` module is imported but never used. | Configure and use the `logging` module for errors and warnings. |