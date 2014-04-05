# coding=utf8

import unittest

from slugify import Slugify
from slugify import slugify, slugify_unicode
from slugify import slugify_ru, slugify_de
from slugify import get_slugify


class SlugifyTestCase(unittest.TestCase):

    def test_slugify_english(self):
        self.assertEqual(slugify('This % is a test ---'), 'This-is-a-test')
        self.assertEqual(slugify('_this_is_a__test___'), 'this-is-a-test')
        self.assertEqual(slugify('- - -This -- is a ## test ---'), 'This-is-a-test')

    def test_slugify_umlaut(self):
        self.assertEqual(slugify('kožušček'), 'kozuscek',)
        self.assertEqual(slugify('C\'est déjà l\'été.'), 'Cest-deja-lete')
        self.assertEqual(slugify('jaja---lol-méméméoo--a'), 'jaja-lol-mememeoo-a')
        self.assertEqual(slugify('Nín hǎo. Wǒ shì zhōng guó rén'), 'Nin-hao-Wo-shi-zhong-guo-ren')
        self.assertEqual(slugify('Programmes de publicité - Solutions d\'entreprise'), 'Programmes-de-publicite-Solutions-dentreprise')

    def test_slugify_chinese(self):
        self.assertEqual(slugify('北亰'), 'Bei-Jing')

    def test_slugify_russian(self):
        self.assertEqual(slugify('Компьютер'), 'Kompiuter')
        self.assertEqual(slugify('Транслитерирует и русский'), 'Transliteriruet-i-russkii')
        self.assertEqual(slugify('ёжик из щуки сварил уху'), 'iozhik-iz-shchuki-svaril-ukhu')
        self.assertEqual(slugify('Ах, Юля-Юля'), 'Akh-Iulia-Iulia')

    def test_slugify_ru(self):
        self.assertEqual(slugify_ru('Компьютер'), 'Komputer')
        self.assertEqual(slugify_ru('Транслитерирует и русский'), 'Transliteriryet-i-rysskii')
        self.assertEqual(slugify_ru('ёжик из щуки сварил уху'), 'ejik-iz-schyki-svaril-yhy')
        self.assertEqual(slugify_ru('Ах, Юля-Юля'), 'Ah-Ulya-Ulya')

    def test_slugify_unicode(self):
        self.assertEqual(slugify_unicode('-=Слово по-русски=-'), u'Слово-по-русски')
        self.assertEqual(slugify_unicode('слово_по_русски'), u'слово-по-русски')


class UpperTestCase(unittest.TestCase):
    def test_full_upper(self):
        self.assertEqual(slugify_ru('ЯНДЕКС'), 'YANDEKS')

    def test_camel_word(self):
        self.assertEqual(slugify_ru('Яндекс'), 'Yandeks')
        self.assertEqual(slugify_ru('ВВЕРХ Яндекс'), 'VVERH-Yandeks')
        self.assertEqual(slugify_ru('Яндекс ВВЕРХ'), 'Yandeks-VVERH')

    def test_part_of_word(self):
        self.assertEqual(slugify_de('ÜBERslugify'), 'UEBERslugify')
        self.assertEqual(slugify_de('ÜBERslugifÜ AUF'), 'UEBERslugifUE-AUF')

    def test_at_start_of_sentence(self):
        self.assertEqual(slugify_ru('Я пошёл'), 'Ya-poshel')
        self.assertEqual(slugify_ru('Я Пошёл'), 'Ya-Poshel')
        self.assertEqual(slugify_ru('Я ПОШёл'), 'YA-POSHel')
        self.assertEqual(slugify_ru('Я ПОШЁЛ. Я Пошел'), 'YA-POSHEL-Ya-Poshel')

    def test_at_end_of_sentence(self):
        self.assertEqual(slugify_ru('пошЁЛ Я'), 'poshEL-YA')
        self.assertEqual(slugify_ru('пошЁЛ Я.'), 'poshEL-YA')
        self.assertEqual(slugify_ru('пошёл Я. ПОШЁЛ'), 'poshel-Ya-POSHEL')

    def test_one_letter_words(self):
        self.assertEqual(slugify_ru('Э Я Г Д Е ?'), 'E-Ya-G-D-E')
        self.assertEqual(slugify_ru('ВВЕРХ Э Я Г Д Е ?'), 'VVERH-E-YA-G-D-E')

    def test_abbreviation(self):
        self.assertEqual(slugify_ru('ВВЕРХ Я.Б.Ч'), 'VVERH-Ya-B-Ch')


class PretranslateTestCase(unittest.TestCase):

    def test_pretranslate(self):
        EMOJI_TRANSLATION= {
            u'ʘ‿ʘ': u'smiling',
            u'ಠ_ಠ': u'disapproval',
            u'♥‿♥': u'enamored',
            u'♥': u'love',

            u'(c)': u'copyright',
            u'©': u'copyright',
        }
        slugify_emoji = Slugify(pretranslate=EMOJI_TRANSLATION)
        self.assertEqual(slugify_emoji(u'ʘ‿ʘ'), u'smiling')
        self.assertEqual(slugify_emoji(u'ಠ_ಠ'), u'disapproval')
        self.assertEqual(slugify_emoji(u'(c)'), u'copyright')
        self.assertEqual(slugify_emoji(u'©'), u'copyright')

    def test_wrong_argument_type(self):
        self.assertRaises(ValueError, lambda: Slugify(pretranslate={1, 2}))


class TruncateTestCase(unittest.TestCase):

    def test_truncate(self):
        self.assertEqual(slugify('one two three four', max_length=7), 'one-two')
        self.assertEqual(slugify('one two three four', max_length=8), 'one-two')
        self.assertEqual(slugify('one two three four', max_length=12), 'one-two-four')
        self.assertEqual(slugify('one two three four', max_length=13), 'one-two-three')
        self.assertEqual(slugify('one two three four', max_length=14), 'one-two-three')

    def test_truncate_on_empty(self):
        self.assertEqual(slugify('', max_length=10), '')

    def test_truncate_short(self):
        self.assertEqual(slugify('dlinnoeslovo', max_length=7), 'dlinnoe')
        self.assertEqual(slugify('dlinnoeslovo и ещё слово', max_length=11), 'dlinnoeslov')

    def test_truncate_long(self):
        self.assertEqual(slugify('шшш щщщ слово', max_length=11), 'shshsh')
        self.assertEqual(slugify('шшш щщщ слово', max_length=12), 'shshsh-slovo')
        self.assertEqual(slugify('шшш щщщ слово', max_length=18), 'shshsh-slovo')
        self.assertEqual(slugify('шшш щщщ слово', max_length=19), 'shshsh-shchshchshch')
        self.assertEqual(slugify('шшш щщщ слово', max_length=24), 'shshsh-shchshchshch')
        self.assertEqual(slugify('шшш щщщ слово', max_length=25), 'shshsh-shchshchshch-slovo')

    def test_truncate_unwanted(self):
        self.assertEqual(slugify('...one...two...three...four...', max_length=12), 'one-two-four')

    def test_truncate_long_separator(self):
        self.assertEqual(slugify('one two three four', max_length=14, separator='...'), 'one...two')


class PretranslateTestCase(unittest.TestCase):

    def test_pretranslate(self):
        ALT_TRANSLATION= {
            u'ʘ‿ʘ': u'smiling',
            u'ಠ_ಠ': u'disapproval',
            u'♥‿♥': u'enamored',
            u'♥': u'love',

            u'(c)': u'copyright',
            u'©': u'copyright',
        }
        slugify_emoji = Slugify(pretranslate=ALT_TRANSLATION)
        self.assertEqual(slugify_emoji(u'ʘ‿ʘ'), u'smiling')
        self.assertEqual(slugify_emoji(u'ಠ_ಠ'), u'disapproval')
        self.assertEqual(slugify_emoji(u'(c)'), u'copyright')
        self.assertEqual(slugify_emoji(u'©'), u'copyright')

    def test_wrong_argument_type(self):
        self.assertRaises(ValueError, lambda: Slugify(pretranslate={1, 2}))


class OtherTestCase(unittest.TestCase):

    def test_prevent_double_translation(self):
        slugify = Slugify(pretranslate={'s': 'ss'})
        self.assertEqual(slugify('BOOST'), 'BOOSST')

    def test_capitalize(self):
        self.assertEqual(slugify('this Is A test', capitalize=True), 'This-Is-A-test')

    def test_capitalize_on_empty(self):
        self.assertEqual(slugify('', capitalize=True), '')

    def test_safe_chars(self):
        filename_slugify = Slugify(safe_chars='-_.', separator='_')
        self.assertEqual(filename_slugify(u'Дrаft №2.txt'), u'Draft_2.txt')


class DeprecationTestCase(unittest.TestCase):

    def test_deprecated_get_slugify(self):
        import warnings

        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter('once')

            slugify = get_slugify()
            self.assertEqual(slugify('This % is a test ---'), 'This-is-a-test')
            self.assertIn("'slugify.get_slugify' is deprecated", str(warning[-1].message))


if __name__ == '__main__':
    unittest.main()