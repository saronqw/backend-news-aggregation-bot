import feedparser

feed = feedparser.parse("http://news.nus.edu.sg/highlights/feed")
# всё парсится ок

feed_entries = feed.entries

#print(feed.keymap)

for entry in feed.entries:

    title = entry.title
    link = entry.link
    summary = entry.summary
    desc = entry.description
    author = entry.author
    pubDate = entry.published

    print('title: {}\nlink: {}\nsummary: {}\nauthor: {}\ndate: {}\n'.format(title, link, desc, author, pubDate))
