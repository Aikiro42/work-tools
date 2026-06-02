```
=ARRAYFORMULA(LET(
  year, INT(TEXT(Conducts2025[Date],"YYYY")),
  offset, IFS(
    WEEKDAY(DATE(year,1,1))<6,-1,
    WEEKDAY(DATE(year,1,1))>=6,0
  ),
  IF(ISBLANK(Conducts2025[Date]), , "Week " & WEEKNUM(Conducts2025[Date], 15) + offset)
))
```