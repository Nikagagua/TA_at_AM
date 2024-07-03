from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category
import uuid


class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        unique_name = lambda: f"Category_{uuid.uuid4()}"
        self.initial_category_name = unique_name()
        self.unique_names = [unique_name() for _ in range(5)]
        self.category_data = {
            "name": self.unique_names[0],
            "children": [
                {
                    "name": self.unique_names[1],
                    "children": [
                        {"name": self.unique_names[2]},
                        {"name": self.unique_names[3]},
                    ],
                },
                {"name": self.unique_names[4]},
            ],
        }
        self.category = Category.objects.create(name=self.initial_category_name)

        initial_categories = Category.objects.all()
        print("Initial categories:", [(cat.id, cat.name) for cat in initial_categories])

    def test_create_category(self):
        initial_count = Category.objects.count()
        response = self.client.post(
            reverse("category-create"), self.category_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_count = initial_count + 5
        self.assertEqual(Category.objects.count(), expected_count)

        created_categories = Category.objects.filter(name__in=self.unique_names)
        print("Created categories:", [(cat.id, cat.name) for cat in created_categories])
        for category in created_categories:
            print("Category:", category.name)

        self.assertEqual(created_categories.count(), 5)

    def test_get_category(self):
        response = self.client.get(
            reverse("category-detail", kwargs={"pk": self.category.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_get_category_with_siblings(self):
        root_category = Category.objects.create(name="Root")
        child_1 = Category.objects.create(name="Child 1", parent=root_category)
        child_2 = Category.objects.create(name="Child 2", parent=root_category)
        child_3 = Category.objects.create(name="Child 3", parent=root_category)
        response = self.client.get(
            reverse("category-detail", kwargs={"pk": child_2.id})
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], child_2.name)
        self.assertEqual(len(response.data["siblings"]), 2)
        sibling_ids = [sibling["id"] for sibling in response.data["siblings"]]
        self.assertIn(child_1.id, sibling_ids)
        self.assertIn(child_3.id, sibling_ids)
