import time, random, os, logging, json, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
log_file = os.getenv('LOG_FILE')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info(f"Joined room: {room_name}")
        time.sleep(2)  # Wait for the next step

        # Enter the student name
        student_name_input = driver.find_element(By.ID, "student-name-input")
        student_name_input.send_keys(student_name)
        student_name_input.send_keys(Keys.RETURN)
        logging.info(f"Entered student name: {student_name}")
        time.sleep(2)  # Wait for the teacher to start the quiz
    except Exception as e:
        print(f"Error while joining room: {e}")

# Function to answer a multiple-choice question
def answer_question():
    try:
        # Solve the question using the Gemini API
        answer = solve_question()
        answer = int(answer)

        # Locate options
        options_elements = driver.find_elements(By.CLASS_NAME, "answerContentWrapper")

        # Convert answer to index (0-3)
        selected_index = answer-1
        if selected_index < 0 or selected_index >= len(options_elements):
            logging.info("Invalid answer index")
            selected_index = random.randint(0, 3)  # Fallback to random if invalid index

        # Select the option
        options_elements[selected_index].click()
        logging.info(f"Answered choice {selected_index+1}.")
        time.sleep(5)

        # Click the submit button
        submit_button = driver.find_element(By.ID, "submit-button")
        submit_button.click()
        time.sleep(2)  # Short wait after submission

    except Exception as e:
        logging.error(f"Error: {e}")

# Function to solve the question using Gemini API
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
        logging.info(input_text)
        logging.info(f"Gemini suggests: {question_number}")
        return question_number
    except Exception as e:
        logging.error(f"Error querying Gemini: {e}")
        return random.choice([1, 2, 3, 4])

# Function to check if rejoining the room is required
def check_rejoin(room_name, student_name):
    try:
        # Check for room name field
        room_name_field = driver.find_element(By.ID, "studentRoomName")
        if room_name_field.is_displayed():
            logging.info("Room name field detected. Rejoining...")
            join_socrative_quiz(room_name, student_name)
            return True
    except Exception:
        pass

    try:
        # Check for student name field
        student_name_field = driver.find_element(By.ID, "student-name-input")
        if student_name_field.is_displayed():
            logging.info("Student name field detected. Re-entering...")
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
                logging.info(f"New question detected")
                last_question_text = current_question_text
                answer_question()
            else:
                pass
            
            time.sleep(os.getenv('POLLING_INTERVAL'))  # Check frequently (adjust as needed)
        except Exception as e:
            print(f"Waiting for the next question or quiz ended.")
            time.sleep(5)

# Function to generate an HTML file with the quiz questions
def generate_html(questions):
    questions_html = ''
    for iQ, question_data in enumerate(questions):
        answers_html = ''
        if not question_data.get('answers'):
            answers_html = '<i>This question does not have alternatives</i>'
        else:
            for iA, answer in enumerate(question_data['answers']):
                answers_html += f'<alt name="{chr(65 + iA)}">{answer["text"]}</alt>'
        answers_html = f'<alternatives>{answers_html}</alternatives>'
        questions_html += f'''
            <question>
                <data>Question {iQ + 1}</data>
                <description>{question_data["question_text"]}</description>
                {answers_html}
            </question>
        '''
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quiz Questions</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            question {{
                display: block;
                margin-bottom: 20px;
            }}
            data {{
                font-weight: bold;
            }}
            description {{
                display: block;
                margin: 10px 0;
            }}
            alternatives {{
                margin-left: 20px;
            }}
            alt {{
                display: block;
            }}
        </style>
    </head>
    <body>
        <h1>Quiz Questions</h1>
        <div id="questions-container">
            {questions_html}
        </div>
    </body>
    </html>
    '''
    return html_content

# Function to extract data similar to the provided JavaScript function
def extract_data():
    try:
        room_code = os.getenv('ROOM_NAME')
        url_get_activity_id = f"https://api.socrative.com/rooms/api/current-activity/{room_code}"
        
        response = requests.get(url_get_activity_id)
        response.raise_for_status()
        data = response.json()
        
        quiz_code = data['activity_id']
        link_to_extract = f"https://teacher.socrative.com/quizzes/{quiz_code}/student?room={room_code}"
        
        # Callback functionality
        logging.info(f"Extracted link: {link_to_extract}")

        # Open a new tab
        driver.execute_script("window.open('');")
        
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        
        # Navigate to the link
        driver.get(link_to_extract)
        
        # Wait for the page to load and extract the JSON content
        time.sleep(5)  # Adjust the sleep time as needed
        json_data = driver.find_element(By.TAG_NAME, 'pre').text
        
        # Generate HTML content
        questions = json.loads(json_data)['questions']
        html_content = generate_html(questions)
        
        # Save HTML content to a file
        with open('socrative-bot/quiz.html', 'w') as html_file:
            html_file.write(html_content)
        
        # Close the new tab and switch back to the original tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        logging.info("Data extracted successfully, view quiz.html for the extracted data.")

        return
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        return None

# Main function to run the bot
def run_quiz_bot(room_name, student_name):
    try:
        join_socrative_quiz(room_name, student_name)
        extract_data()
        monitor_and_answer(room_name, student_name)
    except KeyboardInterrupt:
        logging.info("Quiz bot stopped.")
    finally:
        driver.quit()

# Run the bot with your Socrative room name and student name
if __name__ == "__main__":
    room_name = os.getenv("ROOM_NAME")  # Get the room name from the environment variable
    student_name = os.getenv("STUDENT_NAME")  # Get the student name from the environment variable
    run_quiz_bot(room_name, student_name)