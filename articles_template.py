def generate_articles_html(top_articles):
    """Generate HTML for articles layout"""
    # Create full-width container for articles
    articles_html = """
    <div style="width: 100vw; margin-left: calc(-50vw + 50%); position: relative; padding: 0 0 60px 0;">
        <div class="container">
    """
    
    # Featured article layout (first 3 articles)
    if len(top_articles) >= 3:
        articles_html += '<div class="featured-grid">'
        
        # Main featured article
        main_article = top_articles[0]
        articles_html += generate_main_article_html(main_article)
        
        # Side articles
        articles_html += '<div class="side-articles">'
        for article in top_articles[1:3]:
            articles_html += generate_side_article_html(article)
        
        articles_html += '</div></div>'  # Close side-articles and featured-grid
        
        # Remaining articles
        remaining_articles = top_articles[3:]
    else:
        remaining_articles = top_articles
    
    # Regular article cards
    for article in remaining_articles:
        articles_html += generate_article_card_html(article)
    
    articles_html += """
    """
    
    return articles_html

def generate_main_article_html(article):
    """Generate HTML for main featured article"""
    return f"""
    <div class="main-article">
        <a href="{article['link']}" class="main-article-title" target="_blank">
            {article['title']}
        </a>
        <div class="article-meta">
            <div class="news-source">
                <div class="source-icon">{article['source_icon']}</div>
                <span>Keyword: {article['keyword']}</span>
            </div>
            <span>•</span>
            <span>{article['time_ago']}</span>
        </div>
        <div class="article-stats">
            <span class="{article['sentiment_class']}">{article['sentiment']}</span>
        </div>
    </div>
    """

def generate_side_article_html(article):
    """Generate HTML for side articles"""
    title = article['title'][:80] + ('...' if len(article['title']) > 80 else '')
    
    return f"""
    <div class="side-article">
        <a href="{article['link']}" class="side-article-title" target="_blank">
            {title}
        </a>
        <div class="article-meta">
            <div class="news-source">
                <div class="source-icon">{article['source_icon']}</div>
                <span>{article['keyword']}</span>
            </div>
            <span>•</span>
            <span>{article['time_ago']}</span>
        </div>
        <div class="article-stats">
            <span class="{article['sentiment_class']}">{article['sentiment']}</span>
        </div>
    </div>
    """

def generate_article_card_html(article):
    """Generate HTML for regular article cards"""
    return f"""
    <div class="article-card">
        <a href="{article['link']}" class="article-title" target="_blank">
            {article['title']}
        </a>
        <div class="article-meta">
            <div class="news-source">
                <div class="source-icon">{article['source_icon']}</div>
                <span>Keyword: {article['keyword']}</span>
            </div>
            <span>•</span>
            <span>{article['time_ago']}</span>
        </div>
        <div class="article-stats">
            <span class="{article['sentiment_class']}">{article['sentiment']}</span>
        </div>
    </div>
    """