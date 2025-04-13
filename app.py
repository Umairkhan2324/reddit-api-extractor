import os
from dotenv import load_dotenv
import praw
import prawcore

def main():
    # Load environment variables from the .env file
    load_dotenv()

    # Retrieve Reddit API credentials from environment variables
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")

    # Check if all required credentials are present
    if not all([client_id, client_secret, user_agent, username, password]):
        print("ERROR: Missing one or more Reddit API credentials. Please check your .env file.")
        return

    # Debug information - print credentials (hiding password)
    print(f"Using credentials:")
    print(f"Client ID: {client_id}")
    print(f"User Agent: {user_agent}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")  # Print asterisks instead of the actual password
    
    try:
        # First try with a more standard user agent format
        modified_user_agent = f"script:reddit-post-viewer:v1.0 (by /u/{username})"
        print(f"Trying with modified user agent: {modified_user_agent}")
        
        # Create a Reddit instance using PRAW with password authentication
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=modified_user_agent,
            username=username,
            password=password
        )

        # Try to authenticate - this will force an auth check
        print("Attempting authentication...")
        me = reddit.user.me()
        print(f"Authenticated as: {me}")

        # Prompt for a subreddit name; default to "python" if input is empty.
        subreddit_name = input("Enter the subreddit name (default: python): ").strip() or "python"
        subreddit = reddit.subreddit(subreddit_name)

        print(f"\nFetching 5 latest posts from r/{subreddit_name}...\n")
        
        # Fetch and iterate over the 5 latest posts from the subreddit
        for post in subreddit.new(limit=5):
            # The author may be None if the account was deleted
            author = post.author.name if post.author else "Unknown"
            # Display the required post information
            print(f"Title   : {post.title}")
            print(f"Author  : {author}")
            print(f"Upvotes : {post.score}")
            print("-" * 40)

    except prawcore.exceptions.OAuthException as e:
        print(f"Authentication Error: {e}")
        print("\nPossible solutions:")
        print("1. Double-check your Reddit username and password")
        print("2. Make sure your Reddit App is properly configured as a 'script' type app")
        print("3. Verify your Client ID and Client Secret are correct")
        print("4. Ensure your Reddit account has been verified (email verification)")
        
    except prawcore.exceptions.ResponseException as e:
        print(f"API Response Error: {e}")
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
    except Exception as e:
        # Handle exceptions that could occur during authentication or fetching posts.
        print(f"An error occurred: {type(e).__name__} - {e}")

if __name__ == "__main__":
    main()
