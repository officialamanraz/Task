# import asyncio
# import requests  # Ye nayi library add ki hai
# from deep_translator import GoogleTranslator
# import edge_tts
# from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
# import time
# DEEPGRAM_API_KEY = "26f724217fb89666e715b234672982d60303bb4e"

# def transcript_with_time(video_path):
#     print("1. Video se MP3 nikal rahe hain...")
#     video = VideoFileClip(video_path)
#     video.audio.write_audiofile("temp.mp3") 
    
#     print("2. Deepgram se STT le rahe hain (Isme 1-2 minute lag sakte hain, kripya wait karein)...")
    
#     # Direct API URL aur settings
#     url = "https://api.deepgram.com/v1/listen?model=nova-2&language=en&smart_format=true&utterances=true"
    
#     headers = {
#         "Authorization": f"Token {DEEPGRAM_API_KEY}",
#         "Content-Type": "audio/mp3"
#     }
    
#     # Direct Requests ka use, jisme humne timeout 600 second (10 minute) diya hai
#     with open("temp.mp3", "rb") as file:
#         response = requests.post(url, headers=headers, data=file, timeout=600)
        
#     # Output ko JSON mein convert karein
#     response_data = response.json()
#     if "results" not in response_data:
#         print("\n--- DEEPGRAM ERROR RESPONSE ---")
#         print(response_data)
#         return []
#     utterances = response_data["results"]["utterances"]
    
#     script_data = []
#     for u in utterances:
#         script_data.append({
#             "text": u["transcript"],
#             "start": u["start"],
#             "end": u["end"]
#         })
        
#     return script_data


# import time

# def translate(script_data):
#     print("\n3. English text ko Hindi mein translate kar rahe hain (Safe Batch Mode)...")
    
#     translator = GoogleTranslator(source='auto', target='hi')
#     translated_script = []
    
#     # Ek sath saari lines bhejne ki bajaye, hum 10-10 line ke chunks mein bhejenge
#     chunk_size = 10
#     for i in range(0, len(script_data), chunk_size):
#         chunk = script_data[i:i + chunk_size]
#         english_texts = [line["text"] for line in chunk]
        
#         try:
#             # Batch translate with safety pause
#             hindi_texts = translator.translate_batch(english_texts)
#         except Exception as e:
#             print(f"Error aaya, 2 second wait karke retry kar rahe hain... ({e})")
#             time.sleep(3)
#             hindi_texts = translator.translate_batch(english_texts)
            
#         # Data jod rahe hain
#         for j in range(len(chunk)):
#             translated_script.append({
#                 "start": chunk[j]["start"],
#                 "end": chunk[j]["end"],
#                 "en_text": english_texts[j],
#                 "hi_text": hindi_texts[j]
#             })
#             print(f"EN: {english_texts[j]}")
#             print(f"HI: {hindi_texts[j]}\n")
            
#         # Google ko khush rakhne ke liye har chunk ke baad 1 second ka aram
#         time.sleep(1)
        
#     return translated_script
# if __name__ == "__main__":
#     # Apni video ka sahi naam yahan dalein
#     data = transcript_with_time("Vertical Tabs Come to Chrome!_1080p.mp4")
#     hindi_data=translate(data)
#     print("\n--- DEEPGRAM TIMESTAMPS ---")
#     for line in data:
#         print(f"Time: {line['start']}s to {line['end']}s - Text: {line['text']}")
# import sys
# import io
# import time
# import asyncio
# import requests
# from translate import Translator
# import edge_tts
# from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

# # Windows terminal mein Hindi characters (UTF-8) print karne ke liye
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# DEEPGRAM_API_KEY = "26f724217fb89666e715b234672982d60303bb4e"

# def transcript_with_time(video_path):
#     print("1. Video se MP3 nikal rahe hain...")
#     video = VideoFileClip(video_path)
#     video.audio.write_audiofile("temp.mp3", logger=None) 
    
#     print("2. Deepgram se STT le rahe hain...")
#     url = "https://api.deepgram.com/v1/listen?model=nova-2&language=en&smart_format=true&utterances=true"
#     headers = {
#         "Authorization": f"Token {DEEPGRAM_API_KEY}",
#         "Content-Type": "audio/mp3"
#     }
    
#     with open("temp.mp3", "rb") as file:
#         audio_data = file.read()
        
#     response = requests.post(url, headers=headers, data=audio_data, timeout=600)
#     response_data = response.json()
    
#     if "results" not in response_data:
#         print("Deepgram Error:", response_data)
#         return []
        
#     utterances = response_data["results"]["utterances"]
#     script_data = []
#     for u in utterances:
#         script_data.append({
#             "text": u["transcript"],
#             "start": u["start"],
#             "end": u["end"]
#         })
#     return script_data

# def translate_safely(script_data):
#     print("\n3. English text ko Hindi mein translate kar rahe hain...")
#     translator = Translator(to_lang="hi")
#     translated_script = []
    
#     for index, line in enumerate(script_data):
#         en_text = line["text"]
#         try:
#             hi_text = translator.translate(en_text)
#             if not hi_text or "MYMEMORY" in hi_text:
#                 hi_text = en_text
#         except Exception as e:
#             time.sleep(1)
#             hi_text = en_text
            
#         translated_script.append({
#             "start": line["start"],
#             "end": line["end"],
#             "en_text": en_text,
#             "hi_text": hi_text
#         })
#         print(f"[{index+1}/{len(script_data)}] HI: {hi_text}")
#         time.sleep(0.2)
        
#     return translated_script

# # --- TTS aur Video Syncing Function (Fixed) ---
# # async def make_tts_andsync(hindi_script, video_path):
# #     print("\n4. Edge-TTS se Hindi Audio generate kar rahe hain aur Video mein sync kar rahe hain...")
    
# #     audio_clips = []
# #     voice = "hi-IN-SwaraNeural" 
# #     current_end_time=0.0
# #     # Natural sounding Hindi voice
    
# #     for index, item in enumerate(hindi_script):
# #         text = item["hi_text"]
# #         start_time = item["start"] # yahan spelling theek ki gai hai
        
# #         audio_filename = f"temp_audio_{index}.mp3"
        
# #         # 'Communicate' ka C capital hona zaroori hai
# #         communicate = edge_tts.Communicate(text, voice)
# #         await communicate.save(audio_filename)
        
# #         # if AudioFileClip(audio_filename).duration > 0:
# #         #     clip = AudioFileClip(audio_filename).with_start(start_time)
# #         #     audio_clips.append(clip)
            

# #         audio_clip=AudioFileClip(audio_filename)
# #         if audio_clip.duration>0:
# #             safe_start_time= max(start_time,current_end_time)
# #             clip=audio_clip.with_start(safe_start_time)
# #             audio_clip.append(clip)
# #             current_end_time=safe_start_time+clip.duration

# #         print(f"Processed audio clip {index+1}/{len(hindi_script)}")

# #     print("\n5. Original video load karke nayi dubbed audio merge kar rahe hain...")
# #     video = VideoFileClip(video_path) # AudioFileClip ki jagah VideoFileClip
    
# #     final_audio = CompositeAudioClip(audio_clips)
# #     final_video = video.with_audio(final_audio) # variable name match kiya gaya hai
    
# #     output_filename = "output_dubbed.mp4"
# #     print(f"Video export ho rahi hai: {output_filename} ... Kripya wait karein.")
    
# #     final_video.write_videofile(
# #         output_filename, 
# #         codec="libx264", 
# #         audio_codec="aac", 
# #         fps=video.fps
# #     )
# #     print("\n🎉 BADHAI HO! Aapki Dubbed Video taiyar ho gayi hai:", output_filename)
# async def make_tts_andsync(hindi_script, video_path):
#     print("\n4. Edge-TTS se Hindi Audio generate kar rahe hain aur Video mein sync kar rahe hain...")
    
#     # Notice the "s" here - this is the list!
#     audio_clips = []
#     voice = "hi-IN-SwaraNeural" 
#     current_end_time = 0.0  
    
#     for index, item in enumerate(hindi_script):
#         text = item["hi_text"]
#         start_time = item["start"] 
        
#         audio_filename = f"temp_audio_{index}.mp3"
        
#         communicate = edge_tts.Communicate(text, voice)
#         await communicate.save(audio_filename)
        
#         # Notice no "s" here - this is the individual file!
#         current_audio = AudioFileClip(audio_filename)
#         if current_audio.duration > 0:
            
#             # SMART LOGIC: Wait if the previous audio is still playing
#             safe_start_time = max(start_time, current_end_time)
            
#             clip = current_audio.with_start(safe_start_time)
            
#             # Appending to the plural list
#             audio_clips.append(clip)
            
#             current_end_time = safe_start_time + clip.duration
            
#         print(f"Processed audio clip {index+1}/{len(hindi_script)}")

#     print("\n5. Original video load karke nayi dubbed audio merge kar rahe hain...")
#     video = VideoFileClip(video_path) 
    
#     # Merging the plural list
#     final_audio = CompositeAudioClip(audio_clips)
#     final_video = video.with_audio(final_audio) 
    
#     output_filename = "output_dubbed.mp4"
#     print(f"Video export ho rahi hai: {output_filename} ... Kripya wait karein.")
    
#     final_video.write_videofile(
#         output_filename, 
#         codec="libx264", 
#         audio_codec="aac", 
#         fps=video.fps
#     )
#     print("\n🎉 BADHAI HO! Aapki Dubbed Video taiyar ho gayi hai:", output_filename)

# if __name__ == "__main__":
#     video_file = "Vertical Tabs Come to Chrome!_1080p.mp4"
    
#     # Step 1 & 2: STT
#     data = transcript_with_time(video_file)
    
#     if data:
#         # Step 3: Translation
#         hindi_data = translate_safely(data)
        
#         # Step 4 & 5: TTS and Video Syncing
#         asyncio.run(make_tts_andsync(hindi_data, video_file))
# import sys
# import io
# import time
# import asyncio
# import requests
# import os
# import json
# import subprocess
# from tqdm import tqdm
# from colorama import init, Fore, Style
# from translate import Translator

# # Force Windows terminal encoding
# init(autoreset=True)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # Auto-install/upgrade TTS libraries so ModuleNotFoundError never happens
# try:
#     import edge_tts
#     from gtts import gTTS
# except ModuleNotFoundError:
#     print("[System] Installing required TTS libraries... Please wait.")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "edge-tts", "gTTS"])
#     import edge_tts
#     from gtts import gTTS

# # ---------------- CONFIGURATION ----------------
# # PASTE YOUR ACTUAL DEEPGRAM KEY INSIDE THE QUOTES BELOW:
# DEEPGRAM_API_KEY = "ea117c4a22e2e47af431de8a7a0b06c4fff83e62"

# # Male Voice selected for male speaker video:
# VOICE_MODEL = "hi-IN-MadhurNeural"  # Male: hi-IN-MadhurNeural | Female: hi-IN-SwaraNeural
# # -----------------------------------------------

# try:
#     from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
# except ModuleNotFoundError:
#     from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

# def adjust_speed(clip, factor):
#     try:
#         # MoviePy v2 built-in speed function
#         return clip.with_speed_scaled(factor)
#     except AttributeError:
#         try:
#             # MoviePy v1 fallback
#             import moviepy.audio.fx.all as afx
#             return clip.fx(afx.speedx, factor)
#         except Exception:
#             return clip

# def adjust_volume(clip, factor):
#     try:
#         import moviepy.audio.fx.all as afx
#         return clip.fx(afx.volumex, factor) 
#     except:
#         try:
#             from moviepy.audio.fx.MultiplyVolume import MultiplyVolume
#             return clip.with_effects([MultiplyVolume(factor)]) 
#         except:
#             return clip 

# def transcript_with_time(video_path):
#     if "PASTE_YOUR" in DEEPGRAM_API_KEY or not DEEPGRAM_API_KEY.strip():
#         print(f"{Fore.RED}[ERROR] You forgot to paste your real Deepgram API Key on Line 26!{Style.RESET_ALL}")
#         return []

#     print("\n--- [STEP 1] Extracting Audio & Fetching STT from Deepgram ---")
#     video = VideoFileClip(video_path)
#     video.audio.write_audiofile("temp_main_audio.mp3", logger=None) 
    
#     url = "https://api.deepgram.com/v1/listen?model=nova-2&language=en&smart_format=true&utterances=true&utt_split=0.4"
#     headers = {
#         "Authorization": f"Token {DEEPGRAM_API_KEY.strip()}",
#         "Content-Type": "audio/mp3"
#     }
    
#     with open("temp_main_audio.mp3", "rb") as file:
#         audio_data = file.read()
        
#     print(f"{Fore.LIGHTBLACK_EX}Uploading to Deepgram AI Cloud... (Please wait){Style.RESET_ALL}")
#     response = requests.post(url, headers=headers, data=audio_data, timeout=600)
#     response_data = response.json()
    
#     if "results" not in response_data:
#         print("Deepgram Error:", response_data)
#         return []
        
#     utterances = response_data["results"]["utterances"]
#     script_data = []
    
#     for u in utterances:
#         script_data.append({
#             "text": u["transcript"],
#             "start": u["start"],
#             "end": u["end"],
#             "duration": u["end"] - u["start"]
#         })
        
#     print(f"{Fore.GREEN}✅ Successfully mapped {len(script_data)} timestamps from the video!")
#     return script_data


# def translate_safely(script_data):
#     print("\n--- [STEP 2] Translating English to Hindi ---")
#     translator = Translator(to_lang="hi")
#     translated_script = []
    
#     for line in tqdm(script_data, desc=f"{Fore.MAGENTA}Translating{Style.RESET_ALL}", unit="line"):
#         en_text = line["text"]
        
#         try:
#             hi_text = translator.translate(en_text)
#             if not hi_text or "MYMEMORY" in hi_text:
#                 hi_text = en_text
#         except Exception:
#             time.sleep(1) 
#             hi_text = en_text
            
#         translated_script.append({
#             "start": line["start"],
#             "end": line["end"],
#             "duration": line["duration"],
#             "en_text": en_text,
#             "hi_text": hi_text
#         })
#         time.sleep(0.2) 
        
#     print("✅ Translation Complete!")
#     return translated_script


# async def make_tts_andsync(hindi_script, video_path):
#     print("\n--- [STEP 3] Generating AI Voices & Syncing (Drift Protection) ---")
    
#     audio_clips = []
#     files_to_delete = ["temp_main_audio.mp3"] 
#     current_end_time = 0.0 
#     edge_blocked = False
    
#     for index, item in enumerate(tqdm(hindi_script, desc="Generating Audio", unit="clip")):
#         text = item["hi_text"]
#         start_time = item["start"] 
#         target_duration = item["duration"]
        
#         if not text or not text.strip():
#             continue
            
#         audio_filename = f"temp_audio_{index}.mp3"
#         files_to_delete.append(audio_filename) 
        
#         # Try Edge-TTS first; if Microsoft returns 403, fallback to Google TTS automatically
#         try:
#             if not edge_blocked:
#                 try:
#                     communicate = edge_tts.Communicate(text, VOICE_MODEL)
#                     await communicate.save(audio_filename)
#                     await asyncio.sleep(0.3)
#                 except Exception:
#                     if not edge_blocked:
#                         print(f"\n{Fore.YELLOW}[!] Edge-TTS returned 403. Switching to Google TTS fallback automatically...{Style.RESET_ALL}")
#                     edge_blocked = True
#                     tts = gTTS(text=text, lang="hi", slow=False)
#                     tts.save(audio_filename)
#             else:
#                 tts = gTTS(text=text, lang="hi", slow=False)
#                 tts.save(audio_filename)
#         except Exception as e:
#             print(f"\nSkipping clip {index} due to TTS error: {e}")
#             continue
            
#         if not os.path.exists(audio_filename) or os.path.getsize(audio_filename) == 0:
#             continue
            
#         current_audio = AudioFileClip(audio_filename)
#         actual_duration = current_audio.duration
        
#         if actual_duration > 0 and target_duration > 0: 
#             speed_factor = actual_duration / target_duration
#             speed_factor = max(0.9, speed_factor)
            
#             sync_audio = adjust_speed(current_audio, speed_factor)
            
#             safe_start_time = max(start_time, current_end_time)
#             finale_clip = sync_audio.with_start(safe_start_time)
            
#             audio_clips.append(finale_clip)
#             current_end_time = safe_start_time + finale_clip.duration

#     print("\n--- [STEP 4] Merging Audio & Exporting Final Video ---")
#     video = VideoFileClip(video_path) 
    
#     dubbed_hindi_audio = CompositeAudioClip(audio_clips)
    
#     # STRICT DRIFT PREVENTION (V1 & V2 Compatible)
#     try:
#         dubbed_hindi_audio = dubbed_hindi_audio.with_duration(video.duration)
#         final_video = video.with_audio(dubbed_hindi_audio)
#     except AttributeError:
#         dubbed_hindi_audio = dubbed_hindi_audio.set_duration(video.duration)
#         final_video = video.set_audio(dubbed_hindi_audio)
    
#     output_filename = "FINAL_DUBBED_PRO.mp4"
#     print(f"{Fore.LIGHTBLACK_EX}Rendering final high-quality video...{Style.RESET_ALL}")
        
#     final_video.write_videofile(
#         output_filename, 
#         codec="libx264", 
#         audio_codec="aac", 
#         fps=video.fps,
#         logger="bar" 
#     )
    
#     print("\n--- [STEP 5] Cleaning up temporary files ---")
#     for temp_file in files_to_delete:
#         try:
#             os.remove(temp_file)
#         except Exception:
#             pass
            
#     print("\n🎉 SUCCESS! Your fully dubbed, synchronized video is ready:", output_filename)


# if __name__ == "__main__":
#     video_file = "Improve your Speaking and Conversational skills with me _ English Speaking Practice - English Fluency Journey (1080p, h264).mp4"
#     cache_file = "saved_hindi_data.json"
    
#     # Load from cache if Step 1 & 2 already ran!
#     if os.path.exists(cache_file):
#         print(f"\n{Fore.GREEN}✅ Found saved translation cache ('{cache_file}')! Skipping Step 1 & Step 2...{Style.RESET_ALL}")
#         with open(cache_file, "r", encoding="utf-8") as f:
#             hindi_data = json.load(f)
#     else:
#         data = transcript_with_time(video_file)
#         if data:
#             hindi_data = translate_safely(data)
#             with open(cache_file, "w", encoding="utf-8") as f:
#                 json.dump(hindi_data, f, ensure_ascii=False, indent=2)
#         else:
#             hindi_data = []
            
#     if hindi_data:
#         asyncio.run(make_tts_andsync(hindi_data, video_file))
# import time

# def number_to_words(n):
#     if n == 10000000000000000000000000000000000:
#         return "one million"
    
#     ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
#     teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
#     tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
#     def convert_under_1000(num):
#         words = ""
#         if num >= 100:
#             words += ones[num // 100] + " hundred "
#             num %= 100
#         if num >= 10 and num <= 19:
#             words += teens[num - 10] + " "
#             num = 0
#         elif num >= 20:
#             words += tens[num // 10] + " "
#             num %= 10
#         if num > 0 and num <= 9:
#             words += ones[num] + " "
#         return words.strip()
        
#     result = ""
#     if n >= 1000:
#         result += convert_under_1000(n // 1000) + " thousand "
#         n %= 1000
    
#     if n > 0:
#         result += convert_under_1000(n)
        
#     return result.strip()

# start_time = time.time()
# filename = "one_to_one_million.txt"

# print(f"Starting the count to 1,000,000... This will take about 2 seconds.")

# # Writing to a file is much faster than printing 1 million lines to a screen
# with open(filename, "w") as file:
#     for i in range(1, 1000001):
#         word = number_to_words(i)
#         # Removes spaces and separates each letter with a dash
#         letters = "-".join(list(word.replace(" ", ""))) 
        
#         # Output format: 1 | one | o-n-e
#         file.write(f"{i} | {word} | {letters}\n")

# end_time = time.time()
# print(f"Success! Counted to 1,000,000 in {end_time - start_time:.2f} seconds.")
# print(f"Your output is saved in the file: {filename}")


# from num2words import num2words

# output_file = "numbers_1_to_1000000.txt"

# with open(output_file, "w", encoding="utf-8") as file:
#     for number in range(1, 10):
#         words = num2words(number, lang="en").title()
#         file.write(f"{number} - {words}\n")

# print("Completed! All numbers from 1 to 1,000,000 are saved.")
# print(f"File: {output_file}")
import sys
import io
import time
import asyncio
import requests
import os
import json
import subprocess
import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
from tqdm import tqdm
from colorama import init, Fore, Style
from translate import Translator

# Force Windows terminal encoding
init(autoreset=True)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Auto-install/upgrade TTS libraries so ModuleNotFoundError never happens
try:
    import edge_tts
    from gtts import gTTS
except ModuleNotFoundError:
    print("[System] Installing required TTS libraries... Please wait.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "edge-tts", "gTTS"])
    import edge_tts
    from gtts import gTTS

# ---------------- CONFIGURATION ----------------
DEEPGRAM_API_KEY = "ea117c4a22e2e47af431de8a7a0b06c4fff83e62"

# Male Voice selected for male speaker video:
VOICE_MODEL = "hi-IN-SwaraNeural"  # Male: hi-IN-MadhurNeural | Female: hi-IN-SwaraNeural
# -----------------------------------------------

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
except ModuleNotFoundError:
    from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

def adjust_speed(clip, factor):
    try:
        # MoviePy v2 built-in speed function
        return clip.with_speed_scaled(factor)
    except AttributeError:
        try:
            # MoviePy v1 fallback
            import moviepy.audio.fx.all as afx
            return clip.fx(afx.speedx, factor)
        except Exception:
            return clip

def adjust_volume(clip, factor):
    try:
        import moviepy.audio.fx.all as afx
        return clip.fx(afx.volumex, factor) 
    except:
        try:
            from moviepy.audio.fx.MultiplyVolume import MultiplyVolume
            return clip.with_effects([MultiplyVolume(factor)]) 
        except:
            return clip 

def trim_silence(input_path, output_path):
    # Removes dead silence at the start and end of the TTS file
    cmd = [
        FFMPEG_EXE, "-y", "-i", input_path,
        "-af", "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-40dB,areverse",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def change_speed_keep_pitch(input_path, output_path, factor):
    # Locks speed between 0.9x and 1.5x and keeps 100% natural human pitch
    safe_factor = max(0.9, min(factor, 1.5))
    cmd = [
        FFMPEG_EXE, "-y", "-i", input_path,
        "-filter:a", f"atempo={safe_factor}",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)        

def transcript_with_time(video_path):
    if "PASTE_YOUR" in DEEPGRAM_API_KEY or not DEEPGRAM_API_KEY.strip():
        print(f"{Fore.RED}[ERROR] You forgot to paste your real Deepgram API Key!{Style.RESET_ALL}")
        return []

    print("\n--- [STEP 1] Extracting Audio & Fetching STT from Deepgram ---")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile("temp_main_audio.mp3", logger=None) 
    
    url = "https://api.deepgram.com/v1/listen?model=nova-2&language=en&smart_format=true&utterances=true&utt_split=0.4"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY.strip()}",
        "Content-Type": "audio/mp3"
    }
    
    with open("temp_main_audio.mp3", "rb") as file:
        audio_data = file.read()
        
    print(f"{Fore.LIGHTBLACK_EX}Uploading to Deepgram AI Cloud... (Please wait){Style.RESET_ALL}")
    response = requests.post(url, headers=headers, data=audio_data, timeout=600)
    response_data = response.json()
    
    if "results" not in response_data:
        print("Deepgram Error:", response_data)
        return []
        
    utterances = response_data["results"]["utterances"]
    script_data = []
    
    for u in utterances:
        script_data.append({
            "text": u["transcript"],
            "start": u["start"],
            "end": u["end"],
            "duration": u["end"] - u["start"]
        })
        
    print(f"{Fore.GREEN}✅ Successfully mapped {len(script_data)} timestamps from the video!")
    return script_data


def translate_safely(script_data):
    print("\n--- [STEP 2] Translating English to Hindi ---")
    translator = Translator(to_lang="hi")
    translated_script = []
    
    for line in tqdm(script_data, desc=f"{Fore.MAGENTA}Translating{Style.RESET_ALL}", unit="line"):
        en_text = line["text"]
        
        try:
            hi_text = translator.translate(en_text)
            if not hi_text or "MYMEMORY" in hi_text:
                hi_text = en_text
        except Exception:
            time.sleep(1) 
            hi_text = en_text
            
        translated_script.append({
            "start": line["start"],
            "end": line["end"],
            "duration": line["duration"],
            "en_text": en_text,
            "hi_text": hi_text
        })
        time.sleep(0.2) 
        
    print("✅ Translation Complete!")
    return translated_script


async def make_tts_andsync(hindi_script, video_path):
    print("\n--- [STEP 3] Generating AI Voices & Syncing (Drift Protection) ---")
    
    audio_clips = []
    files_to_delete = ["temp_main_audio.mp3"] 
    current_end_time = 0.0 
    edge_blocked = False
    
    for index, item in enumerate(tqdm(hindi_script, desc="Generating Audio", unit="clip")):
        text = item["hi_text"]
        start_time = item["start"] 
        target_duration = item["duration"]
        
        if not text or not text.strip():
            continue
            
        audio_filename = f"temp_audio_{index}.mp3"
        files_to_delete.append(audio_filename) 
        
        # Try Edge-TTS first; if Microsoft returns 403, fallback to Google TTS automatically
        try:
            if not edge_blocked:
                try:
                    communicate = edge_tts.Communicate(text, VOICE_MODEL)
                    await communicate.save(audio_filename)
                    await asyncio.sleep(0.3)
                except Exception:
                    if not edge_blocked:
                        print(f"\n{Fore.YELLOW}[!] Edge-TTS returned 403. Switching to Google TTS fallback automatically...{Style.RESET_ALL}")
                    edge_blocked = True
                    tts = gTTS(text=text, lang="hi", slow=False)
                    tts.save(audio_filename)
            else:
                tts = gTTS(text=text, lang="hi", slow=False)
                tts.save(audio_filename)
        except Exception as e:
            print(f"\nSkipping clip {index} due to TTS error: {e}")
            continue
            
        if not os.path.exists(audio_filename) or os.path.getsize(audio_filename) == 0:
            continue

        # 1. Trim dead silence from the TTS MP3 so short lines don't get crushed
        trimmed_wav = f"temp_trimmed_{index}.wav"
        synced_wav = f"temp_synced_{index}.wav"
        files_to_delete.extend([trimmed_wav, synced_wav])

        trim_silence(audio_filename, trimmed_wav)
        if not os.path.exists(trimmed_wav):
            trimmed_wav = audio_filename

        trimmed_clip = AudioFileClip(trimmed_wav)
        actual_duration = trimmed_clip.duration
        trimmed_clip.close()

        # 2. Check if there is a silent pause before the next sentence starts
        if index + 1 < len(hindi_script):
            gap_to_next = hindi_script[index + 1]["start"] - item["end"]
            extra_room = min(max(0.0, gap_to_next - 0.1), 0.6) # Borrow up to 0.6s of silence if available
        else:
            extra_room = 0.0

        allowed_duration = target_duration + extra_room

        # 3. Adjust speed WITHOUT changing pitch (no chipmunk voice!)
        if actual_duration > 0 and allowed_duration > 0:
            speed_factor = actual_duration / allowed_duration
            change_speed_keep_pitch(trimmed_wav, synced_wav, speed_factor)

            sync_audio = AudioFileClip(synced_wav)
            safe_start_time = max(start_time, current_end_time)
            finale_clip = sync_audio.with_start(safe_start_time)

            audio_clips.append(finale_clip)
            current_end_time = safe_start_time + finale_clip.duration

    print("\n--- [STEP 4] Merging Audio & Exporting Final Video ---")
    video = VideoFileClip(video_path) 
    
    dubbed_hindi_audio = CompositeAudioClip(audio_clips)
    
    # STRICT DRIFT PREVENTION (V1 & V2 Compatible)
    try:
        dubbed_hindi_audio = dubbed_hindi_audio.with_duration(video.duration)
        final_video = video.with_audio(dubbed_hindi_audio)
    except AttributeError:
        dubbed_hindi_audio = dubbed_hindi_audio.set_duration(video.duration)
        final_video = video.set_audio(dubbed_hindi_audio)
    
    output_filename = "FINAL_DUBBED_PRO.mp4"
    print(f"{Fore.LIGHTBLACK_EX}Rendering final high-quality video...{Style.RESET_ALL}")
        
    final_video.write_videofile(
        output_filename, 
        codec="libx264", 
        audio_codec="aac", 
        fps=video.fps,
        logger="bar" 
    )
    
    print("\n--- [STEP 5] Cleaning up temporary files ---")
    for temp_file in files_to_delete:
        try:
            os.remove(temp_file)
        except Exception:
            pass
            
    print("\n🎉 SUCCESS! Your fully dubbed, synchronized video is ready:", output_filename)


if __name__ == "__main__":
    video_file = "Improve your Speaking and Conversational skills with me _ English Speaking Practice - English Fluency Journey (1080p, h264).mp4"
    cache_file = "saved_hindi_data.json"
    
    # Load from cache if Step 1 & 2 already ran!
    if os.path.exists(cache_file):
        print(f"\n{Fore.GREEN}✅ Found saved translation cache ('{cache_file}')! Skipping Step 1 & Step 2...{Style.RESET_ALL}")
        with open(cache_file, "r", encoding="utf-8") as f:
            hindi_data = json.load(f)
    else:
        data = transcript_with_time(video_file)
        if data:
            hindi_data = translate_safely(data)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(hindi_data, f, ensure_ascii=False, indent=2)
        else:
            hindi_data = []
            
    if hindi_data:
        asyncio.run(make_tts_andsync(hindi_data, video_file))