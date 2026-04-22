# PBR 학습 전략

## 배경 및 목표

- **현재**: 언리얼5 클라이언트 프로그래머
- **목표**: 그래픽스 프로그래머로 이직
- **방법**: 실습 중심 학습 + Claude Code 적극 활용
- **산출물**: 각 Phase마다 GitHub 포트폴리오 구성

---

## 전체 전략

| 역할 | 내용 |
|------|------|
| **Claude Code** | 수학 설명, 코드 디버깅, 개념 질문, 코드 리뷰 |
| **본인** | 직접 코드 작성, 결과 확인, 이해 검증 |
| **PBR 책** | 개념 연결 레퍼런스 (처음부터 정독 X) |

---

## Phase 1 — CPU 레이트레이서 (3주)

**목표**: 빛이 어떻게 동작하는지 코드로 이해

**주요 자료**: [Ray Tracing in One Weekend](https://raytracing.github.io/) 3부작

**구현 목록**
- [ ] 기본 레이-구 교차
- [ ] Diffuse / Metal / Dielectric 재질
- [ ] BVH 가속 구조
- [ ] Monte Carlo 샘플링
- [ ] Cornell Box 씬

**포트폴리오 레포**: `pbr-raytracer`
- 렌더링 결과 이미지를 README 최상단에
- PBR 책 수식과 코드 연결 설명

---

## Phase 2 — 실시간 PBR 렌더러 (4주)

**목표**: UE5가 실제로 쓰는 방식 직접 구현

**주요 자료**: [LearnOpenGL PBR](https://learnopengl.com/PBR/Theory)

**구현 목록**
- [ ] GGX BRDF
- [ ] Cook-Torrance 모델
- [ ] HDR + Tone Mapping
- [ ] IBL — Diffuse Irradiance
- [ ] IBL — Specular (Split-Sum Approximation)

**포트폴리오 레포**: `realtime-pbr-renderer`
- 같은 씬을 UE5와 직접 만든 렌더러로 나란히 비교한 스크린샷

---

## Phase 3 — UE5 커스텀 렌더링 기능 (4주)

**목표**: 프로덕션 렌더러 코드를 읽고 수정할 수 있음을 증명

**작업 목록**
- [ ] UE5 소스코드 빌드
- [ ] RDG(Render Dependency Graph) 구조 파악
- [ ] 커스텀 렌더 패스 추가
- [ ] 심화 기능 구현 (아래 중 선택)

**심화 기능 후보**
- 커스텀 셰도우 기법
- 스크린 스페이스 서브서피스 스캐터링
- 커스텀 포스트 프로세스

**포트폴리오 레포**: `ue5-custom-renderer`
- UE5 렌더러 코드 수정 경험 + Before/After 영상

---

## Phase 4 — 심화 (3주)

Phase 3 완료 후 관심사에 따라 하나 선택:

| 방향 | 프로젝트 |
|------|---------|
| 레이트레이싱 | GPU 레이트레이서 (DXR / Vulkan RT) |
| 조명 | 커스텀 GI 구현 |
| 퍼포먼스 | 렌더링 최적화 (Culling, LOD) |

---

## 타임라인

| 기간 | Phase | 산출물 |
|------|-------|--------|
| 1~3주 | CPU 레이트레이서 | 렌더링 이미지 |
| 4~7주 | 실시간 PBR 렌더러 | 실시간 데모 |
| 8~11주 | UE5 커스텀 기능 | UE5 플러그인/패치 |
| 12~14주 | 심화 | 최종 포트폴리오 완성 |

---

## GitHub 포트폴리오 구성

```
github.com/{계정}/
├── pbr-raytracer          ← Phase 1
├── realtime-pbr-renderer  ← Phase 2
└── ue5-custom-renderer    ← Phase 3~4
```

각 레포 README 필수 항목:
1. 결과 이미지 / 영상 (최상단)
2. 구현한 수식과 코드 연결 설명
3. PBR 책의 어느 개념을 구현했는지 명시
