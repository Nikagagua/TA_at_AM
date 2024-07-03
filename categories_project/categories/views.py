from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from .models import Category
from .serializers import CategorySerializer


class CategoryCreateView(APIView):
    def post(self, request):
        def create_category(data, parent=None):
            name = data.get("name")
            if not name:
                raise ValueError("Each category must have a 'name'.")
            category = Category.objects.create(name=name, parent=parent)
            for child_data in data.get("children", []):
                create_category(child_data, parent=category)

        try:
            create_category(request.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "An error occurred while creating categories."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        parents = []
        parent = category.parent
        while parent:
            parents.append(CategorySerializer(parent).data)
            parent = parent.parent

        children = CategorySerializer(category.children.all(), many=True).data
        siblings = (
            CategorySerializer(
                category.parent.children.exclude(id=category.id), many=True
            ).data
            if category.parent
            else []
        )

        return Response(
            {
                "id": category.id,
                "name": category.name,
                "parents": parents,
                "children": children,
                "siblings": siblings,
            }
        )


def main_page(request):
    api_urls = f"""
    <html>
    <head>
        <title>API Endpoints</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                color: #2c3e50;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
            }}
            a {{
                text-decoration: none;
                color: #2980b9;
                font-weight: bold;
            }}
            a:hover {{
                color: #1abc9c;
            }}
            .instruction {{
                font-size: 0.9em;
                color: #7f8c8d;
            }}
        </style>
    </head>
    <body>
        <h1>API Endpoints</h1>
        <ul>
            <li>
                <a href="{reverse('category-create')}">Create Categories (POST /api/categories/)</a>
                <p class="instruction">Use this endpoint to create a new category with its children. Send a JSON body as specified in the assignment.</p>
            </li>
            <li>
                Category Details (GET /api/categories/&lt;id&gt;/)
                <p class="instruction">Retrieve category details, including its parents, children, and siblings. Replace &lt;id&gt; with the actual category ID.</p>
            </li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(api_urls)
