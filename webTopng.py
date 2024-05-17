import os
import cv2
import numpy as np
from PIL import Image
 
def remove_background_grabcut(image):
    # GrabCut을 위해 전경과 배경을 정의
    mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    # 전경 객체의 바운딩 박스 계산
    rect = (50, 50, image.shape[1]-50, image.shape[0]-50)
    # GrabCut 실행
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    # 배경에 해당하는 부분은 0, 그 외는 1로 마스크 설정
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    # 원본 이미지에 마스크를 곱하여 배경 제거
    result = image * mask2[:, :, np.newaxis]
 
    # 알파 채널을 추가하여 배경을 투명하게 만듦
    alpha = np.ones(image.shape[:2], dtype=np.uint8) * 255  # 모든 픽셀을 불투명으로 초기화
    alpha[mask2 == 0] = 0  # 배경에 해당하는 부분을 투명하게 처리
    result = cv2.merge((result, alpha))
 
    return result
 
def convert_webp_to_png(source_dir, output_dir):
    # 출력 디렉터리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
 
    # 지정된 디렉터리를 순회하며 모든 웹파일 찾기
    for filename in os.listdir(source_dir):
        if filename.endswith('.webp'):
            # 원본 파일 경로
            source_path = os.path.join(source_dir, filename)
            # 출력 파일 경로
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.png")
 
            # 웹피 파일을 OpenCV로 읽기
            image = cv2.imread(source_path)
            # 배경 제거 및 투명한 배경으로 처리
            result = remove_background_grabcut(image)
            # OpenCV 이미지를 PIL 이미지로 변환
            result_pil = Image.fromarray(result)
            # PNG로 저장
            result_pil.save(output_path, 'PNG')
            print(f"Converted {source_path} to {output_path}")
 
# 사용 예시
source_directory = 'webp_dir'
output_directory = 'png_dir'
convert_webp_to_png(source_directory, output_directory)
