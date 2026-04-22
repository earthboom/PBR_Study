import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import os

os.makedirs("diagrams", exist_ok=True)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ── 1. 내적 (Dot Product) ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('내적 (Dot Product)', fontsize=16, fontweight='bold')

cases = [
    ("같은 방향\n(θ ~ 0°)", 15,  "결과 > 0\n(양수)",  "#2ecc71"),
    ("수직\n(θ = 90°)",    90,  "결과 = 0",          "#3498db"),
    ("반대 방향\n(θ ~ 180°)", 165, "결과 < 0\n(음수)", "#e74c3c"),
]

for ax, (title, angle_deg, result, color) in zip(axes, cases):
    ax.set_xlim(-0.3, 1.5)
    ax.set_ylim(-0.3, 1.5)
    ax.set_aspect('equal')
    ax.axhline(0, color='#ccc', linewidth=0.5)
    ax.axvline(0, color='#ccc', linewidth=0.5)
    ax.set_title(title, fontsize=12)

    # 벡터 a (고정)
    ax.annotate("", xy=(1.0, 0.0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50", lw=2))
    ax.text(1.05, 0.05, "a", fontsize=13, color="#2c3e50", fontweight='bold')

    # 벡터 b (각도 변경)
    rad = np.radians(angle_deg)
    bx, by = 0.9 * np.cos(rad), 0.9 * np.sin(rad)
    ax.annotate("", xy=(bx, by), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
    ax.text(bx + 0.05, by + 0.05, "b", fontsize=13, color=color, fontweight='bold')

    # θ 호
    theta_arc = np.linspace(0, np.radians(angle_deg), 50)
    ax.plot(0.25 * np.cos(theta_arc), 0.25 * np.sin(theta_arc), color='gray', lw=1)
    mid = np.radians(angle_deg / 2)
    ax.text(0.32 * np.cos(mid), 0.32 * np.sin(mid), "θ", fontsize=10, color='gray')

    ax.text(0.5, -0.25, result, fontsize=11, ha='center', color=color, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.savefig("diagrams/dot_product.png", dpi=120, bbox_inches='tight')
plt.close()
print("dot_product.png 생성 완료")

# ── 2. 외적 (Cross Product) ───────────────────────────────────────────────────
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('외적 (Cross Product)\na × b = c (두 벡터에 수직)', fontsize=13, fontweight='bold')

# 벡터 a, b, c
a = np.array([1.0, 0.0, 0.0])
b = np.array([0.0, 1.0, 0.0])
c = np.cross(a, b)  # (0, 0, 1)

for vec, color, label, offset in [
    (a, '#e74c3c', 'a = (1,0,0)', (0.05, -0.15, 0)),
    (b, '#2ecc71', 'b = (0,1,0)', (-0.2, 0.05, 0)),
    (c, '#3498db', 'a×b = (0,0,1)', (0.05, 0.05, 0.05)),
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
     r'길이 = $\sqrt{2^2 + 1.5^2}$ ≈ 2.5'),
    (np.array([2.0, 1.5]) / np.linalg.norm([2.0, 1.5]), '#2ecc71', '정규화 후 (단위 벡터)',
     '길이 = 1.0'),
]):
    ax.set_xlim(-0.2, 2.5)
    ax.set_ylim(-0.2, 2.0)
    ax.set_aspect('equal')
    ax.axhline(0, color='#ccc', linewidth=0.8)
    ax.axvline(0, color='#ccc', linewidth=0.8)
    ax.set_title(title, fontsize=12)

    # 단위원
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

print("\n모든 다이어그램 생성 완료 → diagrams/ 폴더")
