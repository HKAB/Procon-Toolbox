# Procon Toolbox
A toolbox for procon contest

Whenever a match about to start, do this in bot.py:
- Update Token (Server supply)
- Update TEAMID, MATCHID (Get from click the Get match button in myindex.html)

Because the time for each turn is varied ~the code is fuking burden~, we sent 1 request/second to check turn, so Update map is unreliable (Sometime **Too many requests** is throw, but it's trade-off, we can have more time to run algorithm :smiley:)
