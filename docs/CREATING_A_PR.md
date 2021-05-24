# 1. Opening a Pull Request (PR)
This doc will help you with creating a pull request.

## First, fork the repo
![some alt](https://raw.githubusercontent.com/hackarmour/discord-assistant/main/docs/Pasted%20image%2020210523153059.png)
## Then, clone the forked repo by
```
git clone https://github.com/{userName}/{forkedRepo}.git
```


## Create new working branch
Right after cloning the repo, switch to a new branch because we dont want to mess with the main/master branch, you do this by
```
git checkout -b {newBranchName}
```
The branch name can be anything, just it shouldn't get conflicted with other branch names, such as, when you create a branch `testing` and the branch already exists on the main upstream, it will create conflicts. After switching branches,

## Commit the changes
after cloning and going into your project, make your changes like creating new files, editing files or deleting files, and after you are done,

to commit the changes, first, add all the edited or new files by
```
git add .
```
and then commit it with a comment by,
```
git commit -m "some message here"
```
and by this you have commited your changes, only thing left is pushing those changes
![some alt](https://raw.githubusercontent.com/hackarmour/discord-assistant/main/docs/Pasted%20image%2020210523154447.png)

## Pushing the changes
After we are done commiting, we need to push it to the forked repo, we will do this by,
```
git push -u origin {branchName}
```
![some alt](https://raw.githubusercontent.com/hackarmour/discord-assistant/main/docs/Pasted%20image%2020210523154537.png)
Note: `origin` here refers to the remote repo, and it may be different, please check your remote repo using command,
```
git remote
```
default is `origin`
## Creating a PR
Finally, after all things done, we have to just create a pull request to the remote upstream, we do this by going to the forked repo, and github will automatically reminds us that our repo is *n* commits ahead the main branch of remote upstream,
![some alt](https://raw.githubusercontent.com/hackarmour/discord-assistant/main/docs/Pasted%20image%2020210523154628.png)
We will just click on the *compare & pull request* button to start creating a PR.
it will show something like this
![some alt](https://raw.githubusercontent.com/hackarmour/discord-assistant/main/docs/Pasted%20image%2020210523154733.png)
We will now add a title and a description about what we changed to created.
after it, we will just click on the *create pull request*
### And voila! PR is created
Now, we will just wait for the moderators to review your changes and merge the Pull Request.
