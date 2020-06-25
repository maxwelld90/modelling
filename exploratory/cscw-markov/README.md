# CSCW Markov Models (Exploratory Analysis)
Exploratory scripts for examining how people use the *SearchX* interface using experimental data from the CSCW experiment.

**Last Update: 2020-06-25**

## Required Software
See [the `requirements.txt` file](https://github.com/maxwelld90/modelling/blob/master/exploratory/cscw-markov/requirements.txt) for the required Python packages. Run this on Python 3.7.x. You also need a MongoDB instance running locally with the interaction logs stored on it.

## Overview
We want to see roughly how behaviours change when interacting with different components on the *SearchX* interface. To start, we limit our exploration using data from an interaction log derived from the independent condition of the CSCW experiment, i.e. participants working solo on a search task. When we look at the data in different ways, what changes in behaviour do we observe? In paricular, we are interested in the number of interactions that take place with the four main components.

Questions we want to consider (I think):
* What are the interaction likelihoods for the main interface components?
* How do interactions with different widgets correspond to interactions with the rest of the search interface?
* If there is more content in a widget, does that entail a greater degree of interaction?
* Do the levels of interaction vary at different points in time during search sessions?

## Exprimental Interface
To represent interactions over the *SearchX* interface, we use (in this first pass) Markov models, with each state representing a different interface component (i.e. the searcher is currently interacting with a given component in some way), with transition probabilities the liklihood of transitioning from interface component *x* to interface component *y*. We keep it simple, considering four main areas in which a participant can interact.

![Interface components](interface.png)

### Interface Components (States)
For the above model, we keep things simple, considering four main components that participants interact with. These are:

* ![#E13D47](https://via.placeholder.com/15/E13D47/000000?text=+) **Querying**, the state where a participant is *entering a query* into the query box.
* ![#E17547](https://via.placeholder.com/15/E17547/000000?text=+) **Results**, the state where a participant interacts with the *organic results, or ten blue links* that are presented to them.
* ![#6CA944](https://via.placeholder.com/15/6CA944/000000?text=+) **Recent**, the state where a participant interacts with the *recent queries component*.
* ![#206BA6](https://via.placeholder.com/15/206BA6/000000?text=+) **Saved**, the state where a participant interacts with the *saved documents component*.

By interact, we mean a hover event. An event where the participant moves their mouse cursor over the component; we have events that capture this. The exception is for the querying component; see *Log Events* below.

### Components of Interest
Note that the *recent queries* component is always placed above the *saved documents* component. Note also of the height of each component; these heights are fixed, and for some reason are different.

Recent Queries             | Saved Documents
:-------------------------:|:-------------------------:
![](interface-queries.png) | ![](interface-saved.png)

Does this have an impact? With the data that I have at my disposal, I cannot be sure. However, given that there is generally a higher recorded percentage of interactions on the saved documents widget, *does that happen because it is simply larger, or it is more useful?* We cannot tell for sure with the available data. We also cannot accurately state how many documents/queries fit in each box (without the need for the scrollbars to become active). If a document with a long title is saved, or a long query is issued, the title/query spills onto a new line, pushing items following it down, thus reducing the number of visible items. If we are to analyse the interactions with these widgets more carefully, I think we need to be better at how we control they are presented to participants.

### Log Events
How do we approximate what people are doing at a given time from the log we have? As we are looking at hover events, we look for the hover events in the log corresponding to a given event!

**Event**  | **Log Event**
:---------:|:-------------------------:
Querying   | `QUERYSUGGESTIONS_GET`*
Results    | `SEARCHRESULT_HOVERENTER`
Recent     | `QUERYHISTORY_HOVERENTER`
Saved      | `BOOKMARK_HOVERENTER`

These are our events that trigger a change in state. Note that for querying, there is *no hover event for the query box widget*. We have to approximate here; instead, we look for when a query suggestion is requested by the client. This means that the participant is interacting with the query box. For the first instance of a `QUERYSUGGESTIONS_GET` event (they typically occur in blocks, character-by-character), we switch state to querying.

At the moment, times are not being tracked, but if it is worth looking into later on, I will do so. I felt that working out a reliable way to track times was not worth the effort at this first pass. Like any other log, there's lots of weird scenarios that a simple script that tracks a start and end event can't reliably capture!

## Basic Method
To compute the values reported below, we took each of the trigger events listed above (representing changes in state), and began counting the number of occurrences. We could then find the sum (over the four) and computer the percentage of interactions belonging to a specific component. For state-to-state transitions, we also counted the number of times transitions occurred from one state to another, and counted those. Percentages were also computed from these values, and slapped onto a Markov model-style illustration.

## Results
Let's have a look at what I've found. A lot of it is to be expected, but interesting nevertheless. First, we'll have a look at the raw percentage values for interactions that take place over each component, and then move towards splitting these values up to construct a basic model showing the percentage likelihood of switching from one state to another.

We chop the dataset up based on a number of different considerations to see what is going on. Each approach is shown in the table below.

**Type**  | **Description**
:--------:|:-------------------------:
`full`    | The entire search session.
`first5`  | The first five minutes of the search session.
`second5` | From 5-10 minutes into the search session.
`savedX`  | Considering only events that take place when `X` documents have been saved.
`queryY`  | Considering only events that take place when `Y` queries have been issued.

The final two are interesting -- the values of `X` and `Y` dictate how many items are present in the saved documents and recent queries components, respectively. By examining the dataset this way, we can see how interactions vary as the number of items in each of the two components increase.

### Dataset Distributions

### Interaction Percentages
Given the datasets, what were the interaction values recorded? We could consider things from two perspectives: *(i)* considering each session by itself, meaning we have 72 unique entries, and show those individually, or *(ii)* sum up all of the interactions that take place over all 72 sessions, and treat them as one. We report findings from both approaches.

#### Considering Sessions Individually

#### Summing Everything Up
When we

### As Content Increases, What Happens?
Another question posed is: *as the content inside the saved documents and recent queries components increases, what happens to the interactions?* To consider this question, we look at the changes in the total percentage of interactions that take place in the four main components as the number of items in the saved documents and recent queries components increases. Note that this first pass controls only the number of items in the two components in isolation; i.e. if we explicitly look at interactions when 4 items are in the saved documents list (`x=4`), there could be a variable number of queries in the recently issued queries component.

![As the number of saved documents increases (x axis), what happens?](saved-documents-increase.png)

So from this plot, we want to look at the orange line first -- which represents the percentage of interactions taking place in the saved documents component, as the number of items in it increases (x axis). This ranges from 0% (at zero documents) to roughly 20% (at seven documents). We generally see an increase as the number of items itself increases. The blue line (recent queries) slowly decreases as the number of saved documents increases. There may be a relationship between the two components -- but I think we need to look at controlling the number of items in both components to draw any meaningful conclusions.

![As the number of recent queries increases (x axis), what happens?](recent-queries-increase.png)

When we look at the second plot, we're looking at what happens when the number of queries increases over time (so more items appear in the recent queries component). One thing that looks a bit weird is why the red line (results) starts at 20%. How can you look at results when there are none (at zero queries)? I think this is an artefact of the search interface; perhaps there's a `<div>` that stores results that is still present at the beginning -- see the screenshot below. The logger is tracking hovers into that red box. So there's still events being captured. I will need to update the script to remove these events. However, looking at the blue line (interactions with recent queries), we again see a gradual increase in interactions that take place. Interestingly, we see a lower percentage for the orange line (saved documents), meaning fewer interactions take place within the previously saved documents component than we witnessed above.

![Big bad red box that swallows up hover events.](interface-results-container.png)

**tl;dr** We see increases in the interactions within both the saved documents and recent queries components as the number of items within them increases. Both seem to follow a similar trend, although the saved documents component affords a slightly higher rate of increase (at least from a crude visual inspection). We need to do a bit more analysis, controlling what's in BOTH components, to see if one is more *dominant* or *important* than the other, or at least, one that does afford more interactions/attraction.

### Towards Markov-Style Representations
Now, let's break things down a bit more. As the log analysis script parses the log events in chronological order, we can work out what the state is at any current point -- and when an event is reached that triggers a state change (see [Log Events](#log-events) above), we can then work out how many occurrences of state changes from one to another happen in a given dataset. We visualise that here with some basic model representations over the four states.

## Thoughts
- so the saved documents widget is double the height of the recent queries widget.
    - we observed a higher percentage of interactions with the saved documents widget.
    - if we increase the size of a widget, does that mean we are priming participants/users into thinking that "hey, this one is more important"?
    - or is it simply due to the fact that in the scenario, it is simply more useful?
    - we should take a look at the data of a collaborative session, and consider interactions on the two widgets there. is there a difference?
        - because recent queries are arguably more important for saved documents, perhaps without defined roles?

- so with recently saved documents and queries controlled, maybe we can get an idea of what one is more dominant.
    - we need to control both to be able to draw meaningful conclusions!