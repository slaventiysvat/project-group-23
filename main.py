"""
Персональний помічник - головний модуль для запуску програми
"""

from personal_assistant.cli import PersonalAssistantCLI


def main():
    """Головна функція для запуску персонального помічника"""
    assistant = PersonalAssistantCLI()
    assistant.run()


if __name__ == "__main__":
    main()