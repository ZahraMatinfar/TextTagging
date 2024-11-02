# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.dataset.models import Dataset, Category
from apps.text.models import Text, Tag
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class DatasetViewSetTests(APITestCase):
    def setUp(self):
        # Set up a user and dataset for testing
        self.user = User.objects.create_user(username="user1", password="password123")
        self.admin_user = User.objects.create_superuser(username="admin", password="password123")

        self.dataset = Dataset.objects.create(name="Sentiment Analysis", description="Analyze user sentiments")
        self.dataset.users.add(self.user)

        # Create categories and texts
        self.category_happy = Category.objects.create(name="Happy", dataset=self.dataset)
        self.category_sad = Category.objects.create(name="Sad", dataset=self.dataset)
        self.text1 = Text.objects.create(content="This is a happy text", dataset=self.dataset)
        self.text2 = Text.objects.create(content="This is a sad text", dataset=self.dataset)
        Tag.objects.create(text=self.text1, category=self.category_happy, user=self.user)

        self.page_size = PageNumberPagination.page_size

    def test_dataset_list_for_user(self):
        # User should only see datasets they have access to
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('dataset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], self.dataset.name)

    def test_dataset_list_for_admin(self):
        # Admin should see all datasets
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('dataset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), self.page_size)

    def test_dataset_detail(self):
        # Test retrieving a dataset with categories and texts
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('dataset-detail', kwargs={'pk': self.dataset.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.dataset.name)
        self.assertIn("categories", response.data)
        self.assertIn("texts", response.data)

    def test_search_texts_in_dataset(self):
        # Test search functionality in dataset detail view
        self.client.force_authenticate(user=self.user)
        url = f"{reverse('dataset-detail', kwargs={'pk': self.dataset.id})}?search=happy"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("texts", response.data)
        self.assertEqual(len(response.data["texts"]), 1)
        self.assertEqual(response.data["texts"][0]["content"], self.text1.content)

    def test_tag_count_annotation_in_categories(self):
        # Test that categories have correct tag count
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('dataset-detail', kwargs={'pk': self.dataset.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        categories = response.data["categories"]
        for category in categories:
            if category["name"] == "Happy":
                self.assertEqual(category["tag_count"], 1)
            else:
                self.assertEqual(category["tag_count"], 0)


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        # Set up an admin and regular user
        self.user = User.objects.create_user(username="user1", password="password123")
        self.admin_user = User.objects.create_superuser(username="admin", password="password123")

        self.dataset = Dataset.objects.create(name="Emotion Dataset", description="Dataset for testing emotions")
        self.category = Category.objects.create(name="Joyful", dataset=self.dataset)

    def test_list_categories_for_admin(self):
        # Admin user should be able to list all categories
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], self.category.name)

    def test_list_categories_for_user(self):
        # Regular users should not see categories outside their datasets
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_category(self):
        # Admin user should be able to retrieve category details
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_unauthorized_access(self):
        # Unauthenticated access should be denied
        response = self.client.get(reverse('dataset-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
