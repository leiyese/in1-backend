# 🚀 Git Branching Workflow (Main → Dev → Features)

## **1️⃣ Ensure You’re on the Main Branch**
```sh
git checkout main  # Switch to the main branch
git pull origin main  # Get the latest changes from remote
```

## **2️⃣ Create and Push the Dev Branch**
```sh
git checkout -b dev  # Create and switch to the 'dev' branch
git push origin dev  # Push 'dev' branch to remote
```

> Now, `dev` is the new working branch for development. `main` stays clean for releases.

---

## **3️⃣ Create Feature Branches from Dev**
Whenever you start working on a new feature, create a **feature branch** from `dev`:

```sh
git checkout dev  # Make sure you are on the dev branch
git pull origin dev  # Get the latest changes

# Create a new feature branch
git checkout -b feature-branch-name
```
Example:
```sh
git checkout -b feature-login
```

Push your feature branch to remote:
```sh
git push origin feature-login
```

---

## **4️⃣ Work on Your Feature & Commit Changes**
After making changes to your feature, commit them:
```sh
git add .  # Stage all changes
git commit -m "Added login functionality"
```

Push your branch to remote:
```sh
git push origin feature-login
```

---

## **5️⃣ Merge Feature Branch into Dev**
Once your feature is ready:
1. Switch to `dev`:
   ```sh
   git checkout dev
   git pull origin dev  # Ensure it's up-to-date
   ```
2. Merge the feature branch:
   ```sh
   git merge feature-login
   ```
3. Push the updated `dev` branch:
   ```sh
   git push origin dev
   ```

---

## **6️⃣ Merge Dev into Main (For Release)**
Once all features are tested, merge `dev` into `main`:
```sh
git checkout main
git pull origin main
git merge dev
git push origin main
```

---

## ** Branching Strategy Summary**
| Branch         | Purpose |
|---------------|---------|
| `main`        | Stable production-ready branch |
| `dev`         | Active development branch |
| `feature-*`   | Individual feature branches (e.g., `feature-auth`, `feature-dashboard`) |

---

## ** Git Branching Workflow Tree**
```plaintext
main
 │
 ├── dev
 │   │
 │   ├── feature-login
 │   ├── feature-dashboard
 │   ├── bugfix-navbar
 │
 └── (Merged into main after testing)
```

---

## ** Best Practices**
- Keep `main` **clean** and **production-ready**.
- Regularly pull from `dev` before working on a feature.
- Use **descriptive branch names** (`feature-login`, `bugfix-navbar`).
- Use **pull requests (PRs)** for merging to `dev` and `main`.

