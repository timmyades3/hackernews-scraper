from django.test import TestCase
from django.urls import reverse
from .models import News, Comment


class NewsViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for News and Comments"""
        cls.news1 = News.objects.create(
            item_id=1,
            type="story",
            author="test_author",
            title="Breaking News",
            text="This is a test news article",
            is_posted=True
        )

        cls.news2 = News.objects.create(
            item_id=2,
            type="story",
            author="another_author",
            title="Another News",
            text="Another news article content",
            is_posted=True
        )

        cls.comment = Comment.objects.create(
            comment_id=101,
            parent=cls.news1.item_id,  # Links to news1
            text="This is a test comment",
            author="comment_author"
        )

    def test_news_list_view(self):
        """Test the news list view returns status 200"""
        response = self.client.get(reverse("item_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Breaking News")
        self.assertContains(response, "Another News")

    def test_news_list_search_filter(self):
        """Test that searching for a news title filters results"""
        response = self.client.get(reverse("item_list"), {"search": "Breaking"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Breaking News")
        self.assertNotContains(response, "Another News")  # Should not include unrelated news

    def test_news_list_type_filter(self):
        """Test filtering by type"""
        response = self.client.get(reverse("item_list"), {"type": "story"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Breaking News")
        self.assertContains(response, "Another News")

    def test_news_detail_view(self):
        """Test that news detail page loads and contains relevant details"""
        response = self.client.get(reverse("item_detail", args=[self.news1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Breaking News")
        self.assertContains(response, "This is a test news article")
        self.assertContains(response, "This is a test comment")  # Should show related comment
