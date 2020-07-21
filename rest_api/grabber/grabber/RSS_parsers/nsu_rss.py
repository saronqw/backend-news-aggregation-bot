import feedparser

feed = feedparser.parse("https://english.nsu.ru/news-events/news/rss/")
# всё парсится ок

feed_entries = feed.entries

for entry in feed.entries:

    title = entry.title
    link = entry.link
    summary = entry.summary
    desc = entry.description
    author = 'entry.author'
    pubDate = entry.published

    print('title: {}\nlink: {}\nsummary: {}\nauthor: {}\ndate: {}\n'.format(title, link, desc, author, pubDate))
