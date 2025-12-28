from django.test import TestCase

# فعلاً تستی نداریم
# این فایل فقط برای جلوگیری از ارور است

class SimpleTest(TestCase):
    def test_basic(self):
        self.assertEqual(1 + 1, 2)
