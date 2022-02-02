# Lento Project Log

## 2021-12-10
`Nathan:` Came up with the idea of Lento and jotted down some quick ideas. I've decided I'll most likely build Lento using Python. This is because I want to learn more Python due to its usage in bioinformatics and data science in general (fields that I'm interested in). I also like Python's widespread use and documentation; this will make it easier to build and maintain Lento. However, Python's not the fastest and isn't a compiled language, which could pose obstacles along the road.

## 2021-12-15
`Nathan:` Started on the project after coming up with the idea. The first thing I did was create a survey to see if I can garner more feedback about my idea.

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
`Nathan:` Took the feature list and started sorting out the technical details. Did a lot of research into how to block websites and apps, and how to structure the code properly. Also tested out some of my ideas on Windows (I use macOS/Fedora so not as familiar with how my ideas would work with that OS).

## 2021-12-18
`Nathan:` Did more research into the idea and added a mini FAQ to my notes about the technical details. Saved down useful articles/forum answers/websites in a Raindrop.io collection: https://raindrop.io/ThatNerd/lento-21974083

## 2021-12-21
`Nathan:` Started making some concept art for how the app would actually look like. This is helpful because it allows me to visualize features and how it will look to the end user.

## 2021-12-22
`Nathan:` Finalized technical details... for now. Hopefully I don't run into any unanswered technical questions during the build process. Also creating some diagrams for planning purposes, to make sure I can efficiently create the entire app.

## 2021-12-24
`Nathan:` Kicked off the project setup by writing the README file for the project repo, which details things like features, installation instructions, and contributing guidelines. In my case, I stated that contributions were closed for now due to Lento being a science fair project.

I also started creating a detailed diagram of how every function in the codebase would fit together for all the features. This is super helpful because it ensure that I have all of the code structuring properly thought out. I'm not done the diagram as of yet, but I've already discovered flaws in my planning from the parts I've done so far and have taken the necessary steps to correct them.

In addition to *that* (can you tell today was a busy day?), I also drew up a little diagram (shown below) covering how the code should handle scenarios where the user tries to tamper with certain files to disable the block early. I've concluded from this that while I can't make the block foolproof, I've structured it in a way where it will be basically impossible to remove for the average user and considerably tedious for a more technically knowledgeable one.

![](https://bn1301files.storage.live.com/y4mnFy238AgTOiXdW01Kn-XNDbj0T5om-882Nu8zbbBuTf3RYMQWfBLA9gb5FJrXwO_OEHIIDHK3fi6DpcVQjed9o92zSNaIBElczorAnrhTeWU9AuXOkh1JGJSe_aMBFO4nnwbx5eeCTioNAlIwupdBH-zuS3zNK6gcoxfooJnQyNVMOgdPC43GiqCgRCvaXym?width=2732&height=2048&cropmode=none)

## 2021-12-27
`Nathan:` Working more on the codebase structure diagram:

![](https://bn1301files.storage.live.com/y4mTrhwBikoFJxD_tR03mD43elHY8yO74f9pDaS6Sug2p_JEIr6q5tG_nlr5-JBJken9oAEQNE_r1nONV72HKvqLSZfemWJmbjYpcw_7D9tqpQUzukR8GD6WR8NXbeWDt-6ZAkzG15xeWNxr66OhFjbS26sNbe-NAYk6nogL7NVjF21dbhhit7cM3xy7aNH3dka?width=1650&height=770&cropmode=none)

Not much interesting progress to report on, but here are some questions/problems/ideas I'm thinking about while building the rest of this graph:
- integrity fix - needs to be moved into a helper?
- all functions called by the daemon need to be either built in or a helper
    - can't depend on CLI in case the app is uninstalled
- should I cut out the CLI for blocks entirely?
    - maybe move blocking functions into helpers and have CLI commands pointing to them for the GUI

## 2022-01-01
`Nathan:` Today was an interesting day. Charlie and I started a conversation about the science fair ideas he was considering, one of which was an app called Topical. We found out halfway through that Topical and Lento had an 80% overlap. Thus, we've decided to collaborate, merging ideas from Topical into Lento.

Rough notes from the meeting:
```
- notifications
    - popup with session goal on idle/app switch
    - goal -> notification
        - notification presets
            - nest under cards
            - type: regular, popup, optional notification sound, audio message
- goalbook
    - each card = goal
    - screen with a list of the cards
        - subtitle/description (1 line)

- technical
    - linting
        - spaces
        - double quotes
    - tests


- 15 min timer for softblocks
    - initially block same way
    - send a notif after reblocking
- softblock counters!!
- "time saved" counter

- pop cheater notif at any tampering
```

## 2022-01-03
`Nathan:` Put in a lot of time restructuring the codebase map today:

![](https://bn1301files.storage.live.com/y4mvut82Qy2Giq7M4KPl6XMKlEnVuJEMKG9nRVJ4YqstVDVQkVhGpWE4fvdCG7Fb0aZVnK5fCZtXy0m4boueUwTyclqSnBTtRI91o42Px-PBuTdA9O6ehmm33VivuHeS6-klO296q9q30aH9vD6imJx8lz5p9DHis_uSw2CACP5d0hwE2LUV-KXK_L_mQaJ47hV?width=1916&height=740&cropmode=none)

It's now a lot clearer. Major sections (GUI, common backend, daemon, etc) are delineated by colour, and the functions for different features are grouped together through rectangular dividers. This will be useful as we move into scheduling/dividing work and actual implementation. I've also merged in Charlie's ideas from our earlier conversation, fully merging our two projects.

In addition, I've moved this log and other existing Lento documentation into the shared repo so that Charlie has full access to read/edit/add/comment.

## 2022-01-09
`Nathan:` Took some time to read over the saved articles that we added to our Raindrop.io collection, just to make sure I was familiar with all the concepts that we were going to need. Based on my experiences with past software development projects, I think it'll be beneficial to create a small app that prototypes some of the concepts that we're going to use in Lento.

## 2022-01-10
`Nathan`: Started on an app called [Peregrine](https://github.com/ThatNerdSquared/peregrine). The ideas and philosophy behind Peregrine is mostly unrelated to Lento, and I've been wanting to build it for a long time. However, I've noticed that a lot of the basic implementation is actually quite similar in terms of what the code needs to do and how the app is structured. So, I've decided to build a basic version of Peregrine as a prototype for Lento.

So far, work on Peregrine has been massively productive. Not only have I managed to build a beta version of Peregrine, I've also been able to see how concepts for Lento will fit together in a real-life software scenario. I've already gotten comfortable with PySide for laying out graphical interfaces and have a good mental model of how the GUI and backend fit together. I've also been able to get some hands-on practice with some general Python tools such as pytest.

It's worth talking about some initial obstacles I had to troubleshoot with this prototype. First, I ended up having to diverge from my original plan of what tool to use for linting. Initially, I planned to use pylint to enforce a consistent style across our code. However, it kept showing cryptic, unsolvable errors related to something within the PySide package. After poking around online for a while I discovered that the problem was caused by pylint and PySide6 not having full support for each other. I decided to solve this problem by replacing pylint with flake8. This was a fairly easy fix.

I also had to overcome an issue with the scrolling log entry interface. The log interface had to be able to scroll in reverse chronological order, as well as wrap text. I couldn't figure out how to to do this for a while. Eventually, after consulting some online documentation and experimenting with different methods, I managed to settle on a solution using a specific combination of QScrollView() and layouts.

## 2022-01-16
`Nathan:` Over the last few days, I've been fixing up some smaller issues with Peregrine. I'm coming to a close with my work on it as a prototype for Lento. Soon, I'll port some parts of Peregrine over to Lento and then stop work on Peregrine until after Lento v1.

The last interesting problem I've encountered with Peregrine involves packaging the Python code into OS-specific app packages. We're using PyInstaller to do this with both Peregrine and Lento. The problem is that PyInstaller requires a certain setup for each OS. For example, the command you need to run to use PyInstaller on macOS differs slightly with the command you need to use on Windows. I spent an hour or two working out the nuances of these setups with Charlie, switching between macOS and Windows to rapidly iterate on my ideas. After a bit of experimenting, I managed to work out the correct configuration for each platform. This was a great experience as I can directly port the PyInstaller setup from Peregrine to Lento, completely avoiding these problems next time.

## 2022-01-18
`Nathan:` Updated some of the docs for Lento to note down all of the things I've learned from the Peregrine prototype.

## 2022-01-23
`Nathan:` Started on the CardsManagement part of the backend. Hoping to write clean code with 100% test coverage. CardsManagement is easier to test and think about than the other parts of the backend so I'm starting with it as a sort of warm-up.

`Charlie:` Started on GUI — Currently learning GUI design with PySide and Qt, wiped computer and set up coding environments again. Currently planning each part of GUI code, scoping out functions needed + requirements + linking w/backend. Experimenting with colours, widget design, page layout, and animations in PySide — mapping out more interfaces as I go.

## 2022-01-25
We ran through a bunch of [CodeWars](https://www.codewars.com) problems today. While not directly related to Lento, they sharpened our skills with Python, which will make development faster/easier. This is especially important for Nathan, as he's coming from JS/TS and still getting used to/learning Python.

## 2022-01-28
`Nathan:` I've been putting some serious work into `CardsManagement` over the last few days. One of the issues I've encountered so far is URL validation. Initially, I wanted to add a check to make sure that when a user adds a URL to a blocklist, a website actually exists at that URL. I also wanted to check to make sure the URL had valid formatting.

However, this turned out to be a lot harder than I originally anticipated. After some research (reading over the original W3C URL spec along with some articles), it turns out that there are so many formats for valid URLs that it's basically impossible to define what a "correct" or "incorrect" URL looks like based on the text alone. Experimenting with different methods also showed that pinging the server at the URL to check for a website also presented issues; we had to consider cases where the user would be offline, where the website would be down, other firewall/router restrictions, etc. Ultimately, we decided to forgo URL validation. While that isn't as clean of a solution as I'd hoped for, it doesn't have any large impact on Lento's UX.

I've also faced some problems with the app blocklists, as they require different methods on macOS and Windows. Right now, I'm not sure how to extract and store all the information we'll need for the blocklists (app name, icon, bundle ID if on macOS, enabled/disabled) on either platform. I'll be investigating this more as I try to finish up the `CardsManagement` section in the next week.

## 2022-02-01
`Nathan:` I've successfully solved the app blocklists issues on macOS! After some thinking and drawing a few diagrams, I've managed to find methods for extracting each bit of required info:
- **app name**: parse from the file path by finding what's directly in front of the ".app" string
- **app icon**: the file name for this is defined in an Info.plist file found inside every app package. After browsing the internet for a while, I've discovered that you can parse these .plist files as Python dictionaries *directly from the Python standard library*! Using the built-in `plistlib` library, I was able to find the file name f the app icon, and then convert it to a .jpg using the `pillow` library. We've decided on storing these in an application support folder, which on macOS is `~/Library/Application Support/Lento/`.
- **bundle ID**: some research (searching StackOverflow) revealed that there was a command to get the bundle ID from a `.app` file, so I'm running this and then capturing the output.
- **enabled/disabled**: default to enabled, this matches with the user expectations.

I'm currently still working on how to do this on Windows. While I'm thinking about that, I'm also working on some of the last parts of `CardsManagement`, namely notification and goal management.
