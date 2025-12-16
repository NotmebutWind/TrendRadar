from trendradar.crawler.fetcher import DataFetcher
import pandas as pd

# 读取config.yaml
import yaml

with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
# 读取config中的platforms：
platform_ids = [platform['id'] for platform in config['platforms']]
print(f"加载的平台ID列表: {platform_ids}")

def results_to_dataframe(results, source_name=None):
    """
    将爬取结果转换为DataFrame格式
    
    Args:
        results: 爬取结果字典，格式为 {source: {title: content_dict}}
        source_name: 指定要转换的数据源名称，如果为None则转换所有数据源
    
    Returns:
        pandas.DataFrame: 包含source, title, ranks, url, mobileUrl列的DataFrame
    
    示例:
        >>> df = results_to_dataframe(results, source_name='wallstreetcn-hot')
        >>> print(df.columns)
        Index(['source', 'title', 'ranks', 'url', 'mobileUrl'], dtype='object')
    """
    import pandas as pd
    
    data_list = []
    
    # 如果指定了source_name，只处理该数据源
    if source_name:
        sources = {source_name: results.get(source_name, {})}
    else:
        sources = results
    
    for source, items in sources.items():
        for title, content in items.items():
            data_list.append({
                'source': source,
                'title': title,
                'ranks': content.get('ranks', []),
                'url': content.get('url', ''),
                'mobileUrl': content.get('mobileUrl', '')
            })
    
    df = pd.DataFrame(data_list)
    return df
    
def hot_daily_news_markdown():
    """
    获取当日热点新闻的Markdown格式字符串

    Returns:
        str: Markdown格式的热点新闻字符串

    示例:
        >>> markdown = hot_daily_news_markdown()
        >>> print(markdown)
        # 热点新闻

        | source | title | ranks | url | mobileUrl |
        |--------|-------|-------|-----|-----------|
        | ... | ... | ... | ... | ... |
        ...
    """
    fetcher = DataFetcher()
    results, id_to_name, failed = fetcher.crawl_websites(
        platform_ids,
        request_interval=1000
    )
    
    # 转换为DataFrame
    df = results_to_dataframe(results)
    
    # 转换为markdown
    return df.to_markdown(index=False)

if __name__ == "__main__":
    markdown = hot_daily_news_markdown()
    print(markdown)