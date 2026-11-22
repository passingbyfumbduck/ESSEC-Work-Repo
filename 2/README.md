# Git mini exercise

## 1�C3. Set up and make the first commit

Use your own GitHub noreply address for commits. Run the setup in a new practice directory.

```sh
git --version
mkdir my-first-repo
cd my-first-repo
git init -b main
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_NOREPLY_ADDRESS"
printf '%s\n' 'This repository is for the Git branching exercise.' > readme.txt
git status
git add readme.txt
git commit -m "Add readme file"
git log
```

## 4�C5. Change a tracked file

```sh
printf '%s\n' 'The feature branch adds a Bash installer for tree.' >> readme.txt
git status
git diff
git add readme.txt
git commit -m "Describe the feature branch"
git log --oneline
```

Before staging, status lists `readme.txt` as modified. The diff shows the added line relative to the index. After committing, the working tree is clean and the one-line log contains two commits, newest first.

## 6�C8. Branch, add a script, and merge

```sh
git branch
git branch feature-script
git switch feature-script
git switch -c dev
git switch feature-script
git branch --show-current
```

Copy the accompanying `install.sh` into the practice directory, then run the following.

```sh
chmod +x install.sh
git add --chmod=+x install.sh
git commit -m "Add install script"
git log --oneline
git switch main
ls
git merge feature-script
ls
git log --oneline
git branch -d feature-script
```

Before merging, main contains only `readme.txt`. The installer first exists on the feature branch. Main has no intervening commits, so Git fast-forwards it to the third commit and both files appear.

## 9�C10. Push and clone the practice repository

For the standalone classroom workflow, create an empty GitHub repository named `my-first-repo` and replace `YOUR_ACCOUNT` below. The repository page will show the two files and the three commits.

```sh
git remote add origin https://github.com/YOUR_ACCOUNT/my-first-repo.git
git push -u origin main
cd ..
rm -r -- my-first-repo
git clone https://github.com/YOUR_ACCOUNT/my-first-repo.git
cd my-first-repo
git ls-files
```

## 11. Repeat with bash-installer

The following cleanup commands are for the disposable practice repository after its remote copy has been verified. The six-assignment repository has a separate history.

```sh
cd ..
rm -r -- my-first-repo
gh repo delete YOUR_ACCOUNT/my-first-repo
mkdir bash-installer
cd bash-installer
git init -b main
printf '%s\n' '# Bash installer' 'Installs tree on Debian and Ubuntu.' > README.md
git add README.md
git commit -m "Describe the Bash installer"
git switch -c feature-install
```

Copy the same `install.sh` into this directory.

```sh
chmod +x install.sh
git add --chmod=+x install.sh
git commit -m "Add install script"
git switch main
git merge feature-install
git branch -d feature-install
gh repo create YOUR_ACCOUNT/bash-installer --private --source=. --remote=origin --push
```
