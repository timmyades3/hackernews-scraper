from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from scraper.models import News, Comment
from django.utils.timezone import now


class NewsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.news_item = News.objects.create(
            item_id=1,
            type="story",
            author="test_author",
            date_created=now(),
            is_posted=True,
            text="This is a test news item.",
            title="Test News",
            score=100,
            url="http://example.com",
        )

    def test_news_list(self):
        """Test retrieving the list of news items"""
        response = self.client.get("/api/item/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_detail(self):
        """Test retrieving a single news item"""
        response = self.client.get(f"/api/item/detail/{self.news_item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_create(self):
        """Test creating a news item"""
        data = {
            "item_id": 2,
            "type": "story",
            "author": "new_author",
            "date_created": now(),
            "is_posted": True,
            "text": "Another test news item.",
            "title": "New Test News",
            "score": 50,
            "url": "http://example.com",
        }
        response = self.client.post("/api/item/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_news_update(self):
        """Test updating an existing news item"""
        data = {"title": "Updated Title"}
        response = self.client.patch(f"/api/item/detail/{self.news_item.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news_item.refresh_from_db()
        self.assertEqual(self.news_item.title, "Updated Title")

    def test_news_delete(self):
        """Test deleting a news item"""
        response = self.client.delete(f"/api/item/detail/{self.news_item.id}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_403_FORBIDDEN])


class CommentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.news_item = News.objects.create(
            item_id=1,
            type="story",
            author="test_author",
            date_created=now(),
            is_posted=True,
            text="This is a test news item.",
            title="Test News",
            score=100,
            url="http://example.com",
        )
        self.comment = Comment.objects.create(
            comment_id=101,
            parent=self.news_item.item_id,  # Assuming parent links to the item's item_id
            text="This is a test comment.",
            date_posted=now(),
            type="comment",
            author="test_commenter",
        )

    def test_comment_list(self):
        """Test retrieving the list of comments"""
        response = self.client.get("/api/item/comment/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_detail(self):
        """Test retrieving a single comment"""
        response = self.client.get(f"/api/item/comment/detail/{self.comment.comment_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
