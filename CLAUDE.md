# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 세션 시작 시 필독

**새 세션을 시작할 때 반드시 `PROGRESS.md`를 먼저 읽어라.**
현재 어느 챕터를 진행 중인지, 막혔던 부분은 무엇인지 파악한 뒤 이어서 진행한다.
학습 전략 전체는 `LEARNING_STRATEGY.md`를 참고한다.

---

## 프로젝트 개요

UE5 클라이언트 프로그래머가 **그래픽스 프로그래머로 이직**하기 위한 PBR 실습 학습 공간.
실습 결과물은 GitHub 포트폴리오로 제출 예정.

- **학습 자료**: `pbr4ed/` — PBR 4th Edition 웹버전 로컬 저장본
- **레이트레이서 프로젝트**: `pbr-raytracer/` — C++17, CMake, Rider + MSVC
- **학습 노트**: `PHASE1_NOTES.md` — 챕터별 개념 정리 (수식 + 다이어그램 포함)
- **다이어그램 생성**: `generate_diagrams.py` — 학습 노트용 이미지 생성 스크립트

## 디렉토리 구조

```
PBR_Study/
├── CLAUDE.md
├── LEARNING_STRATEGY.md   ← 전체 4 Phase 학습 계획
├── PROGRESS.md            ← 현재 진행 상황 (세션 시작 시 필독)
├── PHASE1_NOTES.md        ← Phase 1 챕터별 학습 노트
├── generate_diagrams.py   ← 학습 다이어그램 생성
├── diagrams/              ← 생성된 다이어그램 이미지
├── pbr4ed/                ← PBR 4th Edition 웹버전
└── pbr-raytracer/         ← Phase 1 실습 프로젝트
    ├── CMakeLists.txt
    └── src/
        ├── main.cpp
        └── vec3.h
```

## 빌드 방법

Rider에서 CMake 프로파일(Debug-Visual Studio)로 빌드 및 실행.
출력 이미지는 실행 파일 기준 `output/` 폴더에 저장됨 (코드에서 자동 생성).

PPM → PNG 변환:
```bash
python -c "from PIL import Image; Image.open('path/to/file.ppm').save('path/to/file.png')"
```

## 주요 협업 규칙

- 챕터 완료 시 `PROGRESS.md` 체크박스를 업데이트한다
- 새 개념을 배울 때마다 `PHASE1_NOTES.md`에 수식 + 코드 + 다이어그램을 함께 기록한다
- 코드 주석은 한국어로 작성한다 (CMakeLists.txt에 `/utf-8` 옵션 적용되어 있음)
- IntelliSense 경고(`#include errors`)는 실제 빌드 오류가 아니므로 무시한다
