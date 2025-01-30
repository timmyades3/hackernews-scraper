import requests
from datetime import datetime
from celery import shared_task
from concurrent.futures import ThreadPoolExecutor
import logging
from .models import News, Comment

HACKER_NEWS_BASE_URL = "https://hacker-news.firebaseio.com/v0"
MAX_WORKERS = 5  # Number of threads for parallel API requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@shared_task(name="sync_news_to_db")
def sync_news_to_db():
    """
    Fetch the latest stories and job postings from Hacker News and save them to the database.
    Uses threading to fetch data in parallel.
    """
    try:
        # Fetch the latest 100 stories and job postings
        news_ids = fetch_initial_story_ids("newstories")
        job_ids = fetch_initial_story_ids("jobstories")

        # Merge both lists to remove duplicates
        all_item_ids = list(set(news_ids + job_ids))

        # Ensure we are only processing the top 100 stories (latest first)
        all_item_ids = all_item_ids[:100]

        # Get the last fetched item_id from the database
        last_fetched_item_id = get_last_fetched_item_id()

        # Filter out stories that are already in the database
        new_item_ids = [item_id for item_id in all_item_ids if item_id > last_fetched_item_id]

        # Fetch and save all items using threading
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(fetch_and_save_story, new_item_ids)

        # Update the last fetched story ID after syncing
        if new_item_ids:
            set_last_fetched_story_id(new_item_ids[-1])

    except Exception as e:
        logger.error(f"Error syncing stories and jobs: {str(e)}")


def fetch_initial_story_ids(category):
    """
    Fetch the first 100 item IDs from Hacker News based on category.
    :param category: "newstories" for news, "jobstories" for jobs
    """
    try:
        response = requests.get(f"{HACKER_NEWS_BASE_URL}/{category}.json?print=pretty")
        response.raise_for_status()
        # Ensure we only select the top 100 stories, in descending order
        return response.json()[:100]
    except Exception as e:
        logger.error(f"Error fetching {category}: {str(e)}")
        return []


def fetch_and_save_story(item_id):
    """
    Fetches story/job details and saves them to the database.
    Runs in parallel using ThreadPoolExecutor.
    """
    try:
        # Fetch story/job details
        response = requests.get(f"{HACKER_NEWS_BASE_URL}/item/{item_id}.json?print=pretty")
        response.raise_for_status()
        item_data = response.json()

        # Save or update the item in the database
        news_item, created = News.objects.update_or_create(
            item_id=item_data.get("id"),
            defaults={
                "type": item_data.get("type", "unknown"),
                "author": item_data.get("by", "unknown"),
                "date_created": datetime.fromtimestamp(item_data.get("time", datetime.now().timestamp())),
                "is_posted": False,
                "kids": item_data.get("kids", []),
                "text": item_data.get("text", ""),
                "descendants": item_data.get("descendants", 0),
                "score": item_data.get("score", 0),
                "url": item_data.get("url", ""),
                "title": item_data.get("title", ""),
            }
        )

        # Fetch and save comments if the story has any
        if item_data.get("kids"):
            fetch_and_save_comments(item_data.get("kids"), news_item)

    except Exception as e:
        logger.error(f"Error syncing story {item_id}: {str(e)}")


def fetch_and_save_comments(comment_ids, parent_news=None, parent_comment_id=None):
    """
    Recursively fetch and save comments to the database.
    :param comment_ids: List of comment IDs to fetch
    :param parent_news: The News object to associate with the comment
    :param parent_comment_id: The Hacker News ID of the parent comment
    """
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(lambda cid: fetch_and_save_single_comment(cid, parent_news, parent_comment_id), comment_ids)


def fetch_and_save_single_comment(comment_id, parent_news, parent_comment_id):
    """
    Fetches a single comment and saves it to the database.
    Runs in parallel using ThreadPoolExecutor.
    """
    try:
        # Fetch comment details
        response = requests.get(f"{HACKER_NEWS_BASE_URL}/item/{comment_id}.json?print=pretty")
        response.raise_for_status()
        comment_data = response.json()

        # Skip deleted or dead comments
        if comment_data.get("deleted") or comment_data.get("dead"):
            logger.info(f"Skipping deleted/dead comment {comment_id}")
            return

        # Use the parent field from the Hacker News API response
        parent_id = comment_data.get("parent")  # Directly from API

        # Add the comment to the database
        comment, created = Comment.objects.update_or_create(
            comment_id=comment_data.get("id"),
            defaults={
                "text": comment_data.get("text", ""),
                "date_posted": datetime.fromtimestamp(comment_data.get("time", datetime.now().timestamp())),
                "kids": comment_data.get("kids", []),
                "type": comment_data.get("type", "comment"),
                "author": comment_data.get("by", "unknown"),
                "parent": parent_id,  # Now using the actual Hacker News parent field
            }
        )

        # Fetch nested comments if any
        if comment_data.get("kids"):
            fetch_and_save_comments(comment_data.get("kids"), parent_news, comment.comment_id)

    except Exception as e:
        logger.error(f"Error syncing comment {comment_id}: {str(e)}")


def set_last_fetched_story_id(story_id):
    """
    Store the last fetched story ID (this should ideally be stored in a database or a persistent file).
    """
    # For now, we are just logging it, but ideally, this should be saved to a persistent storage
    logger.info(f"Last fetched story ID: {story_id}")
    # Save this ID to the database or a file for future reference.


def get_last_fetched_item_id():
    """
    Retrieve the last fetched story ID from the database.
    """
    try:
        last_story = News.objects.order_by('-item_id').first()
        return last_story.item_id if last_story else 0  # If no stories exist, return 0
    except Exception as e:
        logger.error(f"Error fetching last fetched item ID: {str(e)}")
        return 0
