Create your own public GitHub repository named “ITMO_ScientificPython_2026” - you will collect there all your home tasks.
Complete sets of levels in Main and Remote sections of [Learn Git Branching game](https://learngitbranching.js.org/?locale=ru_RU).
Screenshot your progress and upload it as text files to HW1 folder of created repo, write README.MD with instruction how to convert it back to image.

# 1. Level completion
---
## 1.1. Introduction Sequence: 1, 2, 3, 4
### 1.1.1. Commits
```bash
git commit
```
### 1.1.2. Branches
```bash
git branch bugFix
git checkout bugFix
```
### 1.1.3. Branches & Merging
```bash
git branch bugFix
git checkout bugFix
git commit
git checkout main
git commit
git merge bugFix
```
### 1.1.4. Rebase
```bash
git branch bugFix
git checkout bugFix
git commit
git checkout main
git commit
git checkout bugFix
git rebase main
```
---
## 1.2. Ramping Up: 1, 2, 3, 4
### 1.2.1. HEAD
```bash
git checkout C4
```
### 1.2.2. Relative Links
```bash
git checkout bugFix^
```
### 1.2.3. Branch Forcing
```bash
git branch -f main C6
git branch -f bugFix C0
git checkout C1
```
### 1.2.4. Revert & Reset
```bash
git checkout local
git reset HEAD~1
git checkout pushed
git revert HEAD
```
---
## 1.3. Moving Work Around: 1, 2
### 1.3.1. Git Cherry-pick
```bash
git cherry-pick C3 C4 C7
```
### 1.3.2. Git Interactive Rebase
```bash
git rebase -i C1
# drop/omit C2, new order: C3, C5, C4
```
---
## 1.4. A Mixed Bag: 1, 2, 3, 4, 5
### 1.4.1. Rebase & Cherry-pick
```bash
git checkout bugFix
git rebase -i main
git branch -f main bugFix
# alternative way:
# git cherry-pick bugFix
# git branch -f bugFix main
```
### 1.4.2. Juggling Сommits
```bash
git rebase -i HEAD~2 # C3 <- C2
git commit --amend
git rebase -i HEAD~2 # C3' <- C2''
git branch -f main HEAD
```
### 1.4.3. Juggling Commits #2
```bash
git checkout main
git cherry-pick C2
git commit --amend
git cherry-pick C3
```
### 1.4.4. Git Tags
```bash
git tag v0 C1
git tag v1 C2
git checkout v1
```
### 1.4.5. Git Describe
```bash
git describe main
git describe bugFix
git commit
```
---
## 1.5. Push & Pull - Git Remotes: 1, 2, 3, 4, 5, 6, 7, 8
### 1.5.1. Git Clone
```bash
git clone
```
### 1.5.2. Git Remote Branches 
```bash
git commit
git checkout o/main
git commit
```
### 1.5.3. Git Fetch
```bash
git fetch
```
### 1.5.4. Git Pull
```bash
git pull
```
### 1.5.5. Git FakeTeamwork
```bash
git clone
git fakeTeamwork 2
git commit
git fetch
git merge o/main
```
or
```bash
git clone
git fakeTeamwork 2
git commit
git pull
```
### 1.5.6. Git Push
```bash
git commit
git commit
git push
```
### 1.5.7. History Divergence
```bash
git clone
git fakeTeamwork
git commit
git pull --rebase
git push
```
### 1.5.8. Remote Rejected
```bash
git checkout -b feature
git push
git branch -f main o/main
```
---
# 2. My progress

![[hw1_results.png|473]]

---
# 3. Converting a text file back into an image

Turning .png to .txt:
```bash
base64 hw1_results.PNG > hw1_results.txt
```

In order to test it, copy the python script below or open any Google Colab or Jupyter Notebook - I've attached a similar .ipynb file.
```python 
import base64
from PIL import Image
import io

with open("hw1_results.txt", "r", encoding="utf-8") as file:
    base64_data = file.read()

if "," in base64_data:
    base64_data = base64_data.split(",")[1]    

image_bytes = base64.b64decode(base64_data)
image = Image.open(io.BytesIO(image_bytes))
image.save("hw1_results_decoded.png")

image
```


