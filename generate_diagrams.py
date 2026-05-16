import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.colors import LinearSegmentedColormap
import os

os.makedirs("diagrams", exist_ok=True)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ── 1. 내적 (Dot Product) ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('내적 (Dot Product)', fontsize=16, fontweight='bold')

cases = [
    ("같은 방향\n(theta ~ 0deg)", 15,  "결과 > 0\n(양수)",  "#2ecc71"),
    ("수직\n(theta = 90deg)",    90,  "결과 = 0",          "#3498db"),
    ("반대 방향\n(theta ~ 180deg)", 165, "결과 < 0\n(음수)", "#e74c3c"),
]

for ax, (title, angle_deg, result, color) in zip(axes, cases):
    ax.set_xlim(-0.3, 1.5)
    ax.set_ylim(-0.3, 1.5)
    ax.set_aspect('equal')
    ax.axhline(0, color='#ccc', linewidth=0.5)
    ax.axvline(0, color='#ccc', linewidth=0.5)
    ax.set_title(title, fontsize=12)

    ax.annotate("", xy=(1.0, 0.0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50", lw=2))
    ax.text(1.05, 0.05, "a", fontsize=13, color="#2c3e50", fontweight='bold')

    rad = np.radians(angle_deg)
    bx, by = 0.9 * np.cos(rad), 0.9 * np.sin(rad)
    ax.annotate("", xy=(bx, by), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
    ax.text(bx + 0.05, by + 0.05, "b", fontsize=13, color=color, fontweight='bold')

    theta_arc = np.linspace(0, np.radians(angle_deg), 50)
    ax.plot(0.25 * np.cos(theta_arc), 0.25 * np.sin(theta_arc), color='gray', lw=1)
    mid = np.radians(angle_deg / 2)
    ax.text(0.32 * np.cos(mid), 0.32 * np.sin(mid), "theta", fontsize=10, color='gray')

    ax.text(0.5, -0.25, result, fontsize=11, ha='center', color=color, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/dot_product.png", dpi=120, bbox_inches='tight')
plt.close()
print("dot_product.png 생성 완료")

# ── 2. 외적 (Cross Product) ───────────────────────────────────────────────────
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('외적 (Cross Product)\na x b = c (두 벡터에 수직)', fontsize=13, fontweight='bold')

a = np.array([1.0, 0.0, 0.0])
b = np.array([0.0, 1.0, 0.0])
c = np.cross(a, b)

for vec, color, label, offset in [
    (a, '#e74c3c', 'a = (1,0,0)', (0.05, -0.15, 0)),
    (b, '#2ecc71', 'b = (0,1,0)', (-0.2, 0.05, 0)),
    (c, '#3498db', 'axb = (0,0,1)', (0.05, 0.05, 0.05)),
]:
    ax.quiver(0, 0, 0, *vec, color=color, arrow_length_ratio=0.15, linewidth=2.5)
    ax.text(vec[0]+offset[0], vec[1]+offset[1], vec[2]+offset[2],
            label, color=color, fontsize=11, fontweight='bold')

ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-0.1, 1.2)
ax.set_zlim(-0.1, 1.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=25, azim=30)

plt.tight_layout()
plt.savefig("diagrams/cross_product.png", dpi=120, bbox_inches='tight')
plt.close()
print("cross_product.png 생성 완료")

# ── 3. 정규화 (Normalization) ─────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle('정규화 (Normalization)', fontsize=16, fontweight='bold')

for ax, (vec, color, title, extra) in zip([ax1, ax2], [
    (np.array([2.0, 1.5]), '#e74c3c', '정규화 전 (임의의 벡터)',
     '길이 = sqrt(2^2 + 1.5^2) ~ 2.5'),
    (np.array([2.0, 1.5]) / np.linalg.norm([2.0, 1.5]), '#2ecc71', '정규화 후 (단위 벡터)',
     '길이 = 1.0'),
]):
    ax.set_xlim(-0.2, 2.5)
    ax.set_ylim(-0.2, 2.0)
    ax.set_aspect('equal')
    ax.axhline(0, color='#ccc', linewidth=0.8)
    ax.axvline(0, color='#ccc', linewidth=0.8)
    ax.set_title(title, fontsize=12)

    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), '--', color='#bdc3c7', lw=1, label='단위원 (반지름=1)')

    ax.annotate("", xy=vec, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5))
    length = np.linalg.norm(vec)
    ax.text(vec[0]+0.05, vec[1]+0.05, f'v\n길이={length:.2f}', color=color,
            fontsize=11, fontweight='bold')
    ax.text(1.0, -0.18, extra, fontsize=9, ha='center', color='#555')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("diagrams/normalization.png", dpi=120, bbox_inches='tight')
plt.close()
print("normalization.png 생성 완료")

# ── 4. 이미지 좌표계 (Image Coordinate System) ───────────────────────────────
fig, ax = plt.subplots(figsize=(9, 7))
ax.set_title('이미지 좌표계 — x는 오른쪽, y는 아래', fontsize=14, fontweight='bold')

W, H = 5, 4
# 픽셀 격자
for i in range(W + 1):
    ax.axvline(i, color='#bdc3c7', lw=0.8)
for j in range(H + 1):
    ax.axhline(j, color='#bdc3c7', lw=0.8)

# 모서리 픽셀 색상 채우기
corner_colors = {
    (0, 0): ('#111111', '(0,0)\n검정'),
    (W-1, 0): ('#e74c3c', f'({W-1},0)\n빨강'),
    (0, H-1): ('#2ecc71', f'(0,{H-1})\n초록'),
    (W-1, H-1): ('#f1c40f', f'({W-1},{H-1})\n노랑'),
}
for (ci, cj), (col, label) in corner_colors.items():
    ax.add_patch(patches.Rectangle((ci, cj), 1, 1, color=col, alpha=0.7))
    ax.text(ci + 0.5, cj + 0.5, label, ha='center', va='center',
            fontsize=9, color='white', fontweight='bold')

# 일반 픽셀들 (회색)
for i in range(W):
    for j in range(H):
        if (i, j) not in corner_colors:
            ax.add_patch(patches.Rectangle((i, j), 1, 1, color='#ecf0f1', alpha=0.5))

# 픽셀 (2,1) 강조 — (i,j) 설명용
ax.add_patch(patches.Rectangle((2, 1), 1, 1, color='#3498db', alpha=0.5))
ax.text(2.5, 1.5, '(i=2, j=1)', ha='center', va='center', fontsize=9,
        color='white', fontweight='bold')

# 축 화살표
ax.annotate("", xy=(W + 0.7, 0), xytext=(-0.3, 0),
            arrowprops=dict(arrowstyle="-|>", color='#2c3e50', lw=2))
ax.text(W + 0.75, 0.1, 'x (i)', fontsize=12, color='#2c3e50', fontweight='bold')

ax.annotate("", xy=(0, H + 0.7), xytext=(0, -0.3),
            arrowprops=dict(arrowstyle="-|>", color='#2c3e50', lw=2))
ax.text(0.1, H + 0.75, 'y (j)\n아래로 증가', fontsize=11, color='#2c3e50', fontweight='bold')

# 메모리 순서 표시
ax.annotate("", xy=(W - 0.1, 0.5), xytext=(0.1, 0.5),
            arrowprops=dict(arrowstyle="-|>", color='#9b59b6', lw=1.5, linestyle='dashed'))
ax.text(W / 2, 0.2, '메모리 저장 순서 (행 단위, 왼쪽→오른쪽)', ha='center',
        fontsize=8, color='#9b59b6')

ax.set_xlim(-0.5, W + 1.2)
ax.set_ylim(-0.5, H + 1.2)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/image_coords.png", dpi=120, bbox_inches='tight')
plt.close()
print("image_coords.png 생성 완료")

# ── 5. 뷰포트 구조 (Viewport) ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title('뷰포트 구조 — 카메라, 가상 스크린, 광선', fontsize=14, fontweight='bold')

# 카메라
cam = np.array([0, 0])
ax.plot(*cam, 'o', color='#2c3e50', markersize=12, zorder=5)
ax.text(-0.3, 0.1, '카메라\n(원점)', fontsize=11, ha='center', color='#2c3e50', fontweight='bold')

# focal_length 화살표
focal = 3.0
ax.annotate("", xy=(focal, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="<->", color='#7f8c8d', lw=1.5))
ax.text(focal / 2, -0.25, 'focal_length', ha='center', fontsize=10, color='#7f8c8d')

# 뷰포트 직사각형
vp_h = 2.0
vp_top = vp_h / 2
vp_bot = -vp_h / 2
ax.plot([focal, focal], [vp_bot, vp_top], color='#3498db', lw=3, label='뷰포트')
ax.add_patch(patches.Rectangle((focal - 0.05, vp_bot), 0.1, vp_h, color='#3498db', alpha=0.2))

# 뷰포트 레이블
ax.text(focal + 0.15, 0, '뷰포트\n(가상 스크린)', fontsize=10, va='center', color='#3498db', fontweight='bold')

# viewport_v 화살표 (세로)
ax.annotate("", xy=(focal - 0.3, vp_bot), xytext=(focal - 0.3, vp_top),
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2))
ax.text(focal - 0.7, 0, 'viewport_v\n(아래 방향)', fontsize=9, va='center',
        ha='center', color='#e74c3c')

# 픽셀 분할선 (3개 픽셀 예시)
n_pixels = 4
pixel_size = vp_h / n_pixels
pixel_centers_y = [vp_top - pixel_size * (i + 0.5) for i in range(n_pixels)]

for y in pixel_centers_y:
    ax.plot(focal, y, 's', color='#e67e22', markersize=6, zorder=4)

for i in range(1, n_pixels):
    y = vp_top - pixel_size * i
    ax.plot([focal - 0.05, focal + 0.05], [y, y], color='#bdc3c7', lw=1)

# pixel_delta_v 표시
ax.annotate("", xy=(focal + 0.4, pixel_centers_y[1]),
            xytext=(focal + 0.4, pixel_centers_y[0]),
            arrowprops=dict(arrowstyle="<->", color='#e67e22', lw=1.5))
ax.text(focal + 0.65, (pixel_centers_y[0] + pixel_centers_y[1]) / 2,
        'pixel_\ndelta_v', fontsize=8, va='center', color='#e67e22')

# pixel00_loc 표시
ax.plot(focal, pixel_centers_y[0], '*', color='#9b59b6', markersize=14, zorder=6)
ax.text(focal + 0.15, pixel_centers_y[0] + 0.15, 'pixel00_loc\n(첫 픽셀 중심)',
        fontsize=9, color='#9b59b6', fontweight='bold')

# 광선들
ray_colors = ['#2ecc71', '#27ae60', '#1a8a4a', '#0f5e32']
for i, (py, col) in enumerate(zip(pixel_centers_y, ray_colors)):
    target = np.array([focal, py])
    direction = target - cam
    end = cam + direction * 1.5
    ax.annotate("", xy=end, xytext=cam,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, alpha=0.8))

ax.text(focal * 1.35, 0.6, '광선들이\n픽셀 중심을\n향해 발사됨',
        fontsize=9, color='#27ae60', ha='center',
        bbox=dict(boxstyle='round', facecolor='#eafaf1', edgecolor='#2ecc71', alpha=0.8))

ax.set_xlim(-0.8, 6.0)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/viewport.png", dpi=120, bbox_inches='tight')
plt.close()
print("viewport.png 생성 완료")

# ── 6. 선형 보간 Lerp (Sky Gradient) ─────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(13, 7))
fig.suptitle('선형 보간 (Lerp) — y값으로 하늘 색상 결정', fontsize=14, fontweight='bold')

# 왼쪽: y값 범위
ax = axes[0]
ax.set_title('① 정규화된 광선의 y값', fontsize=11)
for y_val, label, col in [
    (1.0, 'y = +1.0\n(위)', '#3498db'),
    (0.5, 'y = +0.5', '#5dade2'),
    (0.0, 'y =  0.0\n(수평)', '#aed6f1'),
    (-0.5, 'y = -0.5', '#d5e8d4'),
    (-1.0, 'y = -1.0\n(아래)', '#ffffff'),
]:
    ax.barh(y_val, 1, height=0.4, color=col, edgecolor='#bdc3c7')
    ax.text(1.05, y_val, label, va='center', fontsize=9, color='#2c3e50')
ax.set_xlim(0, 1.8)
ax.set_ylim(-1.3, 1.3)
ax.set_xticks([])
ax.set_ylabel('y 성분 (-1 ~ +1)', fontsize=10)
ax.axhline(0, color='#bdc3c7', lw=0.8, linestyle='--')

# 가운데: t값 변환
ax = axes[1]
ax.set_title('② t = (y+1) / 2 변환', fontsize=11)
y_vals = np.linspace(-1, 1, 100)
t_vals = (y_vals + 1) / 2
ax.plot(t_vals, y_vals, color='#e74c3c', lw=2.5)
for y_val, t_val in [(-1.0, 0.0), (0.0, 0.5), (1.0, 1.0)]:
    ax.plot(t_val, y_val, 'o', color='#2c3e50', markersize=8, zorder=5)
    ax.text(t_val + 0.03, y_val, f'y={y_val:.1f}\nt={t_val:.1f}',
            fontsize=8, va='center', color='#2c3e50')
ax.set_xlabel('t (0 ~ 1)', fontsize=10)
ax.set_ylabel('y (-1 ~ +1)', fontsize=10)
ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-1.3, 1.3)
ax.grid(True, alpha=0.3)
ax.axhline(0, color='#bdc3c7', lw=0.8)
ax.axvline(0.5, color='#bdc3c7', lw=0.8, linestyle='--')

# 오른쪽: 최종 색상 그라디언트
ax = axes[2]
ax.set_title('③ 최종 색상 (1-t)*흰색 + t*하늘색', fontsize=11)
white = np.array([1.0, 1.0, 1.0])
sky   = np.array([0.5, 0.7, 1.0])
gradient = np.array([[(1-t)*white + t*sky for t in np.linspace(0, 1, 200)]])
ax.imshow(gradient, aspect='auto', extent=[0, 1, -1, 1], origin='lower')
ax.text(0.5, 0.85, 't=1.0\n하늘색 (0.5, 0.7, 1.0)', ha='center', fontsize=9,
        color='white', fontweight='bold', transform=ax.transAxes)
ax.text(0.5, 0.08, 't=0.0\n흰색 (1.0, 1.0, 1.0)', ha='center', fontsize=9,
        color='#2c3e50', fontweight='bold', transform=ax.transAxes)
ax.set_ylabel('t값', fontsize=10)
ax.set_xticks([])

plt.tight_layout()
plt.savefig("diagrams/lerp.png", dpi=120, bbox_inches='tight')
plt.close()
print("lerp.png 생성 완료")

# ── 7. 광선-구 교차 3가지 경우 (Ray-Sphere Intersection) ──────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('광선-구 교차 — 판별식에 따른 3가지 경우', fontsize=14, fontweight='bold')

sphere_center = np.array([0.0, 0.0])
sphere_radius = 1.0

cases = [
    {
        'title': '빗나감\n(판별식 < 0)',
        'ray_origin': np.array([-2.5, 1.8]),
        'ray_dir': np.array([1.0, -0.3]),
        'hits': [],
        'disc_color': '#e74c3c',
        'disc_text': 'h² - ac < 0\n교차점 없음',
    },
    {
        'title': '접선 (스침)\n(판별식 = 0)',
        'ray_origin': np.array([-2.5, 1.0]),
        'ray_dir': np.array([1.0, 0.0]),
        'hits': [1],
        'disc_color': '#f39c12',
        'disc_text': 'h² - ac = 0\n교차점 1개',
    },
    {
        'title': '통과\n(판별식 > 0)',
        'ray_origin': np.array([-2.5, 0.2]),
        'ray_dir': np.array([1.0, 0.0]),
        'hits': [2],
        'disc_color': '#2ecc71',
        'disc_text': 'h² - ac > 0\n교차점 2개',
    },
]

for ax, case in zip(axes, cases):
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-2.0, 2.5)
    ax.set_aspect('equal')

    # 구 그리기
    circle = Circle(sphere_center, sphere_radius, fill=True,
                    facecolor='#d6eaf8', edgecolor='#2980b9', lw=2.5)
    ax.add_patch(circle)
    ax.plot(*sphere_center, '+', color='#2980b9', markersize=10, markeredgewidth=2)
    ax.text(sphere_center[0] + 0.1, sphere_center[1] - 0.25, 'C', fontsize=12,
            color='#2980b9', fontweight='bold')

    # 반지름 표시
    ax.annotate("", xy=(sphere_center[0] + sphere_radius, sphere_center[1]),
                xytext=sphere_center,
                arrowprops=dict(arrowstyle="-", color='#7f8c8d', lw=1.2, linestyle='dashed'))
    ax.text(sphere_center[0] + sphere_radius/2, sphere_center[1] + 0.12,
            'r', fontsize=10, ha='center', color='#7f8c8d')

    # 광선 그리기
    origin = case['ray_origin']
    direction = case['ray_dir'] / np.linalg.norm(case['ray_dir'])
    t_end = 5.5
    end = origin + t_end * direction
    ax.annotate("", xy=end, xytext=origin,
                arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2))
    ax.text(origin[0] - 0.1, origin[1] + 0.15, '광선', fontsize=9,
            color='#e74c3c', fontweight='bold')

    # 교차점 표시
    if case['hits'] == [1]:  # 접선
        hit_x = sphere_center[0]
        hit_y = origin[1]
        ax.plot(hit_x, hit_y, 'o', color='#f39c12', markersize=10, zorder=6)
        ax.text(hit_x + 0.1, hit_y + 0.2, 'P\n(t₁=t₂)', fontsize=9,
                color='#f39c12', fontweight='bold')
    elif case['hits'] == [2]:  # 통과
        # 교차점 계산
        oc = sphere_center - origin
        a = np.dot(direction, direction)
        h = np.dot(direction, oc)
        c = np.dot(oc, oc) - sphere_radius**2
        disc = h*h - a*c
        if disc >= 0:
            t1 = (h - np.sqrt(disc)) / a
            t2 = (h + np.sqrt(disc)) / a
            p1 = origin + t1 * direction
            p2 = origin + t2 * direction
            ax.plot(*p1, 'o', color='#2ecc71', markersize=10, zorder=6)
            ax.plot(*p2, 'o', color='#27ae60', markersize=10, zorder=6)
            ax.text(p1[0] - 0.25, p1[1] + 0.2, 'P₁\n(t₁, 첫 교차)', fontsize=8,
                    color='#2ecc71', fontweight='bold')
            ax.text(p2[0] + 0.1, p2[1] + 0.2, 'P₂\n(t₂, 두번째)', fontsize=8,
                    color='#27ae60', fontweight='bold')

    # 판별식 결과 박스
    ax.text(0, 2.2, case['disc_text'], ha='center', fontsize=10,
            color=case['disc_color'], fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white',
                      edgecolor=case['disc_color'], alpha=0.9))
    ax.set_title(case['title'], fontsize=12, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/ray_sphere.png", dpi=120, bbox_inches='tight')
plt.close()
print("ray_sphere.png 생성 완료")

# ── 8. 법선 벡터 색상 매핑 (Normal Color Mapping) ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('법선 벡터 색상 매핑 — 방향을 RGB로 시각화', fontsize=14, fontweight='bold')

# 왼쪽: 법선 벡터 방향과 색상
ax = axes[0]
ax.set_title('구 표면의 법선 벡터 (앞면)', fontsize=11)

center = np.array([0.0, 0.0])
radius = 1.2
circle = Circle(center, radius, fill=True, facecolor='#f0f0f0',
                edgecolor='#2c3e50', lw=2)
ax.add_patch(circle)
ax.plot(*center, '+', color='#2c3e50', markersize=10, markeredgewidth=2)
ax.text(0.08, -0.15, 'C', fontsize=12, color='#2c3e50', fontweight='bold')

# 여러 각도의 법선 벡터
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
for deg in angles_deg:
    rad = np.radians(deg)
    nx = np.cos(rad)
    ny = np.sin(rad)

    # 법선 성분 (x, y 만으로 색상 결정, z=0 가정)
    r_col = (nx + 1) * 0.5
    g_col = (ny + 1) * 0.5
    b_col = 0.5  # z=0이면 (0+1)*0.5 = 0.5 → 약간 파랑
    arrow_color = (r_col, g_col, b_col)

    start = center + 0.3 * np.array([nx, ny])
    end = center + (radius + 0.35) * np.array([nx, ny])
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=3))

    label_pos = center + (radius + 0.7) * np.array([nx, ny])
    r_int = int(r_col * 255)
    g_int = int(g_col * 255)
    b_int = int(b_col * 255)
    ax.text(label_pos[0], label_pos[1],
            f'R={r_int}\nG={g_int}',
            ha='center', va='center', fontsize=7.5,
            color=arrow_color, fontweight='bold')

# 축 레이블
ax.text(1.8, 0, '+X\n(빨강)', ha='center', fontsize=9, color='#e74c3c', fontweight='bold')
ax.text(-1.8, 0, '-X\n(검정)', ha='center', fontsize=9, color='#7f8c8d')
ax.text(0, 1.8, '+Y\n(초록)', ha='center', fontsize=9, color='#2ecc71', fontweight='bold')
ax.text(0, -1.8, '-Y\n(검정)', ha='center', fontsize=9, color='#7f8c8d')

ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-2.3, 2.3)
ax.set_aspect('equal')
ax.axis('off')

# 오른쪽: -1~+1 → 0~1 변환 설명
ax = axes[1]
ax.set_title('변환 공식: (법선 성분 + 1) × 0.5', fontsize=11)

n_vals = np.linspace(-1, 1, 200)
color_vals = (n_vals + 1) * 0.5

# X축 (빨강)
ax.plot(n_vals, color_vals, color='#e74c3c', lw=3, label='R = (nx + 1) × 0.5')
# Y축 (초록)
ax.plot(n_vals, color_vals, color='#2ecc71', lw=3, linestyle='--',
        label='G = (ny + 1) × 0.5', alpha=0.7)

# 주요 점 강조
key_points = [(-1.0, 0.0, '법선=-1\n→ 색상=0\n(검정)'),
              (0.0, 0.5,  '법선= 0\n→ 색상=0.5\n(중간)'),
              (1.0, 1.0,  '법선=+1\n→ 색상=1.0\n(최대)')]
for nx, col, label in key_points:
    ax.plot(nx, col, 'o', color='#2c3e50', markersize=9, zorder=5)
    offset_x = 0.05 if nx >= 0 else -0.05
    ha = 'left' if nx >= 0 else 'right'
    ax.text(nx + offset_x, col, label, va='center', ha=ha, fontsize=9)

ax.set_xlabel('법선 벡터 성분 (-1 ~ +1)', fontsize=11)
ax.set_ylabel('색상 채널 값 (0 ~ 1)', fontsize=11)
ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-0.1, 1.3)
ax.legend(fontsize=9, loc='upper left')
ax.grid(True, alpha=0.3)
ax.axhline(0, color='#bdc3c7', lw=0.8)
ax.axvline(0, color='#bdc3c7', lw=0.8)

plt.tight_layout()
plt.savefig("diagrams/normal_colors.png", dpi=120, bbox_inches='tight')
plt.close()
print("normal_colors.png 생성 완료")

# ── 9. 앞면/뒷면 법선 (Front Face vs Back Face) ────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('앞면/뒷면 법선 — 광선 방향과 법선의 내적 부호로 판별', fontsize=14, fontweight='bold')

sphere_c = np.array([0.0, 0.0])
sphere_r = 1.2

cases = [
    {
        'ax': axes[0],
        'title': '앞면 (Front Face) — 광선이 밖에서 들어옴',
        'origin': np.array([-3.0, 0.6]),
        'outside': True,
        'dot_color': '#2980b9',
        'dot_text': 'dot(광선, 외향법선) < 0\n→ 앞면 (front_face = true)\n→ 법선 그대로 사용',
        'box_color': '#d6eaf8',
        'box_edge': '#2980b9',
    },
    {
        'ax': axes[1],
        'title': '뒷면 (Back Face) — 광선이 안에서 나감',
        'origin': np.array([-0.4, 0.3]),
        'outside': False,
        'dot_color': '#c0392b',
        'dot_text': 'dot(광선, 외향법선) > 0\n→ 뒷면 (front_face = false)\n→ 법선을 뒤집어 사용',
        'box_color': '#fadbd8',
        'box_edge': '#c0392b',
    },
]

for case in cases:
    ax = case['ax']
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.0, 2.5)
    ax.set_aspect('equal')
    ax.set_title(case['title'], fontsize=11, fontweight='bold')

    # 구
    circle = Circle(sphere_c, sphere_r, fill=True,
                    facecolor='#f0f0f0', edgecolor='#2c3e50', lw=2)
    ax.add_patch(circle)
    ax.plot(*sphere_c, '+', color='#2c3e50', markersize=10, markeredgewidth=2)
    ax.text(0.08, -0.18, 'C', fontsize=11, color='#2c3e50', fontweight='bold')

    origin = case['origin']

    # 광선 방향 (구의 표면을 향하도록 설계)
    if case['outside']:
        # 밖→안: 표면에 적당히 부딪히게
        target_angle = np.radians(150)  # 표면 점 위치
        hit_point = sphere_c + sphere_r * np.array([np.cos(target_angle), np.sin(target_angle)])
        direction = (hit_point - origin)
        direction = direction / np.linalg.norm(direction)
    else:
        # 안→밖: 원점이 구 내부, 바깥쪽 표면 향함
        target_angle = np.radians(40)
        hit_point = sphere_c + sphere_r * np.array([np.cos(target_angle), np.sin(target_angle)])
        direction = (hit_point - origin)
        direction = direction / np.linalg.norm(direction)

    # 광선 (시작점에서 hit_point 너머까지)
    ray_end = origin + direction * 5.0
    ax.annotate("", xy=ray_end, xytext=origin,
                arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2.2, alpha=0.85))
    ax.plot(*origin, 'o', color='#e74c3c', markersize=8, zorder=5)
    ax.text(origin[0] - 0.05, origin[1] + 0.25, '광선 시작', fontsize=8.5,
            color='#e74c3c', ha='right', fontweight='bold')

    # 광선 방향 라벨
    mid = origin + direction * 1.3
    ax.text(mid[0], mid[1] + 0.22, 'r.direction()', fontsize=9,
            color='#e74c3c', ha='center', fontweight='bold')

    # 충돌점
    ax.plot(*hit_point, 'o', color='#f39c12', markersize=10, zorder=6)
    ax.text(hit_point[0], hit_point[1] - 0.3, 'P (충돌점)', fontsize=9,
            ha='center', color='#f39c12', fontweight='bold')

    # 외향 법선 (P - C, 항상 바깥 방향)
    outward = (hit_point - sphere_c) / sphere_r
    n_start = hit_point
    n_end = hit_point + outward * 1.0
    ax.annotate("", xy=n_end, xytext=n_start,
                arrowprops=dict(arrowstyle="-|>", color='#2980b9', lw=2.2))
    ax.text(n_end[0] + 0.1 * outward[0], n_end[1] + 0.1 * outward[1] + 0.1,
            '외향 법선\n(P - C) / r', fontsize=8.5, ha='center',
            color='#2980b9', fontweight='bold')

    # 뒷면일 경우, 뒤집힌 법선도 함께 표시
    if not case['outside']:
        flipped_end = hit_point - outward * 1.0
        ax.annotate("", xy=flipped_end, xytext=hit_point,
                    arrowprops=dict(arrowstyle="-|>", color='#27ae60',
                                    lw=2.2, linestyle='dashed'))
        ax.text(flipped_end[0] - 0.15, flipped_end[1] - 0.2,
                '실제 사용할\n법선 (뒤집음)', fontsize=8.5, ha='center',
                color='#27ae60', fontweight='bold')

    # 내적 부호 결과 박스
    ax.text(0, 2.15, case['dot_text'], ha='center', fontsize=9.5,
            color=case['dot_color'], fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=case['box_color'],
                      edgecolor=case['box_edge'], alpha=0.95))

    # 각도 시각화 (광선 방향과 외향 법선 사이)
    # 각도를 작은 호로 표시
    angle_ray = np.degrees(np.arctan2(direction[1], direction[0]))
    angle_n = np.degrees(np.arctan2(outward[1], outward[0]))
    arc_radius = 0.35
    a_start = min(angle_ray, angle_n)
    a_end = max(angle_ray, angle_n)
    arc_theta = np.linspace(np.radians(a_start), np.radians(a_end), 40)
    arc_x = hit_point[0] + arc_radius * np.cos(arc_theta)
    arc_y = hit_point[1] + arc_radius * np.sin(arc_theta)
    ax.plot(arc_x, arc_y, color='#7f8c8d', lw=1.2)

    ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/front_back_face.png", dpi=120, bbox_inches='tight')
plt.close()
print("front_back_face.png 생성 완료")

# ── 10. 가장 가까운 t 선택 (Closest Hit Selection) ─────────────────────────────
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_title('여러 오브젝트 중 가장 가까운 충돌 찾기 (hittable_list)', fontsize=14, fontweight='bold')

# 카메라
cam = np.array([-4.5, 0.0])
ax.plot(*cam, 'o', color='#2c3e50', markersize=12, zorder=6)
ax.text(cam[0] - 0.25, cam[1] - 0.5, '카메라', fontsize=10,
        ha='center', color='#2c3e50', fontweight='bold')

# 광선 방향 (오른쪽으로)
ray_dir = np.array([1.0, 0.0])
ray_end_full = cam + ray_dir * 12.0
ax.annotate("", xy=ray_end_full, xytext=cam,
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2, alpha=0.6))

# 3개의 구체 (각각 다른 t 값에서 충돌)
spheres = [
    {'center': np.array([-1.2, 0.4]),  'radius': 0.7, 't': 2.6, 'label': '구 A',
     'fill': '#aed6f1', 'edge': '#2980b9'},
    {'center': np.array([1.5, -0.5]),  'radius': 0.9, 't': 5.1, 'label': '구 B',
     'fill': '#a9dfbf', 'edge': '#27ae60'},
    {'center': np.array([4.5, 0.3]),   'radius': 1.0, 't': 8.0, 'label': '구 C',
     'fill': '#f5cba7', 'edge': '#d35400'},
]

# 각 구의 충돌점 계산 (실제 광선과 구 교차)
for s in spheres:
    # 광선이 구에 충돌하는 첫 t 계산
    oc = s['center'] - cam
    a_ = np.dot(ray_dir, ray_dir)
    h_ = np.dot(ray_dir, oc)
    c_ = np.dot(oc, oc) - s['radius']**2
    disc = h_*h_ - a_*c_
    if disc >= 0:
        t = (h_ - np.sqrt(disc)) / a_
    else:
        t = None
    s['t_real'] = t

    circle = Circle(s['center'], s['radius'], fill=True,
                    facecolor=s['fill'], edgecolor=s['edge'], lw=2)
    ax.add_patch(circle)
    ax.text(s['center'][0], s['center'][1], s['label'], ha='center', va='center',
            fontsize=10, fontweight='bold', color=s['edge'])

# 충돌점 표시 (가장 가까운 것 강조)
hits = [(s, s['t_real']) for s in spheres if s['t_real'] is not None]
hits.sort(key=lambda x: x[1])

for idx, (s, t) in enumerate(hits):
    p = cam + ray_dir * t
    if idx == 0:
        ax.plot(*p, '*', color='#c0392b', markersize=22, zorder=7,
                markeredgecolor='black', markeredgewidth=1)
        ax.text(p[0], p[1] + 0.7,
                f'★ 채택!\nt = {t:.2f}\n(가장 작은 양수)',
                ha='center', fontsize=9.5, color='#c0392b', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#fadbd8',
                          edgecolor='#c0392b', alpha=0.95))
    else:
        ax.plot(*p, 'o', color='#7f8c8d', markersize=10, zorder=5, alpha=0.6)
        ax.text(p[0], p[1] - 0.6, f't = {t:.2f}\n(가려짐)', ha='center',
                fontsize=8.5, color='#7f8c8d', alpha=0.9)

# 알고리즘 의사 표현 (한글 + 코드 혼합)
code_text = ('알고리즘:\n'
             '  closest = t_max\n'
             '  for obj in world:\n'
             '    if obj.hit(r, t_min, closest, rec):\n'
             '      closest = rec.t   (더 가까운 t로 갱신)\n'
             '  return rec  (가장 작은 t의 충돌)')
ax.text(-4.4, -2.0, code_text, fontsize=9,
        color='#2c3e50',
        bbox=dict(boxstyle='round', facecolor='#fdfefe',
                  edgecolor='#bdc3c7', alpha=0.95))

ax.set_xlim(-5.5, 8.0)
ax.set_ylim(-2.7, 2.5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/closest_hit.png", dpi=120, bbox_inches='tight')
plt.close()
print("closest_hit.png 생성 완료")

# ── 11. 에일리어싱 vs 안티에일리어싱 ──────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('에일리어싱 — 픽셀당 1샘플 vs N샘플 평균', fontsize=14, fontweight='bold')

# 격자 크기와 가상 구의 윤곽
W_grid, H_grid = 16, 10
sphere_cx, sphere_cy = 8.5, 5.0
sphere_r = 4.5

np.random.seed(42)

def is_inside_sphere(x, y):
    return (x - sphere_cx)**2 + (y - sphere_cy)**2 <= sphere_r**2

# ── 왼쪽: 1샘플 (계단 현상)
ax = axes[0]
ax.set_title('① 픽셀당 1샘플 — 계단 현상 (Aliasing)', fontsize=11)

for i in range(W_grid):
    for j in range(H_grid):
        cx, cy = i + 0.5, j + 0.5
        # 픽셀 중심에서만 샘플 → 0 또는 1
        inside = is_inside_sphere(cx, cy)
        color = '#3498db' if inside else '#ecf0f1'
        ax.add_patch(patches.Rectangle((i, j), 1, 1, color=color,
                                       edgecolor='#bdc3c7', lw=0.5))
        ax.plot(cx, cy, 'o', color='#e74c3c', markersize=3, zorder=5)

# 진짜 구 윤곽 (참고용)
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(sphere_cx + sphere_r*np.cos(theta),
        sphere_cy + sphere_r*np.sin(theta),
        '--', color='#27ae60', lw=2, label='실제 구 윤곽')

ax.set_xlim(-0.5, W_grid + 0.5)
ax.set_ylim(-0.5, H_grid + 0.5)
ax.set_aspect('equal')
ax.legend(fontsize=9, loc='upper right')
ax.text(W_grid/2, -1.0, '각 픽셀 → 검정 또는 파랑 (이진)\n경계가 톱니처럼 보임',
        ha='center', fontsize=10, color='#c0392b', fontweight='bold')
ax.axis('off')

# ── 오른쪽: N샘플 평균 (부드러움)
ax = axes[1]
ax.set_title('② 픽셀당 9샘플 평균 — 부드러움 (Anti-aliasing)', fontsize=11)

samples_per_pixel = 9

for i in range(W_grid):
    for j in range(H_grid):
        # 픽셀 안의 무작위 9개 위치
        offsets_x = np.random.uniform(0, 1, samples_per_pixel)
        offsets_y = np.random.uniform(0, 1, samples_per_pixel)
        sample_xs = i + offsets_x
        sample_ys = j + offsets_y

        # 평균 = 구 안에 들어간 샘플 비율 (0.0 ~ 1.0)
        inside_count = sum(is_inside_sphere(sx, sy)
                          for sx, sy in zip(sample_xs, sample_ys))
        ratio = inside_count / samples_per_pixel

        # 비율에 따라 흰색~파랑 보간
        r_col = (1 - ratio) * 0.93 + ratio * 0.20
        g_col = (1 - ratio) * 0.94 + ratio * 0.60
        b_col = (1 - ratio) * 0.96 + ratio * 0.86
        ax.add_patch(patches.Rectangle((i, j), 1, 1,
                                       color=(r_col, g_col, b_col),
                                       edgecolor='#bdc3c7', lw=0.5))

        # 9개 샘플 점 (작게)
        ax.plot(sample_xs, sample_ys, 'o', color='#e74c3c',
                markersize=1.2, alpha=0.6, zorder=5)

ax.plot(sphere_cx + sphere_r*np.cos(theta),
        sphere_cy + sphere_r*np.sin(theta),
        '--', color='#27ae60', lw=2, label='실제 구 윤곽')

ax.set_xlim(-0.5, W_grid + 0.5)
ax.set_ylim(-0.5, H_grid + 0.5)
ax.set_aspect('equal')
ax.legend(fontsize=9, loc='upper right')
ax.text(W_grid/2, -1.0, '각 픽셀 → 9개 샘플 평균 (연속)\n경계가 부드럽게 그라디언트',
        ha='center', fontsize=10, color='#27ae60', fontweight='bold')
ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/aliasing.png", dpi=120, bbox_inches='tight')
plt.close()
print("aliasing.png 생성 완료")

# ── 12. 픽셀 내부 샘플링 좌표 변환 ────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
fig.suptitle('픽셀 내부 샘플링 — 한 픽셀 안의 무작위 위치 선택', fontsize=14, fontweight='bold')

# ── 왼쪽: 픽셀 (i, j) 한 개를 확대
ax = axes[0]
ax.set_title('① 픽셀 (i, j) 확대 — 샘플 위치', fontsize=11)

# 픽셀 정사각형 (큰 사각형)
ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor='#fdfefe',
                               edgecolor='#34495e', lw=2.5))

# 인접 픽셀 일부 (회색)
for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    ax.add_patch(patches.Rectangle((di, dj), 1, 1, facecolor='#ecf0f1',
                                   edgecolor='#bdc3c7', lw=0.8, alpha=0.5))

# 픽셀 중심 (Ch.5 방식 — 1개 샘플)
ax.plot(0.5, 0.5, '*', color='#9b59b6', markersize=22, zorder=6,
        markeredgecolor='black', markeredgewidth=0.8)
ax.text(0.5, -0.18, 'Ch.5 방식: 픽셀 중심 1개만',
        ha='center', fontsize=9, color='#9b59b6', fontweight='bold')

# 픽셀 안 무작위 샘플 N개 (Ch.6 방식)
np.random.seed(7)
N = 12
sample_x = np.random.uniform(0, 1, N)
sample_y = np.random.uniform(0, 1, N)
ax.plot(sample_x, sample_y, 'o', color='#e74c3c', markersize=8,
        markeredgecolor='black', markeredgewidth=0.5, zorder=7,
        label=f'Ch.6 방식: 무작위 {N}개')

# 한 샘플에 좌표 라벨
sample0 = (sample_x[0], sample_y[0])
ax.annotate(f'(i + dx,\n j + dy)\n  dx, dy ∈ [0, 1)',
            xy=sample0, xytext=(sample0[0] + 0.4, sample0[1] + 0.5),
            fontsize=9, color='#c0392b', fontweight='bold',
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.2))

# pixel_delta_u, pixel_delta_v 표시
ax.annotate("", xy=(1.05, -0.08), xytext=(0, -0.08),
            arrowprops=dict(arrowstyle="<->", color='#e67e22', lw=1.5))
ax.text(0.5, -0.32, 'pixel_delta_u', ha='center', fontsize=9, color='#e67e22')

ax.annotate("", xy=(-0.08, 1.05), xytext=(-0.08, 0),
            arrowprops=dict(arrowstyle="<->", color='#e67e22', lw=1.5))
ax.text(-0.32, 0.5, 'pixel_delta_v',
        rotation=90, ha='center', va='center', fontsize=9, color='#e67e22')

# 픽셀 인덱스 라벨
ax.text(0.5, 1.08, '픽셀 (i, j)', ha='center', fontsize=11,
        color='#2c3e50', fontweight='bold')

ax.set_xlim(-1.3, 2.3)
ax.set_ylim(-0.7, 1.8)
ax.set_aspect('equal')
ax.legend(fontsize=9, loc='lower right')
ax.axis('off')

# ── 오른쪽: 좌표 변환 공식
ax = axes[1]
ax.set_title('② 샘플 위치 → 3D 좌표 변환', fontsize=11)
ax.axis('off')

formula = (
    '단계별 변환:\n\n'
    '1. 픽셀 안 무작위 오프셋 생성\n'
    '   dx, dy ← random in [0, 1)\n\n'
    '2. 픽셀 인덱스 + 오프셋 = 연속 인덱스\n'
    '   (i + dx, j + dy)\n\n'
    '3. 뷰포트 위 3D 좌표로 변환\n'
    '   sample_pos = pixel00_loc\n'
    '              + (i + dx) × pixel_delta_u\n'
    '              + (j + dy) × pixel_delta_v\n\n'
    '4. 광선 만들기\n'
    '   ray r(camera_origin,\n'
    '         sample_pos - camera_origin)\n\n'
    '─ 위 과정을 픽셀당 N번 반복하고 ─\n'
    '─ 색상 N개의 평균을 픽셀 색으로 사용 ─'
)

ax.text(0.05, 0.95, formula, fontsize=10.5, va='top', ha='left',
        color='#2c3e50',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#fdfefe',
                  edgecolor='#bdc3c7', lw=1))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig("diagrams/pixel_sampling.png", dpi=120, bbox_inches='tight')
plt.close()
print("pixel_sampling.png 생성 완료")

# ── 13. 람베르트 확산 — 반구 위 무작위 산란 방향 ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('람베르트 확산 (Lambertian Diffuse) — 법선 기준 반구 위 무작위 산란', fontsize=14, fontweight='bold')

# 왼쪽: 산란 방향 분포 시각화
ax = axes[0]
ax.set_title('산란 광선 분포 — 법선 방향으로 코사인 가중', fontsize=11)

surface_y = 0.0
ax.axhline(surface_y, color='#7f8c8d', lw=2.5, label='표면')
ax.fill_between([-2.5, 2.5], surface_y - 0.6, surface_y, color='#d5dbdb', alpha=0.5)

hit_point = np.array([0.0, 0.0])
ax.plot(*hit_point, 'o', color='#f39c12', markersize=12, zorder=6)
ax.text(0.15, -0.25, 'P (충돌점)', fontsize=9, color='#f39c12', fontweight='bold')

# 법선 벡터
normal = np.array([0.0, 1.0])
ax.annotate("", xy=hit_point + 1.4 * normal, xytext=hit_point,
            arrowprops=dict(arrowstyle="-|>", color='#2980b9', lw=2.5))
ax.text(0.12, 1.45, r'$\hat{n}$ (법선)', fontsize=10, color='#2980b9', fontweight='bold')

# 반구 윤곽
theta_hemi = np.linspace(0, np.pi, 100)
ax.plot(np.cos(theta_hemi), np.sin(theta_hemi), '--', color='#bdc3c7', lw=1.5)

# 람베르트 분포에 따른 무작위 방향들 (법선 근처에 더 밀집)
np.random.seed(42)
n_rays = 18
for i in range(n_rays):
    # 람베르트 코사인 분포: 단위구 위 점 + 법선
    rand_vec = np.random.randn(2)
    rand_vec = rand_vec / np.linalg.norm(rand_vec)
    if rand_vec[1] < 0:
        rand_vec[1] = -rand_vec[1]
    scatter = normal + rand_vec
    scatter = scatter / np.linalg.norm(scatter)

    intensity = max(0, scatter[1])  # 법선과의 내적 (코사인)
    color = (1 - intensity * 0.7, 1 - intensity * 0.4, 1 - intensity * 0.1)
    ax.annotate("", xy=hit_point + 0.9 * scatter, xytext=hit_point,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5, alpha=0.8))

ax.text(0, 1.85, '법선 방향(위)에 가까울수록\n산란 확률이 높다\n(코사인 가중)', ha='center',
        fontsize=9, color='#2c3e50',
        bbox=dict(boxstyle='round', facecolor='#fef9e7', edgecolor='#f39c12', alpha=0.9))

ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-0.8, 2.2)
ax.set_aspect('equal')
ax.axis('off')

# 오른쪽: 코드 방식 — 법선 + random_unit_vector()
ax = axes[1]
ax.set_title('코드 방식: 법선 + random_unit_vector()', fontsize=11)
ax.axis('off')

ax.add_patch(patches.FancyBboxPatch((0.02, 0.55), 0.96, 0.42,
    boxstyle="round,pad=0.02", facecolor='#f8f9fa', edgecolor='#adb5bd'))
ax.text(0.5, 0.94, '① 단위구 표면 위 무작위 점 S', ha='center', fontsize=10,
        color='#2c3e50', fontweight='bold', transform=ax.transAxes)
ax.text(0.5, 0.84, 'S = random_unit_vector()', ha='center', fontsize=10,
        color='#e74c3c', family='monospace', transform=ax.transAxes)

ax.text(0.5, 0.72, '② 산란 방향 = 법선 + S', ha='center', fontsize=10,
        color='#2c3e50', fontweight='bold', transform=ax.transAxes)
ax.text(0.5, 0.62, 'scatter_dir = rec.normal + S', ha='center', fontsize=10,
        color='#e74c3c', family='monospace', transform=ax.transAxes)

ax.add_patch(patches.FancyBboxPatch((0.02, 0.08), 0.96, 0.42,
    boxstyle="round,pad=0.02", facecolor='#eaf2ff', edgecolor='#2980b9'))
ax.text(0.5, 0.46, '왜 법선에 더하는가?', ha='center', fontsize=10,
        color='#2980b9', fontweight='bold', transform=ax.transAxes)
ax.text(0.5, 0.35,
        '단위구 위 점 S를 법선 끝점에서 더하면\n'
        '법선 방향으로 치우친 반구 분포가 된다.\n'
        '이것이 람베르트 코사인 법칙과 일치한다:\n'
        '반사 강도 ∝ cos θ (법선과의 각도)',
        ha='center', va='center', fontsize=9.5, color='#1a5276',
        transform=ax.transAxes)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig("diagrams/lambertian_diffuse.png", dpi=120, bbox_inches='tight')
plt.close()
print("lambertian_diffuse.png 생성 완료")

# ── 14. 재귀 광선 추적 (Recursive Ray Tracing) ────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_title('재귀 광선 추적 — 광선이 산란될 때마다 깊이(depth)가 줄어든다', fontsize=14, fontweight='bold')

ax.set_xlim(-0.5, 13)
ax.set_ylim(-0.5, 8.5)
ax.set_aspect('equal')
ax.axis('off')

# 카메라
cam = np.array([0.5, 7.5])
ax.plot(*cam, 's', color='#2c3e50', markersize=15, zorder=6)
ax.text(cam[0], cam[1] + 0.4, '카메라\ndepth=50', ha='center', fontsize=9,
        color='#2c3e50', fontweight='bold')

# 표면들 (y값 다르게)
surfaces = [
    {'y': 6.0, 'x0': 1.0, 'x1': 5.0, 'color': '#aed6f1', 'label': '구 A'},
    {'y': 4.0, 'x0': 3.0, 'x1': 8.0, 'color': '#a9dfbf', 'label': '구 B'},
    {'y': 2.0, 'x0': 5.5, 'x1': 11.0, 'color': '#f5cba7', 'label': '구 C'},
]

ray_nodes = [
    (cam, np.array([3.0, 6.0])),       # depth=50 → 49
    (np.array([3.0, 6.0]), np.array([6.0, 4.0])),   # depth=49 → 48
    (np.array([6.0, 4.0]), np.array([8.5, 2.0])),   # depth=48 → 47
    (np.array([8.5, 2.0]), np.array([11.0, 0.3])),  # depth=47: 배경색 반환
]

colors = ['#8e44ad', '#2980b9', '#27ae60', '#e67e22']
depths = [50, 49, 48, 47]
labels = ['depth=50', 'depth=49', 'depth=48', 'depth=47']

# 표면 선 그리기
for s in surfaces:
    ax.plot([s['x0'], s['x1']], [s['y'], s['y']],
            color='#7f8c8d', lw=3, alpha=0.6)
    ax.add_patch(patches.FancyBboxPatch(
        (s['x0'], s['y'] - 0.25), s['x1'] - s['x0'], 0.25,
        boxstyle="round,pad=0.05", facecolor=s['color'], edgecolor='#7f8c8d',
        alpha=0.5))
    ax.text((s['x0'] + s['x1']) / 2, s['y'] - 0.6, s['label'],
            ha='center', fontsize=9, color='#2c3e50')

# 광선 + 충돌점
for i, ((src, dst), col, depth) in enumerate(zip(ray_nodes, colors, depths)):
    ax.annotate("", xy=dst, xytext=src,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
    mid = (src + dst) / 2
    ax.text(mid[0] - 0.4, mid[1] + 0.25, labels[i], fontsize=8.5,
            color=col, fontweight='bold')

    if i < len(ray_nodes) - 1:
        ax.plot(*dst, 'o', color=col, markersize=10, zorder=6)
        ax.text(dst[0] + 0.2, dst[1] + 0.25,
                f'산란 → depth={depths[i]-1}', fontsize=8, color=col)
    else:
        ax.plot(*dst, '*', color='#e67e22', markersize=16, zorder=6)
        ax.text(dst[0] + 0.2, dst[1] + 0.3, '배경색 반환\n(더 이상 교차 없음)',
                fontsize=8.5, color='#e67e22', fontweight='bold')

# depth=0 종료 박스
ax.text(6.5, 1.0,
        'depth = 0 이면 즉시 color(0,0,0) 반환\n→ 더 이상 재귀하지 않음 (무한루프 방지)',
        ha='center', fontsize=9.5, color='#c0392b',
        bbox=dict(boxstyle='round', facecolor='#fadbd8', edgecolor='#c0392b', alpha=0.9))

# 반환값 화살표 (역방향)
ax.annotate("", xy=(2.5, 6.5), xytext=(8.0, 2.5),
            arrowprops=dict(arrowstyle="-|>", color='#bdc3c7', lw=1.5,
                            connectionstyle="arc3,rad=-0.3"))
ax.text(4.5, 5.2, '색상 × 감쇠율\n(attenuation)\n역방향으로 누산', fontsize=8.5,
        ha='center', color='#7f8c8d',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='#bdc3c7', alpha=0.8))

plt.tight_layout()
plt.savefig("diagrams/recursive_ray.png", dpi=120, bbox_inches='tight')
plt.close()
print("recursive_ray.png 생성 완료")

# ── 15. 정반사 벡터 (Reflection Vector) ──────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle(r'정반사 (Specular Reflection) — $v_{ref} = v - 2(v \cdot \hat{n})\hat{n}$', fontsize=14, fontweight='bold')

# 왼쪽: 기하학적 설명
ax = axes[0]
ax.set_title('① 벡터 분해 — 법선 성분만 뒤집는다', fontsize=11)

ax.axhline(0, color='#7f8c8d', lw=2.5)
ax.fill_between([-2.5, 2.5], -0.7, 0, color='#d5dbdb', alpha=0.5)

hit = np.array([0.0, 0.0])
ax.plot(*hit, 'o', color='#f39c12', markersize=12, zorder=6)

# 입사 벡터 v (왼쪽 위에서 내려옴)
v = np.array([1.0, -1.0])
v_norm = v / np.linalg.norm(v)
ax.annotate("", xy=hit, xytext=hit - 1.4 * v_norm,
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2.5))
ax.text(-1.3, 1.1, 'v (입사 방향)', fontsize=10, color='#e74c3c', fontweight='bold')

# 법선 n
n = np.array([0.0, 1.0])
ax.annotate("", xy=hit + 1.5 * n, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#2980b9', lw=2.5))
ax.text(0.12, 1.55, r'$\hat{n}$', fontsize=12, color='#2980b9', fontweight='bold')

# 법선 방향 성분 (v·n)n — 빨간 점선
dot_vn = np.dot(v_norm, n)  # 음수 (v가 아래로 향함)
proj = dot_vn * n  # 법선 방향 성분 (아래쪽)
ax.annotate("", xy=hit + proj, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#9b59b6', lw=2,
                            linestyle='dashed'))
ax.text(0.12, proj[1] / 2, r'$(v \cdot \hat{n})\hat{n}$' + '\n(법선 성분)', fontsize=8.5,
        color='#9b59b6', fontweight='bold')

# 반사 벡터 v_ref
v_ref = v_norm - 2 * dot_vn * n
ax.annotate("", xy=hit + 1.4 * v_ref, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=2.5))
ax.text(1.0, 1.1, 'v_ref (반사)', fontsize=10, color='#27ae60', fontweight='bold')

# 입사각 = 반사각 표시
theta_in = np.degrees(np.arctan2(-v_norm[0], v_norm[1]))
theta_out = np.degrees(np.arctan2(v_ref[0], v_ref[1]))
arc1 = np.linspace(np.radians(90), np.radians(90 + theta_in), 30)
arc2 = np.linspace(np.radians(90 - theta_in), np.radians(90), 30)
ax.plot(0.5 * np.cos(arc1), 0.5 * np.sin(arc1), color='#e74c3c', lw=1.5)
ax.plot(0.5 * np.cos(arc2), 0.5 * np.sin(arc2), color='#27ae60', lw=1.5)
ax.text(-0.55, 0.55, 'θ', fontsize=12, color='#e74c3c')
ax.text(0.45, 0.55, 'θ', fontsize=12, color='#27ae60')
ax.text(0, -0.5, '입사각 = 반사각 (항상 성립)', ha='center', fontsize=9.5,
        color='#2c3e50', fontweight='bold')

ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-0.9, 2.1)
ax.set_aspect('equal')
ax.axis('off')

# 오른쪽: 수식 전개
ax = axes[1]
ax.set_title('② 수식 전개 — 왜 2를 곱하는가?', fontsize=11)
ax.axis('off')

steps = [
    ('v를 두 성분으로 분해', '#2c3e50',
     'v = v⊥ + v||\n  v|| = (v·n)n   ← 법선 방향 성분\n  v⊥ = v - (v·n)n  ← 법선 수직 성분'),
    ('반사 = 수직 성분은 유지, 법선 성분만 부호 반전', '#2c3e50',
     'v_ref = v⊥ + (-v||)\n      = (v - (v·n)n) + (-(v·n)n)\n      = v - 2(v·n)n'),
    ('코드 구현', '#c0392b',
     'vec3 reflect(const vec3& v, const vec3& n)\n{\n    return v - 2*dot(v,n)*n;\n}'),
]

y_pos = 0.92
for title, tc, body in steps:
    ax.text(0.05, y_pos, title, fontsize=10, color=tc, fontweight='bold',
            transform=ax.transAxes)
    y_pos -= 0.06
    ax.text(0.07, y_pos, body, fontsize=9.5, color='#1a252f',
            transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa',
                      edgecolor='#dee2e6'))
    y_pos -= 0.22

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig("diagrams/reflection.png", dpi=120, bbox_inches='tight')
plt.close()
print("reflection.png 생성 완료")

# ── 16. Fuzz — 금속 흐림 효과 ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 7))
fig.suptitle('Fuzz — 반사 방향에 무작위 벡터를 더해 금속 흐림 구현', fontsize=14, fontweight='bold')

fuzz_values = [0.0, 0.3, 0.8]
titles = ['fuzz = 0.0\n(완벽한 거울)', 'fuzz = 0.3\n(약간 흐림)', 'fuzz = 0.8\n(많이 흐림)']
np.random.seed(0)

for ax, fuzz, title in zip(axes, fuzz_values, titles):
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.axhline(0, color='#7f8c8d', lw=2.5)
    ax.fill_between([-2, 2], -0.8, 0, color='#d5dbdb', alpha=0.5)

    hit = np.array([0.0, 0.0])
    ax.plot(*hit, 'o', color='#f39c12', markersize=11, zorder=6)

    # 입사 광선
    v = np.array([0.8, -1.0])
    v = v / np.linalg.norm(v)
    ax.annotate("", xy=hit, xytext=hit - 1.2 * v,
                arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2))
    ax.text(-1.1, 0.95, '입사 광선', fontsize=8.5, color='#e74c3c', ha='center')

    # 법선 n
    n = np.array([0.0, 1.0])
    # 완전 반사 방향
    dot_vn = np.dot(v, n)
    reflected = v - 2 * dot_vn * n
    reflected = reflected / np.linalg.norm(reflected)

    if fuzz == 0.0:
        # fuzz=0: 단일 반사 방향
        ax.annotate("", xy=hit + 1.3 * reflected, xytext=hit,
                    arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=2.5))
        ax.text(reflected[0] * 1.4, reflected[1] * 1.4 + 0.15, '반사 광선',
                fontsize=8.5, color='#27ae60', ha='center')
    else:
        # fuzz>0: 여러 방향
        n_scatter = 12
        for i in range(n_scatter):
            rand = np.random.randn(2)
            rand = rand / np.linalg.norm(rand)
            perturbed = reflected + fuzz * rand
            if perturbed[1] > 0:  # 표면 위쪽만
                perturbed = perturbed / np.linalg.norm(perturbed)
                alpha = 0.5 + 0.5 * (n_scatter - i) / n_scatter
                ax.annotate("", xy=hit + 1.1 * perturbed, xytext=hit,
                            arrowprops=dict(arrowstyle="-|>",
                                          color='#27ae60', lw=1.5, alpha=alpha))

        # 중심 반사 방향 (굵게)
        ax.annotate("", xy=hit + 1.3 * reflected, xytext=hit,
                    arrowprops=dict(arrowstyle="-|>", color='#1a8a4a', lw=3))
        ax.text(reflected[0] + 0.15, reflected[1] * 1.3 + 0.1,
                f'완전반사 방향\n± fuzz×random', fontsize=8, color='#1a8a4a', ha='center')

        # fuzz 원 표시
        theta_c = np.linspace(0, 2 * np.pi, 100)
        c_center = hit + reflected
        ax.plot(c_center[0] + fuzz * np.cos(theta_c),
                c_center[1] + fuzz * np.sin(theta_c),
                '--', color='#bdc3c7', lw=1.2, alpha=0.7)
        ax.text(c_center[0], c_center[1] - fuzz - 0.2, f'반지름 = {fuzz}',
                ha='center', fontsize=8, color='#7f8c8d')

    ax.set_xlim(-2, 2)
    ax.set_ylim(-0.9, 2.1)
    ax.set_aspect('equal')
    ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/fuzz.png", dpi=120, bbox_inches='tight')
plt.close()
print("fuzz.png 생성 완료")

# ── 17. 굴절 — 스넬의 법칙 벡터 분해 ─────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(15, 8))
fig.suptitle('굴절 (Refraction) — 스넬의 법칙과 벡터 분해', fontsize=14, fontweight='bold')

# 왼쪽: 물리적 그림
ax = axes[0]
ax.set_title('① 스넬의 법칙: η₁·sinθ₁ = η₂·sinθ₂', fontsize=11)

# 매질 구분
ax.fill_between([-3, 3], 0, 3.5, color='#d6eaf8', alpha=0.4, label='공기 (η₁=1.0)')
ax.fill_between([-3, 3], -3.5, 0, color='#a9cce3', alpha=0.5, label='유리 (η₂=1.5)')
ax.axhline(0, color='#2980b9', lw=2.5)
ax.text(-2.8, 2.8, '공기\nη₁ = 1.0', fontsize=10, color='#1a5276', fontweight='bold')
ax.text(-2.8, -2.8, '유리\nη₂ = 1.5', fontsize=10, color='#1a5276', fontweight='bold')

hit = np.array([0.0, 0.0])
ax.plot(*hit, 'o', color='#f39c12', markersize=12, zorder=6)

# 법선 (위쪽)
n = np.array([0.0, 1.0])
ax.plot([0, 0], [-2, 2], '--', color='#7f8c8d', lw=1.5, alpha=0.6)
ax.text(0.1, 2.1, r'$\hat{n}$', fontsize=12, color='#7f8c8d', fontweight='bold')

# 입사 광선 (θ₁ = 45°)
theta1 = np.radians(45)
v_in = np.array([np.sin(theta1), -np.cos(theta1)])
ax.annotate("", xy=hit, xytext=hit - 2.2 * v_in,
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2.5))
ax.text(-2.0, 2.0, '입사 광선', fontsize=10, color='#e74c3c', fontweight='bold')

# θ₁ 각도 호
arc1 = np.linspace(np.radians(90), np.radians(135), 40)
ax.plot(0.8 * np.cos(arc1), 0.8 * np.sin(arc1), color='#e74c3c', lw=2)
ax.text(-0.6, 0.85, 'θ₁', fontsize=12, color='#e74c3c', fontweight='bold')

# 굴절 광선 (스넬의 법칙으로 계산)
eta_ratio = 1.0 / 1.5
cos_t1 = np.cos(theta1)
sin_t1 = np.sin(theta1)
sin_t2 = eta_ratio * sin_t1
cos_t2 = np.sqrt(1 - sin_t2**2)
v_out = np.array([sin_t2, -cos_t2])
ax.annotate("", xy=hit + 2.2 * v_out, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=2.5))
ax.text(1.0, -2.0, '굴절 광선', fontsize=10, color='#27ae60', fontweight='bold')

# θ₂ 각도 호
arc2 = np.linspace(np.radians(270), np.radians(270) + np.arcsin(sin_t2), 40)
ax.plot(0.8 * np.cos(arc2), 0.8 * np.sin(arc2), color='#27ae60', lw=2)
ax.text(0.4, -0.85, 'θ₂', fontsize=12, color='#27ae60', fontweight='bold')

ax.text(0, -3.2,
        'θ₂ < θ₁ (유리가 더 느려서 법선 쪽으로 꺾임)',
        ha='center', fontsize=9.5, color='#1a5276', fontweight='bold')

ax.legend(loc='lower right', fontsize=9)
ax.set_xlim(-3, 3)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')

# 오른쪽: 벡터 분해
ax = axes[1]
ax.set_title(r"② 벡터 분해: $R'_\perp + R'_\parallel$", fontsize=11)

ax.fill_between([-3, 3], 0, 3, color='#d6eaf8', alpha=0.3)
ax.fill_between([-3, 3], -3, 0, color='#a9cce3', alpha=0.4)
ax.axhline(0, color='#2980b9', lw=2)

hit = np.array([0.0, 0.0])
ax.plot(*hit, 'o', color='#f39c12', markersize=12, zorder=6)

# 입사 광선 단위벡터
v_in_u = np.array([np.sin(theta1), -np.cos(theta1)])
ax.annotate("", xy=hit, xytext=hit - 1.8 * v_in_u,
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2))
ax.text(-1.5, 1.5, r'$\hat{R}$ (입사)', fontsize=10, color='#e74c3c', fontweight='bold')

# R'⊥ (수직 성분, 표면 따라 수평)
r_perp = eta_ratio * (v_in_u + cos_t1 * n)
ax.annotate("", xy=hit + r_perp, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#8e44ad', lw=2.5))
ax.text(r_perp[0] + 0.1, r_perp[1] - 0.3, r"$R'_\perp$" + "\n(수평 성분\n× η₁/η₂)", fontsize=8.5,
        color='#8e44ad', fontweight='bold')

# R'∥ (평행 성분, 법선 방향)
r_parallel = np.array([0, -cos_t2])
ax.annotate("", xy=hit + r_parallel, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#d35400', lw=2.5))
ax.text(0.12, -cos_t2 / 2, r"$R'_\parallel$" + "\n(법선 성분\nby 피타고라스)", fontsize=8.5,
        color='#d35400', fontweight='bold')

# 최종 굴절 벡터
v_refracted = r_perp + r_parallel
ax.annotate("", xy=hit + 1.6 * v_refracted, xytext=hit,
            arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=3))
ax.text(1.0, -1.8, r"$R' = R'_\perp + R'_\parallel$" + "\n(최종 굴절 방향)", fontsize=9,
        color='#27ae60', fontweight='bold')

# 피타고라스 설명
ax.text(-2.8, -2.5,
        r"$|R'_\parallel|^2 = 1 - |R'_\perp|^2$" + "\n(단위벡터의 피타고라스 정리)",
        fontsize=8.5, color='#d35400',
        bbox=dict(boxstyle='round', facecolor='#fef5e7', edgecolor='#d35400'))

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/refraction.png", dpi=120, bbox_inches='tight')
plt.close()
print("refraction.png 생성 완료")

# ── 18. 전반사 (Total Internal Reflection) ────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 7))
fig.suptitle('전반사 (Total Internal Reflection) — 각도에 따른 3가지 경우', fontsize=14, fontweight='bold')

eta1, eta2 = 1.5, 1.0  # 유리 → 공기
critical_angle_rad = np.arcsin(eta2 / eta1)  # arcsin(1/1.5) ≈ 41.8°

cases = [
    {'theta_deg': 25, 'title': f'θ < 임계각({np.degrees(critical_angle_rad):.1f}°)\n굴절 가능', 'col': '#27ae60'},
    {'theta_deg': np.degrees(critical_angle_rad), 'title': f'θ = 임계각({np.degrees(critical_angle_rad):.1f}°)\n굴절각 = 90°', 'col': '#f39c12'},
    {'theta_deg': 60, 'title': f'θ > 임계각({np.degrees(critical_angle_rad):.1f}°)\n전반사', 'col': '#e74c3c'},
]

for ax, case in zip(axes, cases):
    ax.set_title(case['title'], fontsize=10, fontweight='bold', color=case['col'])
    ax.fill_between([-2.5, 2.5], 0, 3, color='#a9cce3', alpha=0.4)
    ax.fill_between([-2.5, 2.5], -3, 0, color='#d6eaf8', alpha=0.3)
    ax.axhline(0, color='#2980b9', lw=2)
    ax.text(-2.3, 2.5, '유리\n(η=1.5)', fontsize=8.5, color='#1a5276', fontweight='bold')
    ax.text(-2.3, -2.5, '공기\n(η=1.0)', fontsize=8.5, color='#1a5276', fontweight='bold')

    hit = np.array([0.0, 0.0])
    ax.plot(*hit, 'o', color='#f39c12', markersize=10, zorder=6)
    ax.plot([0, 0], [-2.5, 2.5], '--', color='#7f8c8d', lw=1, alpha=0.5)

    theta1_r = np.radians(case['theta_deg'])
    v_in = np.array([np.sin(theta1_r), -np.cos(theta1_r)])

    # 입사 광선 (아래에서 위로, 유리 안에서 나가려 함)
    ax.annotate("", xy=hit, xytext=hit - 1.8 * v_in,
                arrowprops=dict(arrowstyle="-|>", color='#7f8c8d', lw=2))

    sin_t2 = (eta1 / eta2) * np.sin(theta1_r)

    if sin_t2 <= 1.0:
        # 굴절 가능
        cos_t2 = np.sqrt(max(0, 1 - sin_t2**2))
        v_out = np.array([np.sign(v_in[0]) * sin_t2, -cos_t2])
        ax.annotate("", xy=hit + 1.8 * v_out, xytext=hit,
                    arrowprops=dict(arrowstyle="-|>", color=case['col'], lw=2.5))

        if case['theta_deg'] == np.degrees(critical_angle_rad):
            ax.text(1.0, -0.3, 'θ₂ = 90°\n(표면과 나란)', fontsize=8,
                    color=case['col'], fontweight='bold')
    else:
        # 전반사: 반사만
        n = np.array([0.0, 1.0])
        dot_vn = np.dot(v_in, n)
        v_ref = v_in - 2 * dot_vn * n
        ax.annotate("", xy=hit + 1.8 * v_ref, xytext=hit,
                    arrowprops=dict(arrowstyle="-|>", color=case['col'], lw=2.5))
        ax.text(1.1, 1.5, '반사만\n(굴절 없음)', fontsize=8.5,
                color=case['col'], fontweight='bold')
        ax.text(0, -1.8,
                f'sin_t2 = {sin_t2:.2f} > 1.0\n→ 굴절 불가!',
                ha='center', fontsize=8.5, color='#c0392b',
                bbox=dict(boxstyle='round', facecolor='#fadbd8', edgecolor='#c0392b'))

    # 각도 호
    arc = np.linspace(np.radians(90), np.radians(90 + case['theta_deg']), 30)
    ax.plot(0.6 * np.cos(arc), 0.6 * np.sin(arc), color='#7f8c8d', lw=1.5)
    ax.text(-0.5, 0.65, 'θ₁', fontsize=10, color='#7f8c8d')

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/total_internal_reflection.png", dpi=120, bbox_inches='tight')
plt.close()
print("total_internal_reflection.png 생성 완료")

# ── 19. 속 빈 유리 구 (Hollow Sphere Trick) ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 8))
fig.suptitle('속 빈 유리 구 (Hollow Sphere) — 음수 반지름 트릭', fontsize=14, fontweight='bold')

# 왼쪽: 일반 유리 구 (단단한 구)
ax = axes[0]
ax.set_title('① 일반 유리 구 (r = 0.5)\n빛이 안을 가득 채운 유리를 통과', fontsize=10)

center = np.array([0.0, 0.0])
for r, fc, ec, label in [(1.5, '#d6eaf8', '#2980b9', '유리 (r=0.5)')]:
    circ = plt.Circle(center, r, facecolor=fc, edgecolor=ec, lw=2, alpha=0.6)
    ax.add_patch(circ)
    ax.text(0, -r - 0.3, label, ha='center', fontsize=9, color=ec, fontweight='bold')

# 빛의 경로 (공기→유리→유리→공기, 두 번 굴절)
in_start = np.array([-2.8, 1.0])
in_hit = np.array([-1.3, 0.3])
through = np.array([1.3, -0.4])
out_end = np.array([2.8, -1.2])

path_points = [in_start, in_hit, through, out_end]
path_colors = ['#e74c3c', '#8e44ad', '#27ae60']
path_labels = ['입사 (공기)', '내부 (유리)', '굴절 후 (공기)']

for i in range(len(path_points) - 1):
    ax.annotate("", xy=path_points[i+1], xytext=path_points[i],
                arrowprops=dict(arrowstyle="-|>", color=path_colors[i], lw=2.2))

for pt, col in [(in_hit, '#8e44ad'), (through, '#27ae60')]:
    ax.plot(*pt, 'o', color=col, markersize=9, zorder=6)

ax.text(-2.5, 1.3, '① 공기→유리\n굴절', fontsize=8, color='#e74c3c', ha='center')
ax.text(0, 0.5, '② 유리 안 통과', fontsize=8, color='#8e44ad', ha='center')
ax.text(2.5, -0.7, '③ 유리→공기\n굴절', fontsize=8, color='#27ae60', ha='center')

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.axis('off')

# 오른쪽: 속 빈 유리 구 (바깥 유리 + 안쪽 음수 반지름)
ax = axes[1]
ax.set_title('② 속 빈 유리 구\n바깥(r=0.5) + 안쪽(r=-0.4, 법선이 안쪽)', fontsize=10)

# 바깥 유리 구
outer = plt.Circle(center, 1.5, facecolor='#d6eaf8', edgecolor='#2980b9', lw=2.5,
                   alpha=0.4, label='바깥 구 r=+0.5')
# 안쪽 공기 구멍
inner = plt.Circle(center, 1.2, facecolor='white', edgecolor='#e74c3c', lw=2.5,
                   linestyle='--', alpha=0.9, label='안쪽 구 r=-0.4')
ax.add_patch(outer)
ax.add_patch(inner)

ax.text(0, -1.7, '바깥 유리 구 (r=+0.5)\n법선: 바깥 방향 →', ha='center',
        fontsize=8.5, color='#2980b9', fontweight='bold')
ax.text(0, 0.2, '안쪽 공기\n(r=-0.4)\n법선: 안쪽 방향 ←\n(뒤집힘!)', ha='center',
        fontsize=8.5, color='#e74c3c', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#fef9e7', edgecolor='#f39c12'))

# 법선 화살표들 (바깥 구: 바깥 방향)
for angle_deg in [0, 60, 120, 180, 240, 300]:
    angle_r = np.radians(angle_deg)
    p = 1.5 * np.array([np.cos(angle_r), np.sin(angle_r)])
    n_dir = p / np.linalg.norm(p)
    ax.annotate("", xy=p + 0.4 * n_dir, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color='#2980b9', lw=1.5))

# 법선 화살표들 (안쪽 구: 안쪽 방향)
for angle_deg in [30, 90, 150, 210, 270, 330]:
    angle_r = np.radians(angle_deg)
    p = 1.2 * np.array([np.cos(angle_r), np.sin(angle_r)])
    n_dir = -p / np.linalg.norm(p)  # 안쪽으로
    ax.annotate("", xy=p + 0.35 * n_dir, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=1.5))

# 코드 설명
ax.text(-3.3, -2.2,
        'make_shared<sphere>(pos,  0.5, mat_glass)   // 바깥\n'
        'make_shared<sphere>(pos, -0.4, mat_bubble)  // 안쪽 (음수!)',
        fontsize=8, color='#2c3e50',
        bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#adb5bd'))

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-2.8, 2.5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/hollow_sphere.png", dpi=120, bbox_inches='tight')
plt.close()
print("hollow_sphere.png 생성 완료")

# ── 20. 카메라 로컬 좌표계 (u, v, w) ─────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('카메라 로컬 좌표계 (u, v, w)', fontsize=15, fontweight='bold')

# ── 왼쪽: lookfrom/lookat/vup → w/u/v 구성 과정
ax = axes[0]
ax.set_title('① lookfrom, lookat, vup으로\n카메라 좌표계 구성', fontsize=11)
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 4.0)
ax.set_aspect('equal')
ax.axis('off')

lookfrom = np.array([1.0, 1.0])
lookat   = np.array([3.5, 2.5])

# lookfrom 점
ax.plot(*lookfrom, 'o', color='#2c3e50', markersize=12, zorder=5)
ax.text(lookfrom[0] - 0.15, lookfrom[1] - 0.35, 'lookfrom\n(카메라 위치)', fontsize=9,
        ha='center', color='#2c3e50', fontweight='bold')

# lookat 점
ax.plot(*lookat, 's', color='#8e44ad', markersize=10, zorder=5)
ax.text(lookat[0] + 0.15, lookat[1] + 0.2, 'lookat\n(바라보는 지점)', fontsize=9,
        ha='center', color='#8e44ad', fontweight='bold')

# w = lookfrom - lookat 방향 (뒤쪽)
w_dir = lookfrom - lookat
w_dir = w_dir / np.linalg.norm(w_dir)
ax.annotate("", xy=lookfrom + 0.8 * w_dir, xytext=lookfrom,
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2.5))
ax.text(*(lookfrom + 1.0 * w_dir + np.array([-0.05, 0.15])), 'w\n(뒤쪽)',
        fontsize=10, color='#e74c3c', fontweight='bold', ha='center')

# 바라보는 방향 (lookat - lookfrom, 점선)
view_dir = lookat - lookfrom
view_dir_n = view_dir / np.linalg.norm(view_dir)
ax.annotate("", xy=lookfrom + 0.8 * view_dir_n, xytext=lookfrom,
            arrowprops=dict(arrowstyle="-|>", color='#aaa', lw=1.5, linestyle='dashed'))
ax.text(*(lookfrom + 0.9 * view_dir_n + np.array([0.05, 0.1])), '바라보는\n방향',
        fontsize=8, color='#aaa', ha='center')

# u = vup × w 방향 (오른쪽)
u_dir = np.array([w_dir[1], -w_dir[0]])  # 2D에서 w의 수직(오른쪽)
ax.annotate("", xy=lookfrom + 0.8 * u_dir, xytext=lookfrom,
            arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=2.5))
ax.text(*(lookfrom + 1.0 * u_dir + np.array([0.1, 0.05])), 'u\n(오른쪽)',
        fontsize=10, color='#27ae60', fontweight='bold', ha='center')

# vup (위쪽 참조 벡터)
ax.annotate("", xy=lookfrom + np.array([0, 0.9]), xytext=lookfrom,
            arrowprops=dict(arrowstyle="-|>", color='#3498db', lw=2.0, linestyle='dotted'))
ax.text(lookfrom[0] - 0.25, lookfrom[1] + 1.0, 'vup\n(월드 위쪽)', fontsize=9,
        color='#3498db', ha='center')

# 수식 설명
ax.text(0.0, 3.7,
        'w = normalize(lookfrom − lookat)\n'
        'u = normalize(vup × w)\n'
        'v = w × u',
        fontsize=9, color='#2c3e50',
        bbox=dict(boxstyle='round', facecolor='#fef9e7', edgecolor='#f39c12', alpha=0.9),
        va='top')

# ── 오른쪽: u/v/w로 뷰포트 만들기
ax = axes[1]
ax.set_title('② 카메라 로컬 축(u, v)으로\n뷰포트 구성', fontsize=11)
ax.set_xlim(-1.5, 4.5)
ax.set_ylim(-1.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')

cam = np.array([0.0, 0.0])
focal = 2.5

# 카메라 위치
ax.plot(*cam, 'o', color='#2c3e50', markersize=13, zorder=5)
ax.text(cam[0], cam[1] - 0.4, '카메라\n(lookfrom)', fontsize=9, ha='center',
        color='#2c3e50', fontweight='bold')

# 뷰포트 사각형 (카메라 앞 = x 방향)
vp_cx = cam[0] + focal
vp_h  = 1.4
vp_w  = 2.0
vp_left  = vp_cx
vp_right = vp_cx
vp_bot   = cam[1] - vp_h / 2
vp_top   = cam[1] + vp_h / 2

rect = patches.Rectangle((vp_left - 0.05, vp_bot), vp_w, vp_h,
                          linewidth=2, edgecolor='#8e44ad', facecolor='#e8daef', alpha=0.5)
ax.add_patch(rect)
ax.text(vp_cx + vp_w / 2, vp_top + 0.2, '뷰포트', fontsize=10,
        ha='center', color='#8e44ad', fontweight='bold')

# focal_length 선
ax.annotate("", xy=(vp_cx, cam[1]), xytext=cam,
            arrowprops=dict(arrowstyle="-", color='#7f8c8d', lw=1.5, linestyle='dashed'))
ax.text(vp_cx / 2 + cam[0] / 2, cam[1] - 0.25, 'focal_length\n(= w 방향 이동)', fontsize=8,
        ha='center', color='#7f8c8d')

# u 벡터 (뷰포트 가로 방향)
ax.annotate("", xy=(vp_cx + 0.9, vp_bot + vp_h / 2), xytext=(vp_cx, vp_bot + vp_h / 2),
            arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=2.5))
ax.text(vp_cx + 1.0, vp_bot + vp_h / 2 + 0.2, 'u (오른쪽)\nviewport_width × u',
        fontsize=8.5, color='#27ae60', fontweight='bold')

# v 벡터 (뷰포트 세로 방향, 아래 = +j)
ax.annotate("", xy=(vp_cx + vp_w / 2, vp_bot - 0.7), xytext=(vp_cx + vp_w / 2, vp_bot),
            arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2.5))
ax.text(vp_cx + vp_w / 2 + 0.15, vp_bot - 0.55, '−v (아래쪽)\nviewport_height × (−v)',
        fontsize=8.5, color='#e74c3c', fontweight='bold')

# 기존 방식 vs 새 방식 비교
ax.text(-1.4, 3.3,
        '이전: viewport_u = (width, 0, 0)  ← 세계 x축 고정\n'
        '이후: viewport_u = width × u        ← 카메라 로컬 축',
        fontsize=8.5, color='#2c3e50',
        bbox=dict(boxstyle='round', facecolor='#eafaf1', edgecolor='#27ae60', alpha=0.9),
        va='top')

plt.tight_layout()
plt.savefig("diagrams/camera_coordinate.png", dpi=120, bbox_inches='tight')
plt.close()
print("camera_coordinate.png 생성 완료")

# ── 21. FOV → 뷰포트 높이 변환 ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('FOV → 뷰포트 높이 변환\nh = tan(vfov / 2)', fontsize=15, fontweight='bold')

# ── 왼쪽: 직각삼각형으로 tan 유도
ax = axes[0]
ax.set_title('① tan(vfov/2) = h / focal_length', fontsize=11)
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-2.5, 3.0)
ax.set_aspect('equal')
ax.axis('off')

cam = np.array([0.0, 0.0])
focal = 3.5
h = 1.5

# 삼각형 꼭짓점
A = cam                         # 카메라
B = np.array([focal, 0.0])      # 뷰포트 중심
C = np.array([focal, h])        # 뷰포트 위쪽 끝

tri = plt.Polygon([A, B, C], fill=True, facecolor='#d6eaf8', edgecolor='#2980b9',
                  linewidth=2, alpha=0.6)
ax.add_patch(tri)

# 삼각형 꼭짓점 레이블
ax.plot(*A, 'o', color='#2c3e50', markersize=12, zorder=5)
ax.text(A[0] - 0.2, A[1] - 0.3, '카메라', fontsize=9, color='#2c3e50', fontweight='bold')

ax.plot(*B, 'o', color='#7f8c8d', markersize=8, zorder=5)
ax.text(B[0] + 0.1, B[1] - 0.3, '뷰포트\n중심', fontsize=8.5, color='#7f8c8d')

ax.plot(*C, 'o', color='#8e44ad', markersize=8, zorder=5)
ax.text(C[0] + 0.1, C[1] + 0.1, '뷰포트\n상단', fontsize=8.5, color='#8e44ad')

# focal_length 레이블
ax.text(focal / 2, -0.35, 'focal_length\n(인접한 변)', fontsize=9.5,
        ha='center', color='#2980b9', fontweight='bold')

# h 레이블
ax.annotate("", xy=C, xytext=B,
            arrowprops=dict(arrowstyle="<->", color='#e74c3c', lw=2.0))
ax.text(focal + 0.35, h / 2, 'h\n(반대편)', fontsize=10, color='#e74c3c',
        fontweight='bold', va='center')

# 직각 표시
sq = patches.Rectangle((focal - 0.18, 0), 0.18, 0.18,
                        linewidth=1.5, edgecolor='#555', facecolor='none')
ax.add_patch(sq)

# 각도 호 (vfov/2)
theta_val = np.degrees(np.arctan2(h, focal))
arc = np.linspace(0, np.radians(theta_val), 60)
ax.plot(0.6 * np.cos(arc), 0.6 * np.sin(arc), color='#f39c12', lw=2.0)
ax.text(0.85 * np.cos(np.radians(theta_val / 2)),
        0.85 * np.sin(np.radians(theta_val / 2)),
        'vfov/2', fontsize=9, color='#f39c12', fontweight='bold', ha='center')

# 수식
ax.text(0.0, 2.7,
        'tan(vfov/2) = h / focal_length\n'
        '→  h = tan(vfov/2) × focal_length\n'
        '→  viewport_height = 2h',
        fontsize=10, color='#2c3e50',
        bbox=dict(boxstyle='round', facecolor='#fef9e7', edgecolor='#f39c12', alpha=0.9))

# ── 오른쪽: vfov 변화에 따른 뷰포트 크기 비교
ax = axes[1]
ax.set_title('② vfov에 따른 뷰포트 크기 비교\n(같은 focal_length)', fontsize=11)
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')

cam = np.array([0.0, 0.0])
focal = 3.5
vfov_cases = [
    (20,  '#e74c3c', '좁은 FOV (20°)\n→ 망원, 확대'),
    (60,  '#f39c12', '중간 FOV (60°)\n→ 표준'),
    (90,  '#27ae60', '넓은 FOV (90°)\n→ 광각'),
]

ax.plot(*cam, 'o', color='#2c3e50', markersize=13, zorder=5)
ax.text(cam[0], cam[1] - 0.4, '카메라', fontsize=9, ha='center',
        color='#2c3e50', fontweight='bold')

x_offset = 0.0
for i, (vfov_deg, color, label) in enumerate(vfov_cases):
    h = np.tan(np.radians(vfov_deg / 2)) * focal
    # 시야각 삼각형 (선만)
    upper = np.array([focal, h])
    lower = np.array([focal, -h])
    ax.plot([cam[0], upper[0]], [cam[1], upper[1]], '--', color=color, lw=1.5, alpha=0.7)
    ax.plot([cam[0], lower[0]], [cam[1], lower[1]], '--', color=color, lw=1.5, alpha=0.7)

    # 뷰포트 선분
    lw = 3.5 - i * 0.7
    ax.plot([focal, focal], [-h, h], color=color, lw=lw, solid_capstyle='round', zorder=4)
    ax.text(focal + 0.2 + i * 0.05, 0,
            f'{vfov_deg}°\nh={h:.2f}',
            fontsize=8.5, color=color, fontweight='bold', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=color, alpha=0.8))

    ax.text(focal + 0.15, h + 0.15, label, fontsize=7.5, color=color, va='bottom')

ax.axhline(0, xmin=0.05, xmax=0.95, color='#bdc3c7', lw=0.8, linestyle=':')
ax.text(focal / 2, -3.2, f'focal_length = {focal}', fontsize=9, ha='center', color='#7f8c8d')

plt.tight_layout()
plt.savefig("diagrams/fov_viewport.png", dpi=120, bbox_inches='tight')
plt.close()
print("fov_viewport.png 생성 완료")

# ── Ch.11-1. 핀홀 카메라 vs 렌즈 카메라 ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('핀홀 카메라 vs 렌즈 카메라 (Defocus Blur)', fontsize=15, fontweight='bold')

for ax, (title, use_disk) in zip(axes, [("핀홀 카메라 (defocus_angle=0)", False), ("렌즈 카메라 (defocus_angle>0)", True)]):
    ax.set_xlim(-1, 9)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold')

    # 초점 평면
    ax.plot([6, 6], [-2.5, 2.5], color='#27ae60', lw=2, linestyle='--')
    ax.text(6.1, 2.6, '초점 평면\n(focus_dist)', fontsize=8, color='#27ae60', ha='left')

    # 물체 위치 (초점 평면 위)
    ax.plot(6, 1.0, 'o', color='#27ae60', markersize=10, zorder=5)
    ax.text(6.1, 1.1, '초점 O\n(선명)', fontsize=8, color='#27ae60')

    # 물체 위치 (초점 평면 밖)
    ax.plot(4, 1.2, 's', color='#e74c3c', markersize=9, zorder=5)
    ax.text(4.1, 1.4, '비초점 X\n(흐림)', fontsize=8, color='#e74c3c')

    if not use_disk:
        # 핀홀: 단일 점에서 광선
        cam_pt = np.array([0.0, 0.0])
        ax.plot(*cam_pt, 'o', color='#2c3e50', markersize=8, zorder=5)
        ax.text(-0.1, 0.25, '카메라\n(1점)', fontsize=8, color='#2c3e50', ha='center')
        for target in [(6, 1.0), (6, -1.0), (4, 1.2)]:
            ax.annotate("", xy=target, xytext=cam_pt,
                        arrowprops=dict(arrowstyle="-|>", color='#3498db', lw=1.2))
    else:
        # 렌즈: 원판 위 여러 점에서 광선
        disk_pts = [(-0.1, -0.5), (0.0, 0.0), (0.1, 0.5)]
        ax.plot([0, 0], [-0.7, 0.7], color='#8e44ad', lw=4, solid_capstyle='round', zorder=5)
        ax.text(0.15, 0.85, '조리개\n원판', fontsize=8, color='#8e44ad')
        colors = ['#e67e22', '#3498db', '#1abc9c']
        for (px, py), c in zip(disk_pts, colors):
            for target in [(6, 1.0)]:
                ax.annotate("", xy=target, xytext=(px, py),
                            arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2, alpha=0.8))
        # 비초점 물체: 원판의 여러 점에서 오는 광선이 흩어짐
        for (px, py), c in zip(disk_pts, colors):
            ax.annotate("", xy=(4, 1.2), xytext=(px, py),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.0, alpha=0.5, linestyle='dashed'))

plt.tight_layout()
plt.savefig("diagrams/ch11_pinhole_vs_lens.png", dpi=120, bbox_inches='tight')
plt.close()
print("ch11_pinhole_vs_lens.png 생성 완료")

# ── Ch.11-2. 조리개 원판(Defocus Disk) 구조 ──────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(-1, 9)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('조리개 원판(Defocus Disk) 구조', fontsize=14, fontweight='bold')

# 카메라 위치
cam = np.array([0.0, 0.0])
ax.plot(*cam, 'o', color='#2c3e50', markersize=10, zorder=6)
ax.text(-0.1, 0.35, '카메라\ncenter', fontsize=9, color='#2c3e50', ha='center')

# 조리개 원판 (반지름 = defocus_radius)
disk_r = 0.8
circle = plt.Circle(cam, disk_r, color='#8e44ad', fill=False, lw=2.5, linestyle='-', zorder=5)
ax.add_patch(circle)
ax.plot([0, disk_r], [0, 0], color='#8e44ad', lw=1.5, linestyle='--')
ax.text(disk_r / 2, 0.15, 'defocus_radius\n= focus_dist × tan(defocus_angle/2)',
        fontsize=8, color='#8e44ad', ha='center')

# focus_dist 화살표
ax.annotate("", xy=(6, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="<->", color='#27ae60', lw=2))
ax.text(3, 0.25, 'focus_dist', fontsize=10, color='#27ae60', ha='center')

# 초점 평면
ax.plot([6, 6], [-3, 3], color='#27ae60', lw=2, linestyle='--')
ax.text(6.1, 3.1, '초점 평면', fontsize=9, color='#27ae60')

# defocus_angle 호
theta_half = np.degrees(np.arctan(disk_r / 6))
arc = np.linspace(0, np.radians(theta_half), 40)
ax.plot(1.5 * np.cos(arc), 1.5 * np.sin(arc), color='#e67e22', lw=1.5)
ax.text(1.7, 0.3, f'defocus_angle/2', fontsize=8, color='#e67e22')

# 원판 위 무작위 샘플 점
np.random.seed(42)
for _ in range(8):
    angle = np.random.uniform(0, 2 * np.pi)
    r = np.random.uniform(0, disk_r)
    px, py = r * np.cos(angle), r * np.sin(angle)
    ax.plot(px, py, 'o', color='#e74c3c', markersize=5, zorder=7)

ax.text(0, -1.3, '원판 위 무작위 점들\n(defocus_disk_sample)', fontsize=9,
        color='#e74c3c', ha='center')

# u, v 축
ax.annotate("", xy=(0, disk_r + 0.3), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#3498db', lw=2))
ax.text(0.1, disk_r + 0.4, 'defocus_disk_v\n(= v × radius)', fontsize=8, color='#3498db')
ax.annotate("", xy=(disk_r + 0.3, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color='#e67e22', lw=2))
ax.text(disk_r + 0.4, -0.3, 'defocus_disk_u\n(= u × radius)', fontsize=8, color='#e67e22')

plt.tight_layout()
plt.savefig("diagrams/ch11_defocus_disk.png", dpi=120, bbox_inches='tight')
plt.close()
print("ch11_defocus_disk.png 생성 완료")

# ── Ch.11-3. 초점 평면(Focus Plane) ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-0.5, 10)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('초점 평면 — 여기에 있는 물체만 선명하다', fontsize=13, fontweight='bold')

cam = np.array([0.0, 0.0])
focus_dist = 6.0

# 조리개 원판
ax.plot([0, 0], [-0.7, 0.7], color='#8e44ad', lw=5, solid_capstyle='round', zorder=5)
ax.text(0.1, 1.0, '조리개\n원판', fontsize=9, color='#8e44ad')

# focus_dist 화살표
ax.annotate("", xy=(focus_dist, 0), xytext=(0.05, 0),
            arrowprops=dict(arrowstyle="<->", color='#27ae60', lw=1.5))
ax.text(focus_dist / 2, 0.3, 'focus_dist', fontsize=10, color='#27ae60', ha='center')

# 초점 평면
ax.plot([focus_dist, focus_dist], [-3, 3], color='#27ae60', lw=2.5, linestyle='-')
ax.text(focus_dist + 0.1, 3.1, '초점 평면\n(선명)', fontsize=9, color='#27ae60')

# 초점 평면 위 물체 → 원판의 모든 광선이 한 점에서 만남
target_focused = np.array([focus_dist, 1.0])
ax.plot(*target_focused, 'o', color='#27ae60', markersize=12, zorder=6)
ax.text(focus_dist + 0.15, 1.2, '선명', fontsize=9, color='#27ae60', fontweight='bold')
for py in [-0.5, 0.0, 0.5]:
    ax.plot([py * 0.15, target_focused[0]], [py, target_focused[1]],
            color='#3498db', lw=1.2, alpha=0.7)

# 초점 평면 밖 물체 → 광선이 흩어짐
near_obj = np.array([3.5, 1.2])
ax.plot(*near_obj, 's', color='#e74c3c', markersize=11, zorder=6)
ax.text(near_obj[0] + 0.1, near_obj[1] + 0.3, '흐림\n(앞쪽)', fontsize=9, color='#e74c3c', fontweight='bold')
spread = 0.6
for py, end_y in zip([-0.5, 0.0, 0.5], [near_obj[1] - spread, near_obj[1], near_obj[1] + spread]):
    ax.plot([py * 0.15, near_obj[0]], [py, end_y],
            color='#e74c3c', lw=1.0, alpha=0.5, linestyle='--')

far_obj = np.array([8.5, -1.0])
ax.plot(*far_obj, 's', color='#e67e22', markersize=11, zorder=6)
ax.text(far_obj[0] + 0.1, far_obj[1] - 0.4, '흐림\n(뒤쪽)', fontsize=9, color='#e67e22', fontweight='bold')
for py, end_y in zip([-0.5, 0.0, 0.5], [far_obj[1] + spread, far_obj[1], far_obj[1] - spread]):
    ax.plot([py * 0.15, far_obj[0]], [py, end_y],
            color='#e67e22', lw=1.0, alpha=0.5, linestyle='--')

plt.tight_layout()
plt.savefig("diagrams/ch11_focus_plane.png", dpi=120, bbox_inches='tight')
plt.close()
print("ch11_focus_plane.png 생성 완료")

# ── Ch.11-4. Defocus Blur 효과 요약 ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 10)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('Defocus Blur — defocus_angle에 따른 흐림 변화', fontsize=13, fontweight='bold')

cases = [
    (0,   '0°\n(핀홀, 완전 선명)', '#2ecc71'),
    (5,   '5°\n(약한 흐림)',        '#3498db'),
    (10,  '10°\n(강한 흐림)',       '#e74c3c'),
]

x_positions = [1.5, 5.0, 8.5]
focus_dist_diag = 3.0

for x, (angle, label, color) in zip(x_positions, cases):
    radius = focus_dist_diag * np.tan(np.radians(angle / 2)) if angle > 0 else 0.0
    radius_vis = max(radius * 0.6, 0.04)

    # 조리개 원판
    ax.plot([x, x], [-radius_vis, radius_vis], color=color, lw=max(radius_vis * 18, 2),
            solid_capstyle='round', zorder=5)

    # 초점 평면까지 광선
    target = np.array([x + focus_dist_diag * 0.7, 2.0])
    for dy in np.linspace(-radius_vis, radius_vis, 4):
        ax.plot([x, target[0]], [dy, target[1]], color=color, lw=0.9, alpha=0.6)

    # 물체
    ax.plot(*target, 'o', color=color, markersize=11, zorder=6)

    # 라벨
    ax.text(x, -0.5, label, fontsize=9, ha='center', color=color, fontweight='bold')
    ax.text(x, 4.5, f'반지름\n≈ {radius:.2f}', fontsize=8, ha='center', color=color)

plt.tight_layout()
plt.savefig("diagrams/ch11_defocus_effect.png", dpi=120, bbox_inches='tight')
plt.close()
print("ch11_defocus_effect.png 생성 완료")

print("\n모든 다이어그램 생성 완료 → diagrams/ 폴더")
