# python_final_ucl_and_wc_data_app
A PyQt5 desktop application for exploring and managing statistics from the two biggest football tournaments: the UEFA Champions League and the FIFA World Cup.

# what you can do in the app
- view UEFA Champions League statistics from 1992–2025
- view FIFA World Cup statistics
- see the winner, top scorer, top assistent, and best coach for each tournament
- add new records to the database
- update existing records
- delete records
- browse all stored statistics
- switch between the Champions League and World Cup databases
- enjoy separate background music for the main menu and the Champions League page
- mute or unmute the music at any time

# application windows
- **Main Menu**
  - background music is played
  - switch between available songs
  - mute or unmute the music
  - open the UEFA Champions League page
  - open the FIFA World Cup page
  - exit the application
- **UEFA Champions League Window**
  - displays Champions League statistics
  - allows full CRUD operations (Create, Read, Update, Delete)
  - has its own dedicated Champions League theme song
  - return to the main menu at any time
- **FIFA World Cup Window**
  - displays World Cup statistics
  - allows full CRUD operations (Create, Read, Update, Delete)
  - return to the main menu at any time

# Modules Used
- PyQt5
- sqlite3
- os
- sys

## How to Run
```bash
git clone https://github.com/Nikakurashvili/python_final_ucl_and_wc_data_app.git
cd python_final_ucl_and_wc_data_app
python main.py
```
