LANGUAGE_MESSAGES = {
    "en": {
        "consent": "Please agree to the data practices to continue using ScoutOS.",
    },
    "es": {
        "consent": "Por favor, acepte las prácticas de datos para continuar usando ScoutOS.",
    },
}

def get_consent_message(lang: str = "en"):
    return LANGUAGE_MESSAGES.get(lang, LANGUAGE_MESSAGES["en"])["consent"]
