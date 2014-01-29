Genetic-algorithms
==================
This program based on a genetic algorithm is aimed on finding the best configuration of knights on a chess desk which follows these simple rules:
- The more knights - the better
- The more of them can capture each other - the worse

The genetic algorithm lying in the base of this project can also be applied to different tasks.

To launch the program, execute _Launch.py_ with Python 3 interpreter or execute _Launch.bat_ if you are using Windows or _Launch.sh_ if you are using Linux.

**TODO:**
- Make individuals differentiate
- Add some description and documentation
- Breeding display to see which genes came from whom
  * Some kind of genealogical tree
- Settings file (?)
- Think of a better `__init__()` for Population
- Add loading placeholders in GUI
- Implement saving the progress of evolution (partially done)
- Think about passing all the parametres to the individuals (extra memory)
- Fitness_multiplier?

- CHECK ALL THE CODE FOR REFERENCE TYPE MISTAKES
- Optimize the number of fitness function calls
- Correct `choose_parent()`. Something is definetely wrong with it
  * Maybe force breeding of alpha individuals?
- Some analytics:
  * Count the percent of mutated nextgens on the list
- Implement printing from pool
- Add tooltips for settings
- Try using canvas instead of frames for improved performance on linux
