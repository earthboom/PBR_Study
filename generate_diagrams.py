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

print("\n모든 다이어그램 생성 완료 → diagrams/ 폴더")
