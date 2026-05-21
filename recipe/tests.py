from django.test import TestCase
from django.urls import reverse

from .models import Category, Recipe


class MainViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Soups')
        self.url = reverse('main')

    def _create_recipe(self, title):
        return Recipe.objects.create(
            title=title,
            description='Description',
            instructions='Instructions',
            ingredients='Ingredients',
            category=self.category,
        )

    def test_main_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_main_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main.html')

    def test_main_view_context_contains_recipes(self):
        self._create_recipe('Borscht')
        response = self.client.get(self.url)
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 1)

    def test_main_view_shows_only_latest_five_recipes(self):
        for index in range(6):
            self._create_recipe(f'Recipe {index}')

        response = self.client.get(self.url)
        recipes = list(response.context['recipes'])

        self.assertEqual(len(recipes), 5)
        self.assertNotIn('Recipe 0', [recipe.title for recipe in recipes])
        self.assertIn('Recipe 5', [recipe.title for recipe in recipes])

    def test_main_view_empty_recipes_message(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'No recipes found.')


class CategoryListViewTests(TestCase):
    def setUp(self):
        self.url = reverse('category_list')
        self.desserts = Category.objects.create(name='Desserts')
        self.soups = Category.objects.create(name='Soups')

    def _create_recipe(self, title, category):
        return Recipe.objects.create(
            title=title,
            description='Description',
            instructions='Instructions',
            ingredients='Ingredients',
            category=category,
        )

    def test_category_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_category_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'category_list.html')

    def test_category_list_view_context_contains_categories(self):
        response = self.client.get(self.url)
        self.assertIn('categories', response.context)
        self.assertEqual(response.context['categories'].count(), 2)

    def test_category_list_view_shows_recipe_count_per_category(self):
        self._create_recipe('Cake', self.desserts)
        self._create_recipe('Pie', self.desserts)
        self._create_recipe('Borscht', self.soups)

        response = self.client.get(self.url)
        counts = {
            category.name: category.recipe_count
            for category in response.context['categories']
        }

        self.assertEqual(counts['Desserts'], 2)
        self.assertEqual(counts['Soups'], 1)

    def test_category_list_view_renders_categories_with_counts(self):
        self._create_recipe('Cake', self.desserts)
        response = self.client.get(self.url)
        self.assertContains(response, 'Desserts (1)')
        self.assertContains(response, 'Soups (0)')

    def test_category_list_view_empty_categories_message(self):
        Category.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'No categories found.')
