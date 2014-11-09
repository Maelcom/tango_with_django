from django.test import TestCase
from rango.models import Category
from django.core.urlresolvers import reverse


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
