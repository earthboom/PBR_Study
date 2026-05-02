#include <fstream>
#include <filesystem>

#include "rtweekend.h"
#include "hittable_list.h"
#include "sphere.h"
#include "camera.h"

int main()
{
    // ── 씬 구성 ─────────────────────────────────────────────────
    // 작은 구 + 거대한 땅 구 — 두 구 모두 동일한 hit() 인터페이스로 처리됨
    hittable_list world;
    world.add(make_shared<sphere>(point3(0,    0,   -1), 0.5));    // 정면의 작은 구
    world.add(make_shared<sphere>(point3(0, -100.5, -1), 100));    // 거대한 땅 구

    // ── 카메라 설정 ──────────────────────────────────────────────
    camera cam;
    cam.aspect_ratio      = 16.0 / 9.0;
    cam.image_width       = 400;
    cam.samples_per_pixel = 100;   // 픽셀당 샘플 수 — 안티에일리어싱
    cam.max_depth         = 50;    // 광선 최대 반사 횟수 — 재귀 깊이 제한

    // ── 렌더링 ───────────────────────────────────────────────────
    // PROJECT_SOURCE_DIR 은 CMake 가 컴파일 타임에 박아넣은 절대경로 — IDE/CWD 무관하게 동일 위치에 출력
    const std::filesystem::path out_dir = std::filesystem::path(PROJECT_SOURCE_DIR) / "output";
    std::filesystem::create_directories(out_dir);
    std::ofstream out(out_dir / "ch7_diffuse.ppm");
    if (!out) { std::cerr << "Failed to open output file\n"; return 1; }

    cam.render(world, out);
    return 0;
}
