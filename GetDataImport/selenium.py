from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv


def get_youtube_channel_info(channel_url):
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口

    # 设置Chrome驱动路径
    service = Service('path/to/chromedriver')  # 请替换为你的ChromeDriver实际路径
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(channel_url)
        # 滚动页面以加载更多视频
        for _ in range(5):  # 可以根据需要调整滚动次数
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)

        # 等待页面加载
        time.sleep(5)

        # 查找所有视频元素
        video_elements = driver.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer')

        video_info_list = []
        for video in video_elements:
            try:
                # 获取视频标题
                title = video.find_element(By.ID, 'video-title').text
                # 获取视频URL
                url = video.find_element(By.ID, 'video-title').get_attribute('href')
                # 点击视频标题以打开视频详情页
                video.find_element(By.ID, 'video-title').click()
                time.sleep(3)  # 等待详情页加载
                # 获取视频描述
                description = driver.find_element(By.ID, 'description').text
                video_info = {
                    'title': title,
                    'url': url,
                    'description': description
                }
                video_info_list.append(video_info)
                # 返回频道页面
                driver.back()
                time.sleep(2)
            except Exception as e:
                print(f"Error getting info for video: {e}")

        return video_info_list

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'url', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    channel_url = "https://www.youtube.com/c/@bustyle9734"  # 请替换为实际的频道URL
    video_info = get_youtube_channel_info(channel_url)
    save_to_csv(video_info, 'youtube_channel_info.csv')
    print("Data has been saved to youtube_channel_info.csv")
    