import os.path
import datetime
import numpy as np
import requests as rs
import csv
import os
from pytz import timezone


def get_values(sheet):
  sheet_url = f"https://docs.google.com/spreadsheets/d/1wHpZ6i1mtEL-mifPPIYOR3WpaCfBmuKdn6sWLnImIP0/gviz/tq?tqx=out:csv&sheet={sheet}"
  res = rs.get(url=sheet_url)
  open('matches.csv', 'wb').write(res.content)

  if sheet == "Matches":
    result = np.empty((0,6))
  else:
    result = np.empty((0,4))
    
  with open("matches.csv", "r") as f:
    reader = csv.reader(f)
    if sheet == "Matches":
      next(reader)
    for row in reader:
      result = np.vstack([result, row])
 
  return result


if __name__ == "__main__":
  searching = True
  current_row = 0
  current_datetime = datetime.datetime.now(timezone('US/Eastern'))
  current_month = current_datetime.strftime("%m").lstrip('0')
  current_day = current_datetime.strftime("%d").lstrip('0')
  current_hour = int(current_datetime.strftime("%H"))
  current_minute = int(current_datetime.strftime("%M"))
  current_time_in_minutes = (current_hour*60) + current_minute

  valid_matches = np.empty((0,6))
  recent_matches = np.empty((0,6))
  while searching:
    values = get_values("Matches")
    date = values[current_row][5].split("/")
    hour = int(values[current_row][4].split(":")[0])%12
    minute = values[current_row][4].split(":")[1]
    minute = int(minute.split(" ")[0])
    am_or_pm = values[current_row][4].split(" ")[1]
    if am_or_pm == "pm":
      hour += 12
    time_in_minutes = (hour*60) + minute

    if date[0] == current_month and date[1] == current_day:
      if valid_matches.size == 0:
        if time_in_minutes >= current_time_in_minutes:
          valid_matches = np.vstack([values[current_row], valid_matches])
      else:
        match_hour = int(valid_matches[0][4].split(":")[0])%12
        match_am_or_pm = values[current_row][4].split(" ")[1]
        match_minutes = valid_matches[0][4].split(":")[1]
        match_minutes = int(match_minutes.split(" ")[0])
        if match_am_or_pm == "pm":
          match_hour += 12
        match_time_in_minutes = (match_hour*60) + match_minutes
        if time_in_minutes == match_time_in_minutes:
          valid_matches = np.vstack([values[current_row], valid_matches])

      if date[0] == current_month and date[1] == current_day and time_in_minutes < current_time_in_minutes and time_in_minutes > current_time_in_minutes-15 and recent_matches.size == 0:
        recent_matches = np.vstack([values[current_row], recent_matches])
      elif recent_matches.size > 0:
        if date[0] == current_month and date[1] == current_day and hour == int(recent_matches[0][4].split(":")[0])%12 and minute == int(recent_matches[0][4].split(":")[1].split(" ")[0]):
          recent_matches = np.vstack([values[current_row], recent_matches])
    elif date[0] < current_month or (date[0] == current_month and date[1] < current_day):
      searching = False

    current_row += 1

  chosen_match = 0
  valid_matches = np.vstack([valid_matches, recent_matches])
  if(valid_matches.size > 0 or recent_matches.size > 0):
    if(valid_matches.size > 0):
      if valid_matches.shape[0] > 1:
        prompt_string = "Multiple matches found, please enter a number:"
        recent = False
        for i in range(0, valid_matches.shape[0]):
          if valid_matches.shape[0] - recent_matches.shape[0] <= i and not recent:
            prompt_string += "\nrecently started matches:"
            recent = True
          prompt_string += f"\n{i+1}: {valid_matches[i][2]} vs {valid_matches[i][3]}"
        print(prompt_string)
        chosen_match = int(input())-1


      with open("extra.txt", "w") as f:
        f.write(f"Tier {valid_matches[chosen_match][1]}\nWeek {valid_matches[chosen_match][0]}")

      with open("left_name.txt", "w") as f:
        f.write(valid_matches[chosen_match][2])

      with open("right_name.txt", "w") as f:
        f.write(valid_matches[chosen_match][3]) 

      searching = True
      current_row = 1
      left_pronoun = ""
      left_score = ""
      right_pronoun = ""
      right_score = ""
      values = get_values("Stats")
      for i in range(0, values.shape[0]):
        stats_name = values[i][0].upper()
        left_match_name = valid_matches[chosen_match][2].upper()
        right_match_name = valid_matches[chosen_match][3].upper()
        if stats_name == left_match_name:
          left_pronoun = values[i][3]
          left_score = f"{values[i][1]}-{values[i][2]}"
        if stats_name == right_match_name:
          right_pronoun = values[i][3]
          right_score = f"{values[i][1]}-{values[i][2]}"

      with open("left_pronoun.txt", "w") as f:
        f.write(left_pronoun)

      with open("left_score.txt", "w") as f:
        f.write(left_score)

      with open("right_pronoun.txt", "w") as f:
        f.write(right_pronoun)

      with open("right_score.txt", "w") as f:
        f.write(right_score)
  else:
    print("No matches found. If you think there should be, @tufwfo on discord immediately. Press enter to close")
    input()

    

  os.remove("matches.csv")