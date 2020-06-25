# CSCW Markov Models (Exploratory Analysis)
Exploratory scripts for examining how people use the *SearchX* interface using experimental data from the CSCW experiment.

**Last Update: 2020-06-25**

## Required Software
See [the `requirements.txt` file](https://github.com/maxwelld90/modelling/blob/master/exploratory/cscw-markov/requirements.txt) for the required Python packages. Run this on Python 3.7.x. You also need a MongoDB instance running locally with the interaction logs stored on it.

## Overview
Points to consider:

* We want to see what happens to interactions with the search interface and its widgets.
* How do interactions with different widgets correspond to interactions with the rest of the search interface?
* If there is more content in a widget, does that entail a greater degree of interaction?
* Look at the first five minutes, then the last five minutes?

## Exprimental Interface
To represent interactions over the *SearchX* interface, we use (in this first pass) Markov models, with each state representing a different interface component (i.e. the searcher is currently interacting with a given component in some way), with transition probabilities the liklihood of transitioning from interface component *x* to interface component *y*. We keep it simple, considering four main areas in which a participant can interact.

![Interface components](interface.png)

The four components are:

* Querying, the state where a participant is entering a query 

### Component Sizes
Note that the *recent queries* component is always placed above the *saved documents* component. Note also of the height of each component; these heights are fixed, and for some reason are different.

Recent Queries             | Saved Documents
:-------------------------:|:-------------------------:
![](interface-queries.png) | ![](interface-saved.png)

Does this have an impact? With the data that I have at my disposal, I cannot be sure. However, given that there is generally a higher recorded percentage of interactions on the saved documents widget, *does that happen because it is simply larger, or it is more useful?* We cannot tell for sure with the available data. We also cannot accurately state how many documents/queries fit in each box (without the need for the scrollbars to become active). If a document with a long title is saved, or a long query is issued, the title/query spills onto a new line, pushing items following it down, thus reducing the number of visible items. If we are to analyse the interactions with these widgets more carefully, I think we need to be better at how we control they are presented to participants.


## Data Source

## Log Events
What events do we use to count the number of interactions? What actually counts as an interaction?


