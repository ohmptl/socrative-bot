import time, random, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Selenium WebDriver (adjust the driver path if necessary)
driver = webdriver.Chrome()

# Function to log in and join the quiz
def join_socrative_quiz(room_name, student_name):
    driver.get("https://b.socrative.com/login/student/")
    time.sleep(2)  # Allow the page to load

    # Enter the room name
    try:
        room_name_input = driver.find_element(By.ID, "studentRoomName")
        room_name_input.send_keys(room_name)
        room_name_input.send_keys(Keys.RETURN)
        print(f"Joined room: {room_name}")
        time.sleep(2)  # Wait for the next step

        # Enter the student name
        student_name_input = driver.find_element(By.ID, "student-name-input")
        student_name_input.send_keys(student_name)
        student_name_input.send_keys(Keys.RETURN)
        print(f"Entered student name: {student_name}")
        time.sleep(5)  # Wait for the teacher to start the quiz
    except Exception as e:
        print(f"Error while joining room: {e}")

# Function to answer a multiple-choice question
def answer_question():
    try:
        # Locate all available options for the current question
        options = driver.find_elements(By.CLASS_NAME, "answerContentWrapper")
        if options:
            # Choose a random option (0 to 3 for 4 choices)
            selected_option = random.choice(options)
            selected_option.click()
            print("Answered a question.")

            # Click the submit button
            submit_button = driver.find_element(By.ID, "submit-button")
            submit_button.click()
            time.sleep(2)  # Short wait after submission
        else:
            print("No options found. Waiting for the next question.")
    except Exception as e:
        print(f"Error: {e}")

# Function to check if rejoining the room is required
def check_rejoin(room_name, student_name):
    try:
        # Check for room name field
        room_name_field = driver.find_element(By.ID, "studentRoomName")
        if room_name_field.is_displayed():
            print("Room name field detected. Rejoining...")
            join_socrative_quiz(room_name, student_name)
            return True
    except Exception:
        pass

    try:
        # Check for student name field
        student_name_field = driver.find_element(By.ID, "student-name-input")
        if student_name_field.is_displayed():
            print("Student name field detected. Re-entering...")
            join_socrative_quiz(room_name, student_name)
            return True
    except Exception:
        pass

    return False

# Function to monitor for new questions and answer them
def monitor_and_answer(room_name, student_name):
    last_question_text = ""
    while True:
        try:
            # Check if rejoining is required
            if check_rejoin(room_name, student_name):
                continue

            # Check if there's a new question
            question_element = driver.find_element(By.CLASS_NAME, "question-text")
            current_question_text = question_element.text

            # If the question has changed, answer it
            if current_question_text != last_question_text:
                print(f"New question detected: {current_question_text}")
                last_question_text = current_question_text
                time.sleep(5)
                answer_question()
            else:
                print("No new question yet. Retrying...")
            
            time.sleep(5)  # Check frequently (adjust as needed)
        except Exception as e:
            print(f"Waiting for the next question or quiz ended. Error: {e}")
            time.sleep(5)

# Main function to run the bot
def run_quiz_bot(room_name, student_name):
    try:
        join_socrative_quiz(room_name, student_name)
        monitor_and_answer(room_name, student_name)
    except KeyboardInterrupt:
        print("Quiz bot stopped.")
    finally:
        driver.quit()

# Run the bot with your Socrative room name and student name
if __name__ == "__main__":
    room_name = os.getenv("ROOM_NAME")  # Get the room name from the environment variable
    student_name = os.getenv("STUDENT_NAME")  # Get the student name from the environment variable
    run_quiz_bot(room_name, student_name)