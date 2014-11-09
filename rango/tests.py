from django.test import TestCase
from rango.models import Category, Page
from django.core.urlresolvers import reverse
from django.utils import timezone


class CategoryModelTests(TestCase):
    def test_views_are_not_negative(self):
        """
        test_views_are_not_negative should return True for categories where
        views is >= 0
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertGreaterEqual(cat.views, 0)

    def test_slug_string_creation(self):
        """
        Check that slug is created from Category.name, spaces replaced with
        dashes, all lowercase, i.e.:
        "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, "random-category-string")


class PageModelTests(TestCase):
    def setUp(self):
        cat = Category(name='Testing Page model')
        cat.save()

        page = Page(category=cat, title="Test page", url="http://test.tt.st")
        page.save()

    def test_visit_times_are_not_in_future(self):
        """
        Check that first_visit and last_visit are not set to future
        """
        page = Page.objects.get(title="Test page")

        page_track_url = "{0}?page_id={1}".format(reverse('goto'), page.id)
        self.client.get(page_track_url)

        page = Page.objects.get(title="Test page")
        now = timezone.now()

        self.assertLessEqual(page.last_visit, now)
        self.assertLessEqual(page.first_visit, now)

    def test_last_visit_is_not_before_first_after_two_views(self):
        """
        Check that last_visit >= first_visit
        """
        page = Page.objects.get(title="Test page")
        page_track_url = "{0}?page_id={1}".format(reverse('goto'), page.id)

        # First view of Page (have to refresh Page instance from DB)
        self.client.get(page_track_url)
        page = Page.objects.get(id=page.id)

        self.assertLessEqual(page.first_visit, page.last_visit)

        # Second view of Page (have to refresh Page instance from DB)
        self.client.get(page_track_url)
        page = Page.objects.get(id=page.id)
        self.assertLessEqual(page.first_visit, page.last_visit)



# Helper method for Category tests
def add_cat(name, views=0, likes=0):
    cat = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return cat


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exeist, there is a meaningful message.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat('test1', 1, 1)
        add_cat('test-2')
        add_cat('test_3', 1, 1)
        add_cat('test long Johnson', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test long Johnson')

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)
