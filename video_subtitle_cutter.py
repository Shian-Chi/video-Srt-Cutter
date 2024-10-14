from moviepy.editor import VideoFileClip, concatenate_videoclips
import pysrt

# 1. 定義輸入檔案
FILE_NAME = "/home/ubuntu/大疆影片/0132/DJI_0132" 

input_video = f"{FILE_NAME}.MP4"
input_subtitle = f"{FILE_NAME}.srt"

output_video = f"{FILE_NAME}_crop.mp4"
output_subtitle = f"{FILE_NAME}_crop.srt"

# 2. 定義要移除的時間段（添加新的時間段）
remove_intervals = [
    ('0:34', '0:47'),
    ('2:48', '2:51'),
    ('2:48', '2:51'),
    ('2:53', 'end'),
]

# 3. 讀取影片並獲取總時長
clip = VideoFileClip(input_video)
total_duration = clip.duration  # 總時長（秒）

# 4. 定義時間字串轉換為秒的函數
def time_to_seconds(time_str, total_duration):
    if time_str == 'end':
        return total_duration
    else:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours)*3600 + int(minutes)*60 + float(seconds)
        elif len(parts) == 2:
            minutes, seconds = parts
            return int(minutes)*60 + float(seconds)
        elif len(parts) == 1:
            return float(parts[0])
        else:
            raise ValueError('Invalid time format')

# 5. 解析要移除的時間段，並轉換為秒
remove_intervals_sec = []
for start_str, end_str in remove_intervals:
    start_sec = time_to_seconds(start_str, total_duration)
    end_sec = time_to_seconds(end_str, total_duration)
    remove_intervals_sec.append((start_sec, end_sec))

# 6. 計算要保留的時間段
remove_intervals_sec.sort(key=lambda x: x[0])  # 確保按照時間排序

keep_intervals = []
prev_end = 0
for start_sec, end_sec in remove_intervals_sec:
    if start_sec > prev_end:
        keep_intervals.append((prev_end, start_sec))
    prev_end = end_sec
if prev_end < total_duration:
    keep_intervals.append((prev_end, total_duration))

# 7. 剪輯並合併要保留的影片片段
clips = []
for start_sec, end_sec in keep_intervals:
    subclip = clip.subclip(start_sec, end_sec)
    clips.append(subclip)

final_clip = concatenate_videoclips(clips)
final_clip.write_videofile(output_video)

# 8. 處理字幕文件
subs = pysrt.open(input_subtitle)

# 計算新的時間對應關係
keep_intervals_new = []
cumulative_duration = 0
for start_sec, end_sec in keep_intervals:
    duration = end_sec - start_sec
    keep_intervals_new.append((start_sec, end_sec, cumulative_duration))
    cumulative_duration += duration

# 定義舊時間映射到新時間的函數
def map_time(old_time_sec):
    for start_sec, end_sec, new_base_time in keep_intervals_new:
        if start_sec <= old_time_sec < end_sec:
            offset = old_time_sec - start_sec
            new_time_sec = new_base_time + offset
            return new_time_sec
    return None  # 不在保留的時間段內

# 重新生成字幕
new_subs = pysrt.SubRipFile()
new_index = 1  # 初始化新的字幕索引

for sub in subs:
    # 將字幕時間轉換為秒
    start_sec = sub.start.ordinal / 1000.0
    end_sec = sub.end.ordinal / 1000.0

    # 映射新時間
    new_start_sec = map_time(start_sec)
    new_end_sec = map_time(end_sec)

    if new_start_sec is not None and new_end_sec is not None:
        new_sub = pysrt.SubRipItem(index=new_index)  # 使用新的連續索引
        new_sub.text = sub.text
        new_sub.start.seconds = new_start_sec
        new_sub.end.seconds = new_end_sec
        new_subs.append(new_sub)
        new_index += 1  # 增加索引

# 保存新的字幕文件
new_subs.save(output_subtitle, encoding='utf-8')

print("影片和字幕處理完成。")