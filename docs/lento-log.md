# Lento Project Log

## 2021-12-10
Came up with the idea of Lento and jotted down some quick ideas. I've decided I'll most likely build Lento using Python. This is because I want to learn more Python due to its usage in bioinformatics and data science in general (fields that I'm interested in). I also like Python's widespread use and documentation; this will make it easier to build and maintain Lento. However, Python's not the fastest and isn't a compiled language, which could pose obstacles along the road.

## 2021-12-15
Started on the project after coming up with the idea. The first thing I did was create a survey to see if I can garner more feedback about my idea.

**Required survey questions:**

- How often do you find yourself sidetracked by distracting apps/websites when you're trying to focus?
- Would you be interested in an app that blocks off distracting websites/apps? (by preventing opening them/connecting to them for a period of time via lists you specify)
- Do you currently use an app that blocks off distractions?
    - Please list the one(s) you use:
- Would you be interested in any of the following additional features?

**Optional survey questions:**

- Anything else you'd like to say?
- What's your Discord username and tag (optional, but will be helpful for contacting you if the app materializes)
- What's your job? (optional, but useful for statistical purposes; if you're a student feel free to put your uni/major!)

Also set up a note to record feature ideas and other apps I investigated that Lento improves upon.

## 2021-12-17
Took the feature list and started sorting out the technical details. Did a lot of research into how to block websites and apps, and how to structure the code properly. Also tested out some of my ideas on Windows (I use macOS/Fedora so not as familiar with how my ideas would work with that OS).

## 2021-12-18
Did more research into the idea and added a mini FAQ to my notes about the technical details. Saved down useful articles/forum answers/websites in a Raindrop.io collection: https://raindrop.io/ThatNerd/lento-21974083

## 2021-12-21
Started making some concept art for how the app would actually look like. This is helpful because it allows me to visualize features and how it will look to the end user.

## 2021-12-22
Finalized technical details... for now. Hopefully I don't run into any unanswered technical questions during the build process. Also creating some diagrams for planning purposes, to make sure I can efficiently create the entire app.

## 2021-12-24
Kicked off the project setup by writing the README file for the project repo, which details things like features, installation instructions, and contributing guidelines. In my case, I stated that contributions were closed for now due to Lento being a science fair project.

I also started creating a detailed diagram of how every function in the codebase would fit together for all the features. This is super helpful because it ensure that I have all of the code structuring properly thought out. I'm not done the diagram as of yet, but I've already discovered flaws in my planning from the parts I've done so far and have taken the necessary steps to correct them.

In addition to *that* (can you tell today was a busy day?), I also drew up a little diagram (shown below) covering how the code should handle scenarios wher e the user tries to tamper with certain files to disable the block early. I've concluded from this that while I can't make the block foolproof, I've structured it in a way where it will be basically impossible to remove for the average user and considerably tedious for a more technically knowledgeable one.

![](./attachments/lento-fail-recovery-diagram.png)

## 2021-12-27
Working more on the codebase structure diagram:
![](./attachments/lento-codebase-map-wip.png)

Not much interesting progress to report on, but here are some questions/problems/ideas I'm thinking about while building the rest of this graph:
- integrity fix - needs to be moved into a helper?
- all functions called by the daemon need to be either built in or a helper
    - can't depend on CLI in case the app is uninstalled
- should I cut out the CLI for blocks entirely?
    - maybe move blocking functions into helpers and have CLI commands pointing to them for the GUI