# Get Earliest Date
## Problem
Devise a formula to be put in the first row of the `Events[Date Start]` column that calculates, for each name in `Events[Name]`, its starting date from the table of schedules, i.e. the date of the first schedule of the event.
## Table Structures
- Events: Name, Date Start
- Schedule: Event Name, Resource Speaker, Topic, Date, Time Start, Time End

## Solution
```
=MAP(Events[Name], LAMBDA(name, MIN(FILTER(Schedule[Date], name=Schedule[Event Name]))))
```