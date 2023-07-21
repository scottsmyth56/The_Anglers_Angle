| No. | Process  | Action | Description | Result |
| --- | -------- | ------ | ----------- | ------ |
| 1 | HTTP Request | Receive | GET request | Pass |
| 2 | URL (urls.py) | Analyze URL | Match view name "index" | Pass |
| 4 | template file | Render | "index.html" in blog app | Pass |
| 5 | Blog List | Display | List of  posts | Pass |
| 6 | Blog Post Link | Click | Forward to specific blog post page | Pass |
| 7 | Generate URL | Use tag | `{% url 'viewPost' blog.id %}` | Pass |
| 8 | Result | URL path | "/blog/1/" (assuming the blog post has id 1) | Pass |
| 9 | URL  (urls.py) | Analyze URL | Match view name "post_detailed" | Pass |
| 10 | views.py | Invoke | "class PostDetailView" in blog app | Pass |
| 11 | template file | Render | "Posts/post_detail.html" in blog app | Pass |
| 12 | Blog Post | Display | Blog post title, author, content | Pass |
| 13 | Comment Section | Display | List of comments | Pass |
| 14 | Comment Form | Submit | Comment | Pass |
| 15 | Generate URL | Use tag | `{% url 'add_comment' blog.id %}` | Pass |
| 16 | Result | URL path | "/blog/1/add_comment/" (assuming the blog post has id 1) | Pass |
| 17 | URL  (urls.py) | Analyze URL | Match view name "add_comment" | Pass |
| 18 | views.py | Invoke | "function add_comment" in blog app | Pass |
| 19 | template file | Render | "Posts/add_comment.html" in blog app | Pass |
| 20 | Back to Blog Home | Click | Forward to index | Pass |
| 21 | Generate URL | Use tag | `{% url 'index' %}` | Pass |
| 22 | Result | URL path | "/blog/" | Pass |
| 23 | URL (urls.py) | Analyze URL | Match view name "index" | Pass |
| 24 | views.py | Invoke | "class index" in blog app | Pass |
| 25 | template file | Render | "index.html"  | Pass |
