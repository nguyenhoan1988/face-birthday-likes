from facepy import GraphAPI

# Your access token for your application on facebook
access_token = ''

graph = GraphAPI(access_token)

def like_post(post_id, actions):
    """
        Like a post on facebook

        Attributes:
        -----------
            post_id:
                The id of the post to be liked
            actions:
                The actions dictionary contains the name of the action and the URL of the action link
                        Example:
                            actions = [
                                    {
                                        "name": "Like/Comment",
                                        "link": "https://www.facebook.com/<user_id>/posts/<post_id>"
                                    }
                                ]
        Return:
        -------
            True if success; False otherwise
    """
    result = graph.post(path='%s/likes' % post_id, actions=actions)
    return result['success']

def get_post(since_date, max_posts_num=1000):
    """
        Get all posts to this current user's wall from since_date (or at most max_posts_num posts)

        Attributes:
        -----------
            since_date:
                The beginning date to get posts
            max_posts_num:
                The maximum number of posts to return

        Return:
        -------
            A list of posts
    """
    posts = []
    paging_next = ''

    while True or len(posts) < max_posts_num:
        feed = graph.get(path='me/feed%s' % paging_next)
        cursor = feed['paging']
        until = cursor['next'].split('until=')[1]
        data = feed['data']
        
        print 'Processing %d posts' % len(data)

        for post in data:
            post_from = post['from']
            user_id = post_from['id']
            user_name = post_from['name']
            created_time = datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
            post['user_id'] = user_id
            post['user_name'] = user_name
            post['created_time'] = created_time

            if created_time > since_date:
                posts.append(post)
            else:
                return posts

        paging_next = '?until=%s' % until

    return posts
