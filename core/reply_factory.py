
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    session_key = f'answer_{current_question_id}'
    session[session_key] = answer
    session.modified = True  # Ensure the session is saved after modification

    return True, "Answer recorded successfully."
    # return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    for index, question_info in enumerate(PYTHON_QUESTION_LIST):
        if question_info["question_text"] == current_question_id:
            if index + 1 < len(PYTHON_QUESTION_LIST):
                next_question_info = PYTHON_QUESTION_LIST[index + 1]
                return next_question_info["question_text"], index + 2  # Return the next question and its ID
            else:
                return "No more questions", -1 

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = session.get("correct_answers", [])

    # Calculate score based on correct answers
    score = len(correct_answers)

    # Generate result message
    result_message = f"You answered {score} out of {total_questions} questions correctly.\n\n"

    if score == total_questions:
        result_message += "Congratulations! You answered all questions correctly."
    elif score == 0:
        result_message += "Unfortunately, you did not answer any question correctly."
    else:
        result_message += "Keep it up! You answered some questions correctly."

    return result_message


