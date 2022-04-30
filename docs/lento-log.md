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

## 2022-02-08
`Nathan:` Figured out how to extract app icons on Windows! To understand why this is so hard, it's useful to know that there are 2 types of Windows apps: regular .exes, and Windows Store apps. I didn't understand the distinction between these at first, which led to some problems later on.

I first followed an article giving instructions for how to extract icons from a file using Powershell. This worked on regular .exes. However, I didn't have a filepath to run these commands on for Windows Store apps. After some digging around, I discovered that Windows Store Apps are stored in a folder called `C:\Users\[current_username]\WindowsApps`. Using an administrator-level Powershell window, I navigated through this folder and managed to open up the data folders for some of these apps in File Explorer. Immediately, I noticed that there was a file called `AppxManifest.xml`. Usually manifest files provide metadata, so I opened up one of them in VSCode. A bit of browsing revealed that the path to the app icon files was defined in the `AppxManifest`! I ran a search to see if there was a way to programmatically pull attributes from the `AppxManifest` using Powershell. Sure enough, there was some solid documentation for a command called `Get-AppxManifest`. I tweaked the examples a bit and managed to get it working!

I've documented the exact steps and commands needed to do this on my todo list to implement tomorrow. Hopefully the build will go smoothly now that I have a clear idea of how to extract the app icons.

## 2022-02-13
`Nathan:` Over the last few days, I've been finishing up CardsManagement. There have been a lot less possibly-fatal errors since the 8th, although I've still come across some minor issues that required some research and troubleshooting:

- formatting of powershell commands that we want to run from Python (they get passed through cmd.exe first, leading to some necessary formatting changes)
- making tests involving paths work on both Windows and macOS (different structures/folder conventions need to be accounted for)
- some weird errors that made it past automated tests (comparing orders of items in dicts)

Other than those, I haven't faced any notable issues and have just about finished CardsManagement. Creating a PR today for code review.

## 2022-03-05
`Nathan:` Started on website blocking today. I did some architectural setup for the website blocking functionality, based on what I've learned from research and past experience. So far, I'm pretty proud of how the code is looking. The current plan for website blocks is to use platform-specific firewalls (`pf` on macOS and Windows Firewall on Windows) to block or redirect web requests before they leave the user's computer. Today, I've implemented some basic file modifications to enable and disable `pf` on macOS, along with some basic test cases to make sure this code works as intended.

## 2022-03-18
`Nathan:` Over the past week or two, I've been wrestling with many issues related to the `pf` firewall. I've noticed that there are many idiosyncrasies in how `pf` works, as it uses a fairly complex custom language to describe what requests to block or redirect. This is further complicated by the fact that I'm writing to the `pf` configuration files using Python, meaning that the text must be automatically generated in the correct way in order for `pf` to process it correctly.

Since I've had so many problems with integrating `pf`, I've been wondering whether or not to switch to a different system. If using `pf` from Python is already this difficult, it may take too much time to implement all of our desired features. I also haven't even gotten around to investigating firewalls on Windows, which could be even more problematic than `pf` on macOS. I was chatting with a friend of mine (who is a software engineer with decades of experience) the other day, and he floated the idea of using a proxy server instead of firewalls and modifying system files. We could spin up a proxy server on the user's computer and re-route all web traffic through it, allowing us to inspect requests and block or redirect traffic going to specific websites. While this idea is pretty conceptually complex, it seems more straightforward to implement. A proxy server would work similarly across Windows and macOS, meaning that I wouldn't have to write the same thing twice for the two different platforms.

However,  after spending a day or two investigating the proxy idea, I think I'll probably stick with firewalls for now. The idea of writing a proxy server from scratch sounds fun, but realistically would probably take too much time. The other approach is to embed a pre-existing proxy package that we can modify slightly to fit our needs. I've been researching this for the past one or two days, and I haven't found a solution that works properly so far. So the plan for now is to spend a little bit more time figuring out firewalls, if that doesn't turn out results then I'll come back to proxies.

## 2022-03-19
Fixed the issue with editing the `pf` configuration file from Python! It looks like there is hope that the firewall-based implementation will still work out. I also did a bunch of other work today related to re-organizing the codebase and figuring out how to ask the user for their password in a secure way (we need the user's password to modify `pf` configuration files, as they are protected by administrator permissions).

## 2022-03-22
Hard blocks are now fully functional using `pf`. Did some further code cleanup today so that we can fit soft-blocks into the implementation. I also spent quite a bit of time making the code more readable. After a few weeks of struggling to get this feature working by any means possible, a lot of cruft has grown on top of the code so I took some time today to clean everything up so the code is easy to iterate on top of.

## 2022-03-24
For the past day or two I've been trying to add soft-block support  into our working `pf` firewall integration. The integration currently supports hard-blocks just fine, but for some reason I can't get soft-blocks working. Soft-blocks are a lot more complex, because we need to prompt the user instead of just shutting down the request outright like we do with hard-blocks. It looks like the type of redirection functionality we need is fairly complex to implement in `pf`.

Because of all the problems I've been facing with soft-blocks and our firewall-based implementation, I went back to our earlier idea with proxies. After a little more investigation, I decided to experiment a bit with a package called `proxy.py`. `proxy.py` provides a usable proxy server out of the box, along with tools for adding your own code to the server and integrating the whole thing into a Python project. After breaking my internet connection, freezing my computer, and a host of other mildly terrifying issues, I managed to get `proxy.py` working! Web traffic would successfully pass through the proxy server, and we could see what websites the traffic was going to.

So, I've scrapped my previous work on our firewalls-and-system-files idea and I've switched over most of our website-blocking code to integrate `proxy.py` instead. However, this isn't the end of work on this feature: `proxy.py` by itself is just a simple proxy. It doesn't have methods for blocking traffic based on the website, which is what we need for Lento. However, `proxy.py` does provide an ergonomic way to add code to the package through custom plugins, so over the next few days I plan to write a custom plugin for `proxy.py` that will contain the hard-blocking and soft-blocking features we need for Lento.

## 2022-03-27
So far so good with the `proxy.py` implementation. I've been working on the custom LentoBlocker plugin for `proxy.py` and it's working as intended so far. However, while implementing the necessary features using our new `proxy.py` plan, I've realized that we have a small issue. We want to store data about the block such as what sites are blocked and how much time is left in the block *outside* of the running Lento application. This is because we want to make it so that even if the user restarts their computer or otherwise tries to tamper with the block, we can still access the original block data in a form that the user cannot easily tamper with.

The idea I'm working with so far for that is to store block data, such as how much time is left, as a binary-encoded piece of data in a database. This provides a few benefits:

- Since it's stored in a database, the average user probably doesn't know how to even open up the stored data, let alone tamper with it
- Storing the data in a database allows us to easily retrieve exactly what we need through database interaction functions
- Encoding the data as binary using Python's `pickle` function makes it pretty difficult for users to tamper with. It also makes it pretty efficient to retrieve and store the data: since we're just storing an exact binary representation, we don't need to convert the data between a format that we can store as a file (like text) and a format that we can work with (like a Python object).

I've decided to go with SQLite as the format for our database, because it is lightweight and simple. Our database needs aren't very complex (we just want to store some binary data, along with some labels so we can retrieve certain bits of data at different points), and I've worked with SQLite before, so it seems like an ideal choice. 

So, for the last few days, I've been integrating `proxy.py` and an SQLite database into our project. This is more complex that our previous plan from a technical standpoint, but it is super fun to build and it is a lot more robust and simpler to maintain than our initial approach. I expect that in the next couple of days I'll finish support for this implementation for both Windows and macOS. After that, there's only a little bit of code cleanup left to do before I'm finally finished with this feature.

## 2022-04-03
Finished the website blocking feature! This was definitely the hardest part of the project; everything from here on out is a lot simpler and most of the foundation is laid to build the other features. I'm very proud of the code for this feature as it is quite professional and easy to understand, even though it does a lot of complex things under the hood. I'm now moving on to some code that ties all of this complex logic on the backend to the frontend. This next bit of work should allow us to easily connect the buttons of our app to start a block using `proxy.py`, the database, and all the other things I've built over the last few months.

## 2022-04-04
Added some basic code that modifies the settings file to show whether or not a block is currently ongoing. We don't rely on this internally to actually store the status of a block, but it makes it quick and easy for our app to display what's happening to the user.

## 2022-04-07
I've fixed a host of bugs related to tying all of the parts of our app together. From database connection issues to launching the daemon to compilation issues, the last few days have been a wild ride of sorting out a bunch of small but importnat issues with our code and making sure all of the different parts work together properly. There have been two notable issues so far: PyInstaller multithreading and daemon launching.

PyInstaller is the package that we're using to bundle Lento as an app instead of just raw code. It works great for the frontend based on my tests with some sample code and Peregrine. However, where it falls down is for our backend. On the backend, we use `proxy.py`, which uses multiprocessing to handle multiple simultaneous web requests. This allows us to inspect user web traffic without slowing down a user's web browsing experience. The problem is that PyInstaller doesn't handle code that uses multiprocessing very well: it tends to create multiple processes but never clean up the ones that are finished, resulting in the code taking up more and more of the computer's resources until the whole computer freezes. This is obviously a huge issue, but after some research, I've found a couple lines of code to add to our implementation that seems to mostly stabilize the issue. It seems like a fragile solution so I'm going to keep an eye on it over the next few days.

The other issue is daemon launching. We need to launch the daemon in a way that makes it difficult for the user to just kill the process. There are methods for launching a protected process in the background on both macOS and Windows, which was our original plan. However, this turns out to be quite difficult to do and generally a very complex implementation. So the idea now is to just launch the daemon normally and then build a separate piece of code that is launched as a protected process. This separate piece of code keeps an eye on the daemon and revives it as necessary if the user tampers with it. Armed with this new plan, I'm implementing the daemon launching functionality and it should be done within the next few days.

## 2022-04-09
I've finished the integration code, so we can now tie everything in the project together! It's worth noting that finishing off this feature came with one final challenge. PyInstaller started breaking multiprocessing this time, even with the hacks that I implemented before. To solve this, I decided to look at some other solutions for packaging up the backend. After some research, I stumbled across a package called Nuitka. Nuitka takes a different approach than PyInstaller, converting Python files to C code before compiling that into binary. This approach is a lot more effective and allows multiprocessing to work perfectly!

Unfortunately, Nuitka doesn't work with the rest of our project because it doesn't yet have support for PySide6. So the solution right now is to use Nuitka to package the backend only, then PyInstaller to package up everything else. Not the most ideal situation but it works well enough. And with that, the integration code is finished! We probably won't have time to implement everything we want to do before regionals, but I'm hoping to finish a GUI prototype that we can demo for the judges. Charlie's been working on that and I'll probably jump in and help him with it over the next few days.

## 2022-04-11
GUI prototype finished! We've completed a prototype that has the core features for demonstrating our idea to the judges. Over the next few days, I'm going to implement app blocking, notifications, and other improvements, but that's too late for regionals.

## 2022-04-25
Over the past few days, a lot has happened. We got into CWSF! To take advantage of this opportunity, we're making a ton of improvements to Lento and we're also planning on conducting some beta rounds and experiments for further proof of how beneficial Lento can be. I've been working on app blocking, small bugs with the timer freezing, notifications, and more. At this point, basically everything that we've planned for the backend is done. There haven't been very many notable challenges besides the odd bug here and there so I'm confident that Lento will do quite well as the code is very well written.
