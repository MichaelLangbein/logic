(happy X) should return all matches instead of just one


also encode the 'False' status in facts.
  - oh, but is that wise? what if new data comes in that might make a statement true?
    - To handle this, we need a third, None-state!
    - Or, whenever new data comes in, 
      - check if new data conficts with existing
      - reevaluate the false-facts list by doing a forward-pass.

Try to encode the rules for sudoku, and then solve a game.

When information is missing, ask it from user
        when there are no more candidate rules to try and derive a fact, ask.

Can I do a geospatial inference engine?
        One that takes geopandas as facts
        and deduces rules about the columns relations
