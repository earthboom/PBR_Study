# Phase 1 학습 노트 — CPU 레이트레이서

> 이 노트는 [Ray Tracing in One Weekend](https://raytracing.github.io/) 를 따라가며 배운 내용을 정리한 것입니다.
> 수식보다 **"이게 왜 필요한가"** 와 **"실제로 무슨 의미인가"** 에 집중합니다.

---

## Ch.1 — 이미지 출력 (Output an Image)

### 왜 이걸 먼저 하는가?

레이트레이서를 만들기 전에, **"렌더링 결과를 파일로 저장하는 파이프라인"** 이 정상인지 먼저 확인해야 한다.
아무리 렌더링 코드가 잘 돌아도 결과를 볼 수 없으면 의미가 없다.

---

### PPM 포맷 — 가장 단순한 이미지 저장 방식

PNG, JPG 같은 포맷은 압축/인코딩 라이브러리가 필요하다.
PPM은 그냥 **메모장에 숫자를 적는 것**과 같다. 라이브러리가 전혀 필요 없다.

```
P3           ← "이 파일은 RGB 숫자들입니다" 라는 선언
256 256      ← 가로 256픽셀, 세로 256픽셀
255          ← R, G, B 각각의 최댓값
255 0 0      ← 첫 번째 픽셀: 빨강
0 255 0      ← 두 번째 픽셀: 초록
0 0 255      ← 세 번째 픽셀: 파랑
...
```

#### 왜 255.999를 곱하나? (255.0이 아니라)

```cpp
int ir = int(255.999 * pixel_color.x());
```

부동소수점(소수) 계산에서 정확히 1.0이 나와야 할 값이 0.9999999...로 나오는 경우가 있다.
이 상태에서 `× 255.0` 을 하면 254.9999...가 되고, `int()` 로 자르면 **254** 가 된다.
255.999를 곱하면 0.9999... × 255.999 = 255.998...이 되어 `int()` 결과가 **255** 로 올바르게 나온다.

---

### 색상을 0~255가 아닌 0.0~1.0으로 쓰는 이유

PBR의 모든 빛 계산은 **0.0~1.0 실수**로 이루어진다.

> 예: 반사율 0.8 = "빛의 80%를 반사"
> 예: 투과율 0.3 = "빛의 30%가 통과"

0~255 정수는 모니터 출력 직전에만 필요하다.
중간 계산을 0~255로 하면 정밀도가 떨어지고 곱셈/나눗셈도 불편해진다.

```
계산 중:  0.0 ~ 1.0  (실수)
화면 출력: 0 ~ 255    (정수) ← 맨 마지막에 × 255.999 후 int()로 변환
```

---

### 이미지 좌표계 — y축이 아래를 향한다

수학에서 y축은 위를 향하지만, 이미지(화면)에서는 **y축이 아래를 향한다.**
왼쪽 위가 (0, 0)이고, 오른쪽 아래가 (width-1, height-1)이다.

```
(0,0) ──────────────→ x (i)
  │  ████████████████
  │  ████████████████
  ↓  ████████████████
  y(j)
```

왜 y가 아래 방향인가? → 컴퓨터 메모리는 위 행부터 순서대로 저장한다.
첫 번째 저장되는 픽셀이 (0, 0)이고, 다음 행은 (0, 1)... 이렇게 내려가기 때문.

PPM도 이 순서를 따라 위쪽 행(j=0)부터 픽셀을 저장한다.

![이미지 좌표계](diagrams/image_coords.png)

---

### 결과물 — 좌표를 색상으로

테스트 이미지는 픽셀 위치 `(i, j)` 를 그대로 색상으로 변환해 출력한다:

```cpp
double r = double(i) / (image_width  - 1);  // 가로 위치 → R값 (0.0~1.0)
double g = double(j) / (image_height - 1);  // 세로 위치 → G값 (0.0~1.0)
double b = 0.0;                              // 파랑은 항상 0
```

이 수식이 맞는지 모서리로 확인:

| 모서리 | i, j | R, G 계산 | 결과 색상 |
|--------|------|----------|----------|
| 왼쪽 위 | i=0, j=0 | R=0/max=0, G=0/max=0 | 검정 |
| 오른쪽 위 | i=max, j=0 | R=1.0, G=0 | 빨강 |
| 왼쪽 아래 | i=0, j=max | R=0, G=1.0 | 초록 |
| 오른쪽 아래 | i=max, j=max | R=1.0, G=1.0 | 노랑 |

### 관련 파일
- [src/main.cpp](pbr-raytracer/src/main.cpp)

---

## Ch.2 — vec3 클래스 (The vec3 Class)

### 왜 이걸 만드는가?

레이트레이서에서 다루는 모든 것은 3D 공간 위에 있다:
- 광선의 출발 **위치**
- 광선이 날아가는 **방향**
- 픽셀의 **색상**

이 세 가지를 모두 숫자 3개 묶음 `(x, y, z)` 으로 표현할 수 있다.
vec3은 그 숫자 3개를 묶고 + - × 같은 연산을 편하게 쓰기 위한 클래스다.

---

### vec3의 세 가지 얼굴

같은 `vec3` 타입을 용도에 따라 다르게 부른다:

| 이름 | 뜻 | 예시 |
|------|-----|------|
| `vec3` | 방향 또는 이동량 | "북동쪽으로 2미터" |
| `point3` | 공간상의 위치 | "위도 37°, 경도 127°" |
| `color` | 빛의 색상/세기 | R=0.8, G=0.3, B=0.1 |

코드는 완전히 동일하지만 이름을 달리해서 **"이 변수가 위치인지 방향인지 색상인지"** 를 명확하게 한다.

---

### 내적 (Dot Product) — "두 방향이 얼마나 일치하는가"

$$\vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z$$

이것이 왜 "방향의 일치도"를 나타내는지 직접 숫자로 확인해보자.

**예시 1 — 완전히 같은 방향:**
오른쪽을 향하는 벡터 두 개: $\vec{a} = (1, 0, 0)$, $\vec{b} = (1, 0, 0)$

$$\vec{a} \cdot \vec{b} = 1 \times 1 + 0 \times 0 + 0 \times 0 = 1$$

→ 결과가 **1** (가장 큰 양수) ← 완전히 일치함

**예시 2 — 완전히 수직인 방향:**
오른쪽 $\vec{a} = (1, 0, 0)$, 위쪽 $\vec{b} = (0, 1, 0)$

$$\vec{a} \cdot \vec{b} = 1 \times 0 + 0 \times 1 + 0 \times 0 = 0$$

→ 결과가 **0** ← 전혀 관계없는 방향

**예시 3 — 완전히 반대 방향:**
오른쪽 $\vec{a} = (1, 0, 0)$, 왼쪽 $\vec{b} = (-1, 0, 0)$

$$\vec{a} \cdot \vec{b} = 1 \times (-1) + 0 \times 0 + 0 \times 0 = -1$$

→ 결과가 **-1** (가장 작은 음수) ← 완전히 반대임

이걸 수식으로 정리하면:

$$\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta$$

| 각도 θ | cos θ | 내적 결과 (단위벡터 기준) | 의미 |
|--------|--------|--------------------------|------|
| 0° | 1.0 | 1.0 | 완전히 같은 방향 |
| 90° | 0.0 | 0.0 | 수직 |
| 180° | -1.0 | -1.0 | 완전히 반대 방향 |

![내적 다이어그램](diagrams/dot_product.png)

**직관적 비유:**
손전등을 벽에 비출 때, 손전등이 벽과 수직일수록 밝게 빛난다.
내적은 바로 이것을 수치로 표현한다. `NdotL` (법선 · 광원 방향) = 표면이 빛을 향할수록 밝아지는 PBR의 기본 원리.

```cpp
double dot(vec3 a, vec3 b)  // 결과: 숫자(스칼라)
```

---

### 외적 (Cross Product) — "두 벡터에 동시에 수직인 방향 찾기"

$$\vec{a} \times \vec{b} = \begin{pmatrix} a_y b_z - a_z b_y \\ a_z b_x - a_x b_z \\ a_x b_y - a_y b_x \end{pmatrix}$$

수식이 복잡해 보이지만, **결과가 무엇인가** 에 집중하면 된다.
결과는 항상 입력 두 벡터와 **동시에 수직**인 벡터다.

**예시 — 오른쪽 × 위쪽 = ?**
$\vec{a} = (1, 0, 0)$ (오른쪽), $\vec{b} = (0, 1, 0)$ (위쪽)

$$\vec{a} \times \vec{b} = \begin{pmatrix} 0 \times 0 - 0 \times 1 \\ 0 \times 0 - 1 \times 0 \\ 1 \times 1 - 0 \times 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$$

결과가 $(0, 0, 1)$ = 앞쪽 방향이다. 오른쪽과 위쪽에 동시에 수직인 방향은 앞쪽뿐!

![외적 다이어그램](diagrams/cross_product.png)

**오른손 법칙:** 오른손 검지를 a 방향, 중지를 b 방향으로 펼치면
엄지가 가리키는 방향이 a × b다.

> 주의: 순서가 바뀌면 방향이 반대가 된다.
> $\vec{a} \times \vec{b} = -(\vec{b} \times \vec{a})$

**PBR에서 어디에 쓰이나?**
- 카메라 좌표계 구성: 앞 방향과 위 방향으로 오른쪽 방향을 계산
- 삼각형 법선 계산: 삼각형의 두 변 벡터로 면의 수직 방향을 계산

```cpp
vec3 cross(vec3 a, vec3 b)  // 결과: 벡터
```

---

### 정규화 (Normalization) — "방향만 남기고 크기는 버리기"

$$\hat{v} = \frac{\vec{v}}{|\vec{v}|} = \frac{\vec{v}}{\sqrt{v_x^2 + v_y^2 + v_z^2}}$$

#### 벡터의 "길이"는 어떻게 계산하나?

3D 공간에서 길이는 피타고라스 정리를 두 번 적용해 구한다:

```
1단계: x-z 평면의 대각선 = √(x² + z²)
2단계: 대각선과 y로 최종 거리 = √((√(x²+z²))² + y²) = √(x² + y² + z²)
```

$$|\vec{v}| = \sqrt{v_x^2 + v_y^2 + v_z^2}$$

**예시 — (3, 4, 0) 벡터의 길이:**

$$|(3, 4, 0)| = \sqrt{3^2 + 4^2 + 0^2} = \sqrt{9 + 16} = \sqrt{25} = 5$$

#### 정규화 예시

$(3, 4, 0)$ 을 길이 5로 나누면:

$$\hat{v} = \frac{(3, 4, 0)}{5} = (0.6, 0.8, 0)$$

확인: $\sqrt{0.6^2 + 0.8^2} = \sqrt{0.36 + 0.64} = \sqrt{1.0} = 1.0$ ✓

![정규화 다이어그램](diagrams/normalization.png)

**직관:** "북쪽으로 100km" 와 "북쪽으로 1km" 는 방향은 같지만 거리가 다르다.
정규화는 거리를 버리고 **"방향만"** 남기는 것이다. 결과 벡터의 길이는 항상 1.

**왜 길이를 1로 맞춰야 하나?**
내적 결과 = $|\vec{a}||\vec{b}|\cos\theta$ 에서, 두 벡터의 길이가 모두 1이면:

$$1 \times 1 \times \cos\theta = \cos\theta$$

길이가 1이 아니면 내적 결과에 길이가 섞여 들어와 cos θ 값 자체를 얻을 수 없다.

```cpp
vec3 unit_vector(vec3 v)  // 길이를 1로 맞춘 벡터 반환
```

---

### 왜 `length_squared()`를 따로 만드는가?

$$|\vec{v}|^2 = v_x^2 + v_y^2 + v_z^2$$

`sqrt()` (제곱근)는 CPU에서 꽤 비싼 연산이다.
두 벡터의 길이를 **비교하는 것**이 목적이라면 제곱근 없이도 된다:

$$|\vec{a}| < |\vec{b}| \iff |\vec{a}|^2 < |\vec{b}|^2$$

예시: 3 < 5 가 맞는지 확인할 때
- 제곱근 쓰면: √9 < √25 → 3 < 5 ✓ (제곱근 2번)
- 제곱만 쓰면: 9 < 25 ✓ (제곱근 0번, 결과 동일)

1000번 비교한다면 `sqrt()` 1000번을 절약할 수 있다.

### 관련 파일
- [src/vec3.h](pbr-raytracer/src/vec3.h)

---

## Ch.3 — 광선, 카메라, 배경 (Rays, a Simple Camera, and Background)

### 레이트레이서의 핵심 아이디어

현실에서 빛은 광원 → 물체 → 눈 순서로 온다.
레이트레이서는 이걸 **거꾸로** 한다: 눈(카메라) → 픽셀 → 물체 방향으로 광선을 쏜다.

왜 거꾸로 하는가? → 눈에 도달하는 빛만 계산하면 되기 때문.
광원에서 출발한 빛 대부분은 눈에 도달하지 않아 낭비다.

```
현실:        광원 → 물체 → 눈 (대부분 낭비)
레이트레이서: 눈  → 픽셀 → 물체 → 광원 (필요한 것만 계산)
```

---

### 광선 방정식 — "출발점 + 방향 × 거리"

$$P(t) = \mathbf{A} + t \cdot \mathbf{b}$$

- $\mathbf{A}$: 광선 출발점 (카메라 위치)
- $\mathbf{b}$: 광선 방향
- $t$: 얼마나 멀리 갔는지 (거리 비례)

**구체적 예시** — 카메라가 원점 $(0, 0, 0)$, 정면(z 음의 방향)을 바라볼 때:

| t 값 | 계산 | 결과 위치 | 의미 |
|------|------|----------|------|
| 0 | $(0,0,0) + 0 \times (0,0,-1)$ | $(0,0,0)$ | 카메라 위치 그 자체 |
| 1 | $(0,0,0) + 1 \times (0,0,-1)$ | $(0,0,-1)$ | 1 유닛 앞 |
| 5 | $(0,0,0) + 5 \times (0,0,-1)$ | $(0,0,-5)$ | 5 유닛 앞 |
| -1 | $(0,0,0) + (-1) \times (0,0,-1)$ | $(0,0,+1)$ | 카메라 뒤쪽 (무시) |

t를 조절하면 광선 위의 어느 점이든 구할 수 있다.

```cpp
point3 at(double t) const { return orig + t * dir; }
```

---

### 뷰포트 — "카메라 앞에 놓인 가상의 스크린"

카메라와 씬 사이에 가상의 직사각형을 하나 놓는다.
각 픽셀마다 카메라에서 해당 픽셀 위치를 향해 광선을 하나 쏜다.

```
      카메라
        ●
        │ ← focal_length (카메라~스크린 거리)
  ┌─────┼─────┐
  │  [0,0]    │  ← 뷰포트 (가상 스크린)
  │           │
  └───────────┘
        ↓ 광선들이 이 스크린을 통과해 씬으로 날아감
```

#### 픽셀 하나의 크기 계산

뷰포트 전체 크기를 픽셀 수로 나누면 픽셀 하나의 크기가 나온다:

```cpp
vec3 pixel_delta_u = viewport_u / image_width;   // 가로 픽셀 하나의 폭
vec3 pixel_delta_v = viewport_v / image_height;  // 세로 픽셀 하나의 높이
```

예시: 뷰포트 너비 = 3.55, 이미지 너비 = 400 → 픽셀 하나 = 0.00889 유닛

#### 각 픽셀 중심의 위치 계산

픽셀 (i, j) 의 중심 위치:

```cpp
point3 pixel_center = pixel00_loc         // 첫 번째 픽셀(0,0)의 중심
                    + (i * pixel_delta_u) // i번째 픽셀만큼 오른쪽으로
                    + (j * pixel_delta_v); // j번째 픽셀만큼 아래쪽으로
```

- 뷰포트가 클수록 시야각(FOV)이 넓어진다
- `focal_length`가 클수록 시야각이 좁아진다 (망원렌즈 효과)

![뷰포트 구조](diagrams/viewport.png)

---

### 선형 보간 (Lerp) — "두 색 사이를 부드럽게 섞기"

$$\text{color}(t) = (1-t) \cdot \text{흰색} + t \cdot \text{하늘색}$$

#### y 방향을 0~1 범위로 변환하는 과정

광선 방향을 정규화하면 y 성분은 반드시 **-1 ~ +1** 범위가 된다.
(길이가 1인 벡터의 각 성분은 -1~+1을 벗어날 수 없다)

- 광선이 위를 향하면 y = +1.0
- 광선이 수평을 향하면 y = 0.0
- 광선이 아래를 향하면 y = -1.0

Lerp는 0~1 범위를 입력으로 받으므로 변환이 필요하다:

$$t = \frac{y + 1}{2} = 0.5 \times (y + 1)$$

| y 값 | t = (y+1)/2 | 결과 색상 |
|------|------------|----------|
| -1.0 (아래) | 0.0 | 완전히 흰색 |
| 0.0 (수평) | 0.5 | 흰색+하늘색 중간 |
| +1.0 (위) | 1.0 | 완전히 하늘색 |

```cpp
double t = 0.5 * (unit_dir.y() + 1.0);      // y: -1~+1 → t: 0~1
return (1.0 - t) * white + t * sky_blue;    // Lerp
```

![Lerp 그라디언트](diagrams/lerp.png)

### 결과물

![Ch.3 배경](pbr-raytracer/results/ch3_background.png)

이후 챕터에서 이 배경 위로 구, 재질, 조명이 쌓여간다.

### 관련 파일
- [src/ray.h](pbr-raytracer/src/ray.h)
- [src/main.cpp](pbr-raytracer/src/main.cpp)

---

## Ch.4 — 구 추가 (Adding a Sphere)

### 왜 구부터 시작하는가?

3D 물체 중 **수학이 가장 단순한 것이 구**다.
삼각형, 박스, 메시 등은 훨씬 복잡하다.
레이트레이서의 교차 계산 원리를 가장 쉽게 배울 수 있는 출발점.

---

### 광선-구 교차 — "광선이 구에 맞는지 판별하기"

**직관적 이해:**
풍선(구)에 화살(광선)을 쏜다고 상상해보자.
- 화살이 풍선을 **통과**하면 두 번 맞는다 (들어가는 점, 나오는 점)
- 화살이 풍선에 **접선**으로 스치면 한 번 맞는다
- 화살이 풍선을 **빗나가면** 맞지 않는다

이걸 수학으로 표현해보자. **"광선 위의 어느 t에서 구 표면에 닿는가?"** 를 구하는 것이 목표다.

![광선-구 교차 3가지 경우](diagrams/ray_sphere.png)

---

**① 구의 방정식 — 구가 뭔가**

구 = 중심 $\mathbf{C}$ 로부터 거리가 정확히 $r$ 인 점들의 집합.

$$|\mathbf{P} - \mathbf{C}|^2 = r^2$$

왜 거리를 제곱하나? → 제곱근 없이 계산할 수 있어서 더 빠르다.
$|\mathbf{P} - \mathbf{C}|^2 = (\mathbf{P} - \mathbf{C}) \cdot (\mathbf{P} - \mathbf{C})$ 이므로, 내적 계산만으로 된다.

---

**② 광선 방정식을 구 방정식에 대입**

광선 위의 점은 $\mathbf{P}(t) = \mathbf{A} + t\mathbf{b}$ 이다. ($\mathbf{A}$ = 카메라, $\mathbf{b}$ = 방향)

이 점이 구 위에 있다는 조건:

$$|\mathbf{A} + t\mathbf{b} - \mathbf{C}|^2 = r^2$$

여기서 $\mathbf{oc} = \mathbf{A} - \mathbf{C}$ (카메라에서 구 중심까지의 벡터) 로 치환하면:

$$|t\mathbf{b} + \mathbf{oc}|^2 = r^2$$

---

**③ 전개 — 벡터 내적으로 풀기**

$|\mathbf{u}|^2 = \mathbf{u} \cdot \mathbf{u}$ 이므로:

$$(t\mathbf{b} + \mathbf{oc}) \cdot (t\mathbf{b} + \mathbf{oc}) = r^2$$

내적은 일반 곱셈처럼 분배법칙이 성립한다:

$$(t\mathbf{b}) \cdot (t\mathbf{b}) + (t\mathbf{b}) \cdot \mathbf{oc} + \mathbf{oc} \cdot (t\mathbf{b}) + \mathbf{oc} \cdot \mathbf{oc} = r^2$$

각 항을 정리하면:

| 항 | 정리 결과 | 이유 |
|----|----------|------|
| $(t\mathbf{b}) \cdot (t\mathbf{b})$ | $t^2(\mathbf{b} \cdot \mathbf{b})$ | 스칼라 $t^2$ 은 밖으로 꺼낼 수 있다 |
| $(t\mathbf{b}) \cdot \mathbf{oc}$ | $t(\mathbf{b} \cdot \mathbf{oc})$ | 마찬가지로 $t$ 꺼냄 |
| $\mathbf{oc} \cdot (t\mathbf{b})$ | $t(\mathbf{oc} \cdot \mathbf{b})$ | 내적은 교환법칙 성립: $\mathbf{oc} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{oc}$ |
| $\mathbf{oc} \cdot \mathbf{oc}$ | $\|\mathbf{oc}\|^2$ | 자기 자신과의 내적 = 길이의 제곱 |

두 번째와 세 번째 항은 같으므로 합쳐서:

$$t^2(\mathbf{b} \cdot \mathbf{b}) + 2t(\mathbf{b} \cdot \mathbf{oc}) + (\mathbf{oc} \cdot \mathbf{oc}) - r^2 = 0$$

---

**④ 이차방정식으로 인식**

이건 미지수 $t$ 에 대한 이차방정식 $at^2 + 2ht + c = 0$ 이다:

$$a = \mathbf{b} \cdot \mathbf{b} = |\mathbf{b}|^2 \qquad h = \mathbf{b} \cdot \mathbf{oc} \qquad c = |\mathbf{oc}|^2 - r^2$$

> 왜 $2h$ 로 쓰나? → 판별식 계산에서 2가 약분되어 사라지기 때문 (아래 참고).

---

**⑤ 판별식으로 교차 여부 판단**

이차방정식 $at^2 + 2ht + c = 0$ 의 근의 공식:

$$t = \frac{-2h \pm \sqrt{(2h)^2 - 4ac}}{2a} = \frac{-h \pm \sqrt{h^2 - ac}}{a}$$

중간에 2가 깔끔하게 약분되었다! 이것이 $h$ (절반 계수)를 쓰는 이유다.
**판별식** $= h^2 - ac$ 의 부호로 교차 여부를 판단:

| 판별식 값 | 상황 | 시각적 의미 |
|----------|------|-------------|
| 음수 (< 0) | 근 없음 | 광선이 구를 완전히 빗나감 |
| 0 | 중근 | 광선이 구 표면을 스침 |
| 양수 (> 0) | 두 근 | 광선이 구를 통과 → 앞쪽 근(작은 t)이 첫 교차점 |

---

**⑥ 코드와 연결**

코드에서는 `oc = C - A` (방향이 반대)를 쓰므로 $h = \mathbf{b} \cdot (\mathbf{C} - \mathbf{A})$ 로 부호가 뒤집힌다.
부호가 뒤집히면 근의 공식도 $+h$ 에서 출발하지만, 결국 **작은 t를 원하므로** 빼기 부호가 앞에 온다:

```cpp
vec3 oc = center - r.origin();                // oc = C - A
double a = dot(r.direction(), r.direction()); // |b|²
double h = dot(r.direction(), oc);            // b·(C-A)
double c = dot(oc, oc) - radius * radius;     // |oc|² - r²
double discriminant = h*h - a*c;

if (discriminant < 0)
    return -1.0;                              // 맞지 않음
return (h - sqrt(discriminant)) / a;          // 첫 교차점의 t값
```

---

### 법선 벡터 — "구 표면에서 바깥을 향하는 방향"

교차점 $\mathbf{P}$ 에서 구 중심 $\mathbf{C}$ 로의 방향이 법선이다.
구의 반지름으로 나누면 길이 1인 단위 법선 벡터가 된다:

$$\hat{n} = \frac{\mathbf{P} - \mathbf{C}}{r}$$

#### 법선을 색상으로 변환하는 과정

단위 벡터의 각 성분은 **-1 ~ +1** 범위다.
RGB 색상은 **0 ~ 1** 범위를 필요로 한다.

변환 공식: $(x + 1) \times 0.5$

| 법선 성분 값 | 변환 계산 | 색상 채널 값 |
|------------|---------|------------|
| -1.0 (완전히 반대) | $(-1+1) \times 0.5 = 0.0$ | 0 (검정) |
| 0.0 (수직) | $(0+1) \times 0.5 = 0.5$ | 128 (중간) |
| +1.0 (완전히 바깥) | $(1+1) \times 0.5 = 1.0$ | 255 (최대) |

그래서 구의 각 방향이 이런 색으로 보인다:

| 법선 방향 | 색상 | 이유 |
|-----------|------|------|
| 오른쪽 (+X) | 빨강 | R = (1+1)×0.5 = 1.0 |
| 위쪽 (+Y) | 초록 | G = (1+1)×0.5 = 1.0 |
| 카메라 방향 (+Z) | 파랑 | B = (1+1)×0.5 = 1.0 |

```cpp
vec3 normal = unit_vector(r.at(t) - sphere_center); // 길이 1의 법선벡터
return 0.5 * color(normal.x()+1, normal.y()+1, normal.z()+1); // -1~1 → 0~1
```

![법선 벡터 색상 매핑](diagrams/normal_colors.png)

### 결과물

![Ch.4 구](pbr-raytracer/results/ch4_sphere.png)

법선 방향이 색상으로 표현된 구. 이 법선 벡터가 이후 조명 계산(내적)의 핵심 입력이 된다.

### 관련 파일
- [src/main.cpp](pbr-raytracer/src/main.cpp)

---

## Ch.5 — 표면 법선과 다중 오브젝트 (Surface Normals and Multiple Objects)

### 왜 이걸 하는가?

Ch.4까지는 `main.cpp` 안에 `hit_sphere` 함수 하나로 구 하나만 다뤘다.
실제 씬은 **수많은 오브젝트**(구, 평면, 삼각형 메시…)로 구성된다.
이걸 깔끔히 다루려면 두 가지 변화가 필요하다:

1. **공통 인터페이스로 추상화** — 오브젝트마다 `hit_sphere`, `hit_plane`, `hit_triangle`을 따로 만들면 `ray_color`가 종류별 분기로 가득 찬다. 모두가 따르는 단일 인터페이스 `hittable` 을 만들면 `ray_color`는 종류를 신경 쓰지 않아도 된다.
2. **앞면/뒷면 법선 판별** — Ch.4의 법선 계산 `(P - C) / r` 은 **항상 바깥**을 향한다. 광선이 구 안에서 밖으로 나가는 경우 (유리 내부 굴절 등)에는 이 법선이 광선과 같은 방향이라 조명 계산이 깨진다. 이 챕터에서 광선이 표면을 어느 쪽에서 만났는지 구분하는 규칙을 도입한다.

이번 챕터에서 새로 등장하는 핵심 개념은 **앞면/뒷면 법선 판별**, 그리고 작은 유틸리티 클래스인 **`interval`** 이다.

---

### 추상화의 그림 — `hittable` 인터페이스

```
        ┌─────────────────┐
        │   hittable      │  ← 추상 클래스 (인터페이스)
        │   - hit(...)    │
        └────────┬────────┘
                 │ (상속)
        ┌────────┼────────┐
        ▼        ▼        ▼
     sphere  triangle  mesh   (구체적 구현체들)
```

광선이 어느 오브젝트에 맞았을 때 필요한 정보를 한 묶음으로:

```cpp
struct hit_record {
    point3 p;          // 충돌 지점
    vec3   normal;     // 법선 (광선의 반대쪽을 향하도록 정렬됨)
    double t;          // 광선 위의 거리
    bool   front_face; // 앞면을 맞았는가?
};
```

`hittable_list`는 여러 `hittable`을 담은 컨테이너다. 자기도 `hittable`을 상속해서, 자기 자신을 마치 하나의 거대한 오브젝트처럼 다룰 수 있다.

---

### 새로운 수학 개념: 앞면 vs 뒷면 법선 판별

#### ① 왜 이게 필요한가?

조명 계산에서 법선은 **항상 광선의 반대쪽**을 향해야 한다.
이유: `NdotL` (법선 · 광원 방향) 같은 내적은 "표면이 광원을 얼마나 정면으로 마주하는가"를 측정한다. 법선이 표면 안쪽을 향하면 부호가 뒤집혀 어두워야 할 곳이 밝아지는 식의 오류가 난다.

구 표면에서 단순히 $(P - C) / r$ 로 계산한 법선은 **항상 바깥**을 향한다.
- 광선이 밖에서 들어와서 부딪히면 → 광선과 법선이 **반대 방향** → OK ✓
- 광선이 안에서 나가다 부딪히면 → 광선과 법선이 **같은 방향** → 뒤집어야 함 ✗

#### ② 일상 비유

선풍기 앞에 손바닥을 펼친다고 상상하자. 손등이 선풍기를 향하면 바람이 손등을 때린다. 손바닥이 선풍기를 향해야 정면으로 바람을 맞는다.
**"법선(손바닥이 가리키는 방향)은 들어오는 바람(광선)의 반대 방향이어야 한다."** 이게 우리가 강제하고 싶은 규칙이다.

#### ③ 단계별 전개 — 내적 부호로 어떻게 판별하나?

광선 방향을 $\mathbf{d}$, 외향 법선(밖으로 향하는 법선)을 $\mathbf{n}_{out}$ 이라고 하자.

$$\mathbf{d} \cdot \mathbf{n}_{out} = |\mathbf{d}||\mathbf{n}_{out}|\cos\theta$$

길이는 양수이므로 부호는 $\cos\theta$ 가 결정한다.

| $\theta$ 범위 | $\cos\theta$ | 내적 부호 | 기하학적 의미 |
|---|---|---|---|
| 0° ~ 90° | 양수 | $\mathbf{d} \cdot \mathbf{n}_{out} > 0$ | 광선과 법선이 같은 쪽을 향함 → **광선이 안에서 나감** (뒷면) |
| 90° | 0 | 0 | 광선이 표면을 스침 |
| 90° ~ 180° | 음수 | $\mathbf{d} \cdot \mathbf{n}_{out} < 0$ | 광선과 법선이 반대쪽을 향함 → **광선이 밖에서 들어옴** (앞면) |

규칙:
- `dot(d, n_out) < 0` → **앞면 (front_face = true)**, 법선은 $\mathbf{n}_{out}$ 그대로
- `dot(d, n_out) > 0` → **뒷면 (front_face = false)**, 법선은 $-\mathbf{n}_{out}$ (뒤집기)

#### ④ 구체적 숫자 예시

광선이 오른쪽으로 직진: $\mathbf{d} = (1, 0, 0)$.

**경우 A — 광선이 구의 왼쪽 면에 부딪힘 (밖→안)**
충돌점은 구 중심 왼쪽이므로 외향 법선 $\mathbf{n}_{out} = (-1, 0, 0)$.

$$\mathbf{d} \cdot \mathbf{n}_{out} = 1 \times (-1) + 0 + 0 = -1$$

음수 → **앞면**. 법선 그대로 $(-1, 0, 0)$ 사용.

**경우 B — 광선이 구의 오른쪽 면에 부딪힘 (안→밖)**
충돌점은 구 중심 오른쪽이므로 외향 법선 $\mathbf{n}_{out} = (1, 0, 0)$.

$$\mathbf{d} \cdot \mathbf{n}_{out} = 1 \times 1 + 0 + 0 = +1$$

양수 → **뒷면**. 법선을 뒤집어 $(-1, 0, 0)$ 사용.

두 경우 모두 최종 법선은 광선($+x$ 방향)의 **반대 방향**($-x$)을 향한다 ✓.

![앞면/뒷면 법선](diagrams/front_back_face.png)

#### ⑤ 코드와 연결

```cpp
inline void set_face_normal(const ray& r, const vec3& outward_normal) {
    // outward_normal 은 항상 단위 벡터라고 가정 (호출자 책임)
    front_face = dot(r.direction(), outward_normal) < 0;
    normal     = front_face ? outward_normal : -outward_normal;
}
```

| 수식 | 코드 |
|------|------|
| $\mathbf{d}$ | `r.direction()` |
| $\mathbf{n}_{out}$ | `outward_normal` |
| $\mathbf{d} \cdot \mathbf{n}_{out} < 0$ | `dot(r.direction(), outward_normal) < 0` |
| 법선 뒤집기 | `front_face ? outward_normal : -outward_normal` |

> **설계 결정 — 누가 외향 법선을 만드나?**
> `set_face_normal` 호출자(즉 `sphere::hit`)가 외향 법선을 단위 벡터로 만들어 넘긴다.
> 이유: 오브젝트마다 외향 법선을 효율적으로 계산하는 방법이 다르다 (구는 `(P-C)/r`, 평면은 미리 저장된 상수).
> 인터페이스를 일반화하기보다 **각 오브젝트가 자기에게 최적인 방식으로 만들도록** 한다.

---

### 여러 오브젝트 중 가장 가까운 충돌 찾기

#### 왜 "가장 가까운" 것이 필요한가?

광선이 여러 오브젝트를 동시에 통과할 수 있다.
하지만 우리가 카메라로 보는 건 **가장 앞에 있는 표면**뿐이다 (뒤쪽은 가려져 안 보인다).

알고리즘의 핵심: **`closest`라는 임시 t 상한값을 들고 다니며**, 더 가까운 충돌을 발견할 때마다 갱신한다.

```cpp
double closest = t_max;
for (auto& obj : objects) {
    if (obj->hit(r, t_min, closest, temp_rec)) {
        closest = temp_rec.t;   // 다음 오브젝트는 이보다 가까운 충돌만 인정
        rec = temp_rec;
    }
}
```

이렇게 하면 단 한 번의 순회로 가장 가까운 충돌을 찾는다. 정렬 없이 O(n).

![가장 가까운 충돌 찾기](diagrams/closest_hit.png)

---

### `interval` 클래스 — t 범위를 한 변수로

지금까지 `t_min`과 `t_max`를 두 개의 매개변수로 다녔다. 이걸 하나의 객체로 묶으면:
- 매개변수 개수가 줄어 가독성 ↑
- `surrounds(x)`, `clamp(x)` 같은 범위 관련 유틸을 한 곳에 모을 수 있음

```cpp
class interval {
public:
    double min, max;
    interval(double mn, double mx) : min(mn), max(mx) {}
    bool surrounds(double x) const { return min < x && x < max; }
    bool contains(double x)  const { return min <= x && x <= max; }
};
```

`surrounds` 와 `contains` 의 차이는 경계 포함 여부다. 광선 충돌에서는 t가 정확히 t_min 일 때(자기 자신에게 충돌) 같은 케이스를 배제하기 위해 보통 `surrounds` 를 쓴다.

---

### 클래스 구성 — 누가 누구를 호출하나?

```
ray_color(r, world)
    └─ world.hit(r, [0, infinity], rec)        ← world 는 hittable_list
         ├─ sphere1.hit(r, [0, closest], temp) ← 가장 가까운 충돌 갱신
         ├─ sphere2.hit(r, [0, closest], temp)
         └─ ...
              └─ rec.set_face_normal(r, outward_normal)  ← 앞/뒷면 판별
```

---

### 결과물

![Ch.5 다중 오브젝트](pbr-raytracer/results/ch5_normals.png)

씬에 큰 땅 구(반지름 100, 아래쪽) + 작은 구(반지름 0.5, 정면) 두 개를 배치했다.
두 구 모두 같은 `ray_color` 코드 한 줄 (`world.hit(...)`)로 처리된다.

- 작은 구: 표면 법선이 `(P-C)/r` 로 방향마다 다르므로 RGB 그라디언트로 보인다
- 땅 구: 카메라 시야에 들어오는 부분은 모두 위쪽 면(+Y 방향)이므로 초록(G채널)이 지배적이다
- `hittable` 추상화 덕분에 오브젝트가 100개여도 `ray_color` 코드는 그대로다

### 관련 파일
- [src/hittable.h](pbr-raytracer/src/hittable.h) (이번 챕터에서 추가)
- [src/sphere.h](pbr-raytracer/src/sphere.h) (이번 챕터에서 추가)
- [src/hittable_list.h](pbr-raytracer/src/hittable_list.h) (이번 챕터에서 추가)
- [src/interval.h](pbr-raytracer/src/interval.h) (이번 챕터에서 추가)
- [src/rtweekend.h](pbr-raytracer/src/rtweekend.h) (이번 챕터에서 추가)
- [src/main.cpp](pbr-raytracer/src/main.cpp) (리팩토링)

---

## Ch.6 — 안티에일리어싱 (Antialiasing)

### 왜 이걸 하는가?

Ch.5의 결과 이미지를 자세히 보면 구의 가장자리가 **계단처럼 톱니** 모양이다.
원인: 한 픽셀당 광선을 **딱 한 개**, 그것도 **픽셀 정중앙**으로만 쐈기 때문이다.

이게 왜 문제인가? 한 픽셀의 영역 안에 구가 30%만 차 있다고 하자. 픽셀 중심에서 쏜 광선 하나가 구를 맞히면 그 픽셀은 **100% 구 색**, 빗맞으면 **100% 배경 색**이다. 중간이 없다. 결과적으로 가장자리가 0/100으로 뚝 끊긴다.

이번 챕터의 목표: 픽셀 안의 **여러 위치**에 광선을 쏘고 색의 **평균**을 내자. 그러면 30%가 구를 맞히면 자연스럽게 30% 구색 + 70% 배경색이 섞여 부드러운 가장자리가 된다.

![에일리어싱 비교](diagrams/aliasing.png)

---

### 새로운 수학 개념: 픽셀 내 무작위 샘플링과 평균

#### ① 왜 이게 필요한가?

위의 그림처럼 픽셀 중심 1개로는 "그 픽셀 영역 안의 색"을 잘 대표하지 못한다. 픽셀은 점이 아니라 **작은 사각형 영역**이고, 그 영역에 들어오는 빛의 평균이 그 픽셀의 진짜 색이다.

수식으로 쓰면 픽셀의 진짜 색은 적분이다 ($C(x,y)$는 코드의 `ray_color(x, y)`):

$$\text{픽셀 색} = \frac{1}{\text{픽셀 면적}} \iint_{\text{픽셀}} C(x, y) \, dx \, dy$$

이걸 정확히 계산할 수는 없으므로, 무작위 샘플로 **근사**한다 (몬테카를로 추정):

$$\text{픽셀 색} \approx \frac{1}{N} \sum_{k=1}^{N} C(x_k, y_k)$$

#### ② 일상 비유

흐릿한 사진을 찍는 두 가지 방식을 떠올려보자:
- **방법 A**: 셔터를 1/1000초로 한 번 찍고 결과를 저장 → 그 순간만 포착
- **방법 B**: 셔터를 1/1000초로 100번 찍고 평균 → 흔들림과 노이즈가 줄고 부드러움

레이트레이싱의 안티에일리어싱이 정확히 방법 B다. 픽셀 안의 다양한 위치에서 빛을 여러 번 "찍고" 평균을 낸다.

#### ③ 단계별 전개 — 픽셀 안 무작위 위치는 어떻게 만드나?

지금까지 픽셀 (i, j)의 중심 위치는 ($P_{00}$ = `pixel00_loc`, $\Delta u$ = `pixel_delta_u`, $\Delta v$ = `pixel_delta_v`):

$$P_{ij} = P_{00} + i \cdot \Delta u + j \cdot \Delta v$$

여기서 $i$, $j$ 는 정수다. 픽셀 안의 임의 위치를 가지려면 정수 대신 **연속된 실수**로 만들면 된다:

$$S_{ij} = P_{00} + (i + dx) \cdot \Delta u + (j + dy) \cdot \Delta v$$

여기서 $dx, dy$ 는 $[0, 1)$ 범위의 무작위 실수.
- $dx = 0, dy = 0$ → 픽셀의 왼쪽 위 모서리
- $dx = 0.5, dy = 0.5$ → 픽셀 중심 (Ch.5의 방식)
- $dx = 0.99, dy = 0.99$ → 픽셀의 오른쪽 아래 모서리 근처

![픽셀 내부 샘플링](diagrams/pixel_sampling.png)

#### ④ 구체적 숫자 예시

이미지 너비 400, 뷰포트 너비 3.55라 가정 → `pixel_delta_u = 3.55 / 400 = 0.008875`.

픽셀 (i=100, j=50) 안에 샘플 3개를 만들어보자:

| 샘플 | dx | dy | i + dx | j + dy | 픽셀 안 어느 위치인가? |
|------|-----|-----|--------|--------|--------------------|
| 1 | 0.231 | 0.812 | 100.231 | 50.812 | 왼쪽 위쪽 |
| 2 | 0.674 | 0.105 | 100.674 | 50.105 | 오른쪽 아래쪽 |
| 3 | 0.418 | 0.526 | 100.418 | 50.526 | 거의 중앙 |

이 3개 위치 각각에서 광선을 쏘고 ray_color를 받는다. 그 색 3개를 더해서 3으로 나눈 값이 픽셀 (100, 50)의 최종 색.

#### ⑤ 코드와 연결

샘플 1개를 만들어 광선을 반환하는 함수 (camera 클래스 안에 들어갈 메서드):

```cpp
ray get_ray(int i, int j) const {
    vec3 offset = sample_square();                          // (dx-0.5, dy-0.5, 0)
    point3 pixel_sample = pixel00_loc
                        + ((i + offset.x()) * pixel_delta_u)
                        + ((j + offset.y()) * pixel_delta_v);
    return ray(center, pixel_sample - center);
}

vec3 sample_square() const {
    // [-0.5, +0.5) 범위 사각형 안의 무작위 점 (z=0)
    return vec3(random_double() - 0.5, random_double() - 0.5, 0);
}
```

> 실제 구현에서는 `[0, 1)` 대신 `[-0.5, +0.5)` 를 쓴다. 이러면 `(i, j)` 가 픽셀 **중심** 좌표가 되고 샘플은 그 주변에 균등 분포한다. 의미는 동일.

| 수식 | 코드 |
|------|------|
| $dx, dy$ | `random_double()` 결과 |
| $(i + dx, j + dy)$ | `(i + offset.x(), j + offset.y())` |
| $S_{ij}$ | `pixel_sample` |
| $\frac{1}{N}\sum$ | 색을 누적해 `samples_per_pixel`로 나눔 |

---

### `random_double()` — 0~1 무작위 실수

C++ 표준 라이브러리 사용. 단순하게 시작:

```cpp
inline double random_double() {
    // [0, 1) 범위의 균등분포 실수
    return std::rand() / (RAND_MAX + 1.0);
}
```

> `RAND_MAX + 1.0` 으로 나누는 이유: `std::rand()` 는 [0, RAND_MAX] 정수를 돌려준다. 그대로 RAND_MAX로 나누면 결과 범위가 `[0, 1]` (1 포함) 이라 가끔 1.0이 나온다. `+1.0`으로 분모를 키우면 결과가 `[0, 1)` 이 되어 1을 절대 포함하지 않는다.

나중에 더 좋은 PRNG가 필요해지면 `std::mt19937` (Mersenne Twister)로 교체하면 된다 — 인터페이스(함수 시그니처)만 같으면 호출하는 쪽 코드는 한 줄도 안 바뀐다.

---

### `camera` 클래스로 분리 — 이번 챕터의 진짜 핵심

지금까지 main.cpp 안에 카메라 설정, 뷰포트 계산, 픽셀 순회 루프, 광선 발사가 모두 흩어져 있었다. 이걸 모두 `camera` 클래스 하나로 묶는다.

```
[Ch.5 main.cpp 구조]            [Ch.6 main.cpp 구조]
- 이미지 크기 설정              - 씬 만들기
- 뷰포트 계산                   - 카메라 설정 (3~4줄)
- 픽셀 순회 루프      ────→     - camera.render(world)
- 광선 발사                       끝.
- 색상 출력
```

**왜 이게 중요한가?**
- main.cpp는 **"무엇을 그릴지"**(씬)만 신경 쓴다. **"어떻게 그릴지"**(픽셀 순회/샘플링/광선 발사)는 camera가 모두 처리.
- 다음 챕터들에서 카메라 기능이 추가될 때(이동 가능한 카메라, defocus blur 등) main.cpp는 거의 변하지 않는다.
- 한 씬을 다른 카메라 설정으로 여러 번 렌더하기 쉬워진다.

`camera` 클래스가 책임지는 일:
1. **public 입력**: `aspect_ratio`, `image_width`, `samples_per_pixel`
2. **`render(const hittable& world)`**: 모든 픽셀을 순회하며 PPM 출력
3. **`initialize()`** (private): 뷰포트, 픽셀 델타 등 내부 값 계산
4. **`get_ray(i, j)`** (private): 픽셀 (i, j) 안의 무작위 샘플로 광선 1개 생성
5. **`ray_color(r, world)`** (private): 광선의 색 결정 (Ch.5에서 가져옴)

---

### 결과물

![Ch.6 안티에일리어싱](pbr-raytracer/results/ch6_aa.png)

`samples_per_pixel = 100` 으로 설정. Ch.5의 결과와 같은 씬이지만 **구의 가장자리가 톱니 없이 부드럽다.**
픽셀 하나당 무작위 위치 100개에서 광선을 쏘고 색의 평균을 냈기 때문이다.

대신 렌더 시간은 Ch.5의 ~100배 (광선이 100배 많아짐). Debug 빌드면 1~3분, Release 빌드면 수십 초.

또 한 가지 큰 변화 — `main.cpp`가 30줄로 줄어들었다. 카메라/뷰포트/픽셀 순회/샘플링/광선 발사가 모두 `camera` 클래스 안에 캡슐화됐다.

### 관련 파일
- [src/camera.h](pbr-raytracer/src/camera.h) (이번 챕터에서 추가, 메인 작업)
- [src/color.h](pbr-raytracer/src/color.h) (이번 챕터에서 추가, `write_color()` + 클램핑)
- [src/interval.h](pbr-raytracer/src/interval.h) (`clamp()` 추가)
- [src/rtweekend.h](pbr-raytracer/src/rtweekend.h) (`random_double()` 추가)
- [src/main.cpp](pbr-raytracer/src/main.cpp) (대폭 단순화)

---

## Ch.7 — 확산 재질 (Diffuse Materials)

### 왜 이걸 하는가?

Ch.6까지의 결과는 구가 법선 방향을 색으로 표현한 것이었다. **실제 빛이 없었다.**
조명 없는 렌더링은 포토샵의 "3D 와이어프레임"처럼 기술적인 시각화일 뿐이다.

이번 챕터의 목표: 구가 **물리적으로 빛을 받고 반사하는** 것처럼 보이게 한다.
결과물: 회색 매트 재질의 구, 자연스러운 그림자, 구끼리 서로 빛을 주고받는 간접광.

이를 위해 세 가지 개념을 도입한다:
1. **Diffuse 반사** — 빛이 표면에서 모든 방향으로 흩어짐
2. **재귀 광선 추적** — 반사된 광선도 또다시 씬을 추적
3. **감마 보정** — 저장된 색이 모니터에서 자연스럽게 보이도록 보정

---

### 개념 1: Diffuse란 무엇인가

**머릿속 그림:**
손전등으로 거울을 비추면 빛이 한 방향으로 날카롭게 반사된다.
같은 손전등으로 하얀 종이를 비추면 빛이 **사방으로 흩어진다.**
Diffuse(난반사)는 종이처럼 반사하는 방식이다.

**비유:**
당구공을 시멘트 바닥에 치면 예측 가능한 방향으로 튄다 (거울 반사).
마른 모래 위에서 치면 어디로 튈지 모른다 (Diffuse).

**PBR에서의 위치:**
흙, 나무, 종이, 피부, 천 — 우리 주변 대부분의 재질이 Diffuse다.
금속, 물, 유리처럼 "반짝이는" 재질만이 Diffuse가 아니다.

---

### 개념 2: 무작위 반사 방향 — 수학

#### ① 왜 이게 필요한가?

광선이 구 표면의 점 $\mathbf{P}$에 맞았다. 이 점에서 새 광선을 어느 방향으로 쏠지 결정해야 한다.
Diffuse 재질은 방향이 **무작위**다. 다만 아무 방향이나 아니고, **표면 바깥쪽 반구** 안에서만 무작위다.
(표면 안쪽으로 반사하면 물체를 뚫고 나가는 것이니 물리적으로 말이 안 된다.)

#### ② 머릿속 그림

```
               S (단위구 표면 위의 무작위 점)
              ↗
         P + N  (법선 끝 = 단위구의 중심)
         ↑
         N (법선, 길이 1)
         |
─────────P──────── (구 표면)
```

**전략:**
- 충돌점 $\mathbf{P}$에서 법선 $\mathbf{N}$ 방향으로 1만큼 이동하면 → 점 $\mathbf{P} + \mathbf{N}$
- 이 점을 중심으로 하는 **단위구**(반지름 1) 위의 무작위 점 $\mathbf{S}$를 고른다
- 새 광선 방향 = $\mathbf{S} - \mathbf{P}$

이 방식은 자연스럽게 **법선과 가까운 방향을 더 자주 선택**한다 (람베르트 분포, 아래 설명).

![람베르트 확산](diagrams/lambertian_diffuse.png)

#### ③ 단위구 안의 무작위 점 — 기각 샘플링

단위구 표면 위에서 직접 무작위 점을 고르는 공식은 복잡하다.
대신 더 쉬운 방법을 쓴다:

```
1단계: [-1, 1]³ 정육면체 안의 무작위 점 p를 뽑는다
2단계: p가 단위구 안에 있는가? (|p|² < 1 인가?)
       YES → 반환
       NO  → 버리고 1단계로 돌아가 다시 뽑는다
```

이것이 **기각 샘플링(rejection sampling)**이다.

왜 이게 동작하는가?

| 도형 | 부피 공식 | 수치 (반지름/한 변 = 1) |
|------|---------|----------------------|
| 정육면체 (한 변 2) | $2^3 = 8$ | 8 |
| 단위구 (반지름 1) | $\frac{4}{3}\pi r^3$ | 약 4.19 |
| 구/정육면체 비율 | | 약 52% |

뽑은 점이 구 안에 있을 확률이 52%이므로, 평균 약 2번이면 성공한다.

**숫자 예시:**

임의의 점 $\mathbf{p} = (0.3, -0.8, 0.4)$ 가 단위구 안에 있는가?

$$|\mathbf{p}|^2 = 0.3^2 + (-0.8)^2 + 0.4^2 = 0.09 + 0.64 + 0.16 = 0.89$$

$0.89 < 1$ 이므로 → 구 **안에** 있다. ✓ 사용 가능.

임의의 점 $\mathbf{q} = (0.7, 0.6, 0.6)$ 이라면?

$$|\mathbf{q}|^2 = 0.49 + 0.36 + 0.36 = 1.21$$

$1.21 > 1$ 이므로 → 구 **밖에** 있다. ✗ 버리고 다시 뽑기.

#### ④ 단위구 표면 위의 점으로 정규화

구 **안**의 점을 구했으면, 그것을 정규화(길이를 1로 맞추기)해서 구 **표면** 위의 점으로 변환한다.

$$\hat{v} = \frac{\mathbf{v}}{|\mathbf{v}|}$$

왜 표면 위여야 하는가? → 방향이 필요할 뿐 길이는 필요 없다. 길이를 1로 고정해두면 이후 계산이 단순해진다.

#### ⑤ 코드와 연결

| 수식 기호 | 코드 | 의미 |
|---------|------|------|
| $\mathbf{p}$ (정육면체 안 점) | `vec3::random(-1, 1)` | 각 성분이 [-1, 1) 인 무작위 벡터 |
| $\|\mathbf{p}\|^2 < 1$ | `p.length_squared() < 1` | 단위구 안인지 확인 |
| 구 안의 점 반환 | `random_in_unit_sphere()` | |
| 정규화 | `unit_vector(...)` | 길이를 1로 맞춤 |
| 구 표면 위 무작위 점 | `random_unit_vector()` | |
| 법선과 같은 반구 보장 | `random_on_hemisphere(normal)` | dot < 0 이면 뒤집기 |

```cpp
// 기각 샘플링: 단위구 안의 점
inline vec3 random_in_unit_sphere() {
    while (true) {
        vec3 p = vec3::random(-1, 1);
        if (p.length_squared() < 1)  // |p|² < 1 → 구 안에 있음
            return p;
    }
}

// 정규화해서 구 표면 위의 점으로
inline vec3 random_unit_vector() {
    return unit_vector(random_in_unit_sphere());
}

// 법선과 같은 반구 쪽인지 확인
inline vec3 random_on_hemisphere(const vec3& normal) {
    vec3 on_unit_sphere = random_unit_vector();
    if (dot(on_unit_sphere, normal) > 0.0)  // 내적 > 0 → 같은 방향
        return on_unit_sphere;
    else
        return -on_unit_sphere;  // 반대쪽이면 뒤집기
}
```

---

### 개념 3: 재귀 광선 추적 (Recursive Ray Tracing)

#### ① 왜 이게 필요한가?

새 광선을 쏘면, 그 광선도 또 다른 물체에 맞을 수 있다.
그 물체에서도 또 반사... 이 과정이 반복되면서 **간접광**이 자연스럽게 생긴다.

예: 구 A에서 반사된 광선이 구 B에 맞고, 구 B에서 반사된 광선이 하늘에 닿는다.
결과: 구 A에 구 B의 색이 미세하게 물들고, 그림자도 완전한 검정이 아니라 주변 색을 반사한다.

**머릿속 그림:**

```
카메라 → 광선 → 구 A 표면에 맞음
                    ↓ 반사 (0.5배 감쇠)
              새 광선 → 구 B 표면에 맞음
                            ↓ 반사 (0.5배 감쇠)
                      새 광선 → 하늘 (하늘 색 반환)
                      ← 하늘 색 반환
                  ← 하늘 색 × 0.5 반환
← 하늘 색 × 0.5 × 0.5 반환
```

![재귀 광선 추적](diagrams/recursive_ray.png)

#### ② 감쇠 — 0.5를 곱하는 이유

Diffuse 재질은 들어오는 빛의 일부를 흡수한다.
우리 구는 50%를 흡수하고 50%를 반사한다고 설정한다 → `0.5 * ray_color(...)`.

반사가 3번 일어나면: $0.5^3 = 0.125$ → 원래 밝기의 12.5%만 남는다.
무한히 반사하면 결국 0에 수렴한다. 수학적으로 안전하다.

#### ③ max_depth — 무한 재귀를 막는 방법

이론상 광선이 두 거울 사이에서 영원히 반사될 수 있다.
`max_depth`는 광선이 최대 몇 번 반사될 수 있는지 제한한다.

```
depth = 50 으로 시작
  → 반사 1번: depth = 49
  → 반사 2번: depth = 48
  → ...
  → depth = 0 이 되면 검정(0, 0, 0) 반환 → 더 이상 추적하지 않음
```

**숫자 예시 — 밝기가 어떻게 감쇠하는가:**

하늘 색이 흰색 (1.0, 1.0, 1.0) 이라 가정:

| 반사 횟수 | 밝기 | 계산 |
|---------|------|------|
| 0 (하늘 직접) | 1.0 | $1.0$ |
| 1번 반사 후 | 0.5 | $1.0 \times 0.5$ |
| 2번 반사 후 | 0.25 | $1.0 \times 0.5^2$ |
| 5번 반사 후 | 0.031 | $1.0 \times 0.5^5$ |
| 10번 반사 후 | 0.001 | $1.0 \times 0.5^{10}$ |

10번만 지나도 사실상 검정이다. `max_depth = 50`은 충분히 넉넉하다.

#### ④ 코드와 연결

```cpp
color ray_color(const ray& r, int depth, const hittable& world) const {
    if (depth <= 0)
        return color(0, 0, 0);  // 최대 깊이 초과 → 검정

    hit_record rec;
    // t_min = 0.001: shadow acne 방지 (아래 별도 설명)
    if (world.hit(r, interval(0.001, infinity), rec)) {
        vec3 direction = random_on_hemisphere(rec.normal);  // 무작위 반사 방향
        return 0.5 * ray_color(ray(rec.p, direction), depth - 1, world);
        //     ↑ 50% 흡수   ↑ 재귀 호출, depth 1 감소
    }
    // 하늘 그라디언트 (기존과 동일)
    ...
}
```

| 수식 / 개념 | 코드 |
|-----------|------|
| 최대 반사 횟수 | `max_depth` (public 설정값) |
| 재귀 깊이 | `depth` 매개변수 |
| 50% 감쇠 | `0.5 *` |
| 재귀 호출 | `ray_color(ray(rec.p, direction), depth - 1, world)` |

---

### 개념 4: Shadow Acne — 부동소수점 오차와 그 해결

#### ① 무엇이 문제인가

**머릿속 그림:**

```
광선이 구 표면 점 P에 맞았다.
P에서 새 광선을 쏜다.
              ↓
부동소수점 계산 오차로
P가 구 표면보다 아주 살짝 (0.000001) 아래에 있다.
              ↓
새 광선이 t ≈ 0.000001 에서
자기 자신 구 표면과 다시 교차!
              ↓
결과: 광선이 구에서 반사되자마자 다시 구에 막혀 검정이 됨
      표면 전체에 무작위 검은 점이 찍힘 → "Shadow Acne"
```

#### ② 해결책 — t 범위의 하한을 0이 아닌 0.001로 설정

```cpp
// 이전 (문제 있음)
world.hit(r, interval(0.0, infinity), rec)

// 이후 (해결)
world.hit(r, interval(0.001, infinity), rec)
```

t = 0.001 미만인 교차는 무시한다. 부동소수점 오차로 생기는 자기 교차는 t가 거의 0에 가까우므로 모두 걸러진다.

0.001은 경험적인 값이다. 너무 크면 가까운 물체의 그림자가 잘리고, 너무 작으면 acne가 남는다.

---

### 개념 5: 감마 보정 (Gamma Correction)

#### ① 왜 이게 필요한가?

**머릿속 그림:**
우리 코드는 색을 선형 값(0.0~1.0)으로 계산한다.
예: "이 픽셀은 최대 밝기의 25%" → 0.25

모니터는 이 숫자를 선형으로 해석하지 않는다.
모니터의 밝기 = (저장값)^2.2 (감마 2.2)

결과: 저장값 0.25 → 실제 밝기 $0.25^{2.2} \approx 0.048$ (원래의 19%밖에 안 됨)
어두운 색이 실제보다 **훨씬 더 어둡게** 보인다.

#### ② 해결책 — 저장 전에 역보정

모니터가 $x^{2.2}$를 적용할 것을 알고 있으므로, 저장 전에 $x^{1/2.2}$를 미리 적용한다.
모니터가 다시 2.2제곱하면 원래 선형 값이 복원된다.

정확한 보정은 $x^{1/2.2}$이지만, 우리는 근사값으로 **$\sqrt{x}$ (= $x^{0.5}$)** 를 쓴다 (감마 2 보정).

**숫자 예시 — 저장값과 모니터 표시 밝기 비교:**

| 선형 색값 | 감마 보정 없이 저장 | 보정 후 저장 ($\sqrt{x}$) | 모니터 표시 ($^{2.2}$ 적용) |
|---------|----------------|------------------------|--------------------------|
| 0.04 (4%) | 0.04 → 아주 어두움 | $\sqrt{0.04} = 0.2$ | $0.2^{2.2} \approx 0.033$ ≈ 3% |
| 0.25 (25%) | 0.25 → 너무 어두움 | $\sqrt{0.25} = 0.5$ | $0.5^{2.2} \approx 0.218$ ≈ 22% |
| 1.0 (100%) | 1.0 → 정상 | $\sqrt{1.0} = 1.0$ | $1.0^{2.2} = 1.0$ ✓ |

보정 후 저장값이 모니터를 거쳐도 선형 값에 가까워진다.

#### ③ 시각적 효과

감마 보정 전: 구 전체가 칙칙하고 어두움. 특히 그림자 부분이 거의 검정.
감마 보정 후: 어두운 영역이 밝아지고, 전체적으로 자연스러운 밝기.

#### ④ 코드와 연결

```cpp
inline double linear_to_gamma(double linear_component) {
    if (linear_component > 0)
        return std::sqrt(linear_component);  // sqrt = 감마 2 보정
    return 0;
}

inline void write_color(std::ostream& out, const color& pixel_color) {
    double r = linear_to_gamma(pixel_color.x());  // 저장 직전에 보정
    double g = linear_to_gamma(pixel_color.y());
    double b = linear_to_gamma(pixel_color.z());
    ...
}
```

| 수식 | 코드 |
|------|------|
| 선형 색값 | `pixel_color.x()` 등 |
| $\sqrt{x}$ (감마 보정) | `std::sqrt(linear_component)` |
| 보정된 값 | `r`, `g`, `b` |

---

### 결과물

![Ch.7 Diffuse](pbr-raytracer/results/ch7_diffuse.png)

Ch.6(법선 색)과 비교:

| 항목 | Ch.6 | Ch.7 |
|------|------|------|
| 구 색상 | 방향별 RGB 법선 색 | 회색 매트 재질 |
| 그림자 | 없음 | 자연스러운 그림자 |
| 간접광 | 없음 | 구끼리 빛을 주고받음 |
| 감마 보정 | 없음 | sqrt로 자연스러운 밝기 |

### 관련 파일
- [src/vec3.h](pbr-raytracer/src/vec3.h) (`random()`, `random_in_unit_sphere()`, `random_unit_vector()`, `random_on_hemisphere()` 추가)
- [src/camera.h](pbr-raytracer/src/camera.h) (`max_depth` 추가, `ray_color` 재귀화)
- [src/color.h](pbr-raytracer/src/color.h) (`linear_to_gamma()` 추가, `write_color` 갱신)

---

## Ch.8 — 금속 재질 (Metal)

### 왜 이걸 하는가?

Ch.7까지는 모든 표면이 빛을 무작위 방향으로 흩뿌리는 확산 재질(Diffuse)뿐이었다.
현실의 재질은 훨씬 다양하다 — 금속은 빛을 **정해진 방향으로 반사**하고, 유리는 빛을 통과시킨다.

이번 챕터의 목표:
1. **`material` 추상화** — 재질 종류를 코드 구조로 정리 (OOP 설계)
2. **`lambertian`** — Ch.7의 확산 반사를 재질 클래스로 분리
3. **`metal`** — 정반사(reflection) + `fuzz`(흐림) 구현

결과: 씬 안에서 확산 구와 금속 구가 **각자 다르게 빛을 반사**한다.

---

### 개념 1: `material` 추상화 — 왜 클래스 계층이 필요한가?

Ch.7의 `ray_color()`는 광선이 물체에 맞으면 항상 "람베르트 확산"을 했다.
하드코딩이라 다른 재질을 추가하려면 `if/else` 분기가 끝없이 늘어난다.

**설계 결정:**
`material` 추상 클래스 하나를 만들고, 모든 재질이 `scatter()` 하나만 구현하도록 한다.

```
        ┌──────────────────────┐
        │    material          │  ← 인터페이스 (추상 클래스)
        │    + scatter(...)    │    "이 광선이 어디로 튀는가?"
        └──────────┬───────────┘
                   │ (상속)
          ┌────────┼────────┐
          ▼        ▼        ▼
     lambertian   metal   dielectric  (재질별 구현)
```

`scatter()`의 계약:
- 입력: 입사 광선 `r_in`, 충돌 정보 `rec`
- 출력: 산란 광선 `scattered`, 감쇠 색 `attenuation`
- 반환값: `true` = 빛이 반사됨, `false` = 빛이 완전 흡수됨

`camera.h`의 `ray_color()`는 이제 재질 종류를 전혀 몰라도 된다:

```cpp
if (rec.mat->scatter(r, rec, attenuation, scattered))
    return attenuation * ray_color(scattered, depth - 1, world);
return color(0, 0, 0);  // 흡수됨
```

**`hittable.h`와 `material.h`의 순환 참조 문제:**
`hit_record`는 `shared_ptr<material>`을 들고 있고,
`material`의 `scatter()`는 `hit_record`를 매개변수로 받는다.
A가 B를 include하고 B가 A를 include하면 무한 순환이다.

해결책: **전방 선언(forward declaration)**
```cpp
// hittable.h 맨 위
class material;  // "material이라는 클래스가 존재함"만 선언. 내용은 몰라도 포인터는 만들 수 있다.
```

---

### 개념 2: 정반사(Reflection) — 금속 재질의 핵심 수학

#### ① 왜 이게 필요한가?

Diffuse는 광선이 어디서 왔든 무관하게 무작위 방향으로 튄다.
금속은 다르다 — **입사 방향을 법선에 대해 대칭으로 뒤집은 딱 한 방향**으로만 반사된다.
이 수식 없이는 금속 표면에서 광선이 어디로 가야 할지 계산할 수 없다.

#### ② 머릿속 그림

```
      입사 광선 v          반사 광선 v_ref
             ↘            ↗
              \          /
───────────────P──────────────── 표면
               ↑
               n (법선)
```

법선을 기준으로 좌우가 완전히 대칭. 입사각 = 반사각.

![정반사](diagrams/reflection.png)

#### ③ 일상 비유

당구공이 쿠션에 부딪힐 때, 쿠션(표면)과 **나란한 성분은 그대로**, 쿠션에 **수직인 성분(법선 방향)만 뒤집힌다.**

#### ④ 수식 전개 — 빈 단계 없이

벡터 $\mathbf{v}$ (입사 방향), $\hat{n}$ (표면 법선, 단위벡터).

**1단계 — v를 두 성분으로 분해:**

$$\mathbf{v} = \underbrace{(\mathbf{v} \cdot \hat{n})\hat{n}}_{\text{법선 방향 성분}} + \underbrace{\mathbf{v} - (\mathbf{v} \cdot \hat{n})\hat{n}}_{\text{법선 수직 성분}}$$

**2단계 — 반사 = 법선 수직 성분은 유지, 법선 방향 성분만 부호 반전:**

$$\mathbf{v}_{ref} = \underbrace{\mathbf{v} - (\mathbf{v} \cdot \hat{n})\hat{n}}_{\text{수직 성분 그대로}} + \underbrace{(-(\mathbf{v} \cdot \hat{n})\hat{n})}_{\text{법선 성분 뒤집기}}$$

**3단계 — 정리:**

$$\boxed{\mathbf{v}_{ref} = \mathbf{v} - 2(\mathbf{v} \cdot \hat{n})\hat{n}}$$

#### ⑤ 수식의 의미

$\mathbf{v} - 2(\mathbf{v} \cdot \hat{n})\hat{n}$ 는 "입사 방향에서 법선 방향 성분을 두 배 뺀다"는 뜻이다.
법선 방향만 부호가 바뀌고 나머지는 그대로이므로 **입사각 = 반사각**이 자동으로 성립한다.

#### ⑥ 구체적 숫자 예시

$\mathbf{v} = (1, -1, 0)$ (45도 아래 오른쪽), $\hat{n} = (0, 1, 0)$ (위를 향하는 법선)

$$\mathbf{v} \cdot \hat{n} = (1)(0) + (-1)(1) + (0)(0) = -1$$

$$\mathbf{v}_{ref} = (1, -1, 0) - 2 \times (-1) \times (0, 1, 0) = (1, -1, 0) + (0, 2, 0) = (1, 1, 0)$$

$(1, -1, 0)$이 $(1, 1, 0)$으로 — y 성분만 뒤집혔다 ✓ 완벽한 대칭 반사.

#### ⑦ 코드와 연결

| 수식 기호 | 코드 | 의미 |
|---------|------|------|
| $\mathbf{v}$ | `v` | 입사 광선 방향 |
| $\hat{n}$ | `n` | 표면 법선 (단위벡터) |
| $\mathbf{v} \cdot \hat{n}$ | `dot(v, n)` | 내적 |
| $2(\mathbf{v} \cdot \hat{n})\hat{n}$ | `2*dot(v,n)*n` | 법선 방향 성분 × 2 |
| $\mathbf{v}_{ref}$ | `v - 2*dot(v,n)*n` | 반사 벡터 |

```cpp
// vec3.h
inline vec3 reflect(const vec3& v, const vec3& n)
{
    return v - 2*dot(v,n)*n;
}
```

---

### 개념 3: Fuzz — 흐린 금속 반사

완벽한 거울만 있으면 재미없다. 실제 금속은 표면이 약간 거칠어서 반사가 흐릿하다.

**아이디어:** 반사된 방향에 **작은 무작위 벡터를 더한다.**

```
완벽한 반사: reflected
                 ↗
────────────────── 표면

fuzz = 0.3:  reflected + 0.3 * random_unit_vector()
            /↗   ↗  ↗  (여러 방향 중 하나)
────────────────── 표면
```

- `fuzz = 0` → 완벽한 거울
- `fuzz = 1` → 매우 흐린 금속
- `fuzz > 1` → 의미 없음, 코드에서 1로 클램프

![Fuzz 금속 흐림](diagrams/fuzz.png)

반사된 방향을 정규화한 뒤 fuzz를 더하는 이유:
벡터 크기가 크면 fuzz의 영향이 줄어들고, 크기가 작으면 fuzz의 영향이 커진다.
정규화(길이 = 1)해야 fuzz가 항상 일관된 크기로 작용한다.

```cpp
reflected = unit_vector(reflected) + (fuzz * random_unit_vector());
```

**fuzz가 너무 크면 생기는 문제:**
무작위 벡터가 반사 방향을 표면 안쪽으로 밀어 넣을 수 있다.
이 경우 `dot(scattered.direction(), rec.normal) > 0` 검사로 빛 흡수 처리:

```cpp
return dot(scattered.direction(), rec.normal) > 0;
```

---

### 결과물

![Ch.8 Metal](pbr-raytracer/results/ch8_metal.png)

| 구 | 재질 | fuzz | 특징 |
|----|------|------|------|
| 가운데 (파랑) | `lambertian(0.1, 0.2, 0.5)` | — | 빛이 모든 방향으로 흩어짐 |
| 왼쪽 (은색) | `metal(0.8, 0.8, 0.8)` | 0.3 | 흐린 반사, 주변이 뭉개짐 |
| 오른쪽 (금색) | `metal(0.8, 0.6, 0.2)` | 0.0 | 완벽한 거울, 씬이 선명히 반사 |

오른쪽 금속 구에 왼쪽 금속 구의 모습이 선명하게 비치고, 노란 땅이 두 금속 구 표면에 반사되어 섞인다.
`fuzz` 차이가 시각적으로 명확하게 드러난다.

### 관련 파일
- [src/vec3.h](pbr-raytracer/src/vec3.h) (`near_zero()`, `reflect()` 추가)
- [src/material.h](pbr-raytracer/src/material.h) (이번 챕터에서 추가 — `material`, `lambertian`, `metal`)
- [src/hittable.h](pbr-raytracer/src/hittable.h) (`hit_record`에 `shared_ptr<material> mat` 추가)
- [src/sphere.h](pbr-raytracer/src/sphere.h) (생성자에 `material` 인자 추가, `rec.mat` 저장)
- [src/camera.h](pbr-raytracer/src/camera.h) (`ray_color`에서 `mat->scatter()` 호출로 교체)

---

## Ch.9 — 유전체 재질 (Dielectrics)

### 왜 이걸 하는가?

Ch.8까지는 두 가지 재질만 있었다 — 빛을 무작위로 흩뿌리는 확산(Diffuse)과 빛을 거울처럼 반사하는 금속(Metal).
하지만 현실의 재질은 훨씬 다양하다. **유리, 물, 다이아몬드**는 빛을 반사하기도 하고 통과시키기도 한다.
이 챕터의 목표: 빛이 매질 경계를 지날 때 **꺾이는 현상(굴절)** 을 수학적으로 구현한다.

---

### 개념 1: 굴절 — 스넬의 법칙 (Snell's Law)

#### ① 왜 이게 필요한가?

Metal의 `scatter()`는 "입사 방향을 법선에 대해 뒤집기"만 했다.
유리는 이것으로 부족하다 — 빛이 유리 표면을 **통과**하면서 방향이 바뀐다.
굴절 공식 없이는 유리 구가 그냥 흰 공으로 렌더링된다.

#### ② 머릿속 그림

```
    공기 (η = 1.0)
       ↘ 입사 광선 (θ₁)
────────────────────────  유리 표면
          ↘ 굴절 광선 (θ₂)  ← 법선 쪽으로 꺾임
    유리 (η = 1.5)
```

빛이 **느린 매질(유리)** 로 들어가면 법선 방향으로 꺾이고,
**빠른 매질(공기)** 로 나오면 법선에서 멀어지는 방향으로 꺾인다.

![굴절](diagrams/refraction.png)

#### ③ 일상 비유

수영장에서 물속을 보면 바닥이 실제보다 얕게 보이는 것. 빛이 물과 공기 경계에서 꺾이기 때문이다.

#### ④ 수식 전개

**스넬의 법칙 (기본형)**:

$$\eta_1 \sin\theta_1 = \eta_2 \sin\theta_2$$

η = 굴절률 (공기=1.0, 유리=1.5, 물=1.33, 다이아몬드=2.4)

이걸 코드에 바로 쓸 수 없으므로 **벡터 형태로 전개**한다.
굴절 벡터 $\mathbf{R'}$를 법선에 수직인 성분과 평행인 성분으로 분해한다:

$$\mathbf{R'}_\perp = \frac{\eta_1}{\eta_2}(\mathbf{R} + \cos\theta_1 \cdot \hat{n})$$

$$\mathbf{R'}_\parallel = -\sqrt{1 - |\mathbf{R'}_\perp|^2} \cdot \hat{n}$$

$$\mathbf{R'} = \mathbf{R'}_\perp + \mathbf{R'}_\parallel$$

단, $\cos\theta_1 = \mathbf{-\hat{R}} \cdot \hat{n}$ (입사 광선을 뒤집어서 법선과의 각도를 구함)

#### ⑤ 수식의 의미

$\mathbf{R'}_\perp$는 굴절 벡터의 **"표면과 나란한 성분"** 을 스넬 법칙 비율로 늘리거나 줄인다.
$\mathbf{R'}_\parallel$는 피타고라스 정리로 **"법선 방향 성분"** 을 역으로 계산한다.
둘을 더하면 정확한 굴절 방향 벡터가 나온다.

#### ⑥ 구체적 숫자 예시

수직 입사: $\mathbf{\hat{R}} = (0,-1,0)$, $\hat{n} = (0,1,0)$, $\eta_1/\eta_2 = 1.0/1.5$

$$\cos\theta_1 = (0,1,0) \cdot (0,1,0) = 1.0$$

$$\mathbf{R'}_\perp = \frac{1}{1.5} \cdot ((0,-1,0) + 1.0 \cdot (0,1,0)) = \frac{1}{1.5} \cdot (0,0,0) = (0,0,0)$$

$$\mathbf{R'}_\parallel = -\sqrt{1-0} \cdot (0,1,0) = (0,-1,0)$$

수직 입사라 꺾임 없이 그대로 통과 ✓

#### ⑦ 코드 연결

| 수식 기호 | 코드 | 위치 |
|---------|------|------|
| $\mathbf{\hat{R}}$ | `uv` | `refract()` 인자 |
| $\hat{n}$ | `n` | `refract()` 인자 |
| $\eta_1/\eta_2$ | `etai_over_etat` | `refract()` 인자 |
| $\cos\theta_1$ | `fmin(dot(-uv, n), 1.0)` | `refract()` 내부 |
| $\mathbf{R'}_\perp$ | `r_out_perp` | `refract()` 내부 |
| $\mathbf{R'}_\parallel$ | `r_out_parallel` | `refract()` 내부 |

```cpp
// vec3.h
inline vec3 refract(const vec3& uv, const vec3& n, double etai_over_etat)
{
    double cos_theta = fmin(dot(-uv, n), 1.0);
    vec3 r_out_perp     = etai_over_etat * (uv + cos_theta * n);
    vec3 r_out_parallel = -std::sqrt(std::fabs(1.0 - r_out_perp.length_squared())) * n;
    return r_out_perp + r_out_parallel;
}
```

---

### 개념 2: 전반사 (Total Internal Reflection)

#### ① 왜 이게 필요한가?

유리→공기 방향으로, 입사각이 충분히 크면 굴절이 물리적으로 불가능해진다.
이 경우를 처리하지 않으면 `sqrt()` 안에 음수가 들어가 NaN이 발생한다.

#### ② 머릿속 그림

```
    유리 (η = 1.5)
       ↗ 전반사 (굴절 없음)
──────P──────────────────  유리/공기 경계
    (각도가 임계각보다 크면 빛이 밖으로 못 나감)
    공기 (η = 1.0)
```

수중에서 수면을 비스듬히 올려다보면 수면이 거울처럼 보이는 현상이 바로 전반사다.

#### ③ 조건

스넬 법칙에서 $\sin\theta_2 = \frac{\eta_1}{\eta_2}\sin\theta_1$ 이 1을 초과하면 굴절 불가:

$$\frac{\eta_1}{\eta_2} \cdot \sin\theta_1 > 1.0 \implies \text{전반사}$$

코드에서 `sin_theta`는 피타고라스로 구한다: $\sin\theta = \sqrt{1 - \cos^2\theta}$

```cpp
bool cannot_refract = ri * sin_theta > 1.0;
if (cannot_refract || ...)
    direction = reflect(unit_dir, rec.normal);  // 반사만 일어남
```

![전반사](diagrams/total_internal_reflection.png)

---

### 개념 3: 슐릭 근사 (Schlick Approximation)

#### ① 왜 이게 필요한가?

실제 유리는 각도에 따라 반사율이 달라진다.
정면에서 보면 투명하지만, 비스듬히 보면 반사가 강해진다 (자동차 유리, 물 표면이 그렇다).
이를 정확히 계산하는 프레넬(Fresnel) 방정식은 복잡하므로, Christophe Schlick이 제안한 **5차 다항식 근사**를 쓴다.

#### ② 수식

$$R_0 = \left(\frac{\eta_1 - \eta_2}{\eta_1 + \eta_2}\right)^2$$

$$R(\theta) = R_0 + (1 - R_0)(1 - \cos\theta)^5$$

$R_0$은 수직 입사(θ=0)일 때의 반사율이다. 각도가 커질수록 $R(\theta)$가 1에 가까워진다.

#### ③ 코드 적용

$R(\theta)$와 `random_double()` 을 비교해 확률적으로 반사/굴절을 결정한다:

```cpp
if (cannot_refract || reflectance(cos_theta, ri) > random_double())
    direction = reflect(...);   // 반사
else
    direction = refract(...);   // 굴절
```

이렇게 하면 샘플이 쌓일수록 물리적으로 올바른 평균 반사율이 된다.

---

### 개념 4: 속 빈 유리 구 (Hollow Sphere)

**트릭**: 반지름이 음수인 구를 유리 구 안에 추가한다.

반지름이 음수이면 기하학적으로 같은 구지만 **법선이 안쪽을 향한다**.
결과적으로 `front_face`가 바뀌어 굴절률이 역전된다 → 빛이 유리→공기(안쪽)로 굴절.

```
           r = 0.5 (유리 바깥)
        ┌───────────────┐
        │   r = -0.4    │
        │  ┌─────────┐  │
        │  │  공기   │  │
        │  └─────────┘  │
        └───────────────┘
```

```cpp
auto mat_left   = make_shared<dielectric>(1.50);
auto mat_bubble = make_shared<dielectric>(1.00 / 1.50);  // 역수 = 공기→유리 역방향

world.add(make_shared<sphere>(point3(-1,0,-1),  0.5, mat_left));    // 바깥 유리
world.add(make_shared<sphere>(point3(-1,0,-1), -0.4, mat_bubble));  // 안쪽 공기 방울
```

![속 빈 유리 구](diagrams/hollow_sphere.png)

---

### 결과물

![Ch.9 Dielectrics](pbr-raytracer/results/ch9_dielectric.png)

| 구 | 재질 | 특징 |
|----|------|------|
| 가운데 (파랑) | `lambertian(0.1, 0.2, 0.5)` | 확산 반사 |
| 왼쪽 | `dielectric(1.50)` + 내부 공기 방울 | 속 빈 유리 — 씬이 뒤집혀 보임 |
| 오른쪽 (금색) | `metal(0.8, 0.6, 0.2), fuzz=0` | 완벽한 거울 반사 |

왼쪽 유리 구를 통해 씬이 굴절되어 뒤집혀 보이고, 비스듬히 보이는 가장자리는 슐릭 근사로 반사가 강해진다.

### 관련 파일
- [src/vec3.h](pbr-raytracer/src/vec3.h) (`refract()` 추가)
- [src/material.h](pbr-raytracer/src/material.h) (`dielectric` 클래스 추가)
- [src/main.cpp](pbr-raytracer/src/main.cpp) (씬에 유리 구 + 속 빈 구 추가)

---

## Ch.10 — 위치 조절 가능한 카메라 (Positionable Camera)

### 왜 이걸 하는가?

Ch.9까지는 카메라가 항상 **원점(0, 0, 0)에서 -z 방향**을 바라봤다.
`initialize()` 안에 `center = point3(0,0,0)`이 하드코딩되어 있었고, 뷰포트도 항상 세계 x/y축 기준이었다.

이번 챕터의 목표: 카메라를 **씬 어디서든, 어느 방향으로든** 놓을 수 있게 한다.
이를 위해 두 가지 수학 개념을 도입한다:
1. **카메라 로컬 좌표계 (u, v, w)** — lookfrom/lookat/vup 세 값으로 카메라 방향 확정
2. **FOV → 뷰포트 높이 변환** — 시야각(degree)을 뷰포트 크기(유닛)로 환산

---

### 개념 1: 카메라 로컬 좌표계 (u, v, w)

#### ① 왜 이게 필요한가?

지금 뷰포트는 세계 x축(`vec3(width, 0, 0)`)과 세계 -y축(`vec3(0, -height, 0)`)으로 만들어진다.
카메라가 기울어지거나 다른 방향을 바라보면 이 세계 축 기반 뷰포트는 완전히 틀어진다.
카메라 **자신만의 로컬 좌표축**으로 뷰포트를 만들어야 어느 방향을 바라봐도 올바르다.

#### ② 머릿속 그림

```
        vup (월드 위쪽, 보통 (0,1,0))
         ↑
         │    ← lookat (바라보는 지점)
         │   ╱
  lookfrom (카메라 위치)

구한 뒤:
  w = 카메라 뒤쪽 (lookfrom → lookat의 반대)
  u = 카메라 오른쪽 (w와 vup에 수직)
  v = 카메라 위쪽  (w와 u에 수직, 자동 결정)
```

#### ③ 일상 비유

GPS 내비게이션이 방향을 잡는 법 — "나는 여기(lookfrom) 서서 저기(lookat)를 본다. 하늘(vup)이 위쪽이다." 이 세 정보만 있으면 내 앞/뒤/좌/우가 완전히 확정된다.

#### ④ 수식 전개 — 외적으로 좌표계 구성

세 단위벡터 **w(뒤), u(오른쪽), v(위)** 를 순서대로 구한다:

$$\mathbf{w} = \frac{\text{lookfrom} - \text{lookat}}{|\text{lookfrom} - \text{lookat}|}$$

$$\mathbf{u} = \frac{\mathbf{vup} \times \mathbf{w}}{|\mathbf{vup} \times \mathbf{w}|}$$

$$\mathbf{v} = \mathbf{w} \times \mathbf{u}$$

**왜 이 순서인가?**

- `w`는 "바라보는 방향의 반대"이므로 `lookfrom - lookat`을 정규화.
- `u`는 w와 vup **둘 다에 수직**인 방향 → 외적 `vup × w`로 구한다. 이게 카메라 오른쪽.
- `v`는 w와 u가 확정된 뒤 자동으로 결정 → `w × u`. v는 이미 단위벡터인 두 수직 벡터의 외적이므로 별도 정규화 불필요.

#### ⑤ 수식의 의미

| 벡터 | 의미 | 코드에서 역할 |
|------|------|-------------|
| `w` | 카메라 뒤쪽 | 뷰포트 중심 = center - focal_length × **w** |
| `u` | 카메라 오른쪽 | `viewport_u = viewport_width × u` |
| `v` | 카메라 위쪽 | `viewport_v = -viewport_height × v` (아래가 +j이므로 부호 반전) |

기존의 `vec3(viewport_width, 0, 0)` (세계 x축)이 `viewport_width * u`로 바뀐다.
기존의 `vec3(0, -viewport_height, 0)` (세계 -y축)이 `-viewport_height * v`로 바뀐다.

#### ⑥ 구체적 숫자 예시

`lookfrom = (3, 3, 2)`, `lookat = (0, 0, -1)`, `vup = (0, 1, 0)` 일 때:

```
lookfrom - lookat = (3, 3, 3)
w = normalize(3,3,3) ≈ (0.577, 0.577, 0.577)

vup × w = (0,1,0) × (0.577, 0.577, 0.577)
        = (1×0.577 - 0×0.577, 0×0.577 - 0×0.577, 0×0.577 - 1×0.577)
        = (0.577, 0, -0.577)
u = normalize(0.577, 0, -0.577) ≈ (0.707, 0, -0.707)  ← 오른쪽

v = w × u ≈ (-0.408, 0.816, -0.408)  ← 위쪽 (자동 결정)
```

#### ⑦ 코드와 연결

```cpp
w = unit_vector(lookfrom - lookat);  // 뒤쪽
u = unit_vector(cross(vup, w));      // 오른쪽
v = cross(w, u);                     // 위쪽

vec3 viewport_u =  viewport_width  * u;  // 뷰포트 가로
vec3 viewport_v = -viewport_height * v;  // 뷰포트 세로 (-v: 아래가 +j)
```

![카메라 로컬 좌표계](diagrams/camera_coordinate.png)

---

### 개념 2: FOV → 뷰포트 높이 변환

#### ① 왜 이게 필요한가?

`vfov`는 각도(degree)다. 뷰포트는 유닛 크기의 직사각형이다.
"시야각 20°"를 "뷰포트 높이 몇 유닛"으로 변환해야 픽셀 계산이 가능하다.

#### ② 머릿속 그림

카메라를 옆에서 본 단면도:

```
카메라
  ●────────────────── 뷰포트 중심
  │ ← focal_length →  │
  │ vfov/2 각도        ├── h = viewport_height / 2
  └───────────────────┘
```

카메라~뷰포트 중심을 인접한 변(focal_length), 뷰포트 절반 높이를 반대편(h)으로 보면 직각삼각형이 만들어진다.

#### ③ 수식 전개

직각삼각형 탄젠트 정의:

$$\tan\!\left(\frac{\text{vfov}}{2}\right) = \frac{h}{f}$$

focal\_length를 $f$ 로 표기. 정리하면:

$$h = \tan\!\left(\frac{\text{vfov}}{2}\right) \times f$$

$$\text{viewport height} = 2h = 2 \times \tan\!\left(\frac{\text{vfov}}{2}\right) \times f$$

#### ④ 수식의 의미와 숫자 예시

`h`는 "focal_length 거리에 뷰포트를 놓았을 때 절반 높이"다.

| vfov | h = tan(vfov/2) | viewport_height (focal_length=1) |
|------|-----------------|----------------------------------|
| 90° | tan(45°) = 1.0 | 2.0 ← 이전 챕터 하드코딩 값과 동일 |
| 60° | tan(30°) ≈ 0.577 | 1.155 |
| 20° | tan(10°) ≈ 0.176 | 0.353 |

vfov가 작을수록 뷰포트가 좁아지고 → 씬이 확대되어 보인다 (망원렌즈 효과).

> **기존 코드와의 연결**: 이전 챕터의 `viewport_height = 2.0` 하드코딩은 사실 `vfov = 90°`일 때의 결과였다.

#### ⑤ 코드와 연결

```cpp
double focal_length    = (lookfrom - lookat).length();
double theta           = degrees_to_radians(vfov);
double h               = std::tan(theta / 2);
double viewport_height = 2.0 * h * focal_length;
```

| 수식 기호 | 코드 |
|---------|------|
| focal_length | `(lookfrom - lookat).length()` |
| vfov/2 (라디안) | `theta / 2` |
| tan(vfov/2) | `std::tan(theta / 2)` |
| h | `h` |
| viewport_height | `2.0 * h * focal_length` |

![FOV 뷰포트 높이 변환](diagrams/fov_viewport.png)

---

### 결과물

![Ch.10 Positionable Camera](pbr-raytracer/results/ch10_camera.png)

Ch.9와 동일한 씬이지만 카메라 설정이 완전히 달라졌다:

| 항목 | Ch.9 | Ch.10 |
|------|------|-------|
| 카메라 위치 | (0, 0, 0) 고정 | (3, 3, 2) — 오른쪽 위 대각선 |
| 바라보는 방향 | 항상 -z | lookat (0, 0, -1) 자유 설정 |
| vfov | 하드코딩(90°) | 20° — 망원 효과로 씬 확대 |

카메라가 오른쪽 위에서 내려다보는 구도로, 좁은 FOV 덕분에 구 세 개가 크게 확대되어 보인다.

### 관련 파일
- [src/camera.h](pbr-raytracer/src/camera.h) (`vfov`, `lookfrom`, `lookat`, `vup`, `u/v/w` 추가, `initialize()` 재구성)

---

## Ch.11 — Defocus Blur (심도 흐림 / 피사계 심도)

### 왜 이 기능이 필요한가

지금까지 모든 광선은 카메라의 단 한 점(핀홀)에서 출발했다.
실제 카메라·눈은 그렇지 않다. 렌즈(조리개)를 통해 빛이 들어오고,
**렌즈에서 일정 거리(초점 거리)에 있는 물체만 선명하게 맺히고** 그 앞뒤는 흐릿해진다.
이 효과를 **피사계 심도(Depth of Field, DoF)** 또는 **Defocus Blur**라고 한다.

이 챕터 이전까지는 씬 어디를 봐도 전부 선명했다.
실제 사진처럼 특정 거리만 초점이 맞고 나머지가 흐리게 만들려면 광선의 출발점을 바꿔야 한다.

---

### 개념 1: 핀홀 카메라 vs 렌즈 카메라

**머릿속 그림**
핀홀 카메라는 바늘구멍 하나에서 모든 빛이 들어온다.
어느 방향에서 온 빛이든 구멍을 지나면 하나의 점으로 모이기 때문에 거리와 무관하게 모든 게 선명하다.

렌즈 카메라는 조리개(렌즈)가 면적을 가진다.
같은 물체에서 나온 빛이 렌즈의 여러 점을 통과하는데, **초점 거리에 있는 물체의 빛만 한 점으로 수렴**한다.
초점 밖의 물체에서 온 빛은 렌즈의 여러 점을 지난 뒤 필름에 도달할 때 퍼져버려서 흐릿하게 보인다.

**비유**
손전등을 벽에 비출 때, 손전등과 벽 사이에 볼록 유리를 두면
유리에서 특정 거리의 물체만 뚜렷하게 보이고 나머지는 번진다.
그것이 바로 렌즈 카메라의 원리다.

![핀홀 카메라 vs 렌즈 카메라](diagrams/ch11_pinhole_vs_lens.png)

**레이트레이서에서의 해결책**
- 핀홀: 광선을 항상 `center` 한 점에서 출발시킨다 → 모든 게 선명
- 렌즈: 광선 출발점을 **조리개 원판(defocus disk) 위의 무작위 점**으로 바꾼다 → 초점 평면만 선명

---

### 개념 2: 조리개 원판(Defocus Disk)과 반지름 계산

**왜 이 수식이 필요한가**
조리개의 크기가 클수록 흐림이 강해진다.
`defocus_angle`(조리개의 열린 각도)과 `focus_dist`(초점까지의 거리)가 주어지면,
그로부터 조리개 원판의 실제 반지름을 계산해야 한다.

**머릿속 그림**
카메라 위치에서 초점 평면까지 직선을 그으면 `focus_dist`가 된다.
조리개 원판은 카메라 위치를 중심으로 카메라 면에 수직한 원이다.
`defocus_angle/2`는 이 원의 반지름이 중심 축과 이루는 각도다.

**수식 전개**

직각삼각형을 생각한다:
- 빗변: 초점 평면까지의 직선 (길이 = `focus_dist`)
- 각도: `defocus_angle / 2`
- 맞은편 변: 조리개 원판의 반지름 (`defocus_radius`)

기호 정의:

| 기호 | 코드 변수 |
|------|-----------|
| $\theta$ | `defocus_angle / 2` |
| $d$ | `focus_dist` |
| $r$ | `defocus_radius` |

$$
\tan(\theta) = \frac{r}{d}
$$

양변에 $d$를 곱하면:

$$
r = d \times \tan(\theta)
$$

**수식이 의미하는 것**
초점 거리가 길수록, 또는 조리개 각도가 클수록 원판이 커진다.
원판이 클수록 같은 픽셀에 대한 광선들이 더 넓은 범위에서 출발하므로 흐림이 강해진다.

**숫자 예시**
Ch.11 설정: `focus_dist ≈ 3.74`, `defocus_angle = 10°`

```
defocus_radius = 3.74 × tan(5°) = 3.74 × 0.0875 ≈ 0.327
```

**코드와 1:1 연결**

| 수식 기호 | 코드 변수/표현 |
|-----------|---------------|
| defocus\_angle / 2 | `defocus_angle / 2` (도 단위, `degrees_to_radians`로 변환) |
| focus\_dist | `focus_dist` |
| defocus\_radius | `defocus_radius` (지역 변수) |
| tan(·) | `std::tan(degrees_to_radians(defocus_angle / 2))` |

```cpp
double defocus_radius = focus_dist * std::tan(degrees_to_radians(defocus_angle / 2));
defocus_disk_u = u * defocus_radius;   // 카메라 오른쪽 방향 반지름 벡터
defocus_disk_v = v * defocus_radius;   // 카메라 위쪽 방향 반지름 벡터
```

![조리개 원판(Defocus Disk) 구조](diagrams/ch11_defocus_disk.png)

---

### 개념 3: 초점 평면(Focus Plane)

**왜 이 개념이 필요한가**
조리개 원판 위의 서로 다른 점에서 출발한 광선들이 한 점에서 만나야만 그 물체가 선명하게 보인다.
그 수렴 지점들의 집합이 **초점 평면**이다.

**머릿속 그림**
조리개 원판의 모든 점에서 같은 픽셀을 향해 광선을 쏜다.
각 광선의 방향은 `pixel_sample - ray_origin`으로 계산된다.
`pixel_sample`은 뷰포트 위의 점이고, 뷰포트는 `focus_dist` 거리에 있다.
따라서 원판 위 어느 점에서 출발하든 광선은 뷰포트의 같은 픽셀 위치를 지난다.

즉, **초점 평면 = 뷰포트가 위치한 평면** = 카메라에서 `focus_dist`만큼 떨어진 평면이다.

**비유**
카메라 여러 대가 부채꼴로 늘어서서 모두 같은 점(초점)을 향해 촬영하면
그 점은 모든 사진에서 같은 위치에 찍힌다 = 선명.
다른 거리에 있는 물체는 카메라마다 다른 각도로 찍혀서 합치면 번진다 = 흐림.

![초점 평면](diagrams/ch11_focus_plane.png)

**코드와의 연결**

```cpp
// 뷰포트를 focus_dist 거리에 배치 (기존 focal_length 대신)
double viewport_height = 2.0 * h * focus_dist;
point3 viewport_upper_left = center - (focus_dist * w) - viewport_u/2 - viewport_v/2;
```

Ch.10까지는 `focal_length = 1`이 고정이었다.
Ch.11에서는 `focus_dist`를 `focal_length` 자리에 사용함으로써
뷰포트가 초점 평면과 정확히 일치하게 된다.

---

### 개념 4: 조리개 원판 위 무작위 샘플링 (`defocus_disk_sample`)

**왜 이 수식이 필요한가**
광선 출발점을 원판 위의 무작위 점으로 결정해야 한다.
원판은 카메라의 로컬 좌표계(u, v)로 정의되므로,
단위 원판 안의 2D 점 `(p[0], p[1])`을 `defocus_disk_u`와 `defocus_disk_v`로 변환하면 된다.

**수식**

기호 정의:

| 기호 | 코드 변수 |
|------|-----------|
| $\mathbf{s}$ | sample (광선 출발점) |
| $\mathbf{c}$ | `center` |
| $p_0, p_1$ | `p[0]`, `p[1]` (단위 원판의 x, y 성분) |
| $\mathbf{u_d}$ | `defocus_disk_u` |
| $\mathbf{v_d}$ | `defocus_disk_v` |

$$
\mathbf{s} = \mathbf{c} + p_0 \cdot \mathbf{u_d} + p_1 \cdot \mathbf{v_d}
$$

여기서 $p$는 단위 원판 `random_in_unit_disk()`로 얻은 2D 점이다.

**수식이 의미하는 것**
`p[0]`은 오른쪽(u) 방향 성분, `p[1]`은 위쪽(v) 방향 성분이다.
이 둘을 조리개 반지름으로 스케일된 벡터에 곱하면
카메라 좌표계 기준 원판 위의 실제 3D 점이 된다.

**코드와 1:1 연결**

| 수식 기호 | 코드 |
|-----------|------|
| center | `center` |
| p[0] | `p[0]` (단위 원판의 x 성분) |
| p[1] | `p[1]` (단위 원판의 y 성분) |
| defocus\_disk\_u | `defocus_disk_u` (= `u * defocus_radius`) |
| defocus\_disk\_v | `defocus_disk_v` (= `v * defocus_radius`) |

```cpp
point3 defocus_disk_sample() const
{
    vec3 p = random_in_unit_disk();
    return center + (p[0] * defocus_disk_u) + (p[1] * defocus_disk_v);
}
```

`random_in_unit_disk()`는 기각 샘플링으로 단위 원판(z=0) 안의 무작위 점을 반환한다:
```cpp
inline vec3 random_in_unit_disk()
{
    while (true)
    {
        vec3 p = vec3(random_double(-1,1), random_double(-1,1), 0);
        if (p.length_squared() < 1)   // 원 안에 있으면 사용, 밖이면 버리고 재시도
            return p;
    }
}
```

---

### 개념 5: get_ray() 수정 — 출발점 선택

`defocus_angle`이 0이면 핀홀(기존), 0보다 크면 원판 샘플 사용:

```cpp
point3 ray_origin = (defocus_angle <= 0) ? center : defocus_disk_sample();
vec3 ray_direction = pixel_sample - ray_origin;
return ray(ray_origin, ray_direction);
```

**핵심 포인트**: `ray_direction`은 항상 `pixel_sample - ray_origin`이다.
`pixel_sample`은 뷰포트(초점 평면) 위의 점이기 때문에,
원판의 어느 점에서 출발하든 모든 광선이 뷰포트의 같은 점을 향한다.
결과적으로 초점 평면 위의 물체는 선명, 나머지는 흐릿하게 된다.

![Defocus Blur 효과](diagrams/ch11_defocus_effect.png)

---

### Ch.11 설정값 정리

```cpp
cam.defocus_angle = 10.0;   // 조리개 각도 — 클수록 흐림 강해짐
cam.focus_dist    = (point3(3,3,2) - point3(0,0,-1)).length();
                            // lookat 지점까지의 거리 = 초점이 맞는 거리
```

`focus_dist`를 `(lookfrom - lookat).length()`로 설정하면
**lookat 지점(씬 중심)이 정확히 초점**에 맞는다.
그 앞뒤의 구들은 흐릿하게 보인다.

| 파라미터 | 값 | 효과 |
|---------|-----|------|
| defocus_angle | 0 | 핀홀, 전부 선명 |
| defocus_angle | 10 | 강한 흐림 |
| focus_dist | lookat까지 거리 | lookat 지점에 초점 |

---

### 결과물

![Ch.11 Defocus Blur](pbr-raytracer/results/ch11_defocus.png)

lookat 지점인 `(0, 0, -1)` 근처의 파란 구(mat_center)가 가장 선명하고,
가까운 왼쪽 유리 구와 먼 오른쪽 금속 구는 흐릿하게 보인다.
`defocus_angle = 10°`로 상당히 강한 흐림 효과가 적용된 결과다.

### 관련 파일
- [src/camera.h](pbr-raytracer/src/camera.h) (`defocus_angle`, `focus_dist`, `defocus_disk_u/v`, `defocus_disk_sample()` 추가)
- [src/vec3.h](pbr-raytracer/src/vec3.h) (`random_in_unit_disk()` 추가)
