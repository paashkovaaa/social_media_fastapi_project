from better_profanity import profanity

profanity.load_censor_words()


def moderate_text(text: str):
    if profanity.contains_profanity(text):
        result = {
            "is_approved": False,
        }
    else:
        result = {
            "is_approved": True,
        }
    return result
