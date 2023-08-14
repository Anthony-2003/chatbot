import re
import random
from responses import responses

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty +=1

    percentage = float(message_certainty) / float (len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        probability = message_probability(message, list_of_words, single_response, required_words)
        if probability > 0:
            highest_prob[bot_response] = probability

    for question, possible_responses in responses.items():
        for variant in possible_responses:
            keyword_list = re.split(r'\s|[,:;.?!-_]\s*', variant.lower())
            response(question, keyword_list, single_response=True)

    best_match = max(highest_prob, key=highest_prob.get, default=None)

    if best_match is None:
        return unknown()

    return best_match


def unknown():
    response = ['puedes decirlo de nuevo?', 'No estoy seguro de lo quieres'][random.randrange(2)]
    return response

while True:
    print("Bot: " + get_response(input('You: ')))