import yt_dlp
import csv


def get_youtube_channel_info(channel_url):
    ydl_opts = {
        'extract_flat': True,  # 提取扁平列表，避免递归
        'dump_single_json': True,
        'quiet': True,
        'no_warnings': True,  # 忽略警告
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)  # 提取频道信息
            video_info_list = []
            
            # 处理频道中的视频条目（可能是 'entries' 或直接是视频列表，需根据频道类型调整）
            videos = info.get('entries', [info])  # 兼容不同频道格式（如用户频道、品牌频道）
            
            for entry in videos:
                if not entry or 'id' not in entry:
                    continue
                
                video_id = entry['id']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                video_title = entry.get('title', '无标题')
                
                # 单独获取视频描述（因 extract_flat 模式可能不包含描述）
                single_ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                }
                with yt_dlp.YoutubeDL(single_ydl_opts) as single_ydl:
                    single_info = single_ydl.extract_info(video_url, download=False)
                    video_description = single_info.get('description', '无描述')
                
                video_info_list.append({
                    'title': video_title,
                    'url': video_url,
                    'description': video_description
                })
            
            return video_info_list
        
        except Exception as e:
            print(f"错误：{str(e)}")
            return []


def save_to_csv(data, filename):
    """将视频信息保存到 CSV 文件"""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:  # 使用 utf-8-sig 处理Excel中文乱码
        fieldnames = ['title', 'url', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    # 目标频道 URL（已替换为用户提供的链接）
    channel_url = "https://www.youtube.com/@bustyle9734"
    
    # 获取视频信息
    video_info = get_youtube_channel_info(channel_url)
    
    # 保存到 CSV
    if video_info:
        save_to_csv(video_info, 'bustyle9734_channel_info.csv')
        print(f"成功保存 {len(video_info)} 条视频信息到 bustyle9734_channel_info.csv")
    else:
        print("未获取到视频信息")