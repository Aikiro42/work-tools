```
=MAP(Event[Name], LAMBDA(name, IFERROR(MIN(FILTER(Schedule[Date], name=Schedule[Event Name])))))
```

```
=LET(
  calcDate, IFERROR(DATEVALUE(CalendarMonth & " " & A5 & ", " & CalendarYear),),
  holidays, IFERROR(FILTER(Holiday[Shorthand], CalendarMonth=Holiday[Month], A5=Holiday[Day]),),
  IF(
    ISBLANK(calcDate),
    ,
    JOIN(
      "; " & CHAR(10),
      IFERROR(FILTER(
        Activities[Activity],
        INT(Activities[Anticipated Start Date])<=calcDate,
        calcDate<=INT(
          IF(
            ISBLANK(Activities[Anticipated End Date]),
            Activities[Anticipated Start Date],
            Activities[Anticipated End Date]
          )
        )
      ),)
    )
  )
)
```

```
=LET(
  calcDate, IFERROR(DATEVALUE(CalendarMonth & " " & A5 & ", " & CalendarYear),),
  isPast, IF(calcDate<=NOW(), CHAR(8203),),
  holidays, IFERROR(FILTER(Holiday[Holiday], CalendarMonth=Holiday[Month], A5=Holiday[Day]),),
  hasHoliday, IF(ISBLANK(holidays),,CHAR(8204)),
  dateActivities, IFERROR(FILTER(
        Activities[Activity],
        INT(Activities[Anticipated Start Date])<=calcDate,
        calcDate<=INT(
          IF(
            ISBLANK(Activities[Anticipated End Date]),
            Activities[Anticipated Start Date],
            Activities[Anticipated End Date]
          )
        )
      ),),
  IF(
    ISBLANK(calcDate),
    ,
    TEXTJOIN(
      "; " & CHAR(10),
      TRUE,
      holidays,
      dateActivities
    ) & isPast & hasHoliday
  )
)
```

---

```
=IFERROR(FILTER({Activities[Priority],Activities[Done],Activities[Start Date], Activities[Activity], Activities[Category], Activities[Folder], Activities[Remarks]}, TEXT(Activities[Start Date], "MMMM")=SummaryMonthQuery), {FALSE,"","No pending tasks found."})
```

```
=LET(
  tasksSummary, IFERROR(FILTER({Activities[Priority],Activities[Done],Activities[Start Date], Activities[Activity], Activities[Category], Activities[Folder], Activities[Remarks]}, TEXT(Activities[Start Date], "MMMM")=SummaryMonthQuery), {FALSE,"","No pending tasks found."}),
  tasksSummary
)
```

---

```
=IFERROR(FILTER({Activities[Start Date], Activities[Activity], Activities[Assigned], Activities[Project], Activities[Folder]}, Activities[Month]=SummaryMonthQuery), "No pending activities found.")
```

```
=LET(
  activitiesSummary, IFERROR(
    FILTER(
      {
        Activities[Start Date],
        Activities[Activity],
        Activities[Assigned],
        Activities[Project],
        Activities[Folder]
      },
      Activities[Month]=SummaryMonthQuery
    ), "No pending activities found."
  ),
  SORT(activitiesSummary, 1, TRUE)
)
```

```
=TEXT(IF(NOW()<=Activities[Start Date], DATEDIF(NOW(),Activities[Start Date],"D"), DATEDIF(Activities[Start Date],NOW(),"D")), "D \Da\y\s")
```

```
=IF(
  NOW()<Activities[Start Date],
  TEXT(
    DATEDIF(NOW(), Activities[Start Date], "D"),
    "D \D\a\y\s"
  ),
  "0 Days"
)
```

```
=LET(
  tasksSummary, IFERROR(
    FILTER(
      {
        Activities[Priority],
        Activities[Done],
        Activities[Start Date],
        Activities[Time Left],
        Activities[Activity],
        Activities[Location],
        Activities[Category],
        Activities[Folder],
        Activities[Remarks]
      },
      TEXT(Activities[Start Date], "MMMM")=SummaryMonthQuery
    ),
    {FALSE,"","No pending tasks found."}
  ),
  SORT(tasksSummary, 1, TRUE)
)
```

```
=LET(
  tasksSummary, IFERROR(
    FILTER(
      {
        Activities[Priority],
        Activities[Done],
        Activities[Start Date],
        Activities[Time Left],
        Activities[Activity],
        Activities[Location],
        Activities[Category],
        Activities[Folder],
        Activities[Remarks]
      },
      TEXT(Activities[Start Date], "MMMM")=SummaryMonthQuery
    ),
    {FALSE,"","No pending tasks found."}
  ),
  SORT(tasksSummary, 2, TRUE, 1, TRUE)
)
```

# Search function
```
=LET(
  topic, Schedule[Module],
  resourcePerson, Schedule[Resource Person],
  organizer, Schedule[Organizer],
  location, Schedule[Location/Link],
  schedList, SORT(
    FILTER(
      {
        Schedule[Time Start],
        Schedule[Time End],
        topic,
        resourcePerson,
        organizer,
        location
      },
      Schedule[Event Name]=SummaryEventName, Schedule[Date]=SummaryEventDate,
      IF(ISBLANK(SummaryFilterDateTopic), ROW(topic) > 0, ISNUMBER(SEARCH(SummaryFilterDateTopic, topic))),
      IF(ISBLANK(SummaryFilterDateRP), ROW(resourcePerson) > 0, ISNUMBER(SEARCH(SummaryFilterDateRP, resourcePerson))),
      IF(ISBLANK(SummaryFilterDateOrganizer), ROW(organizer) > 0, ISNUMBER(SEARCH(SummaryFilterDateOrganizer, organizer))),
      IF(ISBLANK(SummaryFilterDateLocation), ROW(location) > 0, ISNUMBER(SEARCH(SummaryFilterDateLocation, location)))
    ), 1, TRUE),
  schedList
)
```

```
=LET(
  schedList, SORT(
    FILTER({
        TEXT(Schedule[Date], "YYYY-MM-DD"),
        Schedule[Organizer],
        Schedule[Resource Person],
        Schedule[Mode of Conduct],
        Schedule[Location/Link],
        Schedule[Module],
        Schedule[Status],
        Schedule[Deliverables],
        Schedule[Org Folder]
      },
      Schedule[Event Name]=SummaryEventName,
      IF(ISBLANK(SummaryFilterTopic), ROW(Schedule[Module]) > 0,SEARCH(SummaryFilterTopic, Schedule[Module])),
      IF(ISBLANK(SummaryFilterRP), ROW(Schedule[Resource Person]) > 0,SEARCH(SummaryFilterRP, Schedule[Resource Person])),
      IF(ISBLANK(SummaryFilterOrganizer), ROW(Schedule[Organizer]) > 0,SEARCH(SummaryFilterOrganizer, Schedule[Organizer])),
      IF(ISBLANK(SummaryFilterDate), ROW(Schedule[Date]) > 0,SEARCH(SummaryFilterDate, TEXT(Schedule[Date], "YYYY-MM-DD")))
    ),
    1, TRUE),
  schedList
)
```

```
=LET(
  eventName, Schedule[Event Name],
  eventDate, Schedule[Date],
  organizer, Schedule[Organizer],
  rp, Schedule[Resource Person],
  moc, Schedule[Mode of Conduct],
  location, Schedule[Location/Link],
  topic, Schedule[Module],
  status, Schedule[Status],
  SORT(
    FILTER({
        TEXT(eventDate, "YYYY-MM-DD"),
        organizer,
        rp,
        moc,
        location,
        topic,
        status,
        Schedule[Deliverables],
        Schedule[Org Folder]
      },
      eventName=SummaryEventName,
      IF(ISBLANK(SummaryFilterDate), ROW(eventName) > 0,SEARCH(SummaryFilterDate, TEXT(eventDate, "YYYY-MM-DD"))),
      IF(ISBLANK(SummaryFilterOrganizer), ROW(eventName) > 0,SEARCH(SummaryFilterOrganizer, organizer)),
      IF(ISBLANK(SummaryFilterRP), ROW(eventName) > 0,SEARCH(SummaryFilterRP, rp)),
      IF(ISBLANK(SummaryFilterMOC), ROW(eventName) > 0,SEARCH(moc, SummaryFilterMOC)),
      IF(ISBLANK(SummaryFilterLocation), ROW(eventName) > 0,SEARCH(SummaryFilterLocation, location)),
      IF(ISBLANK(SummaryFilterTopic), ROW(eventName) > 0,SEARCH(SummaryFilterTopic, topic)),
      IF(ISBLANK(SummaryFilterStatus), ROW(eventName) > 0,SEARCH(status, SummaryFilterStatus))
    ),
    1,
    TRUE
  )
)
```
```

```
# Calendar bullshit again
```
=LET(
  tasksSummary, IFERROR(
    FILTER(
      {
        Activities[Priority],
        Activities[Done],
        Activities[Start Date],
        Activities[Time Left],
        Activities[Activity],
        Activities[Location],
        Activities[Category],
        Activities[Folder],
        Activities[Remarks]
      },
      IF(ISBLANK(SummaryMonthQuery),ROW(Activities[Start Date]) > 0,TEXT(Activities[Start Date], "MMMM")=SummaryMonthQuery)
    ),
    {FALSE,"","No pending tasks found."}
  ),
  SORT(tasksSummary, 2, TRUE, 1, TRUE, 4, TRUE)
)
```

# ---

```
=LET(
  calcDate, IFERROR(DATEVALUE(CalendarMonth & " " & A6 & ", " & CalendarYear),),
  isPast, IF(calcDate<=NOW(), CHAR(8203),),
  holidays, IFERROR(FILTER(Holiday[Holiday], CalendarMonth=Holiday[Month], A6=Holiday[Day]),),
  hasHoliday, IF(ISBLANK(holidays),,CHAR(8204)),
  dateActivities, IFERROR(FILTER(
        Activities[Activity],
        INT(Activities[Start Date])<=calcDate,
        calcDate<=INT(
          IF(
            ISBLANK(Activities[End Date]),
            Activities[Start Date],
            Activities[End Date]
          )
        )
      ),),
  IF(
    ISBLANK(calcDate),
    ,
    TEXTJOIN(
      "; " & CHAR(10),
      TRUE,
      holidays,
      dateActivities
    ) & isPast & hasHoliday
  )
)
```

```
=LET(
  calcDate, IFERROR(DATEVALUE(CalendarMonth & " " & A6 & ", " & CalendarYear),),
  isPast, IF(calcDate<=NOW(), CHAR(8203),),
  holidays, IFERROR(FILTER(Holiday[Holiday], CalendarMonth=Holiday[Month], A6=Holiday[Day]),),
  hasHoliday, IF(ISBLANK(holidays),,CHAR(8204)),
  dateActivities, IFERROR(FILTER(
        Activities[Activity],
        INT(Activities[Start Date])<=calcDate,
        calcDate<=INT(
          IF(
            ISBLANK(Activities[End Date]),
            Activities[Start Date],
            Activities[End Date]
          )
        ),
        IF(ISBLANK(CalendarProject), ROW(Activities[Project]) > 0, ISNUMBER(SEARCH(CalendarProject, Activities[Project])))
      ),),
  IF(
    ISBLANK(calcDate),
    ,
    TEXTJOIN(
      "; " & CHAR(10),
      TRUE,
      holidays,
      dateActivities
    ) & isPast & hasHoliday
  )
)
```