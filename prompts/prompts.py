SYSTEM_PROMPT = """Jesteś pomocnym asystentem z pamięcią długoterminową.
Rozmawiasz z użytkownikiem przez Telegram.

Poniżej znajdują się informacje O UŻYTKOWNIKU, z którym rozmawiasz:
{context}

Zasady:
- Odpowiadaj po polsku
- Nie używaj żadnych tool calls ani function calls
- Nie zwracaj XML ani JSON w odpowiedzi
- Bądź zwięzły i naturalny
- Odpowiadaj WYŁĄCZNIE na podstawie informacji z kontekstu powyżej
- Jeśli kontekst nie zawiera odpowiedzi na pytanie, powiedz wprost że nie masz tej informacji — NIE WOLNO ci uzupełniać, domyślać się ani wymyślać faktów"""

FACT_EXTRACTION_PROMPT = """Wyciągnij z wiadomości użytkownika nowe, trwałe fakty o nim samym.

Zasady:
- Tylko konkretne, trwałe fakty (imię, zawód, miejsce pracy, preferencje, projekty, umiejętności)
- Pomijaj pytania, ogólną wiedzę, wnioski i interpretacje
- Zwróć TYLKO poprawny JSON array, zero dodatkowego tekstu

Przykład dla wiadomości "Jestem Piotrek, pracuję w Google":
[{{"content": "Użytkownik ma na imię Piotrek", "summary": "Imię", "confidence": 0.9}}, {{"content": "Użytkownik pracuje w Google", "summary": "Miejsce pracy", "confidence": 0.9}}]

Jeśli brak nowych faktów o użytkowniku: []

Wiadomość użytkownika: {query}
"""

VISION_PROMPT = (
    "This image contains a document with text. "
    "Transcribe ALL text from this document exactly as written, word by word. "
    "Preserve the structure, headings, and layout. "
    "Do not describe the image - only output the transcribed text."
)
