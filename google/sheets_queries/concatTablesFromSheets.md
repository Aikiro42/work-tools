```
=LET(
	  DATA, FILTER(
		{Schedule[Registration Sheet], Schedule[Registration Table]},
		Schedule[Event Name]=SummaryEventName,
		Schedule[Date]=SummaryEventDate
	  ),
	  FILES, INDEX(DATA, , 1),
	  TABLES, INDEX(DATA, , 2),
	  
	  REDUCE(TOCOL(,1), SEQUENCE(ROWS(FILES)), LAMBDA(acc, i, 
		VSTACK(acc, IMPORTRANGE(INDEX(FILES, i), INDEX(TABLES, i)))
	  ))
	)
```