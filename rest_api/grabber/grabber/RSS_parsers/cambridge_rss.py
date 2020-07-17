import feedparser

feed = feedparser.parse("https://www.cam.ac.uk/news-feed-generator.rss")


feed_entries = feed.entries

for entry in feed.entries:

    title = entry.title
    link = entry.link
    summary = entry.summary
    desc = entry.description
    author = ''
    if hasattr(entry, 'author'):
        author = entry.author
    pubDate = ''
    if hasattr(entry, 'published'):
        pubDate = entry.published

    print('title: {}\nlink: {}\nsummary: {}\nauthor: {}\ndate: {}\n'.format(title, link, desc, author, pubDate))
