`=IFERROR(MAP(Events[Name], LAMBDA(name, MIN(FILTER(Schedule[Date], name=Schedule[Event Name])))), 0)`


```
=LET(
  year, INT(TEXT(Conducts[Date],"YYYY")),
  offset, IFS(
    WEEKDAY(DATE(year,1,1))<6,-1,
    WEEKDAY(DATE(year,1,1))>=6,0
  ),
  IF(ISBLANK(Conducts[Date]), , "Week " & WEEKNUM(Conducts[Date], 15) + offset)
)
```

```
=LET(
  year, INT(TEXT(Conducts[Date],"YYYY")),
  offset, IFS(
    WEEKDAY(DATE(year,1,1))<6,-1,
    WEEKDAY(DATE(year,1,1))>=6,0
  ),
  firstWeekday, Conducts[Date] - (WEEKDAY(Conducts[Date], 15)) + 1,
  IF(ISBLANK(Conducts[Date]), , TEXT(firstWeekday, "MM/dd")&" - "&TEXT(firstWeekday+6, "MM/dd"))
)
```

```
=FILTER(
    Conducts, 
    (searchOffice = "") + (Conducts[Office] = searchOffice), 
    (searchStartDate = "") + (Conducts[Date] >= searchStartDate), 
    (searchEndDate = "") + (Conducts[Date] <= searchEndDate),
    (searchTerm = "") + (ISNUMBER(SEARCH(searchTerm, Conducts[Conduct Title])))
)
```