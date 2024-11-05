# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.text.models import Text, Tag
from apps.dataset.models import Dataset, Category

User = get_user_model()

class TextViewSetTests(APITestCase):
    def setUp(self):
        # Set up users, datasets, and texts
        self.user = User.objects.create_user(username="user1", password="password123")
        self.dataset = Dataset.objects.create(name="Dataset 1", description="Test Dataset")
        self.dataset.users.add(self.user)
        self.text = Text.objects.create(content="Sample content", dataset=self.dataset)

    def test_list_texts_admin(self):
        # Only admin should list all texts
        self.admin_user = User.objects.create_superuser(username="admin", password="password123")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('text-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_text_retrieve(self):
        # Ensure a user can retrieve a specific text in their dataset
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('text-detail', kwargs={'pk': self.text.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], self.text.content)

    def test_unauthorized_text_access(self):
        # Unauthenticated access to text should be denied
        response = self.client.get(reverse('text-detail', kwargs={'pk': self.text.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TextSearchViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="password123")
        self.dataset = Dataset.objects.create(name="Dataset 1", description="Test Dataset")
        self.dataset.users.add(self.user)
        self.text1 = Text.objects.create(content="This is a happy text", dataset=self.dataset)
        self.text2 = Text.objects.create(content="This is a sad text", dataset=self.dataset)

    def test_search_texts_in_dataset(self):
        # Test search within texts in a dataset
        self.client.force_authenticate(user=self.user)
        url = f"{reverse('search-list', kwargs={'dataset_id': self.dataset.id})}?search=happy"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["content"], self.text1.content)


class TagViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="password123")
        self.dataset = Dataset.objects.create(name="Dataset 1", description="Test Dataset")
        self.dataset.users.add(self.user)
        self.text = Text.objects.create(content="Sample text for tagging", dataset=self.dataset)
        self.category = Category.objects.create(name="Category 1", dataset=self.dataset)
    
    def test_create_tag_successful(self):
        # Test creating a new tag by an authorized user
        self.client.force_authenticate(user=self.user)
        data = {
            "text": self.text.id,
            "category": self.category.id,
        }
        response = self.client.post(reverse('tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], self.text.id)

    def test_create_duplicate_tag(self):
        # Test creating a duplicate tag for the same text and category by the same user
        self.client.force_authenticate(user=self.user)
        Tag.objects.create(text=self.text, category=self.category, user=self.user)
        data = {
            "text": self.text.id,
            "category": self.category.id,
        }
        response = self.client.post(reverse('tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You have already tagged this text with this category.", response.data["non_field_errors"])

    def test_tagging_text_in_unauthorized_dataset(self):
        # Create a new dataset not assigned to the user and try tagging its text
        other_dataset = Dataset.objects.create(name="Dataset 2", description="Unauthorized dataset")
        other_text = Text.objects.create(content="Other dataset text", dataset=other_dataset)
        self.client.force_authenticate(user=self.user)
        data = {
            "text": other_text.id,
            "category": self.category.id,
        }
        response = self.client.post(reverse('tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You can only tag texts in your assigned datasets.", response.data["non_field_errors"])

    def test_unauthenticated_tag_access(self):
        # Unauthenticated access to create a tag should be denied
        data = {
            "text": self.text.id,
            "category": self.category.id,
        }
        response = self.client.post(reverse('tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
