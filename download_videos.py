#-*- coding: utf-8 -*-
from pytube import YouTube
import pandas as pd
import numpy as np
import skvideo.io
import cv2
import os
import ipdb
from skvideo.io import vwrite,vreader

def download_and_process_video(row):
    video_id = row['VideoID']
    video_path = row['video_path']
    rename_file = row['VideoID']+'_'+str(row['Start'])+'_'+str(row['End'])+'.mp4'
    full_path = os.path.join('videos',rename_file)
    save_path = full_path
    save_path = save_path.replace('mp4','avi')
    start = row['Start']
    end = row['End']
    print video_id
    if not os.path.exists( save_path ):
        if not os.path.exists( full_path ):
            try:
                youtube = YouTube("https://www.youtube.com/watch?v="+video_id)
                print 'downloading', video_id
            except:
                return
            try:
                video = youtube.streams.get_by_itag(18)
            except:
                ipdb.set_trace()
            video.download('videos')
            os.rename(os.path.join('videos',video.default_filename), full_path )
        print 'converting', video_id
        cap = vreader(full_path)
        frames = []
        frame_count = 0
        for frame in cap:
            frame_count += 1
            if start*30 <= frame_count <= end*30:
                frames.append(frame)
        frames = np.array(frames)
        writer = vwrite(save_path, frames)
        if os.path.exists( full_path ):
            os.remove(full_path)

def main():
    video_data_path='./data/video_corpus.csv'
    video_data = pd.read_csv(video_data_path, sep=',')
    video_data = video_data[video_data['Language'] == 'English']
    video_data['video_path'] = video_data.apply(lambda row: row['VideoID']+'_'+str(row['Start'])+'_'+str(row['End'])+'.avi', axis=1)
    video_data.apply(lambda row: download_and_process_video(row), axis=1)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for i in range(len(video_data)):
        pool.apply_async(download_and_process_video, args=(video_data[i], ))
    pool.close()
    pool.join()

if __name__=="__main__":
    main()
