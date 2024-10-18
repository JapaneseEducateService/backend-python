# import librosa
# import numpy as np
# from scipy.spatial.distance import euclidean
# from fastdtw import fastdtw
# from dtw import *
# from sklearn.preprocessing import MinMaxScaler
# import core.google_text_to_speech as google_text_to_speech

# def get_pitch_comparison(audioFile, referenceText):
#   try:
#     def extract_pitch(audio_file):
#       y, sr = librosa.load(audio_file)
#       pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#       pitch_track = []
#       for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         if pitch > 0:  # 음소거 구간 제거
#           pitch_track.append(pitch)
#       # 정규화
#       scaler = MinMaxScaler()
#       pitch_track = scaler.fit_transform(np.array(pitch_track).reshape(-1, 1))
#       return pitch_track

#     def analyze_pitch_changes(pitch_track):
#       changes = []
#       for i in range(1, len(pitch_track)):
#         if pitch_track[i] > pitch_track[i-1]:
#           changes.append(1)  # 증가
#         elif pitch_track[i] < pitch_track[i-1]:
#           changes.append(-1)  # 감소
#         else:
#           changes.append(0)  # 동일
#       return changes

#     def compare_changes(changes1, changes2):
#       # Apply DTW to align the two time series data
#       changes1 = np.array(changes1).reshape(-1, 1)
#       changes2 = np.array(changes2).reshape(-1, 1)
#       distance, path = fastdtw(changes1, changes2, dist=euclidean)

#       # Normalize the DTW distance to get a similarity score between 0 and 100
#       max_distance = np.sqrt(len(changes1)**2 + len(changes2)**2)
#       similarity = 100 - (distance / max_distance) * 100

#       return similarity

#     TTSAudioFile = google_text_to_speech.get_TTS(referenceText)

#     # 음성 파일에서 피치 추출 및 변화 분석
#     pitch_track_1 = extract_pitch(audioFile)
#     pitch_track_2 = extract_pitch(TTSAudioFile)

#     changes1 = analyze_pitch_changes(pitch_track_1)
#     changes2 = analyze_pitch_changes(pitch_track_2)

#     # 변화 구간의 유사성 비교
#     similarity_score = compare_changes(changes1, changes2)

#     return similarity_score
#   except Exception as e:
#     return {'error': str(e)}


import librosa
import numpy as np
import core.google_text_to_speech as google_text_to_speech

def get_pitch_comparison(audioFile, referenceText):
  TTSAudioFile = google_text_to_speech.get_TTS(referenceText)
  try:
    def extract_prosodic_features(file_path):
      try:
        # 오디오 파일 로드
        y, sr = librosa.load(file_path)
      except Exception as e:
        print(f"오디오 파일 로드 오류: {e}")
        return None, None, None, None
      
      # librosa의 piptrack 또는 pyin을 사용하여 피치(기본 주파수) 추출
      pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
      pitch = [pitches[:, i][magnitudes[:, i].argmax()] for i in range(pitches.shape[1])]
      pitch = np.array([p for p in pitch if p > 0])
      
      # 에너지(스트레스의 대리 변수) 추출
      energy = librosa.feature.rms(y=y)[0]
      
      # 템포(말하기 속도) 추출
      tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
      
      # 지속 시간(프레임 수) 추출
      duration = librosa.get_duration(y=y, sr=sr)
      
      return pitch, energy, tempo, duration

    def calculate_prosody_score(pitch, energy, tempo, duration):
      # 피치 점수 계산 (예: 피치의 분산)
      pitch_score = np.var(pitch) if len(pitch) > 0 else 0
      
      # 에너지 점수 계산 (예: 평균 에너지)
      energy_score = np.mean(energy) if len(energy) > 0 else 0
      
      # 템포 점수 계산 (예: 템포)
      tempo_score = tempo
      
      # 지속 시간 점수 계산 (예: 총 지속 시간)
      duration_score = duration
      
      # 동적으로 점수 정규화
      pitch_score = pitch_score / (np.max(pitch) if np.max(pitch) > 0 else 1)
      energy_score = energy_score / (np.max(energy) if np.max(energy) > 0 else 1)
      tempo_score = tempo_score / 300  # 합리적인 최대 템포 가정
      duration_score = duration_score / 60  # 최대 지속 시간을 60초로 가정
      
      # 가중치로 전체 운율 점수 계산 (필요에 따라 가중치 조정)
      weights = [0.4, 0.3, 0.2, 0.1]  # 피치, 에너지, 템포, 지속 시간에 대한 가중치
      prosody_score = (weights[0]*pitch_score + weights[1]*energy_score +
              weights[2]*tempo_score + weights[3]*duration_score)
      
      return prosody_score

    def evaluate_prosody(file_path):
      pitch, energy, tempo, duration = extract_prosodic_features(file_path)
      if pitch is None or energy is None:
        return None
      prosody_score = calculate_prosody_score(pitch, energy, tempo, duration)
      return prosody_score

    # audioFile의 운율 점수 평가
    prosody_score_audio = evaluate_prosody(audioFile)
    # TTSAudioFile의 운율 점수 평가
    prosody_score_tts = evaluate_prosody(TTSAudioFile)

    if prosody_score_audio is not None and prosody_score_tts is not None:
      similarity_score = 100 - abs(prosody_score_audio - prosody_score_tts) * 100
      return similarity_score
    else:
      return "운율 점수를 평가할 수 없습니다."
  except Exception as e:
    return {'error': str(e)}
    