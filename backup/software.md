---
toc: false
layout: post
description: I hate it.
categories: [markdown]
title: Software
---

Today, at my first day back at work, I realized something: I viscerally hate most software. Here are some programs I have the misfortune of using:

- Microsoft Teams
- Azure DevOps
- Azure in general
- Google Chrome
- Google Search
- Spotify
- The Triodos bank app
- Bloomberg Hypermedia API

Let's talk about each of them in turn.

**Microsoft Teams**  
Chatting is a solved problem. It was solved back in 1993 when IRC was invented. But SOMEHOW, Microsoft managed to fuck it up.  
Messages are not delivered reliably: on occasion you will have thought you informed your colleague only for them to be surprised later, because Teams didn't send your message. What's worse, the program has the audacity *not to even tell you*.  
Inputs are swallowed: when I click on a chat and want to start typing, Teams takes a second to load the chat. It then swallows my inputs and puts them to work in navigating through the UI, putting the program in arcane and arbitrary states. Bash (1989) never has this problem: I open a shell, start typing immediately, and it simply buffers the inputs.  
Manages to fuck up simple commands: teams has a very useful feature inspired by IRC. The ability to go to the top bar and type a command to do something. Like good old `/msg <name> <message>` on IRC, you type `/chat <name> <message>` in the search bar. Except WORKS LIKE SHIT. You need to *wait* for the input thing to recognize your command, or hit tab (I can type "chat" in about 100 ms, why the fuck would I ever use tab to complete it?). **If you're too fast, it will simply not recognize the command**. Oh, and if you do hit tab and keep typing (because you already know you're going to look for the person to chat), this piece of shit will just swallow your fucking inputs. So you have to wait again until Teams decides you are allowed to look for someone. How in the everloving FUCK did this make it into the program, and why, why oh why is this the most used chat program in the world? [1]  
I think this is my main gripe with Teams: it punishes you for being fast or efficient. Why do I need to wait for software to "help" me? If I can type a name or identifier faster than the software can autocomplete it, *it should nevertheless work*. Teams is *constantly* getting in my way when I want to send a quick message to colleagues. But let's continue because I have more to say.  
It generates unncessary notifications: there's a reason I hid the call menu. It's a slow-loading piece of shit which I never use. If I want to call someone, I type `/call`, wait, type a name, wait, and hit enter (I really would like to not have to wait, see above, but alas). Why does it INSIST on showing me notifications with an ugly red dot? Even when I can also see those in the activity menu? Why even is there an activity menu? Why do I need this "holistic overview"? I have four tabs, there's not that much information to go around. More crud.  
That is my main gripe with modern software. It's filled with crap I do not need, and hides all the information I do need. Why do I have to click seven times on any given website to do anything? Why do I always have to wait for the UI to load? Why does every website present as little information as possible? People read books, for fuck's sake. Any given still from Dora the Explorer has more content than any modern UI.  
It integrates like shit: if I make a meeting in Microsoft Outlook, I get different options than in Teams. For instance, in Teams I can connect my meeting to a channel, whereas I can't do this in Outlook. But if I want to make a recurring meeting, Teams only has half the options for recurrence (note that recurrece was solved in 1975 with the advent of CRON). But then meetings in teams with a channel I can't edit in Outlook because I don't show up as the owner. Did I mention it first shows me the calendar and *then* loads the items in it? What's the point of that?

In conclusion, Teams is a laggy, buggy piece of shit. Microsoft really embraced the "Agile" methodology, where "Agile" means "ship low quality software to corporates where end users are forced to use your shite because they don't have sway in the organization".

**Azure DevOps**  
Now that we're on the subject of agile, Azure DevOps. My god what a dumpster fire. [2] There are about forty different views 

**Azure in general**  
As part of one of my projects I wanted to try out Azure's OCR API. I'm a data scientist, so naturally I use Python to do so. A quick Google search yields Microsoft's cognitive services API. Okay, fine, seems relatively up to date, let's have a look. Turns out there are not one, but *two* quickstarts for Python. Here's my experience with the first one:

[Original link](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-recognizing-text), [link to quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/csharp-hand-text), [link to Python quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-hand-text), [link to Python tutorial](https://github.com/Microsoft/Cognitive-Vision-Python) (blue button at the bottom of the page). **THIS TUTORIAL DOES NOT WORK**. Not only is it written in the most horrible Python I have had the ill luck to lay eyes upon (really, you couldn't even manage to follow standard python conventions such as, I don't know, using whitespace in meaningful ways and using underscores in variable names, let alone writing readable code), it doesn't even work!

The second one is using the "Python SDK", which seems little more than an OO fetishists semen spontaneously reproducing with a Python interpreter. Classes. So many fucking classes and namespace. When Tim Peters said "Namespaces are a honking great idea - let's do more of those!", he didn't mean this. I literally have to import this abomination:

````python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
````

How about writing some *pythonic* code for once? Why do I keep being reminded of .NET-applications where you have classes upon classes upon classes? [Stop writing classes]().

**Google Search**  
Google search consistently delivers out of date answers and documentation. Even now I have to look very hard to avoid landing in the python 2.7 documentation. It's UNSUPPORTED. Nobody should be using it! And yet Google merrily continues linking to the python 2.7 docs. Same with Rust, anything you want to do? Let's link you to the old experimental versions! Rust is especially insidious because it's a developing language, and libraries change quickly.

**Notes**  
[1] I know there are reasons and I understand them. Doesn't make me any less mad at this useless piece of shit software.  
[2] We're probably not using it correctly in our organization but I want to complain anyway. Software which is easy to use incorrectly is shit software.
