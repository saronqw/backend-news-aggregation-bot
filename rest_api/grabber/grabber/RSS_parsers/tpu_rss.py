import feedparser

feed = feedparser.parse("https://news.tpu.ru/rss/?channel=1560160c53fb33a24a7753e0b445cc4e")
# всё парсится ок

feed_entries = feed.entries

for entry in feed.entries:

    title = entry.title
    link = entry.link
    summary = entry.summary
    desc = entry.description
    author = entry.author
    pubDate = entry.published

    print('title: {}\nlink: {}\nsummary: {}\nauthor: {}\ndate: {}\n'.format(title, link, summary, author, pubDate))
