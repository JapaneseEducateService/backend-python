import librosa
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from dtw import *
import traceback
import core.google_text_to_speech as google_text_to_speech

def get_pitch_comparison(audioFile, referenceText):
  try:
    def extract_pitch(audio_file):
      y, sr = librosa.load(audio_file)
      pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
      pitch_track = []
      for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:  # 음소거 구간 제거
          pitch_track.append(pitch)
      return pitch_track

    def analyze_pitch_changes(pitch_track):
      changes = []
      for i in range(1, len(pitch_track)):
        if pitch_track[i] > pitch_track[i-1]:
          changes.append(1)  # 증가
        elif pitch_track[i] < pitch_track[i-1]:
          changes.append(-1)  # 감소
        else:
          changes.append(0)  # 동일
      return changes

    def compare_changes(changes1, changes2):
      # Apply DTW to align the two time series data
      changes1 = np.array(changes1).reshape(-1, 1)
      changes2 = np.array(changes2).reshape(-1, 1)
      distance, path = fastdtw(changes1, changes2, dist=euclidean)

      # Create new lists of changes that are aligned according to the DTW path
      aligned_changes1 = [changes1[i] for i, j in path]
      aligned_changes2 = [changes2[j] for i, j in path]

      total = max(len(aligned_changes1), len(aligned_changes2))
      matches = 0
      opposites = 0
      for c1, c2 in zip(aligned_changes1, aligned_changes2):
        if c1 == c2:
          matches += 1
        elif c1 == -c2:
          opposites += 1

      similarity = (matches / total) * 100
      if opposites == total:
        return 0  # 완전히 반대인 경우
      return similarity

    TTSAudioFile = google_text_to_speech.get_TTS(referenceText)

    # 음성 파일에서 피치 추출 및 변화 분석
    pitch_track_1 = extract_pitch(audioFile)
    pitch_track_2 = extract_pitch(TTSAudioFile)

    changes1 = analyze_pitch_changes(pitch_track_1)
    changes2 = analyze_pitch_changes(pitch_track_2)

    # 변화 구간의 유사성 비교
    similarity_score = compare_changes(changes1, changes2)

    print(f"유사성 점수: {similarity_score}%")

    return similarity_score
  except Exception as e:
    return {'error': str(e)}