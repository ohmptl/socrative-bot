# Scheduling the Script

You can schedule the script to run automatically on **Tuesdays and Thursdays at 8:30 AM** and stop at **9:45 AM** using the following methods:

## Windows: Using Task Scheduler

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and hit Enter.

2. **Create a Basic Task**:
   - Click on **Create Basic Task** from the right-hand menu.
   - Name the task (e.g., "Run Socrative Bot") and provide a description.

3. **Set the Trigger**:
   - Choose **Weekly**.
   - Select **Tuesday** and **Thursday** as the days to run.

4. **Set the Start Time**:
   - Set the time to **8:30 AM**.

5. **Set the Action**:
   - Choose **Start a Program**.
   - In the **Program/script** field, browse to your Python executable (e.g., `C:\Python39\python.exe`).
   - In the **Add arguments** field, enter the path to your script (e.g., `C:\path\to\script.py`).

6. **Finish and Save**:
   - Complete the wizard and click **Finish**.

---

## Mac: Using Cron

1. **Open the Terminal**:
   - Open a terminal window from your Applications or by pressing `Cmd + Space`, typing `Terminal`, and hitting Enter.

2. **Edit the Crontab**:
   - Type `crontab -e` to edit the crontab.

3. **Add the Schedule**:
   - Add the following line to schedule the script:
     ```bash
     30 8 * * 2,4 /usr/bin/python3 /path/to/your/script.py
     ```
   - This runs the script every Tuesday and Thursday at 8:30 AM.

4. **Save and Exit**:
   - Save the file and exit the editor.

5. **Automatically Stop the Script**:
   - Use `pkill` to terminate the Python process at 9:45 AM:
     ```bash
     45 9 * * 2,4 pkill -f /path/to/your/script.py
     ```

---

## Testing the Schedule

1. Run the script manually to ensure it works:
   ```bash
   python /path/to/your/script.py
