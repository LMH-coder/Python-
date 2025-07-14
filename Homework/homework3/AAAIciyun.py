import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# 下载必要的NLTK数据
nltk.download('stopwords')
nltk.download('wordnet')

# 初始化停用词和词形还原器
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# 读取数据
data = pd.read_excel(r"C:\python\pachong\zuoye\output\aaai_papers_2020_present.xlsx")

# 按年份分组
data['year'] = data['year'].astype(int)
papers_2020 = data[data['year'] == 2020]
papers_2021 = data[data['year'] == 2021]
papers_2022 = data[data['year'] == 2022]
papers_2023 = data[data['year'] == 2023]
papers_2024 = data[data['year'] == 2024]
papers_2025 = data[data['year'] == 2025]

def extract_keywords(titles):
    keywords = []
    for title in titles:
        # 移除标点符号并转为小写
        words = re.findall(r'\b\w+\b', title.lower())
        # 移除停用词并进行词形还原
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words and len(word) > 2]
        keywords.extend(words)
    return keywords

# 提取各年份关键词
keywords_2020 = extract_keywords(papers_2020['title'])
keywords_2021 = extract_keywords(papers_2021['title'])
keywords_2022 = extract_keywords(papers_2022['title'])
keywords_2023 = extract_keywords(papers_2023['title'])
keywords_2024 = extract_keywords(papers_2024['title'])
keywords_2025 = extract_keywords(papers_2025['title'])

# 统计词频
def get_word_freq(keywords):
    freq = Counter(keywords)
    # 过滤掉一些通用词
    common_words = {'learning', 'network', 'model', 'based', 'using', 'deep', 'neural', 'detection', 'recognition', 'prediction'}
    filtered_freq = {k: v for k, v in freq.items() if k not in common_words}
    return filtered_freq

freq_2020 = get_word_freq(keywords_2020)
freq_2021 = get_word_freq(keywords_2021)
freq_2022 = get_word_freq(keywords_2022)
freq_2023 = get_word_freq(keywords_2023)
freq_2024 = get_word_freq(keywords_2024)
freq_2025 = get_word_freq(keywords_2025)

# 生成词云图
def generate_wordcloud(freq, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=15)
    plt.axis('off')
    plt.show()

generate_wordcloud(freq_2020, 'AAAI 2020 Research Hotspots')
generate_wordcloud(freq_2021, 'AAAI 2021 Research Hotspots')
generate_wordcloud(freq_2022, 'AAAI 2022 Research Hotspots')
generate_wordcloud(freq_2023, 'AAAI 2023 Research Hotspots')
generate_wordcloud(freq_2024, 'AAAI 2024 Research Hotspots')
generate_wordcloud(freq_2025, 'AAAI 2025 Research Hotspots')