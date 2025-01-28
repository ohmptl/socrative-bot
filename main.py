import time, random, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Selenium WebDriver (adjust the driver path if necessary)
driver = webdriver.Chrome()

# Set up the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

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
        time.sleep(2)  # Wait for the teacher to start the quiz
    except Exception as e:
        print(f"Error while joining room: {e}")

# Function to answer a multiple-choice question
def answer_question():
    try:
        # Solve the question using the Gemini API
        answer = solve_question()
        answer = int(answer)

        # Convert answer to index (0-3)
        selected_index = answer-1
        if selected_index < 0 or selected_index >= len(options_elements):
            print("Invalid answer index")
            selected_index = random.randint(0, 3)  # Fallback to random if invalid index

        # Locate options
        options_elements = driver.find_elements(By.CLASS_NAME, "answerContentWrapper")

        # Select the option
        options_elements[selected_index].click()
        print("Answered a question.")
        time.sleep(5)

        # Click the submit button
        submit_button = driver.find_element(By.ID, "submit-button")
        submit_button.click()
        time.sleep(2)  # Short wait after submission

    except Exception as e:
        print(f"Error: {e}")

def solve_question():
    try:
        # Read the question using Selenium
        question_element = driver.find_element(By.CLASS_NAME, 'question-text')
        question_text = question_element.text

        # Assuming the options are within elements with a common CSS class
        option_elements = driver.find_elements(By.CLASS_NAME, 'mc-answer-option-text')
        options = [option.text for option in option_elements[:4]]  # Get up to 4 options

        # Prepare the payload for the Gemini API
        payload = {
            'prompt' : f"Answer the following multiple-choice question by providing *only* the number corresponding to the correct answer.  Do not provide any other text or explanation.",
            'question': question_text,
            'options': options,
        }

        input_text = (
            f"{payload['prompt']}\n"
            f"Question: {payload['question']}\n"
            f"Options:\n"
        )

        for option in payload['options']:
            input_text += f"  - {option}\n"

        response = model.generate_content(input_text)

        question_number = response.text
        print(input_text)
        print(f"Gemini suggests: {question_number}")
        return question_number
    except Exception as e:
        print(f"Error querying ChatGPT: {e}")
        return random.choice([1, 2, 3, 4])

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
                answer_question()
            else:
                print("No new question yet. Retrying...")
            
            time.sleep(os.getenv('POLLING_INTERVAL'))  # Check frequently (adjust as needed)
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