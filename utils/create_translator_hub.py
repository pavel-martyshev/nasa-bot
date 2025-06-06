from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    """
    Initialize and return a TranslatorHub with Russian and English translators.

    Returns:
        TranslatorHub: Configured translation hub with locale mappings and Fluent translators.
    """
    translator_hub = TranslatorHub(
        {"ru": ("ru", "en"), "en": ("en", "ru")},
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(locale="ru-RU", filenames=["locales/ru/LC_MESSAGES/txt.ftl"]),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(locale="en-US", filenames=["locales/en/LC_MESSAGES/txt.ftl"]),
            ),
        ],
    )
    return translator_hub
