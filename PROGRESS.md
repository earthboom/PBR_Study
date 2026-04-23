# 학습 진행 상황

## 현재 Phase: Phase 1 진행 중 — 다음 작업: Ch.3 Rays, a Simple Camera

---

## 환경 세팅

- [x] PBR 4th Edition 웹버전 로컬 저장 (`pbr4ed/` 폴더)
- [x] C++ 개발환경 세팅 (Rider + MSVC + CMake)
- [ ] GitHub 계정 및 레포 생성

---

## Phase 1 — CPU 레이트레이서

**시작일**: 2026-04-23
**완료일**: -

### Ray Tracing in One Weekend (1권)
- [x] Ch.1 Output an Image — PPM 포맷, 이미지 좌표계, 색상 정규화
- [x] Ch.2 The vec3 Class — 내적/외적/정규화, point3/color 별칭
- [x] Ch.3 Rays, a Simple Camera — ray 클래스, 뷰포트, 선형 보간 배경
- [x] Ch.4 Adding a Sphere — 광선-구 교차, 이차방정식, 법선 시각화
- [ ] **Ch.5 Surface Normals ← 현재 위치**
- [ ] Ch.5 Surface Normals
- [ ] Ch.6 Antialiasing
- [ ] Ch.7 Diffuse Materials
- [ ] Ch.8 Metal
- [ ] Ch.9 Dielectrics
- [ ] Ch.10 Positionable Camera
- [ ] Ch.11 Defocus Blur

### Ray Tracing: The Next Week (2권)
- [ ] Motion Blur
- [ ] BVH
- [ ] Texture Mapping
- [ ] Perlin Noise
- [ ] Lights
- [ ] Cornell Box
- [ ] Volumes

### Ray Tracing: The Rest of Your Life (3권)
- [ ] Monte Carlo 기초
- [ ] PDF 샘플링
- [ ] 중요도 샘플링

### PBR 책 연결
- [ ] Ch.2 Monte Carlo Integration 읽기
- [ ] Ch.4 Radiometry 읽기
- [ ] 코드와 수식 연결 정리

---

## Phase 2 — 실시간 PBR 렌더러

**시작일**: -
**완료일**: -

- [ ] OpenGL 환경 세팅
- [ ] GGX BRDF 구현
- [ ] Cook-Torrance 구현
- [ ] HDR + Tone Mapping
- [ ] IBL Diffuse
- [ ] IBL Specular
- [ ] UE5 비교 스크린샷

---

## Phase 3 — UE5 커스텀 렌더링

**시작일**: -
**완료일**: -

- [ ] UE5 소스 빌드
- [ ] RDG 구조 파악
- [ ] 커스텀 패스 추가
- [ ] 심화 기능 구현
- [ ] Before/After 영상 촬영

---

## Phase 4 — 심화

**시작일**: -
**완료일**: -
**선택 방향**: (Phase 3 완료 후 결정)

---

## 메모 / 막혔던 부분

| 날짜 | 내용 | 해결 |
|------|------|------|
| 2026-04-23 | MSVC가 한글 주석을 코드 페이지 949로 읽어 파싱 오류 | CMakeLists.txt에 `/utf-8` 옵션 추가 |
| 2026-04-23 | 실행 파일 작업 디렉토리가 빌드 폴더라 output/ 경로를 못 찾음 | 코드에서 `std::filesystem::create_directories()` 로 직접 생성 |
